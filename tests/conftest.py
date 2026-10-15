import os
import secrets

from app.core.auth import hash_password

# Cada ejecución usa cuentas y secretos efímeros; no hay contraseñas de prueba fijas.
admin_username = "admin-" + secrets.token_hex(4)
admin_password = secrets.token_urlsafe(18)
user_username = "user-" + secrets.token_hex(4)
user_password = secrets.token_urlsafe(18)

os.environ["SESSION_SECRET"] = secrets.token_urlsafe(48)
os.environ["SESSION_HTTPS_ONLY"] = "false"
os.environ["AUTH_ADMIN_USERNAME"] = admin_username
os.environ["AUTH_ADMIN_PASSWORD_HASH"] = hash_password(admin_password)
os.environ["AUTH_USER_USERNAME"] = user_username
os.environ["AUTH_USER_PASSWORD_HASH"] = hash_password(user_password)
os.environ["TEST_ADMIN_PASSWORD"] = admin_password
os.environ["TEST_USER_PASSWORD"] = user_password
