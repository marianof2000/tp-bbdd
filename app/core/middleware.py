from urllib.parse import quote

from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.auth import current_user

PUBLIC_PATHS = {"/login", "/favicon.ico"}


class AuthenticationMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
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
            if message["type"] == "http.response.start":
                self._add_no_store_headers(MutableHeaders(scope=message))
            await send(message)

        await self.app(scope, receive, send_with_no_store)

    @staticmethod
    def _add_no_store_headers(headers) -> None:
        headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        headers["Pragma"] = "no-cache"
        headers["Expires"] = "0"
