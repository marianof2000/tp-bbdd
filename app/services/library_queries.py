from datetime import date
from typing import Any

from sqlalchemy import and_, case, exists, func, or_, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.core.config import get_settings
from app.models import Autor, Ejemplar, Libro, LibroAutor, Persona, Prestamo, Socio


def _serialize_book(book: Libro) -> dict[str, Any]:
    """Convierte un libro y sus relaciones cargadas en una respuesta serializable."""
    return {
        "id_libro": book.id_libro,
        "titulo": book.titulo,
        "isbn": book.isbn,
        "editorial": book.editorial.nombre,
        "autores": [
            f"{authorship.autor.nombre} {authorship.autor.apellido}".strip()
            for authorship in book.autores
        ],
        "anio_publicacion": book.anio_publicacion,
    }


def search_books(db: Session, title: str) -> list[dict[str, Any]]:
    """Busca libros por una parte literal del título sin modificar la base."""
    normalized_title = title.strip()
    if not normalized_title:
        raise ValueError("El título de búsqueda no puede estar vacío.")

    statement = (
        select(Libro)
        .options(
            joinedload(Libro.editorial),
            selectinload(Libro.autores).joinedload(LibroAutor.autor),
        )
        .where(Libro.titulo.icontains(normalized_title, autoescape=True))
        .order_by(Libro.titulo, Libro.id_libro)
    )
    books = db.scalars(statement).unique().all()
    return [_serialize_book(book) for book in books]


def search_books_by_author(db: Session, author: str) -> list[dict[str, Any]]:
    """Busca libros por una parte literal del nombre o apellido de un autor."""
    normalized_author = author.strip()
    if not normalized_author:
        raise ValueError("El autor de búsqueda no puede estar vacío.")

    full_name = Autor.nombre + " " + Autor.apellido
    statement = (
        select(Libro)
        .join(Libro.autores)
        .join(LibroAutor.autor)
        .options(
            joinedload(Libro.editorial),
            selectinload(Libro.autores).joinedload(LibroAutor.autor),
        )
        .where(
            or_(
                Autor.nombre.icontains(normalized_author, autoescape=True),
                Autor.apellido.icontains(normalized_author, autoescape=True),
                full_name.icontains(normalized_author, autoescape=True),
            )
        )
        .order_by(Libro.titulo, Libro.id_libro)
    )
    books = db.scalars(statement).unique().all()
    return [_serialize_book(book) for book in books]


def search_members(db: Session, criterion: str) -> list[dict[str, Any]]:
    """Busca socios por nombre, apellido, documento o email."""
    normalized_criterion = criterion.strip()
    if not normalized_criterion:
        raise ValueError("El criterio de búsqueda no puede estar vacío.")

    full_name = Persona.nombre + " " + Persona.apellido
    statement = (
        select(Socio)
        .join(Socio.persona)
        .options(joinedload(Socio.persona), selectinload(Socio.telefonos))
        .where(
            or_(
                Persona.nombre.icontains(normalized_criterion, autoescape=True),
                Persona.apellido.icontains(normalized_criterion, autoescape=True),
                full_name.icontains(normalized_criterion, autoescape=True),
                Persona.documento.icontains(normalized_criterion, autoescape=True),
                Persona.email.icontains(normalized_criterion, autoescape=True),
            )
        )
        .order_by(Persona.apellido, Persona.nombre, Socio.id_persona)
    )
    members = db.scalars(statement).unique().all()
    return [
        {
            "id_socio": member.id_persona,
            "nombre": member.persona.nombre,
            "apellido": member.persona.apellido,
            "documento": member.persona.documento,
            "email": member.persona.email,
            "fecha_alta": member.fecha_alta.isoformat(),
            "telefonos": [
                {"numero": phone.numero, "tipo": phone.tipo}
                for phone in member.telefonos
            ],
        }
        for member in members
    ]


