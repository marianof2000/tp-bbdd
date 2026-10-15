from datetime import date, timedelta

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
    Socio,
)
from app.schemas.entities import PrestamoData
from app.services.crud import PersistenceError, ReferencedRecordError, create, delete
from app.services.library import BusinessRuleError, create_loan, return_loan


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        yield session


def seed_library(db: Session):
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
    today = date.today()
    return PrestamoData(
        id_socio=member.id_persona,
        id_bibliotecario=librarian.id_persona,
        id_ejemplar=copy.id_ejemplar,
        fecha_prestamo=today,
        fecha_vencimiento_inicial=today + timedelta(days=7),
        fecha_vencimiento_actual=today + timedelta(days=7),
    )


def test_loan_cannot_be_duplicated_and_can_be_returned(db: Session):
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


def test_duplicate_document_rolls_back(db: Session):
    create(db, Persona, {"nombre": "A", "apellido": "A", "documento": "10", "email": None})

    with pytest.raises(PersistenceError):
        create(db, Persona, {"nombre": "B", "apellido": "B", "documento": "10", "email": None})

    assert db.query(Persona).count() == 1


def test_referenced_record_cannot_be_deleted(db: Session):
    _, _, _, publisher = seed_library(db)

    with pytest.raises(ReferencedRecordError):
        delete(db, publisher)


def test_current_due_date_cannot_precede_initial_due_date():
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
