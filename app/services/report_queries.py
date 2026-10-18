from dataclasses import dataclass
from typing import Any

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models import (
    Autor,
    Bibliotecario,
    Editorial,
    Ejemplar,
    Libro,
    LibroAutor,
    Persona,
    Socio,
    TelefonoSocio,
)


@dataclass(frozen=True)
class ReportResult:
    """Resultado tabular de una de las veinte consultas de comprobación."""

    number: int
    question: str
    columns: tuple[tuple[str, str], ...]
    rows: list[dict[str, Any]]


def _rows(db: Session, statement: Any) -> list[dict[str, Any]]:
    """Ejecuta una expresión SQLAlchemy y convierte sus filas en diccionarios."""
    return [dict(row) for row in db.execute(statement).mappings().all()]


def total_people(db: Session) -> list[dict[str, Any]]:
    statement = select(func.count().label("total_personas")).select_from(Persona)
    return _rows(db, statement)


def total_members(db: Session) -> list[dict[str, Any]]:
    statement = (
        select(func.count().label("total_socios"))
        .select_from(Socio)
        .join(Persona, Persona.id_persona == Socio.id_persona)
    )
    return _rows(db, statement)


def total_librarians(db: Session) -> list[dict[str, Any]]:
    statement = (
        select(func.count().label("total_bibliotecarios"))
        .select_from(Bibliotecario)
        .join(Persona, Persona.id_persona == Bibliotecario.id_persona)
    )
    return _rows(db, statement)


def people_without_email(db: Session) -> list[dict[str, Any]]:
    statement = (
        select(Persona.id_persona, Persona.nombre, Persona.apellido)
        .where(Persona.email.is_(None) | (func.trim(Persona.email) == ""))
        .order_by(Persona.apellido, Persona.nombre)
    )
    return _rows(db, statement)


def phone_totals(db: Session) -> list[dict[str, Any]]:
    statement = (
        select(
            func.count(func.distinct(TelefonoSocio.id_telefono_socio)).label(
                "total_telefonos"
            ),
            func.count(func.distinct(Persona.id_persona)).label(
                "socios_con_telefono"
            ),
        )
        .select_from(Persona)
        .join(Socio, Socio.id_persona == Persona.id_persona)
        .join(TelefonoSocio, TelefonoSocio.id_socio == Socio.id_persona)
    )
    return _rows(db, statement)


def members_by_phone_count(db: Session) -> list[dict[str, Any]]:
    phone_counts = (
        select(
            TelefonoSocio.id_socio,
            func.count().label("cantidad_telefonos"),
        )
        .group_by(TelefonoSocio.id_socio)
        .subquery()
    )
    statement = (
        select(
            phone_counts.c.cantidad_telefonos,
            func.count().label("cantidad_socios"),
        )
        .group_by(phone_counts.c.cantidad_telefonos)
        .order_by(phone_counts.c.cantidad_telefonos)
    )
    return _rows(db, statement)


def total_authors(db: Session) -> list[dict[str, Any]]:
    statement = select(func.count().label("total_autores")).select_from(Autor)
    return _rows(db, statement)


def authors_with_and_without_books(db: Session) -> list[dict[str, Any]]:
    statement = (
        select(
            func.count(
                func.distinct(
                    case((Libro.id_libro.is_not(None), Autor.id_autor))
                )
            ).label("autores_con_libro"),
            func.count(
                func.distinct(case((Libro.id_libro.is_(None), Autor.id_autor)))
            ).label("autores_sin_libro"),
        )
        .select_from(Autor)
        .outerjoin(LibroAutor, LibroAutor.id_autor == Autor.id_autor)
        .outerjoin(Libro, Libro.id_libro == LibroAutor.id_libro)
    )
    return _rows(db, statement)


def total_publishers(db: Session) -> list[dict[str, Any]]:
    statement = select(func.count().label("total_editoriales")).select_from(Editorial)
    return _rows(db, statement)


def publishers_without_books(db: Session) -> list[dict[str, Any]]:
    has_books = select(Libro.id_libro).where(
        Libro.id_editorial == Editorial.id_editorial
    ).exists()
    statement = (
        select(func.count().label("editoriales_sin_libros"))
        .select_from(Editorial)
        .where(~has_books)
    )
    return _rows(db, statement)


def total_books(db: Session) -> list[dict[str, Any]]:
    statement = select(func.count().label("total_libros")).select_from(Libro)
    return _rows(db, statement)


