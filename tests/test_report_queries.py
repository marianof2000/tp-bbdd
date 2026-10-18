from collections.abc import Generator
from datetime import date
from typing import Any

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from starlette.requests import Request

from app.db.base import Base
from app.main import app
from app.models import (
    Autor,
    Bibliotecario,
    Editorial,
    Ejemplar,
    Libro,
    LibroAutor,
    Persona,
    Socio,
    TelefonoSocio,
)
from app.services.report_queries import books_starting_with, run_all_reports
from app.routes.helpers import context


@pytest.fixture
def report_db() -> Generator[Session, None, None]:
    """Crea una base pequeña que permite comprobar las veinte consultas."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection: Any, _: Any) -> None:
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        yield session


def seed_reports(db: Session) -> None:
    people = [
        Persona(nombre="Ana", apellido="Paz", documento="1", email=None),
        Persona(nombre="Luis", apellido="Sol", documento="2", email=""),
        Persona(nombre="Eva", apellido="Sur", documento="3", email="eva@example.com"),
    ]
    publishers = [
        Editorial(nombre="Editorial Uno"),
        Editorial(nombre="Editorial Dos"),
        Editorial(nombre="Editorial Sin Libros"),
    ]
    authors = [
        Autor(nombre="Ada", apellido="Uno"),
        Autor(nombre="Beto", apellido="Dos"),
        Autor(nombre="Cata", apellido="Tres"),
    ]
    db.add_all([*people, *publishers, *authors])
    db.flush()

    members = [
        Socio(id_persona=people[0].id_persona, fecha_alta=date(2026, 1, 1)),
        Socio(id_persona=people[2].id_persona, fecha_alta=date(2026, 1, 2)),
    ]
    librarians = [
        Bibliotecario(id_persona=people[1].id_persona, legajo="B-1"),
        Bibliotecario(id_persona=people[2].id_persona, legajo="B-2"),
    ]
    db.add_all([*members, *librarians])
    db.flush()
    db.add_all(
        [
            TelefonoSocio(id_socio=members[0].id_persona, numero="111", tipo="móvil"),
            TelefonoSocio(id_socio=members[0].id_persona, numero="112", tipo="fijo"),
            TelefonoSocio(id_socio=members[1].id_persona, numero="113", tipo="móvil"),
        ]
    )

    books = [
        Libro(
            titulo="El Alfa",
            isbn="978-1",
            anio_publicacion=2020,
            id_editorial=publishers[0].id_editorial,
        ),
        Libro(
            titulo="El Beta",
            isbn="978-2",
            anio_publicacion=2020,
            id_editorial=publishers[0].id_editorial,
        ),
        Libro(
            titulo="Otro título",
            isbn="978-3",
            anio_publicacion=2021,
            id_editorial=publishers[1].id_editorial,
        ),
    ]
    db.add_all(books)
    db.flush()
    db.add_all(
        [
            LibroAutor(
                id_libro=books[0].id_libro,
                id_autor=authors[0].id_autor,
                orden_autoria=1,
            ),
            LibroAutor(
                id_libro=books[1].id_libro,
                id_autor=authors[1].id_autor,
                orden_autoria=1,
            ),
            LibroAutor(
                id_libro=books[0].id_libro,
                id_autor=authors[1].id_autor,
                orden_autoria=2,
            ),
            Ejemplar(
                id_libro=books[0].id_libro,
                codigo_inventario="INV-0001",
                fecha_incorporacion=date(2026, 1, 1),
                estado="operativo",
            ),
            Ejemplar(
                id_libro=books[0].id_libro,
                codigo_inventario="INV-0002",
                fecha_incorporacion=date(2026, 1, 1),
                estado="en_reparacion",
            ),
            Ejemplar(
                id_libro=books[1].id_libro,
                codigo_inventario="INV-0101",
                fecha_incorporacion=date(2026, 1, 1),
                estado="operativo",
            ),
        ]
    )
    db.commit()


def test_twenty_report_queries_match_the_sql_questions(report_db: Session) -> None:
    seed_reports(report_db)

    reports = run_all_reports(report_db)

    assert [report.number for report in reports] == list(range(1, 21))
    assert reports[0].rows == [{"total_personas": 3}]
    assert reports[1].rows == [{"total_socios": 2}]
    assert reports[2].rows == [{"total_bibliotecarios": 2}]
    assert reports[3].rows == [
        {"id_persona": 1, "nombre": "Ana", "apellido": "Paz"},
        {"id_persona": 2, "nombre": "Luis", "apellido": "Sol"},
    ]
    assert reports[4].rows == [{"total_telefonos": 3, "socios_con_telefono": 2}]
    assert reports[5].rows == [
        {"cantidad_telefonos": 1, "cantidad_socios": 1},
        {"cantidad_telefonos": 2, "cantidad_socios": 1},
    ]
    assert reports[6].rows == [{"total_autores": 3}]
    assert reports[7].rows == [{"autores_con_libro": 2, "autores_sin_libro": 1}]
    assert reports[8].rows == [{"total_editoriales": 3}]
    assert reports[9].rows == [{"editoriales_sin_libros": 1}]
    assert reports[10].rows == [{"total_libros": 3}]
    assert reports[11].rows == [{"titulos_que_comienzan_con_el": 2}]
    assert reports[12].rows == [
        {"anio_publicacion": 2020, "cantidad_libros": 2},
        {"anio_publicacion": 2021, "cantidad_libros": 1},
    ]
    assert reports[13].rows == [{"editorial": "Editorial Uno", "cantidad_libros": 2}]
    assert [row["titulo"] for row in reports[14].rows] == ["Otro título"]
    assert [row["titulo"] for row in reports[15].rows] == ["Otro título"]
    assert reports[16].rows == [
        {"cantidad_ejemplares": 0, "cantidad_libros": 1},
        {"cantidad_ejemplares": 1, "cantidad_libros": 1},
        {"cantidad_ejemplares": 2, "cantidad_libros": 1},
    ]
    assert reports[17].rows == [
        {"estado": "en_reparacion", "cantidad_ejemplares": 1},
        {"estado": "operativo", "cantidad_ejemplares": 2},
    ]
    assert reports[18].rows == [
        {
            "editorial": "Editorial Uno",
            "titulo": "El Alfa",
            "ejemplares_en_reparacion": 1,
        }
    ]
    assert reports[19].rows == [
        {
            "editorial": "Editorial Dos",
            "titulo": "Otro título",
            "cantidad_ejemplares": 0,
        },
        {
            "editorial": "Editorial Uno",
            "titulo": "El Beta",
            "cantidad_ejemplares": 1,
        },
        {
            "editorial": "Editorial Uno",
            "titulo": "El Alfa",
            "cantidad_ejemplares": 2,
        },
    ]


def test_report_filter_treats_injection_payload_as_literal(report_db: Session) -> None:
    seed_reports(report_db)

    result = books_starting_with(report_db, "El%' OR 1=1 --")

    assert result == [{"titulos_que_comienzan_con_el": 0}]


def test_reports_template_renders_all_queries(report_db: Session) -> None:
    seed_reports(report_db)
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/consultas",
            "raw_path": b"/consultas",
            "query_string": b"",
            "headers": [],
            "scheme": "http",
            "server": ("test", 80),
            "client": ("test", 1),
            "root_path": "",
            "app": app,
            "router": app.router,
            "session": {"user": {"username": "lector", "role": "user"}},
        }
    )

    response = app.state.templates.TemplateResponse(
        request=request,
        name="reports/list.html",
        context=context(request, reports=run_all_reports(report_db)),
    )
    page = response.body.decode("utf-8")

    assert "20 preguntas de negocio" in page
    assert "Consulta 1" in page
    assert "Consulta 20" in page
    assert "Otro título" in page
