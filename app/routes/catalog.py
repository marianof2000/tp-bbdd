from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.datastructures import FormData

from app.core.auth import require_admin
from app.core.config import get_settings
from app.db.session import get_db
from app.models import Autor, Editorial, Ejemplar, Libro
from app.routes.helpers import context, redirect, validation_message
from app.schemas.entities import EjemplarData, LibroData
from app.services import crud
from app.services.library import BusinessRuleError, save_book

router = APIRouter()


def ordered_author_ids(form: FormData) -> list[int]:
    """Precondiciones: ``form`` contiene autores seleccionados y sus órdenes.
    Postcondiciones: devuelve IDs ordenados o lanza ``ValueError`` si son inválidos.
    """
    selected = [int(value) for value in form.getlist("autores")]
    ordered = []
    for author_id in selected:
        raw_order = str(form.get(f"orden_{author_id}", "")).strip()
        if not raw_order:
            raise ValueError("Indicá el orden de cada autor seleccionado.")
        order = int(raw_order)
        if order < 1:
            raise ValueError("El orden de autoría debe comenzar en 1.")
        ordered.append((order, author_id))
    if len({order for order, _ in ordered}) != len(ordered):
        raise ValueError("El orden de autoría no puede repetirse.")
    return [author_id for _, author_id in sorted(ordered)]