def books_starting_with(db: Session, prefix: str = "El") -> list[dict[str, Any]]:
    """Cuenta títulos por prefijo literal; SQLAlchemy enlaza el valor como parámetro."""
    normalized_prefix = prefix.strip()
    if not normalized_prefix:
        raise ValueError("El prefijo no puede estar vacío.")
    statement = (
        select(func.count().label("titulos_que_comienzan_con_el"))
        .select_from(Libro)
        .where(Libro.titulo.startswith(f"{normalized_prefix} ", autoescape=True))
    )
    return _rows(db, statement)


def books_by_publication_year(db: Session) -> list[dict[str, Any]]:
    statement = (
        select(
            Libro.anio_publicacion,
            func.count().label("cantidad_libros"),
        )
        .group_by(Libro.anio_publicacion)
        .order_by(Libro.anio_publicacion)
    )
    return _rows(db, statement)


def publishers_with_most_books(db: Session) -> list[dict[str, Any]]:
    publisher_counts = (
        select(
            Libro.id_editorial,
            func.count().label("cantidad_libros"),
        )
        .group_by(Libro.id_editorial)
        .subquery()
    )
    maximum = select(func.max(publisher_counts.c.cantidad_libros)).scalar_subquery()
    book_count = func.count(func.distinct(Libro.id_libro))
    statement = (
        select(
            Editorial.nombre.label("editorial"),
            book_count.label("cantidad_libros"),
        )
        .join(Libro, Libro.id_editorial == Editorial.id_editorial)
        .outerjoin(LibroAutor, LibroAutor.id_libro == Libro.id_libro)
        .group_by(Editorial.id_editorial, Editorial.nombre)
        .having(book_count == maximum)
        .order_by(Editorial.nombre)
    )
    return _rows(db, statement)


def books_without_authors(db: Session) -> list[dict[str, Any]]:
    has_authors = select(LibroAutor.id_libro_autor).where(
        LibroAutor.id_libro == Libro.id_libro
    ).exists()
    statement = (
        select(Libro.id_libro, Libro.titulo)
        .where(~has_authors)
        .order_by(Libro.titulo)
    )
    return _rows(db, statement)


def books_without_copies(db: Session) -> list[dict[str, Any]]:
    has_copies = select(Ejemplar.id_ejemplar).where(
        Ejemplar.id_libro == Libro.id_libro
    ).exists()
    statement = (
        select(Libro.id_libro, Libro.titulo)
        .where(~has_copies)
        .order_by(Libro.titulo)
    )
    return _rows(db, statement)


def books_grouped_by_copy_count(db: Session) -> list[dict[str, Any]]:
    copy_counts = (
        select(
            Libro.id_libro,
            func.count(Ejemplar.id_ejemplar).label("cantidad_ejemplares"),
        )
        .outerjoin(Ejemplar, Ejemplar.id_libro == Libro.id_libro)
        .group_by(Libro.id_libro)
        .subquery()
    )
    statement = (
        select(
            copy_counts.c.cantidad_ejemplares,
            func.count().label("cantidad_libros"),
        )
        .group_by(copy_counts.c.cantidad_ejemplares)
        .order_by(copy_counts.c.cantidad_ejemplares)
    )
    return _rows(db, statement)


def copies_by_state(
    db: Session,
    first_inventory_code: str = "INV-0001",
    last_inventory_code: str = "INV-0101",
) -> list[dict[str, Any]]:
    statement = (
        select(Ejemplar.estado, func.count().label("cantidad_ejemplares"))
        .where(
            Ejemplar.codigo_inventario.between(
                first_inventory_code, last_inventory_code
            )
        )
        .group_by(Ejemplar.estado)
        .order_by(Ejemplar.estado)
    )
    return _rows(db, statement)


def books_with_copies_in_repair(
    db: Session,
    first_inventory_code: str = "INV-0001",
    last_inventory_code: str = "INV-0101",
    repair_state: str = "en_reparacion",
) -> list[dict[str, Any]]:
    statement = (
        select(
            Editorial.nombre.label("editorial"),
            Libro.titulo,
            func.count(Ejemplar.id_ejemplar).label("ejemplares_en_reparacion"),
        )
        .select_from(Editorial)
        .join(Libro, Libro.id_editorial == Editorial.id_editorial)
        .join(Ejemplar, Ejemplar.id_libro == Libro.id_libro)
        .where(
            Ejemplar.estado == repair_state,
            Ejemplar.codigo_inventario.between(
                first_inventory_code, last_inventory_code
            ),
        )
        .group_by(
            Editorial.id_editorial,
            Editorial.nombre,
            Libro.id_libro,
            Libro.titulo,
        )
        .order_by(Libro.titulo)
    )
    return _rows(db, statement)


