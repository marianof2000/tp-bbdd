from datetime import date, timedelta
from collections.abc import Generator
from typing import Any

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models import (
    Autor,
    Bibliotecario,
    Editorial,
    Ejemplar,
    Libro,
    LibroAutor,
    Persona,
    Prestamo,
    Socio,
)
from app.schemas.entities import PrestamoData
from app.services.crud import PersistenceError, ReferencedRecordError, create, delete
from app.services.library import BusinessRuleError, create_loan, return_loan
from app.services.library_queries import (
    get_book_availability,
    get_library_statistics,
    list_overdue_loans,
    search_books,
    search_books_by_author,
    search_members,
)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    """Precondiciones: SQLite está disponible en memoria.
    Postcondiciones: entrega una sesión aislada con el esquema creado.
    """
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection: Any, _: Any) -> None:
        """Precondiciones: SQLite acaba de abrir una conexión DB-API.
        Postcondiciones: activa la verificación de claves foráneas.
        """
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        yield session


def seed_library(db: Session) -> tuple[Socio, Bibliotecario, Ejemplar, Editorial]:
    """Precondiciones: ``db`` es una sesión vacía con el esquema creado.
    Postcondiciones: confirma y devuelve datos básicos relacionados.
    """
    member_person = Persona(nombre="Ana", apellido="Paz", documento="1", email=None)
    librarian_person = Persona(nombre="Luis", apellido="Sol", documento="2", email=None)
    publisher = Editorial(nombre="Editorial de prueba")
    author = Autor(nombre="Ada", apellido="Lovelace")
    db.add_all([member_person, librarian_person, publisher, author])
    db.flush()

    member = Socio(id_persona=member_person.id_persona, fecha_alta=date.today())
    librarian = Bibliotecario(id_persona=librarian_person.id_persona, legajo="B-1")
    book = Libro(
        titulo="Libro de prueba",
        isbn="978-0-00-000000-1",
        anio_publicacion=2020,
        id_editorial=publisher.id_editorial,
    )
    db.add_all([member, librarian, book])
    db.flush()
    db.add(LibroAutor(id_libro=book.id_libro, id_autor=author.id_autor, orden_autoria=1))
    copy = Ejemplar(
        id_libro=book.id_libro,
        codigo_inventario="E-1",
        fecha_incorporacion=date.today(),
        estado="operativo",
    )
    db.add(copy)
    db.commit()
    return member, librarian, copy, publisher


def loan_data(member: Socio, librarian: Bibliotecario, copy: Ejemplar) -> PrestamoData:
    """Precondiciones: las tres entidades tienen identificadores persistidos.
    Postcondiciones: devuelve datos coherentes para un préstamo de siete días.
    """
    today = date.today()
    return PrestamoData(
        id_socio=member.id_persona,
        id_bibliotecario=librarian.id_persona,
        id_ejemplar=copy.id_ejemplar,
        fecha_prestamo=today,
        fecha_vencimiento_inicial=today + timedelta(days=7),
        fecha_vencimiento_actual=today + timedelta(days=7),
    )


def test_loan_cannot_be_duplicated_and_can_be_returned(db: Session) -> None:
    """Precondiciones: la prueba recibe una base aislada.
    Postcondiciones: verifica unicidad del préstamo activo y su devolución.
    """
    member, librarian, copy, _ = seed_library(db)
    data = loan_data(member, librarian, copy)

    loan = create_loan(db, data)
    assert loan.fecha_devolucion is None
    assert copy.estado == "operativo"

    with pytest.raises(BusinessRuleError, match="préstamo activo"):
        create_loan(db, data)

    return_loan(db, loan, date.today())
    assert loan.fecha_devolucion == date.today()
    assert copy.estado == "operativo"


def test_duplicate_document_rolls_back(db: Session) -> None:
    """Precondiciones: la prueba recibe una base aislada.
    Postcondiciones: verifica el rollback ante un documento duplicado.
    """
    create(db, Persona, {"nombre": "A", "apellido": "A", "documento": "10", "email": None})

    with pytest.raises(PersistenceError):
        create(db, Persona, {"nombre": "B", "apellido": "B", "documento": "10", "email": None})

    assert db.query(Persona).count() == 1


def test_referenced_record_cannot_be_deleted(db: Session) -> None:
    """Precondiciones: la prueba recibe una base aislada con claves foráneas.
    Postcondiciones: verifica que no se elimine una editorial referenciada.
    """
    _, _, _, publisher = seed_library(db)

    with pytest.raises(ReferencedRecordError):
        delete(db, publisher)


def test_current_due_date_cannot_precede_initial_due_date() -> None:
    """Precondiciones: se construyen fechas deterministas relativas a hoy.
    Postcondiciones: verifica el rechazo de vencimientos incoherentes.
    """
    today = date.today()

    with pytest.raises(ValueError, match="vencimiento actual"):
        PrestamoData(
            id_socio=1,
            id_bibliotecario=2,
            id_ejemplar=3,
            fecha_prestamo=today,
            fecha_vencimiento_inicial=today + timedelta(days=14),
            fecha_vencimiento_actual=today + timedelta(days=7),
        )


