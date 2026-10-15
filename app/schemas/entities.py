from datetime import date
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from app.core.config import get_settings

class PersonaData(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=80)]
    apellido: Annotated[str, Field(min_length=1, max_length=80)]
    documento: Annotated[str, Field(min_length=1, max_length=20)]
    email: EmailStr | None = None

    @field_validator("email", mode="before")
    @classmethod
    def email_vacio_es_nulo(cls, value):
        return value or None


class SocioData(BaseModel):
    id_persona: int = Field(gt=0)
    fecha_alta: date


class BibliotecarioData(BaseModel):
    id_persona: int = Field(gt=0)
    legajo: Annotated[str, Field(min_length=1, max_length=30)]


class TelefonoData(BaseModel):
    numero: Annotated[str, Field(min_length=1, max_length=25)]
    tipo: Annotated[str, Field(min_length=1, max_length=20)] | None = None

    @field_validator("tipo", mode="before")
    @classmethod
    def tipo_vacio_es_nulo(cls, value):
        return value or None


class EditorialData(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=120)]


class AutorData(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=80)]
    apellido: Annotated[str, Field(min_length=1, max_length=80)]


class LibroData(BaseModel):
    titulo: Annotated[str, Field(min_length=1, max_length=200)]
    isbn: Annotated[str, Field(min_length=1, max_length=17)]
    anio_publicacion: int | None = Field(default=None, ge=1000, le=9999)
    id_editorial: int = Field(gt=0)

    @field_validator("anio_publicacion", mode="before")
    @classmethod
    def anio_vacio_es_nulo(cls, value):
        return value or None


class EjemplarData(BaseModel):
    id_libro: int = Field(gt=0)
    codigo_inventario: Annotated[str, Field(min_length=1, max_length=40)]
    fecha_incorporacion: date
    estado: Annotated[str, Field(min_length=1, max_length=30)]

    @field_validator("estado")
    @classmethod
    def estado_valido(cls, value):
        if value not in get_settings().copy_states:
            raise ValueError("El estado del ejemplar no es válido")
        return value


class PrestamoData(BaseModel):
    id_socio: int = Field(gt=0)
    id_ejemplar: int = Field(gt=0)
    id_bibliotecario: int = Field(gt=0)
    fecha_prestamo: date
    fecha_vencimiento_inicial: date
    fecha_vencimiento_actual: date

    @model_validator(mode="after")
    def fechas_coherentes(self):
        if self.fecha_vencimiento_inicial < self.fecha_prestamo:
            raise ValueError("El vencimiento no puede ser anterior al préstamo")
        if self.fecha_vencimiento_actual < self.fecha_prestamo:
            raise ValueError("El vencimiento actual no puede ser anterior al préstamo")
        return self