def get_book_availability(db: Session, book_id: int) -> dict[str, Any] | None:
    """Devuelve las cantidades de ejemplares de un libro, o ``None`` si no existe."""
    book = db.execute(
        select(Libro.id_libro, Libro.titulo).where(Libro.id_libro == book_id)
    ).one_or_none()
    if book is None:
        return None

    settings = get_settings()
    active_loan_exists = exists().where(
        Prestamo.id_ejemplar == Ejemplar.id_ejemplar,
        Prestamo.fecha_devolucion.is_(None),
    )
    statement = select(
        func.count(Ejemplar.id_ejemplar).label("total"),
        func.sum(
            case(
                (
                    and_(
                        Ejemplar.estado == settings.available_copy_state,
                        ~active_loan_exists,
                    ),
                    1,
                ),
                else_=0,
            )
        ).label("disponibles"),
        func.sum(case((active_loan_exists, 1), else_=0)).label("prestados"),
        func.sum(
            case((Ejemplar.estado == settings.repair_copy_state, 1), else_=0)
        ).label("en_reparacion"),
    ).where(Ejemplar.id_libro == book_id)
    counts = db.execute(statement).one()

    return {
        "id_libro": book.id_libro,
        "titulo": book.titulo,
        "total": int(counts.total or 0),
        "disponibles": int(counts.disponibles or 0),
        "prestados": int(counts.prestados or 0),
        "en_reparacion": int(counts.en_reparacion or 0),
    }


def list_overdue_loans(
    db: Session, *, as_of: date | None = None
) -> list[dict[str, Any]]:
    """Lista préstamos activos cuya fecha de vencimiento vigente ya pasó."""
    reference_date = as_of or date.today()
    statement = (
        select(
            Prestamo.id_prestamo,
            Socio.id_persona.label("id_socio"),
            Persona.nombre.label("socio_nombre"),
            Persona.apellido.label("socio_apellido"),
            Persona.documento.label("socio_documento"),
            Ejemplar.id_ejemplar,
            Ejemplar.codigo_inventario,
            Libro.id_libro,
            Libro.titulo.label("libro_titulo"),
            Libro.isbn,
            Prestamo.fecha_prestamo,
            Prestamo.fecha_vencimiento_inicial,
            Prestamo.fecha_vencimiento_actual,
        )
        .join(Socio, Socio.id_persona == Prestamo.id_socio)
        .join(Persona, Persona.id_persona == Socio.id_persona)
        .join(Ejemplar, Ejemplar.id_ejemplar == Prestamo.id_ejemplar)
        .join(Libro, Libro.id_libro == Ejemplar.id_libro)
        .where(
            Prestamo.fecha_devolucion.is_(None),
            Prestamo.fecha_vencimiento_actual < reference_date,
        )
        .order_by(Prestamo.fecha_vencimiento_actual, Prestamo.id_prestamo)
    )
    rows = db.execute(statement).all()
    return [
        {
            "id_prestamo": row.id_prestamo,
            "socio": {
                "id_socio": row.id_socio,
                "nombre": f"{row.socio_nombre} {row.socio_apellido}".strip(),
                "documento": row.socio_documento,
            },
            "libro": {
                "id_libro": row.id_libro,
                "titulo": row.libro_titulo,
                "isbn": row.isbn,
            },
            "ejemplar": {
                "id_ejemplar": row.id_ejemplar,
                "codigo_inventario": row.codigo_inventario,
            },
            "fecha_prestamo": row.fecha_prestamo.isoformat(),
            "fecha_vencimiento_inicial": row.fecha_vencimiento_inicial.isoformat(),
            "fecha_vencimiento_actual": row.fecha_vencimiento_actual.isoformat(),
            "dias_vencido": (reference_date - row.fecha_vencimiento_actual).days,
        }
        for row in rows
    ]


def get_library_statistics(db: Session, *, as_of: date | None = None) -> dict[str, int]:
    """Calcula indicadores generales de la biblioteca mediante consultas de lectura."""
    reference_date = as_of or date.today()

    def count(model: type[Any], *criteria: Any) -> int:
        statement = select(func.count()).select_from(model)
        if criteria:
            statement = statement.where(*criteria)
        return int(db.scalar(statement) or 0)

    return {
        "libros": count(Libro),
        "ejemplares": count(Ejemplar),
        "socios": count(Socio),
        "prestamos_activos": count(Prestamo, Prestamo.fecha_devolucion.is_(None)),
        "prestamos_vencidos": count(
            Prestamo,
            Prestamo.fecha_devolucion.is_(None),
            Prestamo.fecha_vencimiento_actual < reference_date,
        ),
    }
