SELECT concepto, esperado, obtenido,
       IF(esperado = obtenido, 'Coincide', 'Revisar') AS conclusion
FROM (
    SELECT 'Personas registradas' AS concepto, 50 AS esperado,
           (SELECT COUNT(*) FROM persona) AS obtenido
    UNION ALL
    SELECT 'Socios registrados', 45, (SELECT COUNT(*) FROM socio)
    UNION ALL
    SELECT 'Bibliotecarios registrados', 5,
           (SELECT COUNT(*) FROM bibliotecario)
    UNION ALL
    SELECT 'Editoriales después de la limpieza', 30,
           (SELECT COUNT(*) FROM editorial)
    UNION ALL
    SELECT 'Editoriales sin libros', 11,
           (SELECT COUNT(*)
            FROM editorial AS e
            WHERE NOT EXISTS (
                SELECT 1 FROM libro AS l
                WHERE l.id_editorial = e.id_editorial
            ))
    UNION ALL
    SELECT 'Libros registrados', 50, (SELECT COUNT(*) FROM libro)
    UNION ALL
    SELECT 'Ejemplares registrados', 101,
           (SELECT COUNT(*) FROM ejemplar)
    UNION ALL
    SELECT 'Ejemplares en reparación', 4,
           (SELECT COUNT(*) FROM ejemplar
            WHERE estado = 'en_reparacion')
) AS verificacion;


SELECT COUNT(*) AS total_editoriales,
       COUNT(DISTINCT nombre) AS nombres_distintos,
       COUNT(*) - COUNT(DISTINCT nombre) AS nombres_repetidos
FROM editorial;

SHOW INDEX FROM ejemplar;

EXPLAIN
SELECT l.titulo, COUNT(e.id_ejemplar) AS ejemplares_en_reparacion
FROM libro AS l
JOIN ejemplar AS e ON e.id_libro = l.id_libro
WHERE e.estado = 'en_reparacion'
  AND e.codigo_inventario BETWEEN 'INV-0001' AND 'INV-0101'
GROUP BY l.id_libro, l.titulo
ORDER BY l.titulo;