@router.get("/libros", response_class=HTMLResponse)
def books(request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: la sesión de base de datos está activa.
    Postcondiciones: devuelve el listado de libros sin modificar datos.
    """
    return request.app.state.templates.TemplateResponse(
        request=request, name="books/list.html",
        context=context(request, books=crud.list_all(db, Libro)),
    )


def book_form_context(
    request: Request,
    db: Session,
    book: Libro | None = None,
    form: FormData | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    """Precondiciones: la sesión está activa; libro y formulario son opcionales.
    Postcondiciones: devuelve el contexto completo del formulario de libro.
    """
    selected = (
        {int(value) for value in form.getlist("autores")}
        if form is not None
        else ({link.id_autor for link in book.autores} if book else set())
    )
    return context(
        request,
        book=book,
        editorials=crud.list_all(db, Editorial),
        authors=crud.list_all(db, Autor),
        selected=selected,
        form=form,
        error=error,
    )


@router.get("/libros/nuevo", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
def book_new(request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el usuario es administrador.
    Postcondiciones: devuelve el formulario vacío de libro.
    """
    return request.app.state.templates.TemplateResponse(
        request=request, name="books/form.html", context=book_form_context(request, db)
    )


@router.post("/libros/nuevo", dependencies=[Depends(require_admin)])
async def book_create(request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el administrador envió datos de libro y autoría.
    Postcondiciones: crea el libro o devuelve el formulario con error.
    """
    form = await request.form()
    try:
        data = LibroData.model_validate(dict(form))
        author_ids = ordered_author_ids(form)
        save_book(db, None, data, author_ids)
        return redirect("/libros", "Libro creado correctamente.")
    except (ValidationError, ValueError) as exc:
        message = validation_message(exc) if isinstance(exc, ValidationError) else str(exc)
        return request.app.state.templates.TemplateResponse(
            request=request, name="books/form.html",
            context=book_form_context(request, db, form=form, error=message),
            status_code=422,
        )
    except BusinessRuleError as exc:
        return request.app.state.templates.TemplateResponse(
            request=request, name="books/form.html",
            context=book_form_context(request, db, form=form, error=str(exc)),
            status_code=422,
        )


@router.get("/libros/{book_id}", response_class=HTMLResponse)
def book_detail(book_id: int, request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: ``book_id`` es un identificador entero.
    Postcondiciones: devuelve el detalle del libro o lanza HTTP 404.
    """
    book = db.get(Libro, book_id)
    if not book: raise HTTPException(404)
    return request.app.state.templates.TemplateResponse(
        request=request, name="books/detail.html", context=context(request, book=book)
    )


@router.get("/libros/{book_id}/editar", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
def book_edit(book_id: int, request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el usuario es administrador y el libro existe.
    Postcondiciones: devuelve el formulario cargado o lanza HTTP 404.
    """
    book = db.get(Libro, book_id)
    if not book: raise HTTPException(404)
    return request.app.state.templates.TemplateResponse(
        request=request, name="books/form.html", context=book_form_context(request, db, book)
    )


@router.post("/libros/{book_id}/editar", dependencies=[Depends(require_admin)])
async def book_update(book_id: int, request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el administrador envió datos para un libro existente.
    Postcondiciones: actualiza libro y autoría o devuelve un error.
    """
    book = db.get(Libro, book_id)
    if not book: raise HTTPException(404)
    form = await request.form()
    try:
        save_book(db, book, LibroData.model_validate(dict(form)), ordered_author_ids(form))
        return redirect("/libros", "Libro actualizado.")
    except (ValidationError, ValueError, BusinessRuleError) as exc:
        message = validation_message(exc) if isinstance(exc, ValidationError) else str(exc)
        return request.app.state.templates.TemplateResponse(
            request=request, name="books/form.html",
            context=book_form_context(request, db, book=book, form=form, error=message),
            status_code=422,
        )


@router.post("/libros/{book_id}/eliminar", dependencies=[Depends(require_admin)])
def book_delete(book_id: int, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el usuario es administrador y el ID es entero.
    Postcondiciones: elimina el libro o informa que está referenciado.
    """
    book = db.get(Libro, book_id)
    if not book: raise HTTPException(404)
    try:
        crud.delete(db, book)
        return redirect("/libros", "Libro eliminado.")
    except crud.ReferencedRecordError as exc:
        return redirect("/libros", error=str(exc))


@router.get("/ejemplares", response_class=HTMLResponse)
def copies(request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: la sesión de base de datos está activa.
    Postcondiciones: devuelve el listado de ejemplares sin modificar datos.
    """
    return request.app.state.templates.TemplateResponse(
        request=request, name="copies/list.html",
        context=context(request, copies=crud.list_all(db, Ejemplar)),
    )


def copy_form_context(
    request: Request,
    db: Session,
    copy: Ejemplar | None = None,
    form: dict[str, Any] | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    """Precondiciones: la sesión está activa; ejemplar y formulario son opcionales.
    Postcondiciones: devuelve el contexto completo del formulario de ejemplar.
    """
    return context(
        request,
        copy=copy,
        books=crud.list_all(db, Libro),
        copy_states=get_settings().copy_states,
        form=form,
        error=error,
    )


@router.get("/ejemplares/nuevo", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
def copy_new(request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el usuario es administrador.
    Postcondiciones: devuelve el formulario vacío de ejemplar.
    """
    return request.app.state.templates.TemplateResponse(
        request=request, name="copies/form.html",
        context=copy_form_context(request, db),
    )


@router.post("/ejemplares/nuevo", dependencies=[Depends(require_admin)])
async def copy_create(request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el administrador envió un formulario de ejemplar.
    Postcondiciones: crea el ejemplar o devuelve un error validado.
    """
    values = dict(await request.form())
    try:
        crud.create(db, Ejemplar, EjemplarData.model_validate(values).model_dump())
        return redirect("/ejemplares", "Ejemplar creado.")
    except ValidationError as exc:
        return request.app.state.templates.TemplateResponse(
            request=request, name="copies/form.html",
            context=copy_form_context(request, db, form=values, error=validation_message(exc)),
            status_code=422,
        )


@router.get("/ejemplares/{copy_id}/editar", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
def copy_edit(copy_id: int, request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el usuario es administrador y el ID es entero.
    Postcondiciones: devuelve el formulario cargado o lanza HTTP 404.
    """
    copy = db.get(Ejemplar, copy_id)
    if not copy: raise HTTPException(404)
    return request.app.state.templates.TemplateResponse(
        request=request, name="copies/form.html",
        context=copy_form_context(request, db, copy=copy),
    )


@router.get("/ejemplares/{copy_id}", response_class=HTMLResponse)
def copy_detail(copy_id: int, request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: ``copy_id`` es un identificador entero.
    Postcondiciones: devuelve el detalle del ejemplar o lanza HTTP 404.
    """
    copy = db.get(Ejemplar, copy_id)
    if not copy: raise HTTPException(404)
    return request.app.state.templates.TemplateResponse(
        request=request, name="copies/detail.html", context=context(request, copy=copy)
    )


@router.post("/ejemplares/{copy_id}/editar", dependencies=[Depends(require_admin)])
async def copy_update(copy_id: int, request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el administrador envió datos para un ejemplar existente.
    Postcondiciones: actualiza el ejemplar o devuelve un error validado.
    """
    copy = db.get(Ejemplar, copy_id)
    if not copy: raise HTTPException(404)
    values = dict(await request.form())
    try:
        crud.update(db, copy, EjemplarData.model_validate(values).model_dump())
        return redirect("/ejemplares", "Ejemplar actualizado.")
    except ValidationError as exc:
        return request.app.state.templates.TemplateResponse(
            request=request, name="copies/form.html",
            context=copy_form_context(
                request, db, copy=copy, form=values, error=validation_message(exc)
            ),
            status_code=422,
        )


@router.post("/ejemplares/{copy_id}/eliminar", dependencies=[Depends(require_admin)])
def copy_delete(copy_id: int, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el usuario es administrador y el ID es entero.
    Postcondiciones: elimina el ejemplar o informa que está referenciado.
    """
    copy = db.get(Ejemplar, copy_id)
    if not copy: raise HTTPException(404)
    try:
        crud.delete(db, copy)
        return redirect("/ejemplares", "Ejemplar eliminado.")
    except crud.ReferencedRecordError as exc:
        return redirect("/ejemplares", error=str(exc))
