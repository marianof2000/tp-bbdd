from datetime import date

from sqlalchemy import delete, exists, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import (Autor, Bibliotecario, Ejemplar, Libro, LibroAutor, Prestamo,
                        Socio, TelefonoSocio)
from app.schemas.entities import LibroData, PrestamoData, TelefonoData
from app.services.crud import PersistenceError, persistence_message


class BusinessRuleError(Exception):
    pass


def save_book(db: Session, book: Libro | None, data: LibroData, author_ids: list[int]) -> Libro:
    if not author_ids:
        raise BusinessRuleError("Seleccioná al menos un autor.")
    authors = list(db.scalars(select(Autor).where(Autor.id_autor.in_(author_ids))))
    if len(authors) != len(set(author_ids)):
        raise BusinessRuleError("Uno o más autores no existen.")
    try:
        if book is None:
            book = Libro(**data.model_dump())
            db.add(book)
            db.flush()
        else:
            for key, value in data.model_dump().items():
                setattr(book, key, value)
            db.execute(delete(LibroAutor).where(LibroAutor.id_libro == book.id_libro))
        for order, author_id in enumerate(author_ids, start=1):
            db.add(LibroAutor(id_libro=book.id_libro, id_autor=author_id, orden_autoria=order))
        db.commit()
        db.refresh(book)
        return book
    except BusinessRuleError:
        db.rollback()
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise PersistenceError(persistence_message(exc)) from exc


def add_phone(db: Session, member: Socio, data: TelefonoData) -> TelefonoSocio:
    try:
        phone = TelefonoSocio(id_socio=member.id_persona, **data.model_dump())
        db.add(phone)
        db.commit()
        db.refresh(phone)
        return phone
    except SQLAlchemyError as exc:
        db.rollback()
        raise PersistenceError(persistence_message(exc)) from exc


def create_loan(db: Session, data: PrestamoData) -> Prestamo:
    settings = get_settings()
    member = db.get(Socio, data.id_socio)
    librarian = db.get(Bibliotecario, data.id_bibliotecario)
    copy = db.scalar(
        select(Ejemplar)
        .where(Ejemplar.id_ejemplar == data.id_ejemplar)
        .with_for_update()
    )
    if not member or not librarian or not copy:
        raise BusinessRuleError("El socio, ejemplar o bibliotecario seleccionado no existe.")
    if copy.estado.casefold() != settings.available_copy_state.casefold():
        raise BusinessRuleError(f"El ejemplar no está {settings.available_copy_state}.")
    try:
        active_loan = db.scalar(
            select(Prestamo.id_prestamo).where(
                Prestamo.id_ejemplar == copy.id_ejemplar,
                Prestamo.fecha_devolucion.is_(None),
            ).limit(1)
        )
        if active_loan:
            raise BusinessRuleError("El ejemplar ya tiene un préstamo activo.")
        loan = Prestamo(**data.model_dump(), fecha_devolucion=None)
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return loan
    except BusinessRuleError:
        db.rollback()
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise PersistenceError(persistence_message(exc)) from exc


def return_loan(db: Session, loan: Prestamo, returned_on: date) -> None:
    if loan.fecha_devolucion:
        raise BusinessRuleError("Este préstamo ya fue devuelto.")
    if returned_on < loan.fecha_prestamo:
        raise BusinessRuleError("La devolución no puede ser anterior al préstamo.")
    try:
        loan.fecha_devolucion = returned_on
        loan.ejemplar.estado = get_settings().available_copy_state
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise PersistenceError(persistence_message(exc)) from exc


def list_available_copies(db: Session) -> list[Ejemplar]:
    active_loan_exists = exists().where(
        Prestamo.id_ejemplar == Ejemplar.id_ejemplar,
        Prestamo.fecha_devolucion.is_(None),
    )
    statement = select(Ejemplar).where(
        Ejemplar.estado == get_settings().available_copy_state,
        ~active_loan_exists,
    )
    return list(db.scalars(statement).all())
