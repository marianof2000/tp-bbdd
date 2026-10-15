from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.sessions import SessionMiddleware

from app.core.auth import PermissionDenied, current_user
from app.core.config import get_settings
from app.core.middleware import AuthenticationMiddleware
from app.routes import auth, basic, catalog, loans
from app.services.crud import PersistenceError

BASE_DIR = Path(__file__).resolve().parent
settings = get_settings()
app = FastAPI(title=settings.app_name)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.state.templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
    session_cookie="biblioteca_session",
    max_age=settings.session_max_age_seconds,
    same_site="lax",
    https_only=settings.session_https_only,
)


def database_error_response(request: Request, status_code: int = 503) -> Response:
    """Precondiciones: ``request`` pertenece a la aplicación y el estado tiene plantillas.
    Postcondiciones: devuelve una respuesta HTML segura con el estado indicado.
    """
    return app.state.templates.TemplateResponse(
        request=request,
        name="database_error.html",
        context={
            "request": request,
            "current_user": current_user(request),
            "error": "No se pudo acceder a la base de datos. Revisá la conexión e intentá nuevamente.",
        },
        status_code=status_code,
    )


@app.exception_handler(PersistenceError)
def persistence_error_handler(request: Request, exc: PersistenceError) -> Response:
    """Precondiciones: se produjo un ``PersistenceError`` durante una petición.
    Postcondiciones: devuelve una página de error con estado HTTP 409.
    """
    return app.state.templates.TemplateResponse(
        request=request,
        name="database_error.html",
        context={"request": request, "current_user": current_user(request), "error": str(exc)},
        status_code=409,
    )


@app.exception_handler(SQLAlchemyError)
def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError) -> Response:
    """Precondiciones: SQLAlchemy produjo un error durante una petición.
    Postcondiciones: devuelve una página genérica con estado HTTP 503.
    """
    return database_error_response(request)


@app.exception_handler(PermissionDenied)
def permission_denied_handler(request: Request, exc: PermissionDenied) -> Response:
    """Precondiciones: una operación protegida lanzó ``PermissionDenied``.
    Postcondiciones: devuelve una página comprensible con estado HTTP 403.
    """
    return app.state.templates.TemplateResponse(
        request=request,
        name="forbidden.html",
        context={
            "request": request,
            "current_user": current_user(request),
            "error": str(exc),
        },
        status_code=403,
    )


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> Response:
    """Precondiciones: la petición tiene una sesión autenticada.
    Postcondiciones: devuelve la página principal de la biblioteca.
    """
    return app.state.templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"request": request, "current_user": current_user(request)},
    )


@app.get("/health", include_in_schema=False)
def health() -> dict[str, str]:
    """Precondiciones: ninguna.
    Postcondiciones: informa que la aplicación vive sin abrir MySQL.
    """
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> RedirectResponse:
    """Precondiciones: el favicon está disponible entre los archivos estáticos.
    Postcondiciones: redirige temporalmente al recurso SVG.
    """
    return RedirectResponse(url="/static/favicon.svg", status_code=307)


app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(catalog.router)
app.include_router(basic.router)