def books_with_fewer_copies(
    db: Session, maximum_copies: int = 3
) -> list[dict[str, Any]]:
    if maximum_copies < 1:
        raise ValueError("La cantidad máxima de ejemplares debe ser positiva.")
    copy_count = func.count(Ejemplar.id_ejemplar)
    statement = (
        select(
            Editorial.nombre.label("editorial"),
            Libro.titulo,
            copy_count.label("cantidad_ejemplares"),
        )
        .select_from(Editorial)
        .join(Libro, Libro.id_editorial == Editorial.id_editorial)
        .outerjoin(Ejemplar, Ejemplar.id_libro == Libro.id_libro)
        .group_by(
            Editorial.id_editorial,
            Editorial.nombre,
            Libro.id_libro,
            Libro.titulo,
        )
        .having(copy_count < maximum_copies)
        .order_by(copy_count, Libro.titulo)
    )
    return _rows(db, statement)


def run_all_reports(db: Session) -> list[ReportResult]:
    """Ejecuta en Python las veinte preguntas del script SQL de comprobación."""
    definitions = (
        (1, "¿Cuántas personas están registradas?", (("total_personas", "Total"),), total_people),
        (2, "¿Cuántas personas tienen rol de socio?", (("total_socios", "Total"),), total_members),
        (3, "¿Cuántas personas trabajan como bibliotecarias?", (("total_bibliotecarios", "Total"),), total_librarians),
        (4, "¿Hay personas sin correo electrónico registrado?", (("id_persona", "ID"), ("nombre", "Nombre"), ("apellido", "Apellido")), people_without_email),
        (5, "¿Cuántos teléfonos se registraron y cuántos socios tienen al menos uno?", (("total_telefonos", "Teléfonos"), ("socios_con_telefono", "Socios")), phone_totals),
        (6, "¿Cuántos socios tienen uno o dos teléfonos?", (("cantidad_telefonos", "Teléfonos por socio"), ("cantidad_socios", "Socios")), members_by_phone_count),
        (7, "¿Cuántos autores están registrados?", (("total_autores", "Total"),), total_authors),
        (8, "¿Cuántos autores tienen libros asociados y cuántos no?", (("autores_con_libro", "Con libro"), ("autores_sin_libro", "Sin libro")), authors_with_and_without_books),
        (9, "¿Cuántas editoriales están registradas?", (("total_editoriales", "Total"),), total_publishers),
        (10, "¿Cuántas editoriales no tienen libros asociados?", (("editoriales_sin_libros", "Total"),), publishers_without_books),
        (11, "¿Cuántos libros integran el catálogo?", (("total_libros", "Total"),), total_books),
        (12, '¿Cuántos títulos comienzan con "El"?', (("titulos_que_comienzan_con_el", "Total"),), books_starting_with),
        (13, "¿Cuántos libros se publicaron en cada año?", (("anio_publicacion", "Año"), ("cantidad_libros", "Libros")), books_by_publication_year),
        (14, "¿Qué editoriales tienen la mayor cantidad de libros?", (("editorial", "Editorial"), ("cantidad_libros", "Libros")), publishers_with_most_books),
        (15, "¿Hay libros sin autor asociado?", (("id_libro", "ID"), ("titulo", "Título")), books_without_authors),
        (16, "¿Hay libros sin ejemplares registrados?", (("id_libro", "ID"), ("titulo", "Título")), books_without_copies),
        (17, "¿Cuántos libros tienen uno, dos o tres ejemplares?", (("cantidad_ejemplares", "Ejemplares"), ("cantidad_libros", "Libros")), books_grouped_by_copy_count),
        (18, "¿Cuántos ejemplares están operativos y cuántos en reparación?", (("estado", "Estado"), ("cantidad_ejemplares", "Ejemplares")), copies_by_state),
        (19, "¿Qué libros tienen ejemplares en reparación?", (("editorial", "Editorial"), ("titulo", "Título"), ("ejemplares_en_reparacion", "En reparación")), books_with_copies_in_repair),
        (20, "¿Qué libros tienen menos de tres ejemplares?", (("editorial", "Editorial"), ("titulo", "Título"), ("cantidad_ejemplares", "Ejemplares")), books_with_fewer_copies),
    )
    return [
        ReportResult(number, question, columns, query(db))
        for number, question, columns, query in definitions
    ]
