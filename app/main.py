from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.routes import basic, catalog, loans
from app.services.crud import PersistenceError

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title=get_settings().app_name)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.state.templates = Jinja2Templates(directory=BASE_DIR / "templates")


def database_error_response(request: Request, status_code: int = 503):
    return app.state.templates.TemplateResponse(
        request=request,
        name="database_error.html",
        context={
            "request": request,
            "error": "No se pudo acceder a la base de datos. Revisá la conexión e intentá nuevamente.",
        },
        status_code=status_code,
    )


@app.exception_handler(PersistenceError)
def persistence_error_handler(request: Request, exc: PersistenceError):
    return app.state.templates.TemplateResponse(
        request=request,
        name="database_error.html",
        context={"request": request, "error": str(exc)},
        status_code=409,
    )


@app.exception_handler(SQLAlchemyError)
def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    return database_error_response(request)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return app.state.templates.TemplateResponse(
        request=request, name="home.html", context={"request": request}
    )


@app.get("/health", include_in_schema=False)
def health():
    """Comprobación de vida; no abre una conexión con MySQL."""
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return RedirectResponse(url="/static/favicon.svg", status_code=307)


app.include_router(loans.router)
app.include_router(catalog.router)
app.include_router(basic.router)
