from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
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


def database_error_response(request: Request, status_code: int = 503):
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
def persistence_error_handler(request: Request, exc: PersistenceError):
    return app.state.templates.TemplateResponse(
        request=request,
        name="database_error.html",
        context={"request": request, "current_user": current_user(request), "error": str(exc)},
        status_code=409,
    )


@app.exception_handler(SQLAlchemyError)
def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    return database_error_response(request)


@app.exception_handler(PermissionDenied)
def permission_denied_handler(request: Request, exc: PermissionDenied):
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
def home(request: Request):
    return app.state.templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"request": request, "current_user": current_user(request)},
    )


@app.get("/health", include_in_schema=False)
def health():
    """Comprobación de vida; no abre una conexión con MySQL."""
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return RedirectResponse(url="/static/favicon.svg", status_code=307)


app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(catalog.router)
app.include_router(basic.router)
