from typing import Any, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.base import Base

Model = TypeVar("Model", bound=Base)


class ReferencedRecordError(Exception):
    pass


class PersistenceError(Exception):
    """Error de persistencia apto para mostrar sin exponer datos de conexión."""


def persistence_message(exc: SQLAlchemyError) -> str:
    if isinstance(exc, IntegrityError):
        return "No se pudo guardar porque el valor está repetido o relacionado con datos inválidos."
    return "No se pudo acceder a la base de datos. Revisá la conexión e intentá nuevamente."


def list_all(db: Session, model: type[Model]) -> list[Model]:
    return list(db.scalars(select(model)).all())


def get_or_none(db: Session, model: type[Model], record_id: int) -> Model | None:
    return db.get(model, record_id)


def create(db: Session, model: type[Model], data: dict[str, Any]) -> Model:
    try:
        obj = model(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except SQLAlchemyError as exc:
        db.rollback()
        raise PersistenceError(persistence_message(exc)) from exc


def update(db: Session, obj: Model, data: dict[str, Any]) -> Model:
    try:
        for key, value in data.items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj
    except SQLAlchemyError as exc:
        db.rollback()
        raise PersistenceError(persistence_message(exc)) from exc


def delete(db: Session, obj: Model) -> None:
    try:
        db.delete(obj)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ReferencedRecordError("El registro está siendo utilizado y no se puede eliminar.") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise PersistenceError(persistence_message(exc)) from exc
