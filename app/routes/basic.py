from dataclasses import dataclass
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Autor, Bibliotecario, Editorial, Persona, Socio
from app.schemas.entities import AutorData, BibliotecarioData, EditorialData, PersonaData, SocioData
from app.services import crud
from app.routes.helpers import context, redirect, validation_message

router = APIRouter()


@dataclass
class Resource:
    title: str
    singular: str
    model: type
    schema: type[BaseModel]
    pk: str
    fields: list[tuple[str, str, str]]


RESOURCES = {
    "personas": Resource("Personas", "persona", Persona, PersonaData, "id_persona",
                         [("nombre", "Nombre", "text"), ("apellido", "Apellido", "text"),
                          ("documento", "Documento", "text"), ("email", "Email", "email")]),
    "socios": Resource("Socios", "socio", Socio, SocioData, "id_persona",
                       [("id_persona", "Persona", "persona"), ("fecha_alta", "Fecha de alta", "date")]),
    "bibliotecarios": Resource("Bibliotecarios", "bibliotecario", Bibliotecario, BibliotecarioData,
                               "id_persona", [("id_persona", "Persona", "persona"), ("legajo", "Legajo", "text")]),
    "editoriales": Resource("Editoriales", "editorial", Editorial, EditorialData, "id_editorial",
                            [("nombre", "Nombre", "text")]),
    "autores": Resource("Autores", "autor", Autor, AutorData, "id_autor",
                        [("nombre", "Nombre", "text"), ("apellido", "Apellido", "text")]),
}


def resource_or_404(name: str) -> Resource:
    if name not in RESOURCES:
        raise HTTPException(404)
    return RESOURCES[name]


def choices(db: Session, resource: Resource):
    if any(field[2] == "persona" for field in resource.fields):
        return {"personas": crud.list_all(db, Persona)}
    return {}


@router.get("/{resource_name}", response_class=HTMLResponse)
def resource_list(resource_name: str, request: Request, db: Session = Depends(get_db)):
    resource = resource_or_404(resource_name)
    return request.app.state.templates.TemplateResponse(
        request=request, name="basic/list.html",
        context=context(request, resource=resource, items=crud.list_all(db, resource.model)),
    )


@router.get("/{resource_name}/nuevo", response_class=HTMLResponse)
def resource_new(resource_name: str, request: Request, db: Session = Depends(get_db)):
    resource = resource_or_404(resource_name)
    return request.app.state.templates.TemplateResponse(
        request=request, name="basic/form.html",
        context=context(request, resource=resource, item=None, choices=choices(db, resource)),
    )


@router.post("/{resource_name}/nuevo")
async def resource_create(resource_name: str, request: Request, db: Session = Depends(get_db)):
    resource = resource_or_404(resource_name)
    values = dict(await request.form())
    try:
        data = resource.schema.model_validate(values)
        crud.create(db, resource.model, data.model_dump())
        return redirect(f"/{resource_name}", f"{resource.singular.capitalize()} creado correctamente.")
    except ValidationError as exc:
        return request.app.state.templates.TemplateResponse(
            request=request, name="basic/form.html",
            context=context(
                request, resource=resource, item=None, choices=choices(db, resource),
                form=values, error=validation_message(exc),
            ),
            status_code=422,
        )
    except crud.PersistenceError as exc:
        return request.app.state.templates.TemplateResponse(
            request=request, name="basic/form.html",
            context=context(
                request, resource=resource, item=None, choices=choices(db, resource),
                form=values, error=str(exc),
            ),
            status_code=409,
        )


@router.get("/{resource_name}/{record_id:int}", response_class=HTMLResponse)
def resource_detail(resource_name: str, record_id: int, request: Request, db: Session = Depends(get_db)):
    resource = resource_or_404(resource_name)
    item = crud.get_or_none(db, resource.model, record_id)
    if not item: raise HTTPException(404)
    return request.app.state.templates.TemplateResponse(
        request=request, name="basic/detail.html",
        context=context(request, resource=resource, item=item),
    )


@router.get("/{resource_name}/{record_id:int}/editar", response_class=HTMLResponse)
def resource_edit(resource_name: str, record_id: int, request: Request, db: Session = Depends(get_db)):
    resource = resource_or_404(resource_name)
    item = crud.get_or_none(db, resource.model, record_id)
    if not item: raise HTTPException(404)
    return request.app.state.templates.TemplateResponse(
        request=request, name="basic/form.html",
        context=context(request, resource=resource, item=item, choices=choices(db, resource)),
    )


@router.post("/{resource_name}/{record_id:int}/editar")
async def resource_update(resource_name: str, record_id: int, request: Request, db: Session = Depends(get_db)):
    resource = resource_or_404(resource_name)
    item = crud.get_or_none(db, resource.model, record_id)
    if not item: raise HTTPException(404)
    values = dict(await request.form())
    try:
        if resource.pk == "id_persona" and "id_persona" in values:
            values["id_persona"] = record_id
        data = resource.schema.model_validate(values)
        changes = data.model_dump()
        changes.pop(resource.pk, None)
        crud.update(db, item, changes)
        return redirect(f"/{resource_name}", "Cambios guardados.")
    except ValidationError as exc:
        return request.app.state.templates.TemplateResponse(
            request=request, name="basic/form.html",
            context=context(
                request, resource=resource, item=item, choices=choices(db, resource),
                form=values, error=validation_message(exc),
            ),
            status_code=422,
        )


@router.post("/{resource_name}/{record_id:int}/eliminar")
def resource_delete(resource_name: str, record_id: int, db: Session = Depends(get_db)):
    resource = resource_or_404(resource_name)
    item = crud.get_or_none(db, resource.model, record_id)
    if not item: raise HTTPException(404)
    try:
        crud.delete(db, item)
        return redirect(f"/{resource_name}", "Registro eliminado.")
    except crud.ReferencedRecordError as exc:
        return redirect(f"/{resource_name}", error=str(exc))
