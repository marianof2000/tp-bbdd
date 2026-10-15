import base64
import hashlib
import hmac
import secrets
from getpass import getpass
from dataclasses import dataclass

from fastapi import Request

from app.core.config import Settings, get_settings

SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_DKLEN = 64


@dataclass(frozen=True)
class AuthenticatedUser:
    username: str
    role: str


class PermissionDenied(Exception):
    pass


def hash_password(password: str) -> str:
    """Precondiciones: ``password`` es una cadena apta para codificar en UTF-8.
    Postcondiciones: devuelve un hash scrypt con sal aleatoria, nunca la clave original.
    """
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=SCRYPT_DKLEN,
    )
    encoded_salt = base64.urlsafe_b64encode(salt).decode("ascii")
    encoded_digest = base64.urlsafe_b64encode(digest).decode("ascii")
    return f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${encoded_salt}${encoded_digest}"


def verify_password(password: str, encoded_hash: str) -> bool:
    """Precondiciones: los argumentos son cadenas; el hash puede ser inválido.
    Postcondiciones: devuelve si la clave coincide sin propagar errores de formato.
    """
    try:
        algorithm, n, r, p, encoded_salt, encoded_digest = encoded_hash.split("$", 5)
        if algorithm != "scrypt":
            return False
        salt = base64.urlsafe_b64decode(encoded_salt.encode("ascii"))
        expected = base64.urlsafe_b64decode(encoded_digest.encode("ascii"))
        actual = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=len(expected),
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def authenticate(username: str, password: str, settings: Settings | None = None) -> AuthenticatedUser | None:
    """Precondiciones: usuario y clave fueron recibidos como cadenas.
    Postcondiciones: devuelve la cuenta autenticada o ``None`` sin revelar la causa.
    """
    settings = settings or get_settings()
    accounts = (
        (settings.auth_admin_username, settings.auth_admin_password_hash, "admin"),
        (settings.auth_user_username, settings.auth_user_password_hash, "user"),
    )
    authenticated = None
    for configured_username, password_hash, role in accounts:
        username_matches = hmac.compare_digest(username, configured_username)
        password_matches = verify_password(password, password_hash)
        if username_matches and password_matches:
            authenticated = AuthenticatedUser(username=configured_username, role=role)
    return authenticated


def current_user(request: Request) -> AuthenticatedUser | None:
    """Precondiciones: la petición pasó por el middleware de sesiones.
    Postcondiciones: devuelve un usuario válido o ``None``; no modifica la sesión.
    """
    session_user = request.session.get("user")
    if not isinstance(session_user, dict):
        return None
    username = session_user.get("username")
    role = session_user.get("role")
    if not isinstance(username, str) or role not in {"admin", "user"}:
        return None
    return AuthenticatedUser(username=username, role=role)


def require_admin(request: Request) -> AuthenticatedUser:
    """Precondiciones: la petición posee una sesión accesible.
    Postcondiciones: devuelve al administrador o lanza ``PermissionDenied``.
    """
    user = current_user(request)
    if user is None or user.role != "admin":
        raise PermissionDenied("Tu cuenta tiene permisos de consulta y no puede modificar datos.")
    return user


def main() -> None:
    """Precondiciones: se ejecuta en una terminal interactiva.
    Postcondiciones: imprime un hash si ambas claves no vacías coinciden.
    """
    password = getpass("Nueva contraseña: ")
    confirmation = getpass("Repetir contraseña: ")
    if not password or password != confirmation:
        raise SystemExit("Las contraseñas no coinciden o están vacías.")
    print(hash_password(password))


if __name__ == "__main__":
    main()
