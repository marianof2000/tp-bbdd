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
│   ├── mcp_server.py  # Servidor MCP de consultas de solo lectura
│   └── main.py        # Creación y configuración de FastAPI
├── sql/
│   ├── Biblioteca_2026-10-12T20_27_58.966Z.sql  # Creación del esquema
│   ├── 01_carga_personas_biblioteca.sql
│   ├── 02_carga_110_autores.sql
│   ├── 03_carga_30_editoriales.sql
│   ├── 04_carga_50_libros_revisado.sql
│   ├── 05_carga_telefonos_socios.sql
│   ├── 06_carga_ejemplares.sql
│   └── 07_consultas_20_preguntas_biblioteca.sql
├── .env.example
├── requirements.txt
├── pyproject.toml
└── main.py            # Punto de entrada breve
```

Al comenzar no había un script SQL ni modelos previos en el proyecto. Los modelos y
el esquema agregado respetan el DER y fueron comparados con las diez tablas reales,
incluyendo longitudes, nulabilidad, claves y restricciones únicas.

La aplicación **no crea, altera ni elimina tablas al arrancar**. Tampoco incluye
migraciones automáticas.

## Instalación y configuración

Con `uv`:

```bash
uv sync
cp .env.example .env
```

`pyproject.toml` es la fuente editable de dependencias y `uv.lock` fija las versiones.
Si cambia una dependencia, regenerá `requirements.txt` con:

```bash
uv export --format requirements-txt --no-dev --no-hashes --output-file requirements.txt
```

Editá `.env` y completá `DB_PASSWORD` con la contraseña real. `.env` está ignorado
por Git. Los valores iniciales son host `172.16.0.105`, puerto `3306`, usuario
`dbeaver` y base `biblioteca`.

La inspección de la base real confirmó que `ejemplar.estado` es un `ENUM` con los
valores `operativo` y `en_reparacion`. Un ejemplar está disponible cuando está
operativo y no tiene un préstamo activo. La aplicación bloquea su fila mientras
registra el préstamo para evitar dos préstamos simultáneos. Al devolverlo se conserva
o restaura el estado operativo. Los valores están centralizados:

```dotenv
AVAILABLE_COPY_STATE=operativo
REPAIR_COPY_STATE=en_reparacion
```

Los modelos también reflejan las longitudes, campos opcionales y restricciones únicas
observadas en la base real. La inspección fue de solo lectura; no se ejecutó DDL.

## Acceso y roles

Las cuentas iniciales de desarrollo son:

| Usuario | Clave inicial | Rol | Permisos |
|---|---|---|---|
| `admin` | `admin` | Administrador | Consulta, alta, edición y eliminación |
| `user` | `user` | Consulta | Listados y detalles únicamente |

Los nombres y hashes se leen desde `.env`; no hay usuarios en el código ni una tabla
adicional en MySQL. Las claves se verifican con `scrypt` y nunca se guardan en texto
plano. Para cambiar una contraseña, generá un hash nuevo:

```bash
uv run python -m app.core.auth
```

Copiá el resultado en `AUTH_ADMIN_PASSWORD_HASH` o `AUTH_USER_PASSWORD_HASH`. Los
nombres se cambian con `AUTH_ADMIN_USERNAME` y `AUTH_USER_USERNAME`.

Antes de usar la aplicación fuera del entorno de demostración:

1. Cambiá ambas contraseñas iniciales.
2. Generá una clave de sesión nueva con
   `uv run python -c "import secrets; print(secrets.token_urlsafe(48))"` y guardala
   en `SESSION_SECRET`.
3. Configurá `SESSION_HTTPS_ONLY=true` cuando el sitio funcione mediante HTTPS.
4. Reiniciá la aplicación para invalidar las sesiones anteriores.

La cookie de sesión es `HttpOnly`, usa `SameSite=Lax`, tiene una duración configurable
y puede limitarse a HTTPS. Las respuestas protegidas usan `Cache-Control: no-store`:
después de cerrar sesión, volver con el botón “Atrás” no rehabilita el acceso.

## Archivos SQL

El directorio `sql/` contiene el esquema completo de la base, seis cargas ordenadas
de datos de prueba y veinte consultas de lectura. Los scripts no se ejecutan al
iniciar la aplicación.

Orden sugerido para una base vacía:

1. `Biblioteca_2026-10-12T20_27_58.966Z.sql`: crea la base y las diez tablas.
2. `01_carga_personas_biblioteca.sql`: personas, socios y bibliotecarios.
3. `02_carga_110_autores.sql`: autores.
4. `03_carga_30_editoriales.sql`: editoriales.
5. `04_carga_50_libros_revisado.sql`: libros y sus autores.
6. `05_carga_telefonos_socios.sql`: teléfonos.
7. `06_carga_ejemplares.sql`: ejemplares.
8. `07_consultas_20_preguntas_biblioteca.sql`: consultas de comprobación.

Para crear el esquema en una base vacía, seleccioná primero la base de destino y
ejecutá:

```bash
mysql -u USUARIO -p < sql/Biblioteca_2026-10-12T20_27_58.966Z.sql
```

Los scripts de carga insertan datos. No los ejecutes sobre la base existente sin
revisar primero su contenido y confirmar que corresponde cargar esos registros.

## Ejecución

```bash
uv run uvicorn app.main:app --reload
```

Abrí <http://127.0.0.1:8000>. La documentación técnica de FastAPI queda disponible
en <http://127.0.0.1:8000/docs>.

## Integración MCP de solo lectura

El servidor MCP (Model Context Protocol) permite que un asistente de IA consulte el
catálogo y los préstamos mediante herramientas con parámetros definidos. Reutiliza
las sesiones SQLAlchemy y la capa de servicios de la aplicación: no recibe SQL, no
expone la configuración de MySQL y no ofrece herramientas de alta, modificación o
eliminación.

Herramientas disponibles:

- `buscar_libros(titulo: str)`: busca una coincidencia parcial o total en el título
  e incluye autores, editorial, ISBN y año.
- `consultar_disponibilidad(id_libro: int)`: informa ejemplares totales,
  disponibles, prestados y en reparación.
- `listar_prestamos_vencidos()`: lista préstamos activos ya vencidos con socio,
  libro, ejemplar y fechas relevantes.
- `obtener_estadisticas_biblioteca()`: resume libros, ejemplares, socios, préstamos
  activos y préstamos vencidos.

Con el mismo `.env` de la aplicación, iniciá el servidor local mediante `stdio`:

```bash
uv run python -m app.mcp_server
```

Normalmente el cliente MCP inicia ese proceso por sí mismo. Una configuración stdio
genérica (reemplazando `/ruta/al/proyecto` por la ruta absoluta del repositorio) es:

```json
{
  "mcpServers": {
    "biblioteca": {
      "command": "uv",
      "args": [
        "--directory",
        "/ruta/al/proyecto",
        "run",
        "python",
        "-m",
        "app.mcp_server"
      ]
    }
  }
}
```

Después de habilitar el servidor en un cliente compatible, una consulta posible es:
“Buscá los libros disponibles de Borges”. El cliente puede combinar la búsqueda por
título con una consulta de disponibilidad para cada resultado.

Un ejemplar se cuenta como disponible si está `operativo` y no tiene un préstamo
activo. Se cuenta como prestado si tiene un préstamo sin fecha de devolución, y como
vencido sólo si ese préstamo sigue activo y `fecha_vencimiento_actual` es anterior a
la fecha de la consulta.

## Funcionalidad

- Listado, detalle, alta, edición y eliminación protegida de personas, socios,
  bibliotecarios, autores y editoriales.
- Gestión de teléfonos desde el detalle de cada socio.
- Catálogo con editorial y uno o más autores, guardando el orden de autoría.
- Alta, consulta, edición y eliminación protegida de ejemplares.
- Alta, consulta y edición de préstamos activos con validación de relaciones y disponibilidad.
- Devolución transaccional: registra la fecha y conserva/restaura el estado operativo.
- Mensajes de validación e integridad sin exponer la cadena de conexión.
- Inicio y cierre de sesión con roles `admin` y `user`.
- Autorización aplicada tanto a los controles HTML como a las rutas de escritura.

## Verificación de autenticación

Las pruebas automatizadas comprueban que:

1. `admin` puede consultar y crear registros.
2. `user` puede abrir listados y detalles sin ver controles de escritura.
3. Una petición directa de `user` a una ruta de escritura responde `403` y no
   modifica la base.
4. Una petición sin sesión es redirigida a `/login`.
5. Credenciales incorrectas responden con un mensaje genérico y no abren sesión.
6. El cierre de sesión elimina la sesión y vuelve a bloquear las páginas protegidas.

Resultado actual: **12 pruebas aprobadas**.

La conexión de lectura y el esquema de las diez tablas fueron verificados contra
MySQL. Los flujos de escritura se prueban en una base SQLite aislada para no modificar
los datos reales:

```bash
uv run python -m pytest -q
```
