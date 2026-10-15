-- Carga de ejemplares para los 50 libros ficticios del set de prueba.
-- Cada libro recibe entre 1 y 3 ejemplares; total esperado: 101.
-- Hay 4 ejemplares en reparación y al menos uno operativo por libro.
-- Ejecutar después de cargar los libros. Los códigos INV son ficticios y únicos.
USE biblioteca;

START TRANSACTION;

INSERT IGNORE INTO ejemplar (id_libro, codigo_inventario, fecha_incorporacion, estado)
SELECT l.id_libro, d.codigo_inventario, d.fecha_incorporacion, d.estado
FROM (
    SELECT '9781234560010' AS isbn, 'INV-0001' AS codigo_inventario, '2023-01-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560010' AS isbn, 'INV-0002' AS codigo_inventario, '2023-01-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560027' AS isbn, 'INV-0003' AS codigo_inventario, '2023-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560027' AS isbn, 'INV-0004' AS codigo_inventario, '2023-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560027' AS isbn, 'INV-0005' AS codigo_inventario, '2023-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560034' AS isbn, 'INV-0006' AS codigo_inventario, '2023-03-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560041' AS isbn, 'INV-0007' AS codigo_inventario, '2023-04-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560041' AS isbn, 'INV-0008' AS codigo_inventario, '2023-04-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560058' AS isbn, 'INV-0009' AS codigo_inventario, '2023-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560058' AS isbn, 'INV-0010' AS codigo_inventario, '2023-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560058' AS isbn, 'INV-0011' AS codigo_inventario, '2023-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560065' AS isbn, 'INV-0012' AS codigo_inventario, '2023-06-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560072' AS isbn, 'INV-0013' AS codigo_inventario, '2023-07-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560072' AS isbn, 'INV-0014' AS codigo_inventario, '2023-07-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560089' AS isbn, 'INV-0015' AS codigo_inventario, '2023-08-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560089' AS isbn, 'INV-0016' AS codigo_inventario, '2023-08-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560089' AS isbn, 'INV-0017' AS codigo_inventario, '2023-08-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560096' AS isbn, 'INV-0018' AS codigo_inventario, '2023-09-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560102' AS isbn, 'INV-0019' AS codigo_inventario, '2023-10-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560102' AS isbn, 'INV-0020' AS codigo_inventario, '2023-10-15' AS fecha_incorporacion, 'en_reparacion' AS estado
    UNION ALL SELECT '9781234560119' AS isbn, 'INV-0021' AS codigo_inventario, '2023-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560119' AS isbn, 'INV-0022' AS codigo_inventario, '2023-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560119' AS isbn, 'INV-0023' AS codigo_inventario, '2023-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560126' AS isbn, 'INV-0024' AS codigo_inventario, '2023-12-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560133' AS isbn, 'INV-0025' AS codigo_inventario, '2024-01-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560133' AS isbn, 'INV-0026' AS codigo_inventario, '2024-01-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560140' AS isbn, 'INV-0027' AS codigo_inventario, '2024-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560140' AS isbn, 'INV-0028' AS codigo_inventario, '2024-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560140' AS isbn, 'INV-0029' AS codigo_inventario, '2024-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560157' AS isbn, 'INV-0030' AS codigo_inventario, '2024-03-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560164' AS isbn, 'INV-0031' AS codigo_inventario, '2024-04-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560164' AS isbn, 'INV-0032' AS codigo_inventario, '2024-04-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560171' AS isbn, 'INV-0033' AS codigo_inventario, '2024-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560171' AS isbn, 'INV-0034' AS codigo_inventario, '2024-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560171' AS isbn, 'INV-0035' AS codigo_inventario, '2024-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560188' AS isbn, 'INV-0036' AS codigo_inventario, '2024-06-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560195' AS isbn, 'INV-0037' AS codigo_inventario, '2024-07-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560195' AS isbn, 'INV-0038' AS codigo_inventario, '2024-07-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560201' AS isbn, 'INV-0039' AS codigo_inventario, '2024-08-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560201' AS isbn, 'INV-0040' AS codigo_inventario, '2024-08-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560201' AS isbn, 'INV-0041' AS codigo_inventario, '2024-08-15' AS fecha_incorporacion, 'en_reparacion' AS estado
    UNION ALL SELECT '9781234560218' AS isbn, 'INV-0042' AS codigo_inventario, '2024-09-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560225' AS isbn, 'INV-0043' AS codigo_inventario, '2024-10-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560225' AS isbn, 'INV-0044' AS codigo_inventario, '2024-10-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560232' AS isbn, 'INV-0045' AS codigo_inventario, '2024-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560232' AS isbn, 'INV-0046' AS codigo_inventario, '2024-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560232' AS isbn, 'INV-0047' AS codigo_inventario, '2024-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560249' AS isbn, 'INV-0048' AS codigo_inventario, '2024-12-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560256' AS isbn, 'INV-0049' AS codigo_inventario, '2025-01-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560256' AS isbn, 'INV-0050' AS codigo_inventario, '2025-01-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560263' AS isbn, 'INV-0051' AS codigo_inventario, '2025-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560263' AS isbn, 'INV-0052' AS codigo_inventario, '2025-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560263' AS isbn, 'INV-0053' AS codigo_inventario, '2025-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560270' AS isbn, 'INV-0054' AS codigo_inventario, '2025-03-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560287' AS isbn, 'INV-0055' AS codigo_inventario, '2025-04-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560287' AS isbn, 'INV-0056' AS codigo_inventario, '2025-04-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560294' AS isbn, 'INV-0057' AS codigo_inventario, '2025-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560294' AS isbn, 'INV-0058' AS codigo_inventario, '2025-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560294' AS isbn, 'INV-0059' AS codigo_inventario, '2025-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560300' AS isbn, 'INV-0060' AS codigo_inventario, '2025-06-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560317' AS isbn, 'INV-0061' AS codigo_inventario, '2025-07-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560317' AS isbn, 'INV-0062' AS codigo_inventario, '2025-07-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560324' AS isbn, 'INV-0063' AS codigo_inventario, '2025-08-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560324' AS isbn, 'INV-0064' AS codigo_inventario, '2025-08-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560324' AS isbn, 'INV-0065' AS codigo_inventario, '2025-08-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560331' AS isbn, 'INV-0066' AS codigo_inventario, '2025-09-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560348' AS isbn, 'INV-0067' AS codigo_inventario, '2025-10-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560348' AS isbn, 'INV-0068' AS codigo_inventario, '2025-10-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560355' AS isbn, 'INV-0069' AS codigo_inventario, '2025-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560355' AS isbn, 'INV-0070' AS codigo_inventario, '2025-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560355' AS isbn, 'INV-0071' AS codigo_inventario, '2025-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560362' AS isbn, 'INV-0072' AS codigo_inventario, '2025-12-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560379' AS isbn, 'INV-0073' AS codigo_inventario, '2026-01-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560379' AS isbn, 'INV-0074' AS codigo_inventario, '2026-01-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560386' AS isbn, 'INV-0075' AS codigo_inventario, '2026-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560386' AS isbn, 'INV-0076' AS codigo_inventario, '2026-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560386' AS isbn, 'INV-0077' AS codigo_inventario, '2026-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560393' AS isbn, 'INV-0078' AS codigo_inventario, '2026-03-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560409' AS isbn, 'INV-0079' AS codigo_inventario, '2026-04-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560409' AS isbn, 'INV-0080' AS codigo_inventario, '2026-04-15' AS fecha_incorporacion, 'en_reparacion' AS estado
    UNION ALL SELECT '9781234560416' AS isbn, 'INV-0081' AS codigo_inventario, '2026-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560416' AS isbn, 'INV-0082' AS codigo_inventario, '2026-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560416' AS isbn, 'INV-0083' AS codigo_inventario, '2026-05-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560423' AS isbn, 'INV-0084' AS codigo_inventario, '2026-06-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560430' AS isbn, 'INV-0085' AS codigo_inventario, '2026-07-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560430' AS isbn, 'INV-0086' AS codigo_inventario, '2026-07-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560447' AS isbn, 'INV-0087' AS codigo_inventario, '2026-08-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560447' AS isbn, 'INV-0088' AS codigo_inventario, '2026-08-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560447' AS isbn, 'INV-0089' AS codigo_inventario, '2026-08-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560454' AS isbn, 'INV-0090' AS codigo_inventario, '2026-09-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560461' AS isbn, 'INV-0091' AS codigo_inventario, '2026-10-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560461' AS isbn, 'INV-0092' AS codigo_inventario, '2026-10-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560478' AS isbn, 'INV-0093' AS codigo_inventario, '2026-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560478' AS isbn, 'INV-0094' AS codigo_inventario, '2026-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560478' AS isbn, 'INV-0095' AS codigo_inventario, '2026-11-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560485' AS isbn, 'INV-0096' AS codigo_inventario, '2026-12-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560492' AS isbn, 'INV-0097' AS codigo_inventario, '2023-01-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560492' AS isbn, 'INV-0098' AS codigo_inventario, '2023-01-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560508' AS isbn, 'INV-0099' AS codigo_inventario, '2023-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560508' AS isbn, 'INV-0100' AS codigo_inventario, '2023-02-15' AS fecha_incorporacion, 'operativo' AS estado
    UNION ALL SELECT '9781234560508' AS isbn, 'INV-0101' AS codigo_inventario, '2023-02-15' AS fecha_incorporacion, 'en_reparacion' AS estado
) AS d
JOIN libro AS l ON l.isbn = d.isbn;

