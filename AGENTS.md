# AGENTS.md

## Contexto del proyecto

Aplicación de biblioteca desarrollada con FastAPI, SQLAlchemy y MySQL.
Los scripts SQL están en `sql/` y el informe académico en `docs/`.

## Fuentes de verdad

- El esquema MySQL está en `sql/Biblioteca_2026-10-12T20_27_58.966Z.sql`.
- Las consultas de negocio están en
  `sql/07_consultas_20_preguntas_biblioteca.sql`.
- Su implementación Python está en
  `app/services/report_queries.py`.
- `docs/content.md` contiene la fuente del informe académico.

## Seguridad y base de datos

- No mostrar valores del archivo `.env`.
- No ejecutar scripts de carga sin autorización explícita.
- No crear índices, modificar tablas ni alterar datos durante una revisión.
- No afirmar que una consulta fue ejecutada en MySQL sin evidencia.
- Las pruebas SQLite no deben presentarse como validación del set MySQL.

## Convenciones de implementación

- Mantener sincronizadas las consultas SQL y sus equivalentes SQLAlchemy.
- Usar parámetros enlazados; no concatenar entradas dentro del SQL.
- Controlar la multiplicación de totales producida por relaciones uno a muchos.
- Preservar los nombres de tablas y columnas definidos en el esquema.

## Verificación

Después de modificar código Python, ejecutar:

`PYTHONPATH=. uv run pytest -q`

Antes de finalizar:

- Ejecutar `git diff --check`.
- Informar qué pruebas se ejecutaron.
- Diferenciar resultados comprobados de resultados esperados.

## Documentación académica

- Distinguir lo implementado en código de lo incorporado al informe.
- Cada consulta de la Parte 6 debe registrar:
  - pregunta de negocio;
  - consulta SQL;
  - resultado esperado;
  - resultado obtenido;
  - comprobación y conclusión.
- El uso de IA debe registrar prompt, respuesta y correcciones humanas.