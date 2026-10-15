from urllib.parse import quote

from fastapi import Request
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app.core.auth import current_user


def redirect(url: str, message: str = "", error: str = "") -> RedirectResponse:
    parts = []
    if message:
        parts.append("mensaje=" + quote(message))
    if error:
        parts.append("error=" + quote(error))
    return RedirectResponse(url + (("?" + "&".join(parts)) if parts else ""), status_code=303)


def validation_message(exc: ValidationError) -> str:
    return "; ".join(str(item["msg"]).replace("Value error, ", "") for item in exc.errors())


def context(request: Request, **values):
    return {"request": request, "mensaje": request.query_params.get("mensaje"),
            "error": request.query_params.get("error"), "current_user": current_user(request), **values}
