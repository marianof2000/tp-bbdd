from urllib.parse import quote

from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.auth import current_user

PUBLIC_PATHS = {"/login", "/favicon.ico"}


class AuthenticationMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        """Precondiciones: ``app`` implementa el protocolo ASGI.
        Postcondiciones: conserva la aplicación para procesar peticiones.
        """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Precondiciones: recibe una llamada ASGI con alcance bien formado.
        Postcondiciones: permite la petición o redirige al ingreso y evita caché.
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        path = request.url.path
        is_static = path.startswith("/static/")
        is_public = path in PUBLIC_PATHS or is_static

        if is_static:
            await self.app(scope, receive, send)
            return

        if not is_public and current_user(request) is None:
            next_path = quote(path, safe="/") if request.method == "GET" else ""
            target = f"/login?next={next_path}" if next_path else "/login"
            response = RedirectResponse(target, status_code=303)
            self._add_no_store_headers(response.headers)
            await response(scope, receive, send)
            return

        async def send_with_no_store(message: Message) -> None:
            """Precondiciones: ``message`` es un mensaje ASGI válido.
            Postcondiciones: envía el mensaje con cabeceras anti-caché al iniciar.
            """
            if message["type"] == "http.response.start":
                self._add_no_store_headers(MutableHeaders(scope=message))
            await send(message)

        await self.app(scope, receive, send_with_no_store)

    @staticmethod
    def _add_no_store_headers(headers: MutableHeaders) -> None:
        """Precondiciones: ``headers`` es una colección mutable de cabeceras.
        Postcondiciones: incorpora directivas que impiden almacenar la respuesta.
        """
        headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        headers["Pragma"] = "no-cache"
        headers["Expires"] = "0"
