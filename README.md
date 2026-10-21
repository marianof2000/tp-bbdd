# Biblioteca — FastAPI + MySQL

Aplicación web educativa para administrar el catálogo, las personas y la
circulación de ejemplares de una biblioteca. Incluye autenticación por sesión,
permisos por rol y un servidor MCP de solo lectura para consultar la misma base
desde un cliente de IA.

El proyecto usa Python 3.12, FastAPI, SQLAlchemy 2, PyMySQL, Pydantic, Jinja2,
MySQL y FastMCP.

## Funcionalidad

- ABM de personas, socios, bibliotecarios, autores y editoriales.
- Gestión de los teléfonos asociados a cada socio.
- Catálogo de libros con editorial, ISBN y uno o más autores en orden explícito.
- Inventario de ejemplares y distinción entre estado físico y disponibilidad.
- Registro y edición de préstamos, renovación del vencimiento y devolución.
- Validación de formularios, relaciones, fechas, duplicados e integridad referencial.
- Sesiones con roles `admin` y `user` y protección de todas las rutas privadas.
- Seis herramientas MCP de consulta, sin acceso a SQL ni operaciones de escritura.
- Veinte consultas de negocio ejecutadas desde Python y visibles en la aplicación.
- Scripts para crear y poblar la base, además de sus consultas SQL de referencia.

## Requisitos

