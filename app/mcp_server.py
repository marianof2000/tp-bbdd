from collections.abc import Callable
from typing import Any

from fastmcp import FastMCP
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.library_queries import (
    get_book_availability,
    get_library_statistics,
    list_overdue_loans,
    search_books,
    search_books_by_author,
    search_members,
)

DATABASE_ERROR = "No se pudo consultar la biblioteca en este momento."
READ_ONLY_ANNOTATIONS = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": False,
}

mcp = FastMCP(
    name="Biblioteca",
    instructions=(
        "Herramientas de consulta de la biblioteca. Este servidor es de solo lectura: "
        "no acepta SQL ni permite crear, modificar o eliminar registros."
    ),
    mask_error_details=True,
)


def _read(operation: Callable[[Session], dict[str, Any]]) -> dict[str, Any]:
    """Ejecuta una consulta con la fábrica de sesiones existente y oculta errores internos."""
    try:
        with SessionLocal() as db:
            return operation(db)
    except ValueError as exc:
        return {"error": str(exc)}
    except SQLAlchemyError:
        return {"error": DATABASE_ERROR}
    except Exception:
        return {"error": DATABASE_ERROR}


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def buscar_libros(titulo: str) -> dict[str, Any]:
    """Busca coincidencias parciales o totales en el título de los libros."""

    def query(db: Session) -> dict[str, Any]:
        books = search_books(db, titulo)
        return {"cantidad": len(books), "libros": books}

    return _read(query)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def buscar_libros_por_autor(autor: str) -> dict[str, Any]:
    """Busca libros por coincidencias en el nombre o apellido de sus autores."""

    def query(db: Session) -> dict[str, Any]:
        books = search_books_by_author(db, autor)
        return {"cantidad": len(books), "libros": books}

    return _read(query)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def buscar_socios(criterio: str) -> dict[str, Any]:
    """Busca socios por nombre, apellido, documento o email."""

    def query(db: Session) -> dict[str, Any]:
        members = search_members(db, criterio)
        return {"cantidad": len(members), "socios": members}

    return _read(query)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def consultar_disponibilidad(id_libro: int) -> dict[str, Any]:
    """Informa ejemplares totales, disponibles, prestados y en reparación de un libro."""

    def query(db: Session) -> dict[str, Any]:
        availability = get_book_availability(db, id_libro)
        if availability is None:
            return {"error": "No se encontró un libro con ese identificador."}
        return availability

    return _read(query)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def listar_prestamos_vencidos() -> dict[str, Any]:
    """Lista préstamos todavía activos cuyo vencimiento vigente ya pasó."""

    def query(db: Session) -> dict[str, Any]:
        loans = list_overdue_loans(db)
        return {"cantidad": len(loans), "prestamos": loans}

    return _read(query)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def obtener_estadisticas_biblioteca() -> dict[str, Any]:
    """Devuelve cantidades generales de libros, ejemplares, socios y préstamos."""
    return _read(get_library_statistics)


if __name__ == "__main__":
    mcp.run(transport="stdio")
