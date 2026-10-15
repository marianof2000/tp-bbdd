-- Carga básica de personas y roles para la base biblioteca
-- Datos ficticios de prueba: 45 socios y 5 bibliotecarios.
-- Ejecutar después de crear el esquema y seleccionar la base biblioteca.
-- Los roles se vinculan por documento; no se presupone el valor de AUTO_INCREMENT.

USE biblioteca;

START TRANSACTION;

INSERT INTO persona (nombre, apellido, documento, email) VALUES
    ('Lucía', 'Benítez', '30100001', 'lucia.benitez@example.com'),
    ('Mateo', 'Sosa', '30100002', 'mateo.sosa@example.com'),
    ('Valentina', 'Giménez', '30100003', 'valentina.gimenez@example.com'),
    ('Joaquín', 'Pereyra', '30100004', 'joaquin.pereyra@example.com'),
    ('Camila', 'López', '30100005', 'camila.lopez@example.com'),
    ('Benjamín', 'Molina', '30100006', 'benjamin.molina@example.com'),
    ('Martina', 'Acosta', '30100007', 'martina.acosta@example.com'),
    ('Santiago', 'Romero', '30100008', 'santiago.romero@example.com'),
    ('Sofía', 'Herrera', '30100009', 'sofia.herrera@example.com'),
    ('Tomás', 'Díaz', '30100010', 'tomas.diaz@example.com'),
    ('Mía', 'Torres', '30100011', 'mia.torres@example.com'),
    ('Bautista', 'Álvarez', '30100012', 'bautista.alvarez@example.com'),
    ('Emma', 'Ruiz', '30100013', 'emma.ruiz@example.com'),
    ('Felipe', 'Ramírez', '30100014', 'felipe.ramirez@example.com'),
    ('Catalina', 'Flores', '30100015', 'catalina.flores@example.com'),
    ('Benicio', 'Acosta', '30100016', 'benicio.acosta@example.com'),
    ('Olivia', 'Medina', '30100017', 'olivia.medina@example.com'),
    ('Thiago', 'Suárez', '30100018', 'thiago.suarez@example.com'),
    ('Ambar', 'Castro', '30100019', 'ambar.castro@example.com'),
    ('Franco', 'Ortiz', '30100020', 'franco.ortiz@example.com'),
    ('Renata', 'Silva', '30100021', 'renata.silva@example.com'),
    ('Lautaro', 'Núñez', '30100022', 'lautaro.nunez@example.com'),
    ('Julieta', 'Rojas', '30100023', 'julieta.rojas@example.com'),
    ('Dante', 'Cabrera', '30100024', 'dante.cabrera@example.com'),
    ('Abril', 'Vega', '30100025', 'abril.vega@example.com'),
    ('Máximo', 'Luna', '30100026', 'maximo.luna@example.com'),
    ('Zoe', 'Ferreyra', '30100027', 'zoe.ferreyra@example.com'),
    ('Valentín', 'Aguirre', '30100028', 'valentin.aguirre@example.com'),
    ('Alma', 'Méndez', '30100029', 'alma.mendez@example.com'),
    ('Ciro', 'Vázquez', '30100030', 'ciro.vazquez@example.com'),
    ('Pilar', 'Miranda', '30100031', 'pilar.miranda@example.com'),
    ('Juan', 'Ponce', '30100032', 'juan.ponce@example.com'),
    ('Delfina', 'Carrizo', '30100033', 'delfina.carrizo@example.com'),
    ('Facundo', 'Peralta', '30100034', 'facundo.peralta@example.com'),
    ('Clara', 'Domínguez', '30100035', 'clara.dominguez@example.com'),
    ('Agustín', 'Benítez', '30100036', 'agustin.benitez@example.com'),
    ('Josefina', 'Correa', '30100037', 'josefina.correa@example.com'),
    ('Nicolás', 'Sosa', '30100038', 'nicolas.sosa@example.com'),
    ('Malena', 'Ibarra', '30100039', 'malena.ibarra@example.com'),
    ('Simón', 'Godoy', '30100040', 'simon.godoy@example.com'),
    ('Lola', 'Figueroa', '30100041', 'lola.figueroa@example.com'),
    ('Pedro', 'Cáceres', '30100042', 'pedro.caceres@example.com'),
    ('Ana', 'Montenegro', '30100043', 'ana.montenegro@example.com'),
    ('Ezequiel', 'Quiroga', '30100044', 'ezequiel.quiroga@example.com'),
    ('Carolina', 'Vera', '30100045', 'carolina.vera@example.com'),
    ('Mariana', 'Costa', '30100046', 'mariana.costa@example.com'),
    ('Pablo', 'Ledesma', '30100047', 'pablo.ledesma@example.com'),
    ('Gabriela', 'Serrano', '30100048', 'gabriela.serrano@example.com'),
    ('Diego', 'Paz', '30100049', 'diego.paz@example.com'),
    ('Laura', 'Mansilla', '30100050', 'laura.mansilla@example.com');

-- Los 45 socios se identifican por el documento, no por un id supuesto.
INSERT INTO socio (id_persona, fecha_alta)
SELECT p.id_persona, DATE_ADD('2025-01-01', INTERVAL (CAST(RIGHT(p.documento, 2) AS UNSIGNED) MOD 300) DAY)
FROM persona AS p
WHERE p.documento BETWEEN '30100001' AND '30100045';

-- Los 5 bibliotecarios: legajos de prueba únicos.
INSERT INTO bibliotecario (id_persona, legajo)
SELECT p.id_persona, CONCAT('BIB-', RIGHT(p.documento, 2))
FROM persona AS p
WHERE p.documento BETWEEN '30100046' AND '30100050';

-- Verificación: deben resultar 50 personas, 45 socios y 5 bibliotecarios.
SELECT
    (SELECT COUNT(*) FROM persona WHERE documento BETWEEN '30100001' AND '30100050') AS personas_cargadas,
    (SELECT COUNT(*) FROM socio s JOIN persona p ON p.id_persona = s.id_persona WHERE p.documento BETWEEN '30100001' AND '30100045') AS socios_cargados,
    (SELECT COUNT(*) FROM bibliotecario b JOIN persona p ON p.id_persona = b.id_persona WHERE p.documento BETWEEN '30100046' AND '30100050') AS bibliotecarios_cargados;

COMMIT;
