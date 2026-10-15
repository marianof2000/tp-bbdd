from urllib.parse import quote
from typing import Any

from fastapi import Request
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app.core.auth import current_user


def redirect(url: str, message: str = "", error: str = "") -> RedirectResponse:
    """Precondiciones: ``url`` es una ruta de redirección válida.
    Postcondiciones: devuelve una redirección 303 con mensajes codificados.
    """
    parts = []
    if message:
        parts.append("mensaje=" + quote(message))
    if error:
        parts.append("error=" + quote(error))
    return RedirectResponse(url + (("?" + "&".join(parts)) if parts else ""), status_code=303)


def validation_message(exc: ValidationError) -> str:
    """Precondiciones: ``exc`` contiene errores de validación de Pydantic.
    Postcondiciones: devuelve sus mensajes unidos y aptos para mostrar.
    """
    return "; ".join(str(item["msg"]).replace("Value error, ", "") for item in exc.errors())


def context(request: Request, **values: Any) -> dict[str, Any]:
    """Precondiciones: ``request`` posee parámetros de consulta y sesión.
    Postcondiciones: devuelve el contexto base combinado con los valores dados.
    """
    return {"request": request, "mensaje": request.query_params.get("mensaje"),
            "error": request.query_params.get("error"), "current_user": current_user(request), **values}
