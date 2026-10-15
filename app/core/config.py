from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Biblioteca"
    db_host: str = "172.16.0.105"
    db_port: int = 3306
    db_name: str = "biblioteca"
    db_user: str = "dbeaver"
    db_password: str = Field(default="", repr=False)
    available_copy_state: str = "operativo"
    repair_copy_state: str = "en_reparacion"
    session_secret: str = Field(min_length=32, repr=False)
    session_https_only: bool = False
    session_max_age_seconds: int = Field(default=28800, gt=0)
    auth_admin_username: str = Field(min_length=1)
    auth_admin_password_hash: str = Field(min_length=1, repr=False)
    auth_user_username: str = Field(min_length=1)
    auth_user_password_hash: str = Field(min_length=1, repr=False)

    @model_validator(mode="after")
    def distinct_account_names(self) -> "Settings":
        """Precondiciones: las variables de ambas cuentas fueron cargadas.
        Postcondiciones: devuelve la configuración si los usuarios son distintos.
        """
        if self.auth_admin_username == self.auth_user_username:
            raise ValueError("Las cuentas admin y user deben tener nombres diferentes")
        return self

    @property
    def copy_states(self) -> tuple[str, str]:
        """Precondiciones: los estados de ejemplar están configurados.
        Postcondiciones: devuelve los estados disponible y en reparación.
        """
        return self.available_copy_state, self.repair_copy_state

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def database_url(self) -> str:
        """Precondiciones: existen los datos de conexión requeridos.
        Postcondiciones: devuelve una URL MySQL con credenciales escapadas.
        """
        user = quote_plus(self.db_user)
        password = quote_plus(self.db_password)
        return f"mysql+pymysql://{user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"


@lru_cache
def get_settings() -> Settings:
    """Precondiciones: el entorno contiene las variables obligatorias.
    Postcondiciones: devuelve una instancia validada y almacenada en caché.
    """
    return Settings()
