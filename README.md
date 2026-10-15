# Biblioteca — FastAPI + MySQL

Aplicación web educativa para administrar personas, socios, bibliotecarios, catálogo,
ejemplares y préstamos de una biblioteca. Usa FastAPI, SQLAlchemy 2, PyMySQL,
Pydantic y plantillas Jinja2.

## Estructura

```text
.
├── app/
│   ├── core/          # Configuración leída desde el entorno
│   ├── db/            # Base declarativa, motor y sesiones SQLAlchemy
│   ├── models/        # Mapeo exacto de las diez tablas del DER
│   ├── schemas/       # Validación de formularios con Pydantic
│   ├── services/      # CRUD y transacciones de negocio
│   ├── routes/        # Rutas web separadas por dominio
│   ├── templates/     # Vistas HTML Jinja2
│   ├── static/css/    # Estilos propios
│   └── main.py        # Creación y configuración de FastAPI
├── .env.example
├── requirements.txt
├── pyproject.toml
└── main.py            # Punto de entrada breve
```

No había un script SQL ni modelos previos en este proyecto para comparar con el DER.
Los modelos respetan los nombres de tablas, campos, claves primarias y claves foráneas
mostrados en la imagen. Las longitudes de los campos de texto no aparecen en el DER:
las longitudes usadas por los modelos son límites razonables, pero deben compararse
con `SHOW CREATE TABLE ...` antes de operar contra la base real.

La aplicación **no crea, altera ni elimina tablas al arrancar**. Tampoco incluye
migraciones automáticas.

## Instalación y configuración

Con `uv`:

```bash
uv sync
cp .env.example .env
```

O con un entorno virtual y pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Editá `.env` y completá `DB_PASSWORD` con la contraseña real. `.env` está ignorado
por Git. Los valores iniciales son host `172.16.0.105`, puerto `3306`, usuario
`dbeaver` y base `biblioteca`.

El DER no define los valores admitidos por `ejemplar.estado`. Esta implementación
considera `disponible` como apto para prestar y cambia el estado a `prestado` al
registrar un préstamo. Ambos valores están centralizados y pueden configurarse:

```dotenv
AVAILABLE_COPY_STATE=disponible
LOANED_COPY_STATE=prestado
```

Verificá que coincidan con los datos reales antes de usar la aplicación.

## Ejecución

```bash
uv run uvicorn app.main:app --reload
```

Abrí <http://127.0.0.1:8000>. La documentación técnica de FastAPI queda disponible
en <http://127.0.0.1:8000/docs>.

## Funcionalidad

- Listado, detalle, alta, edición y eliminación protegida de personas, socios,
  bibliotecarios, autores y editoriales.
- Gestión de teléfonos desde el detalle de cada socio.
- Catálogo con editorial y uno o más autores, guardando el orden de autoría.
- Alta, consulta, edición y eliminación protegida de ejemplares.
- Alta, consulta y edición de préstamos activos con validación de relaciones y disponibilidad.
- Devolución transaccional: registra la fecha y vuelve a marcar el ejemplar como
  disponible.
- Mensajes de validación e integridad sin exponer la cadena de conexión.

La conexión y los flujos contra MySQL no pueden verificarse sin la contraseña y sin
acceso a la base. Para comprobar el esquema real de forma no destructiva, compará la
salida de `SHOW CREATE TABLE nombre_tabla` para las diez tablas con los modelos en
`app/models/entities.py`.
