from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from app.core.auth import authenticate, current_user
from app.routes.helpers import context, redirect

router = APIRouter()


def safe_next_path(value: str | None) -> str:
    """Precondiciones: ``value`` es una ruta opcional proporcionada por el cliente.
    Postcondiciones: devuelve una ruta interna segura o ``/``.
    """
    if value and value.startswith("/") and not value.startswith("//"):
        return value
    return "/"


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request) -> Response:
    """Precondiciones: la petición tiene soporte de sesión.
    Postcondiciones: muestra el ingreso o redirige si ya existe una sesión.
    """
    if current_user(request):
        return redirect("/")
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context=context(request, next_path=safe_next_path(request.query_params.get("next"))),
    )


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request) -> Response:
    """Precondiciones: el cuerpo puede interpretarse como formulario.
    Postcondiciones: inicia una sesión válida o responde 401 sin revelar detalles.
    """
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
async def logout(request: Request) -> Response:
    """Precondiciones: la petición tiene soporte de sesión.
    Postcondiciones: vacía la sesión y redirige al ingreso.
    """
    request.session.clear()
    return redirect("/login", "La sesión se cerró correctamente.")
