-- 20 preguntas de negocio sobre la base biblioteca.
-- Las sentencias son consultas de lectura (SELECT); no modifican datos.
-- Los resultados esperados presuponen que se cargaron los sets de prueba anteriores.
USE biblioteca;

-- 1. ¿Cuántas personas están registradas?
-- Esperado: 50.
SELECT COUNT(*) AS total_personas
FROM persona;

-- 2. ¿Cuántas personas tienen rol de socio?
-- Esperado: 45. JOIN con persona para contar personas del set cargado.
SELECT COUNT(*) AS total_socios
FROM socio AS s
JOIN persona AS p ON p.id_persona = s.id_persona;

-- 3. ¿Cuántas personas trabajan como bibliotecarias?
-- Esperado: 5.
SELECT COUNT(*) AS total_bibliotecarios
FROM bibliotecario AS b
JOIN persona AS p ON p.id_persona = b.id_persona;

-- 4. ¿Hay personas sin correo electrónico registrado?
-- Esperado: 0 filas. Esta consulta lista los casos para revisarlos.
SELECT id_persona, nombre, apellido
FROM persona
WHERE email IS NULL OR TRIM(email) = ''
ORDER BY apellido, nombre;

-- 5. ¿Cuántos teléfonos se registraron y cuántos socios tienen al menos uno?
-- Esperado: 55 teléfonos para 45 socios.
-- Informe multitabla: persona + socio + telefono_socio.
SELECT
    COUNT(DISTINCT ts.id_telefono_socio) AS total_telefonos,
    COUNT(DISTINCT p.id_persona) AS socios_con_telefono
FROM persona AS p
JOIN socio AS s ON s.id_persona = p.id_persona
JOIN telefono_socio AS ts ON ts.id_socio = s.id_persona;

-- 6. ¿Cuántos socios tienen uno o dos teléfonos?
-- Esperado: 35 socios con 1 teléfono y 10 socios con 2 teléfonos.
SELECT cantidad_telefonos, COUNT(*) AS cantidad_socios
FROM (
    SELECT id_socio, COUNT(*) AS cantidad_telefonos
    FROM telefono_socio
    GROUP BY id_socio
) AS telefonos_por_socio
GROUP BY cantidad_telefonos
ORDER BY cantidad_telefonos;

-- 7. ¿Cuántos autores están registrados?
-- Esperado: 110 si la tabla estaba vacía antes de la carga.
SELECT COUNT(*) AS total_autores
FROM autor;

-- 8. ¿Cuántos autores tienen al menos un libro asociado y cuántos no tienen ninguno?
-- Esperado: 50 con libro y 60 sin libro.
-- Informe multitabla: autor + libro_autor + libro.
SELECT
    COUNT(DISTINCT CASE WHEN l.id_libro IS NOT NULL THEN a.id_autor END)
        AS autores_con_libro,
    COUNT(DISTINCT CASE WHEN l.id_libro IS NULL THEN a.id_autor END)
        AS autores_sin_libro
FROM autor AS a
LEFT JOIN libro_autor AS la ON la.id_autor = a.id_autor
LEFT JOIN libro AS l ON l.id_libro = la.id_libro;

-- 9. ¿Cuántas editoriales están registradas?
-- Esperado: 30 si la tabla estaba vacía antes de la carga.
SELECT COUNT(*) AS total_editoriales
FROM editorial;

-- 10. ¿Cuántas editoriales no tienen libros asociados?
-- Esperado: 11.
SELECT COUNT(*) AS editoriales_sin_libros
FROM editorial AS e
WHERE NOT EXISTS (
    SELECT 1
    FROM libro AS l
    WHERE l.id_editorial = e.id_editorial
);

-- 11. ¿Cuántos libros integran el catálogo?
-- Esperado: 50.
SELECT COUNT(*) AS total_libros
FROM libro;

-- 12. ¿Cuántos títulos comienzan con "El"?
-- Esperado: 18 títulos.
SELECT COUNT(*) AS titulos_que_comienzan_con_el
FROM libro
WHERE titulo LIKE 'El %';

-- 13. ¿Cuántos libros se publicaron en cada año?
-- Esperado: 2017: 4; 2018: 7; 2019: 7; 2020: 9;
--           2021: 8; 2022: 6; 2023: 5; 2024: 4.
SELECT anio_publicacion, COUNT(*) AS cantidad_libros
FROM libro
GROUP BY anio_publicacion
ORDER BY anio_publicacion;

