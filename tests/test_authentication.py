import asyncio
import os
from dataclasses import dataclass
from http.cookies import SimpleCookie
from urllib.parse import urlencode, urlsplit

import pytest
from starlette.requests import Request

from app.core.auth import PermissionDenied, require_admin
from app.main import app
from app.routes import basic, catalog, loans
from app.routes.helpers import context


@dataclass
class Response:
    status_code: int
    headers: dict[str, str]
    text: str


class ASGITestClient:
    """Cliente mínimo para probar la aplicación sin depender de un cliente HTTP externo."""

    def __init__(self):
        self.cookies: dict[str, str] = {}

    async def request(self, method: str, url: str, data=None) -> Response:
        parsed = urlsplit(url)
        body = urlencode(data or {}).encode("utf-8")
        headers = [(b"host", b"test")]
        if data is not None:
            headers.extend([
                (b"content-type", b"application/x-www-form-urlencoded"),
                (b"content-length", str(len(body)).encode("ascii")),
            ])
        if self.cookies:
            cookie_value = "; ".join(f"{key}={value}" for key, value in self.cookies.items())
            headers.append((b"cookie", cookie_value.encode("ascii")))

        delivered = False
        messages = []

        async def receive():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": body, "more_body": False}
            await asyncio.sleep(3600)

        async def send(message):
            messages.append(message)

        scope = {
            "type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
            "method": method, "scheme": "http", "path": parsed.path,
            "raw_path": parsed.path.encode("utf-8"), "query_string": parsed.query.encode("utf-8"),
            "root_path": "", "headers": headers, "client": ("127.0.0.1", 1),
            "server": ("test", 80),
        }
        await asyncio.wait_for(app(scope, receive, send), timeout=5)
        start = next(message for message in messages if message["type"] == "http.response.start")
        response_headers = {
            key.decode("latin-1").lower(): value.decode("latin-1")
            for key, value in start["headers"]
        }
        if "set-cookie" in response_headers:
            parsed_cookie = SimpleCookie()
            parsed_cookie.load(response_headers["set-cookie"])
            for key, morsel in parsed_cookie.items():
                if morsel["max-age"] == "0":
                    self.cookies.pop(key, None)
                else:
                    self.cookies[key] = morsel.value
        response_body = b"".join(
            message.get("body", b"") for message in messages if message["type"] == "http.response.body"
        )
        return Response(start["status"], response_headers, response_body.decode("utf-8"))

    async def get(self, url: str) -> Response:
        return await self.request("GET", url)

    async def post(self, url: str, data=None) -> Response:
        return await self.request("POST", url, data=data)


def test_authentication_and_role_permissions():
    async def exercise_flows():
        anonymous = ASGITestClient()
        response = await anonymous.get("/")
        assert response.status_code == 303
        assert response.headers["location"].startswith("/login")
        assert response.headers["cache-control"].startswith("no-store")

        response = await anonymous.get("/docs")
        assert response.status_code == 303

        response = await anonymous.post(
            "/login",
            data={"username": os.environ["AUTH_ADMIN_USERNAME"], "password": "incorrecta", "next": "/"},
        )
        assert response.status_code == 401
        assert "Usuario o contraseña incorrectos" in response.text

        reader = ASGITestClient()
        response = await reader.post(
            "/login",
            data={
                "username": os.environ["AUTH_USER_USERNAME"],
                "password": os.environ["TEST_USER_PASSWORD"],
                "next": "/libros",
            },
        )
        assert response.status_code == 303
        assert response.headers["location"] == "/libros"
        assert "httponly" in response.headers["set-cookie"].lower()
        assert "samesite=lax" in response.headers["set-cookie"].lower()

        response = await reader.post("/logout")
        assert response.status_code == 303
        response = await reader.get("/")
        assert response.status_code == 303
        assert response.headers["location"].startswith("/login")

        administrator = ASGITestClient()
        response = await administrator.post(
            "/login",
            data={
                "username": os.environ["AUTH_ADMIN_USERNAME"],
                "password": os.environ["TEST_ADMIN_PASSWORD"],
                "next": "/editoriales",
            },
        )
        assert response.status_code == 303

    asyncio.run(exercise_flows())

    reader_request = Request({
        "type": "http", "method": "GET", "path": "/libros", "raw_path": b"/libros",
        "query_string": b"", "headers": [], "scheme": "http", "server": ("test", 80),
        "client": ("test", 1), "root_path": "", "app": app, "router": app.router,
        "session": {"user": {"username": os.environ["AUTH_USER_USERNAME"], "role": "user"}},
    })
    response = app.state.templates.TemplateResponse(
        request=reader_request,
        name="books/list.html",
        context=context(reader_request, books=[]),
    )
    assert "Nuevo libro" not in response.body.decode("utf-8")
    with pytest.raises(PermissionDenied):
        require_admin(reader_request)

    admin_request = Request({
        **reader_request.scope,
        "session": {"user": {"username": os.environ["AUTH_ADMIN_USERNAME"], "role": "admin"}},
    })
    assert require_admin(admin_request).role == "admin"

    for router in (basic.router, catalog.router, loans.router):
        for route in router.routes:
            methods = getattr(route, "methods", set())
            is_write_route = "POST" in methods or route.path.endswith(("/nuevo", "/editar"))
            if is_write_route:
                dependencies = {dependency.call for dependency in route.dependant.dependencies}
                assert require_admin in dependencies, f"Falta autorización en {route.path}"
