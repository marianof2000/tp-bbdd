import os

from app.core.config import Settings
from app.models import (Autor, Bibliotecario, Editorial, Ejemplar, Libro, LibroAutor,
                        Persona, Prestamo, Socio, TelefonoSocio)
from app.routes.catalog import ordered_author_ids
from starlette.datastructures import FormData


def test_database_url_escapes_credentials() -> None:
    """Precondiciones: se pueden construir ajustes sin archivo de entorno.
    Postcondiciones: verifica que usuario y clave queden escapados en la URL.
    """
    settings = Settings(db_user="user@example", db_password="p@ss word", _env_file=None)
    assert "user%40example:p%40ss+word@" in settings.database_url


def test_der_table_names_are_mapped() -> None:
    """Precondiciones: todos los modelos fueron importados.
    Postcondiciones: verifica que sus tablas coincidan con el DER.
    """
    models = [Persona, Socio, Bibliotecario, TelefonoSocio, Editorial, Autor,
              Libro, LibroAutor, Ejemplar, Prestamo]
    assert {model.__tablename__ for model in models} == {
        "persona", "socio", "bibliotecario", "telefono_socio", "editorial",
        "autor", "libro", "libro_autor", "ejemplar", "prestamo",
    }


def test_app_does_not_create_tables_on_import() -> None:
    """Precondiciones: la configuración de prueba está disponible.
    Postcondiciones: verifica que importar la aplicación no requiera crear tablas.
    """
    from app.main import app
    assert app.title == "Biblioteca"


def test_home_renders_with_current_starlette_signature() -> None:
    """Precondiciones: existe una petición simulada con sesión de administrador.
    Postcondiciones: verifica que la portada se renderice correctamente.
    """
    from starlette.requests import Request
    from app.main import app, home

    request = Request({
        "type": "http", "method": "GET", "path": "/", "raw_path": b"/",
        "query_string": b"", "headers": [], "scheme": "http",
        "server": ("test", 80), "client": ("test", 1), "root_path": "",
        "app": app, "router": app.router,
        "session": {"user": {"username": os.environ["AUTH_ADMIN_USERNAME"], "role": "admin"}},
    })
    response = home(request)
    assert response.status_code == 200
    assert b"Biblioteca" in response.body


def test_health_is_lightweight() -> None:
    """Precondiciones: el endpoint de salud puede invocarse directamente.
    Postcondiciones: verifica una respuesta simple sin acceso a la base.
    """
    from app.main import health

    assert health() == {"status": "ok"}


def test_foreign_api_path_does_not_match_crud_detail() -> None:
    """Precondiciones: las rutas CRUD están registradas.
    Postcondiciones: verifica que una ruta ajena no coincida con un detalle.
    """
    from starlette.routing import Match
    from app.routes.basic import router

    scope = {"type": "http", "method": "GET", "path": "/v1/models"}
    assert all(route.matches(scope)[0] is Match.NONE for route in router.routes)


def test_author_order_is_explicit() -> None:
    """Precondiciones: el formulario contiene autores y órdenes válidos.
    Postcondiciones: verifica que los IDs respeten el orden declarado.
    """
    form = FormData([("autores", "7"), ("autores", "3"), ("orden_7", "2"), ("orden_3", "1")])
    assert ordered_author_ids(form) == [3, 7]
