from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.auth import authenticate, current_user
from app.routes.helpers import context, redirect

router = APIRouter()


def safe_next_path(value: str | None) -> str:
    if value and value.startswith("/") and not value.startswith("//"):
        return value
    return "/"


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    if current_user(request):
        return redirect("/")
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context=context(request, next_path=safe_next_path(request.query_params.get("next"))),
    )


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request):
    form = await request.form()
    username = str(form.get("username", ""))
    password = str(form.get("password", ""))
    next_path = safe_next_path(str(form.get("next", "/")))
    user = authenticate(username, password)
    if user is None:
        return request.app.state.templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context=context(
                request,
                next_path=next_path,
                username=username,
                error="Usuario o contraseña incorrectos.",
            ),
            status_code=401,
        )
    request.session.clear()
    request.session["user"] = {"username": user.username, "role": user.role}
    return RedirectResponse(next_path, status_code=303)


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return redirect("/login", "La sesión se cerró correctamente.")
