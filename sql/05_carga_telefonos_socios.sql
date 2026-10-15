-- Carga de teléfonos ficticios para los socios de la base biblioteca.
-- 45 socios con un teléfono principal y 10 de ellos con un número alternativo (55 teléfonos).
-- Los números son valores sintéticos de prueba; no corresponden a contactos reales.
-- Se vinculan por documento, sin suponer valores de AUTO_INCREMENT.
USE biblioteca;

START TRANSACTION;

INSERT IGNORE INTO telefono_socio (id_socio, numero, tipo)
SELECT s.id_persona, t.numero, t.tipo
FROM (
    SELECT '30100001' AS documento, '+54 9 11 0000 0001' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100002' AS documento, '+54 9 11 0000 0002' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100003' AS documento, '+54 9 11 0000 0003' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100004' AS documento, '+54 9 11 0000 0004' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100005' AS documento, '+54 9 11 0000 0005' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100006' AS documento, '+54 9 11 0000 0006' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100007' AS documento, '+54 9 11 0000 0007' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100008' AS documento, '+54 9 11 0000 0008' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100009' AS documento, '+54 9 11 0000 0009' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100010' AS documento, '+54 9 11 0000 0010' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100011' AS documento, '+54 9 11 0000 0011' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100012' AS documento, '+54 9 11 0000 0012' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100013' AS documento, '+54 9 11 0000 0013' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100014' AS documento, '+54 9 11 0000 0014' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100015' AS documento, '+54 9 11 0000 0015' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100016' AS documento, '+54 9 11 0000 0016' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100017' AS documento, '+54 9 11 0000 0017' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100018' AS documento, '+54 9 11 0000 0018' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100019' AS documento, '+54 9 11 0000 0019' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100020' AS documento, '+54 9 11 0000 0020' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100021' AS documento, '+54 9 11 0000 0021' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100022' AS documento, '+54 9 11 0000 0022' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100023' AS documento, '+54 9 11 0000 0023' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100024' AS documento, '+54 9 11 0000 0024' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100025' AS documento, '+54 9 11 0000 0025' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100026' AS documento, '+54 9 11 0000 0026' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100027' AS documento, '+54 9 11 0000 0027' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100028' AS documento, '+54 9 11 0000 0028' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100029' AS documento, '+54 9 11 0000 0029' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100030' AS documento, '+54 9 11 0000 0030' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100031' AS documento, '+54 9 11 0000 0031' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100032' AS documento, '+54 9 11 0000 0032' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100033' AS documento, '+54 9 11 0000 0033' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100034' AS documento, '+54 9 11 0000 0034' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100035' AS documento, '+54 9 11 0000 0035' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100036' AS documento, '+54 9 11 0000 0036' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100037' AS documento, '+54 9 11 0000 0037' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100038' AS documento, '+54 9 11 0000 0038' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100039' AS documento, '+54 9 11 0000 0039' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100040' AS documento, '+54 9 11 0000 0040' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100041' AS documento, '+54 9 11 0000 0041' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100042' AS documento, '+54 9 11 0000 0042' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100043' AS documento, '+54 9 11 0000 0043' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100044' AS documento, '+54 9 11 0000 0044' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100045' AS documento, '+54 9 11 0000 0045' AS numero, 'móvil' AS tipo
    UNION ALL SELECT '30100001' AS documento, '+54 9 11 9999 0001' AS numero, 'alternativo' AS tipo
    UNION ALL SELECT '30100002' AS documento, '+54 9 11 9999 0002' AS numero, 'alternativo' AS tipo
    UNION ALL SELECT '30100003' AS documento, '+54 9 11 9999 0003' AS numero, 'alternativo' AS tipo
    UNION ALL SELECT '30100004' AS documento, '+54 9 11 9999 0004' AS numero, 'alternativo' AS tipo
    UNION ALL SELECT '30100005' AS documento, '+54 9 11 9999 0005' AS numero, 'alternativo' AS tipo
    UNION ALL SELECT '30100006' AS documento, '+54 9 11 9999 0006' AS numero, 'alternativo' AS tipo
    UNION ALL SELECT '30100007' AS documento, '+54 9 11 9999 0007' AS numero, 'alternativo' AS tipo
    UNION ALL SELECT '30100008' AS documento, '+54 9 11 9999 0008' AS numero, 'alternativo' AS tipo
    UNION ALL SELECT '30100009' AS documento, '+54 9 11 9999 0009' AS numero, 'alternativo' AS tipo
    UNION ALL SELECT '30100010' AS documento, '+54 9 11 9999 0010' AS numero, 'alternativo' AS tipo
) AS t
JOIN persona AS p ON p.documento = t.documento
JOIN socio AS s ON s.id_persona = p.id_persona;

-- Verificación: se esperan 55 teléfonos distribuidos entre los 45 socios.
SELECT
    COUNT(*) AS telefonos_cargados,
    COUNT(DISTINCT ts.id_socio) AS socios_con_telefono
FROM telefono_socio AS ts
JOIN socio AS s ON s.id_persona = ts.id_socio
JOIN persona AS p ON p.id_persona = s.id_persona
WHERE p.documento BETWEEN '30100001' AND '30100045';

COMMIT;
