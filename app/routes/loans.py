from datetime import date
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.auth import require_admin
from app.db.session import get_db
from app.models import Bibliotecario, Prestamo, Socio, TelefonoSocio
from app.routes.helpers import context, redirect, validation_message
from app.schemas.entities import PrestamoData, TelefonoData
from app.services import crud
from app.services.library import (
    BusinessRuleError,
    add_phone,
    create_loan,
    list_available_copies,
    return_loan,
)

router = APIRouter()


@router.post("/socios/{member_id}/telefonos", dependencies=[Depends(require_admin)])
async def phone_create(member_id: int, request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el administrador envió un teléfono para un socio existente.
    Postcondiciones: agrega el teléfono o redirige con un error validado.
    """
    member = db.get(Socio, member_id)
    if not member: raise HTTPException(404)
    try:
        add_phone(db, member, TelefonoData.model_validate(dict(await request.form())))
        return redirect(f"/socios/{member_id}", "Teléfono agregado.")
    except ValidationError as exc:
        return redirect(f"/socios/{member_id}", error=validation_message(exc))


@router.post("/socios/{member_id}/telefonos/{phone_id}/eliminar", dependencies=[Depends(require_admin)])
def phone_delete(member_id: int, phone_id: int, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el usuario es administrador y ambos IDs son enteros.
    Postcondiciones: elimina el teléfono del socio o lanza HTTP 404.
    """
    phone = db.get(TelefonoSocio, phone_id)
    if not phone or phone.id_socio != member_id: raise HTTPException(404)
    crud.delete(db, phone)
    return redirect(f"/socios/{member_id}", "Teléfono eliminado.")


@router.get("/prestamos", response_class=HTMLResponse)
def loans(request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: la sesión de base de datos está activa.
    Postcondiciones: devuelve el listado de préstamos sin modificar datos.
    """
    return request.app.state.templates.TemplateResponse(
        request=request, name="loans/list.html",
        context=context(request, loans=crud.list_all(db, Prestamo)),
    )


@router.get("/prestamos/nuevo", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
def loan_new(request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el usuario es administrador.
    Postcondiciones: devuelve el formulario para registrar un préstamo.
    """
    return request.app.state.templates.TemplateResponse(
        request=request, name="loans/form.html",
        context=loan_form_context(request, db),
    )


def loan_form_context(
    request: Request,
    db: Session,
    form: dict[str, Any] | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    """Precondiciones: la sesión está activa; formulario y error son opcionales.
    Postcondiciones: devuelve socios, bibliotecarios y ejemplares disponibles.
    """
    return context(
        request,
        members=crud.list_all(db, Socio),
        librarians=crud.list_all(db, Bibliotecario),
        copies=list_available_copies(db),
        form=form,
        error=error,
    )


@router.post("/prestamos/nuevo", dependencies=[Depends(require_admin)])
async def loan_create(request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el administrador envió un formulario de préstamo.
    Postcondiciones: registra el préstamo o devuelve un error comprensible.
    """
    values = dict(await request.form())
    try:
        create_loan(db, PrestamoData.model_validate(values))
        return redirect("/prestamos", "Préstamo registrado.")
    except ValidationError as exc:
        return request.app.state.templates.TemplateResponse(
            request=request, name="loans/form.html",
            context=loan_form_context(request, db, form=values, error=validation_message(exc)),
            status_code=422,
        )
    except BusinessRuleError as exc:
        return request.app.state.templates.TemplateResponse(
            request=request, name="loans/form.html",
            context=loan_form_context(request, db, form=values, error=str(exc)),
            status_code=422,
        )


@router.get("/prestamos/{loan_id}", response_class=HTMLResponse)
def loan_detail(loan_id: int, request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: ``loan_id`` es un identificador entero.
    Postcondiciones: devuelve el detalle del préstamo o lanza HTTP 404.
    """
    loan = db.get(Prestamo, loan_id)
    if not loan: raise HTTPException(404)
    return request.app.state.templates.TemplateResponse(
        request=request, name="loans/detail.html",
        context=context(request, loan=loan, today=date.today()),
    )


@router.get("/prestamos/{loan_id}/editar", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
def loan_edit(loan_id: int, request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el usuario es administrador y el ID es entero.
    Postcondiciones: muestra la edición si el préstamo sigue activo.
    """
    loan = db.get(Prestamo, loan_id)
    if not loan: raise HTTPException(404)
    if loan.fecha_devolucion:
        return redirect(f"/prestamos/{loan_id}", error="Un préstamo devuelto no se puede editar.")
    return request.app.state.templates.TemplateResponse(
        request=request, name="loans/edit.html",
        context=context(request, loan=loan, librarians=crud.list_all(db, Bibliotecario)),
    )


@router.post("/prestamos/{loan_id}/editar", dependencies=[Depends(require_admin)])
async def loan_update(loan_id: int, request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el administrador envió datos para un préstamo activo.
    Postcondiciones: actualiza el préstamo o devuelve un error validado.
    """
    loan = db.get(Prestamo, loan_id)
    if not loan: raise HTTPException(404)
    if loan.fecha_devolucion:
        return redirect(f"/prestamos/{loan_id}", error="Un préstamo devuelto no se puede editar.")
    values = dict(await request.form())
    values.update(id_socio=loan.id_socio, id_ejemplar=loan.id_ejemplar)
    try:
        data = PrestamoData.model_validate(values)
        crud.update(db, loan, data.model_dump())
        return redirect(f"/prestamos/{loan_id}", "Préstamo actualizado.")
    except ValidationError as exc:
        return request.app.state.templates.TemplateResponse(
            request=request, name="loans/edit.html",
            context=context(
                request, loan=loan, librarians=crud.list_all(db, Bibliotecario),
                form=values, error=validation_message(exc),
            ),
            status_code=422,
        )


@router.post("/prestamos/{loan_id}/devolver", dependencies=[Depends(require_admin)])
async def loan_return(loan_id: int, request: Request, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el administrador envió una fecha para un préstamo existente.
    Postcondiciones: registra la devolución o redirige con el error.
    """
    loan = db.get(Prestamo, loan_id)
    if not loan: raise HTTPException(404)
    try:
        returned_on = date.fromisoformat(str((await request.form()).get("fecha_devolucion")))
        return_loan(db, loan, returned_on)
        return redirect(f"/prestamos/{loan_id}", "Devolución registrada.")
    except (ValueError, BusinessRuleError) as exc:
        return redirect(f"/prestamos/{loan_id}", error=str(exc))


@router.post("/prestamos/{loan_id}/eliminar", dependencies=[Depends(require_admin)])
def loan_delete(loan_id: int, db: Session = Depends(get_db)) -> Response:
    """Precondiciones: el usuario es administrador y el ID es entero.
    Postcondiciones: elimina solo un préstamo devuelto o informa el impedimento.
    """
    loan = db.get(Prestamo, loan_id)
    if not loan: raise HTTPException(404)
    if not loan.fecha_devolucion:
        return redirect("/prestamos", error="No se puede eliminar un préstamo activo; registrá primero la devolución.")
    crud.delete(db, loan)
    return redirect("/prestamos", "Préstamo eliminado.")
