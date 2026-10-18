-- Comparación del plan de ejecución antes y después de una optimización.
-- Consulta elegida: informe 19, libros con ejemplares en reparación.
--
-- Ejecutar las secciones en orden y conservar las dos grillas producidas por
-- EXPLAIN. La primera ejecución presupone el esquema original, que no contiene
-- el índice ix_ejemplar_estado_codigo_libro. Si el índice ya fue creado en una
-- ejecución anterior, eliminarlo manualmente antes de repetir la comparación.

USE biblioteca;

-- 1. ANTES DE OPTIMIZAR
-- El esquema original tiene un índice sobre codigo_inventario y otro sobre
-- (id_libro), pero no uno que comience por el filtro de igualdad estado y
-- continúe con el rango de codigo_inventario.
EXPLAIN
SELECT ed.nombre AS editorial, l.titulo,
       COUNT(e.id_ejemplar) AS ejemplares_en_reparacion
FROM editorial AS ed
JOIN libro AS l ON l.id_editorial = ed.id_editorial
JOIN ejemplar AS e ON e.id_libro = l.id_libro
WHERE e.estado = 'en_reparacion'
  AND e.codigo_inventario BETWEEN 'INV-0001' AND 'INV-0101'
GROUP BY ed.id_editorial, ed.nombre, l.id_libro, l.titulo
ORDER BY l.titulo;

-- 2. OPTIMIZACIÓN
-- estado encabeza el índice porque se compara por igualdad. A continuación se
-- ubica codigo_inventario, utilizado como rango. id_libro completa el índice
-- con la columna empleada para unir ejemplar con libro.
CREATE INDEX ix_ejemplar_estado_codigo_libro
    ON ejemplar (estado, codigo_inventario, id_libro);

-- Actualiza las estadísticas para que el optimizador pueda evaluar el índice.
ANALYZE TABLE ejemplar;

-- 3. DESPUÉS DE OPTIMIZAR
-- Es exactamente la misma consulta: la única diferencia es el nuevo índice.
EXPLAIN
SELECT ed.nombre AS editorial, l.titulo,
       COUNT(e.id_ejemplar) AS ejemplares_en_reparacion
FROM editorial AS ed
JOIN libro AS l ON l.id_editorial = ed.id_editorial
JOIN ejemplar AS e ON e.id_libro = l.id_libro
WHERE e.estado = 'en_reparacion'
  AND e.codigo_inventario BETWEEN 'INV-0001' AND 'INV-0101'
GROUP BY ed.id_editorial, ed.nombre, l.id_libro, l.titulo
ORDER BY l.titulo;

-- 4. QUÉ COMPARAR EN LOS DOS RESULTADOS
-- type  : se espera un acceso más selectivo que ALL para ejemplar.
-- key   : después debería poder elegirse ix_ejemplar_estado_codigo_libro.
-- rows  : la estimación de filas examinadas debería disminuir.
-- Extra : revisar "Using index condition", "Using where" y las operaciones
--         temporales o de ordenamiento. El resultado concreto depende de las
--         estadísticas y del volumen de datos de la instancia MySQL.
--
-- Para deshacer la optimización después de documentar la actividad:
-- DROP INDEX ix_ejemplar_estado_codigo_libro ON ejemplar;