def test_search_books_returns_catalog_details(db: Session) -> None:
    """Precondiciones: existe un libro con autor y editorial.
    Postcondiciones: la búsqueda parcial ignora mayúsculas y devuelve sus relaciones.
    """
    seed_library(db)

    results = search_books(db, "LIBRO DE")

    assert results == [
        {
            "id_libro": 1,
            "titulo": "Libro de prueba",
            "isbn": "978-0-00-000000-1",
            "editorial": "Editorial de prueba",
            "autores": ["Ada Lovelace"],
            "anio_publicacion": 2020,
        }
    ]


def test_search_books_by_author_returns_catalog_details(db: Session) -> None:
    """Precondiciones: existe un libro relacionado con una autora.
    Postcondiciones: la búsqueda acepta nombre completo sin distinguir mayúsculas.
    """
    seed_library(db)

    results = search_books_by_author(db, "ADA LOVELACE")

    assert len(results) == 1
    assert results[0]["titulo"] == "Libro de prueba"
    assert results[0]["autores"] == ["Ada Lovelace"]


def test_search_members_returns_only_members(db: Session) -> None:
    """Precondiciones: existen un socio y una persona que sólo es bibliotecaria.
    Postcondiciones: devuelve el socio por nombre completo con sus datos públicos.
    """
    member, _, _, _ = seed_library(db)

    results = search_members(db, "ANA PAZ")

    assert results == [
        {
            "id_socio": member.id_persona,
            "nombre": "Ana",
            "apellido": "Paz",
            "documento": "1",
            "email": None,
            "fecha_alta": date.today().isoformat(),
            "telefonos": [],
        }
    ]


def test_read_only_library_queries(db: Session) -> None:
    """Precondiciones: hay ejemplares en distintos estados e historiales de préstamo.
    Postcondiciones: disponibilidad, vencimientos y estadísticas respetan préstamos activos.
    """
    member, librarian, available_copy, _ = seed_library(db)
    book_id = available_copy.id_libro
    reference_date = date(2026, 1, 20)
    repair_copy = Ejemplar(
        id_libro=book_id,
        codigo_inventario="E-2",
        fecha_incorporacion=reference_date,
        estado="en_reparacion",
    )
    overdue_copy = Ejemplar(
        id_libro=book_id,
        codigo_inventario="E-3",
        fecha_incorporacion=reference_date,
        estado="operativo",
    )
    current_copy = Ejemplar(
        id_libro=book_id,
        codigo_inventario="E-4",
        fecha_incorporacion=reference_date,
        estado="operativo",
    )
    db.add_all([repair_copy, overdue_copy, current_copy])
    db.flush()
    db.add_all(
        [
            Prestamo(
                id_socio=member.id_persona,
                id_bibliotecario=librarian.id_persona,
                id_ejemplar=overdue_copy.id_ejemplar,
                fecha_prestamo=date(2026, 1, 1),
                fecha_vencimiento_inicial=date(2026, 1, 10),
                fecha_vencimiento_actual=date(2026, 1, 10),
                fecha_devolucion=None,
            ),
            Prestamo(
                id_socio=member.id_persona,
                id_bibliotecario=librarian.id_persona,
                id_ejemplar=current_copy.id_ejemplar,
                fecha_prestamo=date(2026, 1, 15),
                fecha_vencimiento_inicial=date(2026, 1, 25),
                fecha_vencimiento_actual=date(2026, 1, 25),
                fecha_devolucion=None,
            ),
            Prestamo(
                id_socio=member.id_persona,
                id_bibliotecario=librarian.id_persona,
                id_ejemplar=repair_copy.id_ejemplar,
                fecha_prestamo=date(2025, 12, 20),
                fecha_vencimiento_inicial=date(2026, 1, 5),
                fecha_vencimiento_actual=date(2026, 1, 5),
                fecha_devolucion=date(2026, 1, 6),
            ),
        ]
    )
    db.commit()

    assert get_book_availability(db, book_id) == {
        "id_libro": book_id,
        "titulo": "Libro de prueba",
        "total": 4,
        "disponibles": 1,
        "prestados": 2,
        "en_reparacion": 1,
    }

    overdue = list_overdue_loans(db, as_of=reference_date)
    assert len(overdue) == 1
    assert overdue[0]["socio"]["nombre"] == "Ana Paz"
    assert overdue[0]["libro"]["titulo"] == "Libro de prueba"
    assert overdue[0]["ejemplar"]["codigo_inventario"] == "E-3"
    assert overdue[0]["dias_vencido"] == 10

    assert get_library_statistics(db, as_of=reference_date) == {
        "libros": 1,
        "ejemplares": 4,
        "socios": 1,
        "prestamos_activos": 2,
        "prestamos_vencidos": 1,
    }
