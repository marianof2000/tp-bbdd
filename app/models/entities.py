from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Integer, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Persona(Base):
    __tablename__ = "persona"
    id_persona: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    apellido: Mapped[str] = mapped_column(String(80), nullable=False)
    documento: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str | None] = mapped_column(String(254), nullable=True)
    socio: Mapped["Socio | None"] = relationship(back_populates="persona", uselist=False)
    bibliotecario: Mapped["Bibliotecario | None"] = relationship(back_populates="persona", uselist=False)


class Socio(Base):
    __tablename__ = "socio"
    id_persona: Mapped[int] = mapped_column(ForeignKey("persona.id_persona"), primary_key=True)
    fecha_alta: Mapped[date] = mapped_column(Date, nullable=False)
    persona: Mapped[Persona] = relationship(back_populates="socio")
    telefonos: Mapped[list["TelefonoSocio"]] = relationship(back_populates="socio")


class Bibliotecario(Base):
    __tablename__ = "bibliotecario"
    id_persona: Mapped[int] = mapped_column(ForeignKey("persona.id_persona"), primary_key=True)
    legajo: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    persona: Mapped[Persona] = relationship(back_populates="bibliotecario")


class TelefonoSocio(Base):
    __tablename__ = "telefono_socio"
    __table_args__ = (UniqueConstraint("id_socio", "numero"),)
    id_telefono_socio: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_socio: Mapped[int] = mapped_column(ForeignKey("socio.id_persona"), nullable=False)
    numero: Mapped[str] = mapped_column(String(25), nullable=False)
    tipo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    socio: Mapped[Socio] = relationship(back_populates="telefonos")


class Editorial(Base):
    __tablename__ = "editorial"
    id_editorial: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)


class Autor(Base):
    __tablename__ = "autor"
    id_autor: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    apellido: Mapped[str] = mapped_column(String(80), nullable=False)


class Libro(Base):
    __tablename__ = "libro"
    id_libro: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    isbn: Mapped[str] = mapped_column(String(17), nullable=False, unique=True)
    anio_publicacion: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    id_editorial: Mapped[int] = mapped_column(ForeignKey("editorial.id_editorial"), nullable=False)
    editorial: Mapped[Editorial] = relationship()
    autores: Mapped[list["LibroAutor"]] = relationship(back_populates="libro", order_by="LibroAutor.orden_autoria")


class LibroAutor(Base):
    __tablename__ = "libro_autor"
    __table_args__ = (UniqueConstraint("id_libro", "id_autor"),)
    id_libro_autor: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_libro: Mapped[int] = mapped_column(ForeignKey("libro.id_libro"), nullable=False)
    id_autor: Mapped[int] = mapped_column(ForeignKey("autor.id_autor"), nullable=False)
    orden_autoria: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    libro: Mapped[Libro] = relationship(back_populates="autores")
    autor: Mapped[Autor] = relationship()


class Ejemplar(Base):
    __tablename__ = "ejemplar"
    id_ejemplar: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_libro: Mapped[int] = mapped_column(ForeignKey("libro.id_libro"), nullable=False)
    codigo_inventario: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    fecha_incorporacion: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(Enum("operativo", "en_reparacion"), nullable=False)
    libro: Mapped[Libro] = relationship()


class Prestamo(Base):
    __tablename__ = "prestamo"
    id_prestamo: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_socio: Mapped[int] = mapped_column(ForeignKey("socio.id_persona"), nullable=False)
    id_ejemplar: Mapped[int] = mapped_column(ForeignKey("ejemplar.id_ejemplar"), nullable=False)
    id_bibliotecario: Mapped[int] = mapped_column(ForeignKey("bibliotecario.id_persona"), nullable=False)
    fecha_prestamo: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_vencimiento_inicial: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_vencimiento_actual: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_devolucion: Mapped[date | None] = mapped_column(Date, nullable=True)
    socio: Mapped[Socio] = relationship(foreign_keys=[id_socio])
    ejemplar: Mapped[Ejemplar] = relationship()
    bibliotecario: Mapped[Bibliotecario] = relationship(foreign_keys=[id_bibliotecario])