- Python 3.12 o posterior.
- [uv](https://docs.astral.sh/uv/) para instalar y ejecutar el proyecto.
- MySQL accesible desde el equipo donde se inicia la aplicación.

## Inicio rápido

1. Instalá las dependencias y creá la configuración local:

   ```bash
   uv sync
   cp .env.example .env
   ```

2. Editá `.env`. Como mínimo, configurá la conexión MySQL y reemplazá
   `SESSION_SECRET` antes de usar la aplicación fuera de una demostración.

3. Si necesitás crear una base nueva, ejecutá el esquema y luego las cargas en
   el orden indicado en [Base de datos](#base-de-datos).

4. Iniciá el servidor web:

   ```bash
   uv run uvicorn app.main:app --reload
   ```

5. Abrí <http://127.0.0.1:8000> e ingresá con una de las cuentas de desarrollo.

También se puede usar el punto de entrada abreviado:

```bash
uv run uvicorn main:app --reload
```

## Configuración

La configuración se lee desde variables de entorno o desde `.env`. Este archivo
está excluido de Git; `.env.example` contiene una plantilla funcional para
desarrollo.

| Variable | Valor de ejemplo | Uso |
|---|---|---|
| `DB_HOST` | `172.16.0.105` | Host de MySQL |
| `DB_PORT` | `3306` | Puerto de MySQL |
| `DB_NAME` | `biblioteca` | Nombre de la base |
| `DB_USER` | `dbeaver` | Usuario de MySQL |
| `DB_PASSWORD` | vacío | Contraseña de MySQL |
| `AVAILABLE_COPY_STATE` | `operativo` | Estado físico que permite prestar |
| `REPAIR_COPY_STATE` | `en_reparacion` | Estado de un ejemplar en reparación |
| `SESSION_SECRET` | valor de demostración | Firma de la cookie; exige al menos 32 caracteres |
| `SESSION_HTTPS_ONLY` | `false` | Restringe la cookie a HTTPS |
| `SESSION_MAX_AGE_SECONDS` | `28800` | Duración de la sesión en segundos |
| `AUTH_ADMIN_USERNAME` | `admin` | Nombre de la cuenta administradora |
| `AUTH_ADMIN_PASSWORD_HASH` | hash incluido | Hash scrypt de la clave administradora |
| `AUTH_USER_USERNAME` | `user` | Nombre de la cuenta de consulta |
| `AUTH_USER_PASSWORD_HASH` | hash incluido | Hash scrypt de la clave de consulta |

La URL de conexión se construye internamente con el driver `mysql+pymysql` y
escapa el usuario y la contraseña. La aplicación **no crea, altera ni elimina
tablas al arrancar** y no incluye migraciones automáticas.

## Base de datos

El modelo relacional contiene diez tablas:

```text
persona ──┬── socio ── telefono_socio
          └── bibliotecario

editorial ── libro ── libro_autor ── autor
                 └── ejemplar ── prestamo ── socio
                                      └── bibliotecario
```

Los modelos SQLAlchemy reflejan las longitudes, la nulabilidad, las claves y las
restricciones únicas del esquema. `ejemplar.estado` admite `operativo` y
`en_reparacion`.

Un ejemplar está disponible solamente cuando:

1. su estado físico es `operativo`; y
2. no existe un préstamo activo, es decir, sin `fecha_devolucion`.

Al registrar un préstamo se bloquea la fila del ejemplar y se vuelve a comprobar
su disponibilidad para evitar préstamos simultáneos. La devolución registra la
fecha y deja el ejemplar en estado operativo.

### Scripts SQL

El directorio `sql/` contiene:

1. `Biblioteca_2026-10-12T20_27_58.966Z.sql`: crea la base `biblioteca` y las diez tablas.
2. `01_carga_personas_biblioteca.sql`: personas, socios y bibliotecarios.
3. `02_carga_110_autores.sql`: autores.
4. `03_carga_30_editoriales.sql`: editoriales.
5. `04_carga_50_libros_revisado.sql`: libros y autorías.
6. `05_carga_telefonos_socios.sql`: teléfonos de socios.
7. `06_carga_ejemplares.sql`: ejemplares.
8. `07_consultas_20_preguntas_biblioteca.sql`: veinte consultas de comprobación.
9. `08_explain_optimizacion.sql`: comparación del plan de una consulta antes y
   después de crear un índice compuesto.

Para crear el esquema:

```bash
mysql -u USUARIO -p < sql/Biblioteca_2026-10-12T20_27_58.966Z.sql
```

Después ejecutá los seis archivos `01_` a `06_` en orden. Todos los scripts
incluyen `USE biblioteca`; si elegís otro `DB_NAME`, debés adaptar esa sentencia
y la creación del esquema antes de ejecutarlos.

Los archivos de carga hacen inserciones reales. No los ejecutes sobre una base
existente sin revisar previamente su contenido.

### Consultas de negocio de la Parte 6

La aplicación implementa las veinte preguntas del archivo
`07_consultas_20_preguntas_biblioteca.sql` mediante expresiones SQLAlchemy en
`app/services/report_queries.py`. Los resultados se pueden consultar desde
`/consultas`.

Entre las veinte consultas implementadas, las cinco que combinan tres tablas son:

| N.º | Pregunta resumida | Tablas combinadas |
|---:|---|---|
| 5 | Teléfonos registrados y socios con teléfono | `persona`, `socio`, `telefono_socio` |
| 8 | Autores con libros y sin libros | `autor`, `libro_autor`, `libro` |
| 14 | Editoriales con mayor cantidad de libros | `editorial`, `libro`, `libro_autor` |
| 19 | Libros con ejemplares en reparación | `editorial`, `libro`, `ejemplar` |
| 20 | Libros con menos de tres ejemplares | `editorial`, `libro`, `ejemplar` |

En el informe 14, `libro_autor` permite exponer y controlar la multiplicación
de un libro con varios autores, aunque no es indispensable para responder qué
editorial tiene más libros. Si se exige que las tres tablas sean necesarias para
la pregunta de negocio, este informe debe reemplazarse por otro que cumpla ese
criterio de forma sustantiva.

Estas cinco consultas no deben confundirse con los cinco informes de gestión
adicionales propuestos en la sección 6.2 de `docs/content.md`: catálogo con
autores y editoriales, ejemplares disponibles, préstamos pendientes por socio,
préstamos registrados por bibliotecario y libros más prestados. Esos informes
están definidos conceptualmente en la memoria académica, pero todavía no cuentan
con scripts, resultados ni evidencias de ejecución incorporados a la entrega.

Las consultas 6, 13, 14, 17, 18, 19 y 20 emplean agregación con `GROUP BY`.
Las consultas 14 y 20 agregan `HAVING`. Las consultas 6, 10, 14 y 17 contienen
subconsultas, ya sea como tabla derivada, `NOT EXISTS` o subconsulta escalar.

Los conteos susceptibles a multiplicación por las uniones emplean
`COUNT(DISTINCT ...)`. Esto se aplica a socios, teléfonos, autores y libros en
las consultas 5, 8 y 14. Las pruebas automatizadas incluyen relaciones de uno a
muchos para comprobar que esos totales no se dupliquen.

Cada sentencia del archivo SQL incluye su pregunta de negocio y el resultado
esperado para el set de carga. La pantalla `/consultas` muestra el resultado
obtenido en la base conectada, pero actualmente no compara ese valor con el
esperado ni conserva evidencia de una ejecución sobre MySQL. Las pruebas usan un
set reducido en SQLite y verifican la lógica de las veinte consultas; no
acreditan por sí solas los totales previstos para el set completo de MySQL.

### EXPLAIN y optimización

`08_explain_optimizacion.sql` prepara la comparación del informe 19 antes y
después de crear el índice compuesto
`ix_ejemplar_estado_codigo_libro (estado, codigo_inventario, id_libro)`. El
procedimiento ejecuta la misma consulta en ambos casos e indica comparar
`type`, `key`, `rows` y `Extra`.

El script no constituye evidencia de ejecución por sí mismo. Para completar la
actividad deben conservarse las dos salidas reales de `EXPLAIN` y documentarse
la comparación. Como `CREATE INDEX` y `ANALYZE TABLE` modifican el esquema o sus
estadísticas, deben ejecutarse de forma controlada y no forman parte del arranque
de la aplicación ni de las pruebas automatizadas.

### Estado de la documentación de la Parte 6

La implementación SQL y Python está disponible. `docs/content.md` y el PDF local
ya contienen las Partes 6, 7 y 8, pero la Parte 6 conserva apartados y resultados
marcados como pendientes. Para completar la entrega documental se debe
incorporar:

1. el SQL, resultado esperado, resultado obtenido y comprobación de cada
   consulta;
2. la justificación de los `JOIN`, agregaciones, `HAVING` y subconsultas;
3. el control de totales potencialmente duplicados por relaciones uno a muchos;
4. los planes reales de `EXPLAIN` antes y después del índice; y
5. el registro de uso de IA de esta parte: prompt, respuesta, revisión humana y
   correcciones realizadas.

### Consultas parametrizadas e inyección SQL

Una inyección SQL ocurre cuando una aplicación concatena una entrada externa con
el texto de una sentencia y permite que esa entrada cambie la operación que
ejecutará la base. Este proyecto no construye sentencias de esa forma:
SQLAlchemy envía la estructura de la consulta y sus valores por separado como
parámetros enlazados. Por eso una entrada como `' OR 1=1 --` se trata como un
valor literal y no como una parte ejecutable del SQL. En los filtros `LIKE`
también se usa escape automático para que `%` y `_` puedan buscarse literalmente.

## Acceso y roles

Las credenciales iniciales definidas por `.env.example` son:

| Usuario | Clave inicial | Rol | Permisos |
|---|---|---|---|
| `admin` | `admin` | Administrador | Consulta, alta, edición y eliminación |
| `user` | `user` | Consulta | Listados y detalles únicamente |

Las cuentas no se almacenan en MySQL. Las claves se verifican contra hashes
`scrypt` y nunca se guardan en texto plano. Para generar un hash nuevo:

```bash
uv run python -m app.core.auth
```

Copiá el resultado en `AUTH_ADMIN_PASSWORD_HASH` o `AUTH_USER_PASSWORD_HASH`.
Para generar un secreto de sesión:

```bash
uv run python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Antes de desplegar la aplicación:

1. Cambiá las dos claves iniciales y `SESSION_SECRET`.
2. Usá `SESSION_HTTPS_ONLY=true` cuando el sitio funcione mediante HTTPS.
3. Reiniciá el proceso después de cambiar credenciales o secretos.

La cookie `biblioteca_session` es `HttpOnly`, usa `SameSite=Lax` y tiene una
duración configurable. Las respuestas privadas envían `Cache-Control: no-store`
para que el navegador no recupere contenido protegido después de cerrar sesión.
Los permisos se aplican tanto en la interfaz como en las rutas del servidor: una
petición de escritura directa con rol `user` responde HTTP 403.

## Aplicación web

Las secciones principales son:

| Ruta | Contenido |
|---|---|
| `/personas` | Datos personales |
| `/socios` | Socios y sus teléfonos |
| `/bibliotecarios` | Personal que registra préstamos |
| `/libros` | Catálogo, editorial y autorías |
| `/autores` | Autores |
| `/editoriales` | Editoriales |
| `/ejemplares` | Copias físicas y estado |
| `/prestamos` | Préstamos, vencimientos y devoluciones |
| `/consultas` | Las veinte preguntas de negocio ejecutadas desde Python |
| `/docs` | Documentación OpenAPI generada por FastAPI |
| `/health` | Estado liviano del proceso, sin consultar MySQL |

Salvo `/login`, el favicon y los archivos estáticos, las rutas requieren una
sesión válida. Esto incluye `/docs` y `/health`.

## Servidor MCP de solo lectura

El servidor MCP reutiliza las sesiones SQLAlchemy y la capa de consultas de la
aplicación. No recibe SQL, no publica las credenciales de MySQL y no ofrece
operaciones de alta, modificación ni eliminación.

Herramientas disponibles:

- `buscar_libros(titulo: str)`: coincidencia parcial y sin distinción de
  mayúsculas; devuelve autores, editorial, ISBN y año.
- `buscar_libros_por_autor(autor: str)`: busca por nombre, apellido o nombre
  completo del autor y devuelve los datos de catálogo de sus libros.
- `buscar_socios(criterio: str)`: busca socios por nombre, apellido, nombre
  completo, documento o email; devuelve también fecha de alta y teléfonos.
- `consultar_disponibilidad(id_libro: int)`: informa ejemplares totales,
  disponibles, prestados y en reparación.
- `listar_prestamos_vencidos()`: lista préstamos activos cuyo vencimiento actual
  ya pasó, con socio, libro, ejemplar y fechas.
- `obtener_estadisticas_biblioteca()`: resume libros, ejemplares, socios,
  préstamos activos y préstamos vencidos.

### Requisitos para usarlo

Antes de conectar un cliente MCP:

1. Instalá las dependencias con `uv sync`.
2. Creá y completá `.env`, especialmente las variables de conexión a MySQL.
3. Verificá que MySQL esté accesible y que el esquema `biblioteca` tenga datos.

El servidor puede iniciarse manualmente para comprobar que carga sin errores:

```bash
uv run python -m app.mcp_server
```

El proceso queda esperando mensajes MCP por entrada estándar. No es una consola
interactiva y no se escriben consultas en esa terminal. Se detiene con `Ctrl+C`.
En el uso normal no hace falta iniciarlo manualmente: el cliente MCP crea y
administra el proceso.

### Configuración en Codex

Codex admite una configuración global en `~/.codex/config.toml` y una
configuración limitada al repositorio en `.codex/config.toml`. Para este
proyecto se recomienda la segunda opción, que Codex carga cuando el repositorio
está marcado como confiable.

Creá `.codex/config.toml` con el siguiente contenido y reemplazá `cwd` por la
ruta absoluta de tu copia del repositorio:

```toml
[mcp_servers.biblioteca]
command = "uv"
args = ["run", "python", "-m", "app.mcp_server"]
cwd = "/ruta/absoluta/al/proyecto"
startup_timeout_sec = 20
```

Las configuraciones global y local se combinan por capas. El archivo del
proyecto tiene mayor prioridad para las propiedades que declara, pero no
reemplaza por completo al global. Un valor inválido en `~/.codex/config.toml`
puede impedir que Codex arranque antes de cargar la configuración local.

Desde una terminal Bash, verificá el registro del servidor:

```bash
codex mcp list
```

El estado de `biblioteca` debe ser `enabled`. Luego iniciá la interfaz de Codex:

```bash
codex
```

Dentro de la interfaz de Codex, no en Bash, escribí:

```text
/mcp
```

La sección `biblioteca` debe mostrar las seis herramientas. El texto
`Auth: Unsupported` es normal para este servidor local: usa transporte `stdio`
y no implementa OAuth.

Codex descubre las herramientas al iniciar la sesión. Si se agregan, eliminan o
modifican herramientas en `app/mcp_server.py`, cerrá Codex y abrí una sesión
nueva antes de probarlas.

La configuración de servidores MCP en Codex está documentada en la
[guía oficial de MCP](https://learn.chatgpt.com/docs/extend/mcp).

### Ejemplos de consultas

Las herramientas se invocan desde el chat mediante lenguaje natural:

```text
Usá biblioteca para buscar libros cuyo título contenga "Quijote".
```

```text
Buscá libros de Borges mediante la herramienta buscar_libros_por_autor.
```

```text
Buscá socios cuyo apellido contenga "Sosa" mediante buscar_socios.
```

```text
Consultá la disponibilidad del libro con identificador 15.
```

```text
Listá los préstamos vencidos y mostrá cuántos días de atraso tiene cada uno.
```

```text
Mostrá las estadísticas generales de la biblioteca.
```

El cliente también puede combinar herramientas. Por ejemplo:

```text
Buscá libros cuyo título contenga "Python" y consultá la disponibilidad de
cada resultado.
```

Para comprobar específicamente la integración MCP y evitar que el agente ejecute
la consulta mediante Python o el shell, se puede indicar:

```text
Usá exclusivamente la herramienta MCP biblioteca.buscar_socios con el criterio
"Sosa". No ejecutes comandos de shell ni Python directamente.
```

### Otros clientes MCP

Los clientes que utilizan configuración JSON pueden iniciar el mismo proceso.
La forma exacta y la ubicación del archivo dependen del cliente:

```json
{
  "mcpServers": {
    "biblioteca": {
      "command": "uv",
      "args": [
        "--directory",
        "/ruta/absoluta/al/proyecto",
        "run",
        "python",
        "-m",
        "app.mcp_server"
      ]
    }
  }
}
```

### Solución de problemas

- `ModuleNotFoundError: No module named 'app'`: iniciá el proceso desde la raíz
  del repositorio o configurá correctamente `cwd`.
- La terminal parece detenida después de ejecutar `app.mcp_server`: el servidor
  está esperando mensajes por `stdio`; esto es normal.
- Bash responde `bash: /mcp: No such file or directory`: `/mcp` debe escribirse
  dentro de la interfaz interactiva de Codex.
- Una herramienta nueva no aparece: cerrá Codex, abrí una sesión nueva y volvé
  a comprobar `/mcp`.
- Codex propone ejecutar `python -c` o solicita permiso para `uv run python`:
  está intentando consultar la base sin usar MCP. Cancelá la operación y pedí
  explícitamente la herramienta `biblioteca.<nombre>`.
- La respuesta contiene `No se pudo consultar la biblioteca`: revisá `.env`,
  la disponibilidad de MySQL y los permisos del usuario configurado.
- `codex mcp list` informa un error en `~/.codex/config.toml`: corregí primero
  el archivo global; Codex valida esa capa antes de aplicar la configuración del
  proyecto.

## Pruebas

La suite usa SQLite en memoria para verificar las escrituras sin modificar la
base MySQL configurada. Cubre configuración, mapeos del DER, validaciones,
transacciones, reglas de préstamo, consultas de biblioteca, autenticación,
autorización y exposición segura de herramientas MCP.

```bash
uv run python -m pytest -q
```

Resultado de la última verificación: **20 pruebas aprobadas**.

## Estructura del proyecto

```text
.
├── app/
│   ├── core/          # Configuración, autenticación y middleware
│   ├── db/            # Motor, base declarativa y sesiones SQLAlchemy
│   ├── models/        # Mapeo de las diez tablas
│   ├── schemas/       # Validación Pydantic de formularios
│   ├── services/      # CRUD, reglas de negocio y consultas
│   ├── routes/        # Rutas web por dominio
│   ├── templates/     # Plantillas HTML Jinja2
│   ├── static/        # CSS y favicon
│   ├── main.py        # Configuración de FastAPI
│   └── mcp_server.py  # Servidor MCP de solo lectura
├── docs/               # Memoria escrita del trabajo final
├── sql/                # Esquema, datos de prueba y consultas
├── tests/              # Pruebas automatizadas
├── .env.example        # Plantilla de configuración
├── main.py             # Punto de entrada abreviado
├── pyproject.toml      # Metadatos y dependencias directas
├── requirements.txt    # Exportación reproducible sin dependencias de desarrollo
└── uv.lock             # Versiones resueltas por uv
```

`pyproject.toml` es la fuente editable de dependencias y `uv.lock` fija la
resolución completa. Si cambia una dependencia de producción, actualizá la
exportación con:

```bash
uv export --format requirements-txt --no-dev --no-hashes --output-file requirements.txt
```