-- Verificación general: se esperan 101 ejemplares asociados a 50 libros.
SELECT
    COUNT(*) AS ejemplares_cargados,
    COUNT(DISTINCT e.id_libro) AS libros_con_ejemplares,
    SUM(e.estado = 'en_reparacion') AS ejemplares_en_reparacion,
    SUM(e.estado = 'operativo') AS ejemplares_operativos
FROM ejemplar AS e
JOIN libro AS l ON l.id_libro = e.id_libro
WHERE l.isbn BETWEEN '9781234560010' AND '9781234560508'
  AND e.codigo_inventario BETWEEN 'INV-0001' AND 'INV-0101';

-- Verificación por libro: ninguna fila debe indicar menos de 1 ni más de 3 ejemplares.
SELECT l.isbn, l.titulo, COUNT(e.id_ejemplar) AS cantidad_ejemplares
FROM libro AS l
LEFT JOIN ejemplar AS e ON e.id_libro = l.id_libro
  AND e.codigo_inventario BETWEEN 'INV-0001' AND 'INV-0101'
WHERE l.isbn BETWEEN '9781234560010' AND '9781234560508'
GROUP BY l.id_libro, l.isbn, l.titulo
HAVING COUNT(e.id_ejemplar) NOT BETWEEN 1 AND 3;

COMMIT;
