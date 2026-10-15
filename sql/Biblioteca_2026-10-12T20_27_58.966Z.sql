CREATE DATABASE IF NOT EXISTS biblioteca
    CHARACTER SET utf8mb4;

USE biblioteca;


CREATE TABLE IF NOT EXISTS `persona` (
	`id_persona` INT NOT NULL AUTO_INCREMENT,
	`nombre` VARCHAR(80) NOT NULL,
	`apellido` VARCHAR(80) NOT NULL,
	`documento` VARCHAR(20) NOT NULL UNIQUE COMMENT 'Obligatorio y único según el alcance del proyecto.',
	`email` VARCHAR(254) COMMENT 'Opcional; puede compartirse. No es clave candidata.',
	PRIMARY KEY(`id_persona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Identidad común de socios y bibliotecarios. Especialización total y superpuesta.';


CREATE TABLE IF NOT EXISTS `socio` (
	`id_persona` INT NOT NULL COMMENT 'PK/FK a persona.id_persona; no genera identidad independiente.',
	`fecha_alta` DATE NOT NULL,
	PRIMARY KEY(`id_persona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Rol que habilita a recibir préstamos. Persona 0..1 socio; todo socio tiene 1 persona.';


CREATE TABLE IF NOT EXISTS `bibliotecario` (
	`id_persona` INT NOT NULL COMMENT 'PK/FK a persona.id_persona; no genera identidad independiente.',
	`legajo` VARCHAR(30) NOT NULL UNIQUE,
	PRIMARY KEY(`id_persona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Rol que habilita a registrar préstamos. Persona 0..1 bibliotecario; todo bibliotecario tiene 1 persona.';


CREATE TABLE IF NOT EXISTS `telefono_socio` (
	`id_telefono_socio` INT NOT NULL AUTO_INCREMENT,
	`id_socio` INT NOT NULL COMMENT 'FK hacia socio.id_persona. Identifica el rol socio.',
	`numero` VARCHAR(25) NOT NULL,
	`tipo` VARCHAR(20) COMMENT 'Clasificación del contacto informado por este socio.',
	PRIMARY KEY(`id_telefono_socio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Cada socio puede registrar 0..N teléfonos. Número único dentro de cada socio.';


CREATE UNIQUE INDEX `uq_telefono_socio_numero`
ON `telefono_socio` (`id_socio`, `numero`);

CREATE TABLE IF NOT EXISTS `editorial` (
	`id_editorial` INT NOT NULL AUTO_INCREMENT,
	`nombre` VARCHAR(120) NOT NULL,
	PRIMARY KEY(`id_editorial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Editorial que publica libros. No se presupone unicidad del nombre.';


CREATE TABLE IF NOT EXISTS `autor` (
	`id_autor` INT NOT NULL AUTO_INCREMENT,
	`nombre` VARCHAR(80) NOT NULL,
	`apellido` VARCHAR(80) NOT NULL,
	PRIMARY KEY(`id_autor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Identidad bibliográfica independiente de la jerarquía persona. Puede asociarse a 0..N libros.';


CREATE TABLE IF NOT EXISTS `libro` (
	`id_libro` INT NOT NULL AUTO_INCREMENT,
	`titulo` VARCHAR(200) NOT NULL,
	`isbn` VARCHAR(17) NOT NULL UNIQUE COMMENT 'Obligatorio y único según el alcance del proyecto.',
	`anio_publicacion` SMALLINT,
	`id_editorial` INT NOT NULL,
	PRIMARY KEY(`id_libro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registro bibliográfico independiente de las copias. Cada libro tiene 1 editorial, 0..N ejemplares y 1..N autores para considerarse completo.';


CREATE INDEX `ix_libro_editorial`
ON `libro` (`id_editorial`);

CREATE TABLE IF NOT EXISTS `ejemplar` (
	`id_ejemplar` INT NOT NULL AUTO_INCREMENT,
	`id_libro` INT NOT NULL,
	`codigo_inventario` VARCHAR(40) NOT NULL UNIQUE,
	`fecha_incorporacion` DATE NOT NULL,
	`estado` ENUM('operativo', 'en_reparacion') NOT NULL COMMENT 'Estado físico, diferente de disponibilidad.',
	PRIMARY KEY(`id_ejemplar`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Copia física de un libro. Disponibilidad derivada: operativo y sin préstamo pendiente. No se almacena disponibilidad.';


CREATE INDEX `ix_ejemplar_libro`
ON `ejemplar` (`id_libro`);

CREATE TABLE IF NOT EXISTS `prestamo` (
	`id_prestamo` INT NOT NULL AUTO_INCREMENT,
	`id_socio` INT NOT NULL COMMENT 'FK hacia socio.id_persona; receptor del ejemplar.',
	`id_ejemplar` INT NOT NULL,
	`id_bibliotecario` INT NOT NULL COMMENT 'FK hacia bibliotecario.id_persona; responsable del registro.',
	`fecha_prestamo` DATE NOT NULL,
	`fecha_vencimiento_inicial` DATE NOT NULL COMMENT 'Dato histórico inmutable ante renovaciones.',
	`fecha_vencimiento_actual` DATE NOT NULL COMMENT 'Plazo vigente; puede cambiar por renovación.',
	`fecha_devolucion` DATE COMMENT 'NULL indica pendiente de devolución.',
	PRIMARY KEY(`id_prestamo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Una operación por ejemplar. No se repiten datos personales ni bibliográficos. Reglas de fechas y simultaneidad en notas.';


CREATE INDEX `ix_prestamo_socio`
ON `prestamo` (`id_socio`);
CREATE INDEX `ix_prestamo_ejemplar_devolucion`
ON `prestamo` (`id_ejemplar`, `fecha_devolucion`);
CREATE INDEX `ix_prestamo_bibliotecario`
ON `prestamo` (`id_bibliotecario`);

CREATE TABLE IF NOT EXISTS `libro_autor` (
	`id_libro_autor` INT NOT NULL AUTO_INCREMENT,
	`id_libro` INT NOT NULL,
	`id_autor` INT NOT NULL,
	`orden_autoria` SMALLINT NOT NULL COMMENT 'Posición del autor en este libro; depende de la combinación libro-autor.',
	PRIMARY KEY(`id_libro_autor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Entidad asociativa que resuelve libro N:M autor y conserva orden_autoria. No debe repetirse libro-autor.';


CREATE UNIQUE INDEX `uq_libro_autor`
ON `libro_autor` (`id_libro`, `id_autor`);
CREATE INDEX `ix_libro_autor_autor`
ON `libro_autor` (`id_autor`);

ALTER TABLE `socio`
ADD CONSTRAINT `fk_socio_persona`
    FOREIGN KEY (`id_persona`) REFERENCES `persona` (`id_persona`)
    ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE `bibliotecario`
ADD CONSTRAINT `fk_bibliotecario_persona`
    FOREIGN KEY (`id_persona`) REFERENCES `persona` (`id_persona`)
    ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE `telefono_socio`
ADD CONSTRAINT `fk_telefono_socio_socio`
    FOREIGN KEY (`id_socio`) REFERENCES `socio` (`id_persona`)
    ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE `libro`
ADD CONSTRAINT `fk_libro_editorial`
    FOREIGN KEY (`id_editorial`) REFERENCES `editorial` (`id_editorial`)
    ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE `ejemplar`
ADD CONSTRAINT `fk_ejemplar_libro`
    FOREIGN KEY (`id_libro`) REFERENCES `libro` (`id_libro`)
    ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE `prestamo`
ADD CONSTRAINT `fk_prestamo_socio`
    FOREIGN KEY (`id_socio`) REFERENCES `socio` (`id_persona`)
    ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE `prestamo`
ADD CONSTRAINT `fk_prestamo_ejemplar`
    FOREIGN KEY (`id_ejemplar`) REFERENCES `ejemplar` (`id_ejemplar`)
    ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE `prestamo`
ADD CONSTRAINT `fk_prestamo_bibliotecario`
    FOREIGN KEY (`id_bibliotecario`)
    REFERENCES `bibliotecario` (`id_persona`)
    ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE `libro_autor`
ADD CONSTRAINT `fk_libro_autor_libro`
    FOREIGN KEY (`id_libro`) REFERENCES `libro` (`id_libro`)
    ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE `libro_autor`
ADD CONSTRAINT `fk_libro_autor_autor`
    FOREIGN KEY (`id_autor`) REFERENCES `autor` (`id_autor`)
    ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE prestamo
    ADD CONSTRAINT chk_vencimiento_inicial
    CHECK (fecha_vencimiento_inicial >= fecha_prestamo),
    ADD CONSTRAINT chk_vencimiento_actual
    CHECK (fecha_vencimiento_actual >= fecha_vencimiento_inicial),
    ADD CONSTRAINT chk_fecha_devolucion
    CHECK (
        fecha_devolucion IS NULL
        OR fecha_devolucion >= fecha_prestamo
    );
ALTER TABLE libro_autor
    ADD CONSTRAINT chk_orden_autoria
    CHECK (orden_autoria > 0);