-- 14. ¿Qué editoriales tienen la mayor cantidad de libros en el set?
-- Esperado: Alfaguara y HarperCollins, con 5 libros cada una.
-- Informe multitabla: editorial + libro + libro_autor.
-- DISTINCT evita repetir libros que tengan más de un autor.
SELECT e.nombre AS editorial, COUNT(DISTINCT l.id_libro) AS cantidad_libros
FROM editorial AS e
JOIN libro AS l ON l.id_editorial = e.id_editorial
LEFT JOIN libro_autor AS la ON la.id_libro = l.id_libro
GROUP BY e.id_editorial, e.nombre
HAVING COUNT(DISTINCT l.id_libro) = (
    SELECT MAX(cantidad_libros)
    FROM (
        SELECT COUNT(*) AS cantidad_libros
        FROM libro
        GROUP BY id_editorial
    ) AS conteos
)
ORDER BY e.nombre;

-- 15. ¿Hay libros sin autor asociado?
-- Esperado: 0 filas.
SELECT l.id_libro, l.titulo
FROM libro AS l
LEFT JOIN libro_autor AS la ON la.id_libro = l.id_libro
WHERE la.id_libro IS NULL
ORDER BY l.titulo;

-- 16. ¿Hay libros sin ejemplares registrados?
-- Esperado: 0 filas.
SELECT l.id_libro, l.titulo
FROM libro AS l
LEFT JOIN ejemplar AS e ON e.id_libro = l.id_libro
WHERE e.id_ejemplar IS NULL
ORDER BY l.titulo;

-- 17. ¿Cuántos libros tienen uno, dos o tres ejemplares?
-- Esperado: 1 ejemplar: 16 libros; 2 ejemplares: 17; 3 ejemplares: 17.
SELECT cantidad_ejemplares, COUNT(*) AS cantidad_libros
FROM (
    SELECT l.id_libro, COUNT(e.id_ejemplar) AS cantidad_ejemplares
    FROM libro AS l
    LEFT JOIN ejemplar AS e ON e.id_libro = l.id_libro
    GROUP BY l.id_libro
) AS ejemplares_por_libro
GROUP BY cantidad_ejemplares
ORDER BY cantidad_ejemplares;

-- 18. ¿Cuántos ejemplares están operativos y cuántos en reparación?
-- Esperado para el set cargado: 97 operativos y 4 en reparación.
SELECT estado, COUNT(*) AS cantidad_ejemplares
FROM ejemplar
WHERE codigo_inventario BETWEEN 'INV-0001' AND 'INV-0101'
GROUP BY estado
ORDER BY estado;

-- 19. ¿Qué libros tienen ejemplares en reparación?
-- Esperado: El último tren de la memoria; Pequeño atlas de la noche;
--           Los nombres del bosque profundo; El mapa de los pájaros azules.
-- Informe multitabla: editorial + libro + ejemplar.
SELECT ed.nombre AS editorial, l.titulo,
       COUNT(e.id_ejemplar) AS ejemplares_en_reparacion
FROM editorial AS ed
JOIN libro AS l ON l.id_editorial = ed.id_editorial
JOIN ejemplar AS e ON e.id_libro = l.id_libro
WHERE e.estado = 'en_reparacion'
  AND e.codigo_inventario BETWEEN 'INV-0001' AND 'INV-0101'
GROUP BY ed.id_editorial, ed.nombre, l.id_libro, l.titulo
ORDER BY l.titulo;

-- 20. ¿Qué libros tienen menos de tres ejemplares para evaluar una ampliación del inventario?
-- Esperado: 33 libros. La consulta lista sus títulos y cantidades actuales.
-- Informe multitabla: editorial + libro + ejemplar.
SELECT ed.nombre AS editorial, l.titulo,
       COUNT(e.id_ejemplar) AS cantidad_ejemplares
FROM editorial AS ed
JOIN libro AS l ON l.id_editorial = ed.id_editorial
LEFT JOIN ejemplar AS e ON e.id_libro = l.id_libro
GROUP BY ed.id_editorial, ed.nombre, l.id_libro, l.titulo
HAVING COUNT(e.id_ejemplar) < 3
ORDER BY cantidad_ejemplares, l.titulo;
