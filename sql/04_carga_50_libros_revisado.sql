-- Carga de 50 libros con títulos ficticios; saltea ISBN y asociaciones ya existentes.
-- Autores y editoriales son los registros reales cargados en los scripts anteriores.
-- ISBN de prueba sintéticos, únicos y con dígito de control ISBN-13 válido; no son asignaciones editoriales reales.
-- Ejecutar después de las cargas de personas, autores y editoriales.
-- Este script presupone que el esquema ya está creado y usa nombres para resolver claves foráneas.
USE biblioteca;

START TRANSACTION;

INSERT IGNORE INTO libro (titulo, isbn, anio_publicacion, id_editorial)
SELECT datos.titulo, datos.isbn, datos.anio_publicacion, e.id_editorial
FROM (
    SELECT 'El jardín de las brújulas dormidas' AS titulo, '9781234560010' AS isbn, 2021 AS anio_publicacion, 'Editorial Sudamericana' AS editorial
    UNION ALL SELECT 'La casa de los mapas invisibles' AS titulo, '9781234560027' AS isbn, 2020 AS anio_publicacion, 'Alfaguara' AS editorial
    UNION ALL SELECT 'Los huéspedes del espejo' AS titulo, '9781234560034' AS isbn, 2019 AS anio_publicacion, 'Emecé Editores' AS editorial
    UNION ALL SELECT 'Canciones para una luna de papel' AS titulo, '9781234560041' AS isbn, 2022 AS anio_publicacion, 'Ediciones Colihue' AS editorial
    UNION ALL SELECT 'El archivo de las mareas' AS titulo, '9781234560058' AS isbn, 2018 AS anio_publicacion, 'Seix Barral' AS editorial
    UNION ALL SELECT 'La ciudad de los nombres perdidos' AS titulo, '9781234560065' AS isbn, 2023 AS anio_publicacion, 'Editorial Anagrama' AS editorial
    UNION ALL SELECT 'Inventario de un invierno azul' AS titulo, '9781234560072' AS isbn, 2021 AS anio_publicacion, 'Penguin Random House Grupo Editorial' AS editorial
    UNION ALL SELECT 'Las voces del patio vacío' AS titulo, '9781234560089' AS isbn, 2024 AS anio_publicacion, 'Editorial Sudamericana' AS editorial
    UNION ALL SELECT 'Una biblioteca bajo la lluvia' AS titulo, '9781234560096' AS isbn, 2022 AS anio_publicacion, 'Alfaguara' AS editorial
    UNION ALL SELECT 'El último tren de la memoria' AS titulo, '9781234560102' AS isbn, 2017 AS anio_publicacion, 'Editorial Losada' AS editorial
    UNION ALL SELECT 'Cuaderno de los días transparentes' AS titulo, '9781234560119' AS isbn, 2020 AS anio_publicacion, 'Siglo XXI Editores' AS editorial
    UNION ALL SELECT 'El río que aprendió a hablar' AS titulo, '9781234560126' AS isbn, 2019 AS anio_publicacion, 'Planeta' AS editorial
    UNION ALL SELECT 'Cartografía de una despedida' AS titulo, '9781234560133' AS isbn, 2021 AS anio_publicacion, 'Alfaguara' AS editorial
    UNION ALL SELECT 'La estación de las camelias negras' AS titulo, '9781234560140' AS isbn, 2023 AS anio_publicacion, 'Penguin Random House Grupo Editorial' AS editorial
    UNION ALL SELECT 'Manual para ordenar las estrellas' AS titulo, '9781234560157' AS isbn, 2018 AS anio_publicacion, 'Fondo de Cultura Económica' AS editorial
    UNION ALL SELECT 'El reloj de arena verde' AS titulo, '9781234560164' AS isbn, 2020 AS anio_publicacion, 'Editorial Anagrama' AS editorial
    UNION ALL SELECT 'Los días que caben en una taza' AS titulo, '9781234560171' AS isbn, 2022 AS anio_publicacion, 'Planeta' AS editorial
    UNION ALL SELECT 'El rumor de las piedras azules' AS titulo, '9781234560188' AS isbn, 2017 AS anio_publicacion, 'Siglo XXI Editores' AS editorial
    UNION ALL SELECT 'La ruta de los faroles' AS titulo, '9781234560195' AS isbn, 2019 AS anio_publicacion, 'Editorial Losada' AS editorial
    UNION ALL SELECT 'Pequeño atlas de la noche' AS titulo, '9781234560201' AS isbn, 2024 AS anio_publicacion, 'Alfaguara' AS editorial
    UNION ALL SELECT 'La habitación de las ventanas altas' AS titulo, '9781234560218' AS isbn, 2021 AS anio_publicacion, 'Editorial Siruela' AS editorial
    UNION ALL SELECT 'El coleccionista de mañanas' AS titulo, '9781234560225' AS isbn, 2018 AS anio_publicacion, 'Alfaguara' AS editorial
    UNION ALL SELECT 'La isla donde termina el mapa' AS titulo, '9781234560232' AS isbn, 2020 AS anio_publicacion, 'Editorial Anagrama' AS editorial
    UNION ALL SELECT 'El puente de los días breves' AS titulo, '9781234560249' AS isbn, 2019 AS anio_publicacion, 'Planeta' AS editorial
    UNION ALL SELECT 'Los jardines de la lluvia roja' AS titulo, '9781234560256' AS isbn, 2017 AS anio_publicacion, 'Editorial Losada' AS editorial
    UNION ALL SELECT 'La última carta de invierno' AS titulo, '9781234560263' AS isbn, 2021 AS anio_publicacion, 'Oxford University Press' AS editorial
    UNION ALL SELECT 'El salón de las decisiones pequeñas' AS titulo, '9781234560270' AS isbn, 2020 AS anio_publicacion, 'Penguin Random House Grupo Editorial' AS editorial
    UNION ALL SELECT 'Las campanas de Copperfield' AS titulo, '9781234560287' AS isbn, 2018 AS anio_publicacion, 'Oxford University Press' AS editorial
    UNION ALL SELECT 'El herbario de la señora Shelley' AS titulo, '9781234560294' AS isbn, 2022 AS anio_publicacion, 'HarperCollins' AS editorial
    UNION ALL SELECT 'Un faro para Virginia' AS titulo, '9781234560300' AS isbn, 2023 AS anio_publicacion, 'Hachette Livre' AS editorial
    UNION ALL SELECT 'La república de los relojes detenidos' AS titulo, '9781234560317' AS isbn, 2019 AS anio_publicacion, 'Scholastic' AS editorial
    UNION ALL SELECT 'El jardín de las voces mecánicas' AS titulo, '9781234560324' AS isbn, 2024 AS anio_publicacion, 'Macmillan Publishers' AS editorial
    UNION ALL SELECT 'El enigma del retrato de invierno' AS titulo, '9781234560331' AS isbn, 2021 AS anio_publicacion, 'HarperCollins' AS editorial
    UNION ALL SELECT 'El caso de la brújula rota' AS titulo, '9781234560348' AS isbn, 2020 AS anio_publicacion, 'Oxford University Press' AS editorial
    UNION ALL SELECT 'Los reinos del viento quieto' AS titulo, '9781234560355' AS isbn, 2018 AS anio_publicacion, 'HarperCollins' AS editorial
    UNION ALL SELECT 'La puerta de la colina azul' AS titulo, '9781234560362' AS isbn, 2022 AS anio_publicacion, 'Macmillan Publishers' AS editorial
    UNION ALL SELECT 'Crónicas del mar interior' AS titulo, '9781234560379' AS isbn, 2023 AS anio_publicacion, 'Hachette Livre' AS editorial
    UNION ALL SELECT 'La escuela de los objetos perdidos' AS titulo, '9781234560386' AS isbn, 2020 AS anio_publicacion, 'Scholastic' AS editorial
    UNION ALL SELECT 'La casa al final del sendero blanco' AS titulo, '9781234560393' AS isbn, 2024 AS anio_publicacion, 'Simon & Schuster' AS editorial
    UNION ALL SELECT 'Los nombres del bosque profundo' AS titulo, '9781234560409' AS isbn, 2019 AS anio_publicacion, 'HarperCollins' AS editorial
    UNION ALL SELECT 'El jardín de las estaciones futuras' AS titulo, '9781234560416' AS isbn, 2021 AS anio_publicacion, 'Macmillan Publishers' AS editorial
    UNION ALL SELECT 'La memoria de las magnolias' AS titulo, '9781234560423' AS isbn, 2018 AS anio_publicacion, 'Simon & Schuster' AS editorial
    UNION ALL SELECT 'Cartas desde el patio amarillo' AS titulo, '9781234560430' AS isbn, 2022 AS anio_publicacion, 'Hachette Livre' AS editorial
    UNION ALL SELECT 'El verano de las páginas azules' AS titulo, '9781234560447' AS isbn, 2020 AS anio_publicacion, 'Penguin Random House Grupo Editorial' AS editorial
    UNION ALL SELECT 'La brújula de los pescadores' AS titulo, '9781234560454' AS isbn, 2017 AS anio_publicacion, 'Editorial Sudamericana' AS editorial
    UNION ALL SELECT 'El hotel de las últimas luces' AS titulo, '9781234560461' AS isbn, 2019 AS anio_publicacion, 'Simon & Schuster' AS editorial
    UNION ALL SELECT 'Las aventuras del señor del río' AS titulo, '9781234560478' AS isbn, 2021 AS anio_publicacion, 'Oxford University Press' AS editorial
    UNION ALL SELECT 'La isla de las mareas quietas' AS titulo, '9781234560485' AS isbn, 2018 AS anio_publicacion, 'Macmillan Publishers' AS editorial
    UNION ALL SELECT 'El retrato que olvidó su nombre' AS titulo, '9781234560492' AS isbn, 2023 AS anio_publicacion, 'Editorial Acme Agency' AS editorial
    UNION ALL SELECT 'El mapa de los pájaros azules' AS titulo, '9781234560508' AS isbn, 2020 AS anio_publicacion, 'HarperCollins' AS editorial
) AS datos
JOIN editorial AS e ON e.nombre = datos.editorial;

-- Vincula cada libro con el autor correspondiente mediante ISBN y nombre.
INSERT IGNORE INTO libro_autor (id_libro, id_autor, orden_autoria)
SELECT l.id_libro, a.id_autor, 1
FROM libro AS l
JOIN (
    SELECT '9781234560010' AS isbn, 'Jorge Luis' AS nombre_autor, 'Borges' AS apellido_autor
    UNION ALL SELECT '9781234560027' AS isbn, 'Julio' AS nombre_autor, 'Cortázar' AS apellido_autor
    UNION ALL SELECT '9781234560034' AS isbn, 'Silvina' AS nombre_autor, 'Ocampo' AS apellido_autor
    UNION ALL SELECT '9781234560041' AS isbn, 'María Elena' AS nombre_autor, 'Walsh' AS apellido_autor
    UNION ALL SELECT '9781234560058' AS isbn, 'Juan José' AS nombre_autor, 'Saer' AS apellido_autor
    UNION ALL SELECT '9781234560065' AS isbn, 'Ricardo' AS nombre_autor, 'Piglia' AS apellido_autor
    UNION ALL SELECT '9781234560072' AS isbn, 'César' AS nombre_autor, 'Aira' AS apellido_autor
    UNION ALL SELECT '9781234560089' AS isbn, 'Samanta' AS nombre_autor, 'Schweblin' AS apellido_autor
    UNION ALL SELECT '9781234560096' AS isbn, 'Claudia' AS nombre_autor, 'Piñeiro' AS apellido_autor
    UNION ALL SELECT '9781234560102' AS isbn, 'Ernesto' AS nombre_autor, 'Sabato' AS apellido_autor
    UNION ALL SELECT '9781234560119' AS isbn, 'Alejandra' AS nombre_autor, 'Pizarnik' AS apellido_autor
    UNION ALL SELECT '9781234560126' AS isbn, 'Gabriel García' AS nombre_autor, 'Márquez' AS apellido_autor
    UNION ALL SELECT '9781234560133' AS isbn, 'Mario' AS nombre_autor, 'Vargas Llosa' AS apellido_autor
    UNION ALL SELECT '9781234560140' AS isbn, 'Isabel' AS nombre_autor, 'Allende' AS apellido_autor
    UNION ALL SELECT '9781234560157' AS isbn, 'Pablo' AS nombre_autor, 'Neruda' AS apellido_autor
    UNION ALL SELECT '9781234560164' AS isbn, 'Roberto' AS nombre_autor, 'Bolaño' AS apellido_autor
    UNION ALL SELECT '9781234560171' AS isbn, 'Laura' AS nombre_autor, 'Esquivel' AS apellido_autor
    UNION ALL SELECT '9781234560188' AS isbn, 'Augusto' AS nombre_autor, 'Roa Bastos' AS apellido_autor
    UNION ALL SELECT '9781234560195' AS isbn, 'Eduardo' AS nombre_autor, 'Galeano' AS apellido_autor
    UNION ALL SELECT '9781234560201' AS isbn, 'Mario' AS nombre_autor, 'Benedetti' AS apellido_autor
    UNION ALL SELECT '9781234560218' AS isbn, 'Clarice' AS nombre_autor, 'Lispector' AS apellido_autor
    UNION ALL SELECT '9781234560225' AS isbn, 'José' AS nombre_autor, 'Saramago' AS apellido_autor
    UNION ALL SELECT '9781234560232' AS isbn, 'Fernando' AS nombre_autor, 'Pessoa' AS apellido_autor
    UNION ALL SELECT '9781234560249' AS isbn, 'Miguel' AS nombre_autor, 'de Cervantes' AS apellido_autor
    UNION ALL SELECT '9781234560256' AS isbn, 'Federico García' AS nombre_autor, 'Lorca' AS apellido_autor
    UNION ALL SELECT '9781234560263' AS isbn, 'William' AS nombre_autor, 'Shakespeare' AS apellido_autor
    UNION ALL SELECT '9781234560270' AS isbn, 'Jane' AS nombre_autor, 'Austen' AS apellido_autor
    UNION ALL SELECT '9781234560287' AS isbn, 'Charles' AS nombre_autor, 'Dickens' AS apellido_autor
    UNION ALL SELECT '9781234560294' AS isbn, 'Mary' AS nombre_autor, 'Shelley' AS apellido_autor
    UNION ALL SELECT '9781234560300' AS isbn, 'Virginia' AS nombre_autor, 'Woolf' AS apellido_autor
    UNION ALL SELECT '9781234560317' AS isbn, 'George' AS nombre_autor, 'Orwell' AS apellido_autor
    UNION ALL SELECT '9781234560324' AS isbn, 'Aldous' AS nombre_autor, 'Huxley' AS apellido_autor
    UNION ALL SELECT '9781234560331' AS isbn, 'Agatha' AS nombre_autor, 'Christie' AS apellido_autor
    UNION ALL SELECT '9781234560348' AS isbn, 'Arthur Conan' AS nombre_autor, 'Doyle' AS apellido_autor
    UNION ALL SELECT '9781234560355' AS isbn, 'J. R. R.' AS nombre_autor, 'Tolkien' AS apellido_autor
    UNION ALL SELECT '9781234560362' AS isbn, 'C. S.' AS nombre_autor, 'Lewis' AS apellido_autor
    UNION ALL SELECT '9781234560379' AS isbn, 'George R. R.' AS nombre_autor, 'Martin' AS apellido_autor
    UNION ALL SELECT '9781234560386' AS isbn, 'J. K.' AS nombre_autor, 'Rowling' AS apellido_autor
    UNION ALL SELECT '9781234560393' AS isbn, 'Stephen' AS nombre_autor, 'King' AS apellido_autor
    UNION ALL SELECT '9781234560409' AS isbn, 'Ursula K. Le' AS nombre_autor, 'Guin' AS apellido_autor
    UNION ALL SELECT '9781234560416' AS isbn, 'Margaret' AS nombre_autor, 'Atwood' AS apellido_autor
    UNION ALL SELECT '9781234560423' AS isbn, 'Toni' AS nombre_autor, 'Morrison' AS apellido_autor
    UNION ALL SELECT '9781234560430' AS isbn, 'Maya' AS nombre_autor, 'Angelou' AS apellido_autor
    UNION ALL SELECT '9781234560447' AS isbn, 'Harper' AS nombre_autor, 'Lee' AS apellido_autor
    UNION ALL SELECT '9781234560454' AS isbn, 'Ernest' AS nombre_autor, 'Hemingway' AS apellido_autor
    UNION ALL SELECT '9781234560461' AS isbn, 'F. Scott' AS nombre_autor, 'Fitzgerald' AS apellido_autor
    UNION ALL SELECT '9781234560478' AS isbn, 'Mark' AS nombre_autor, 'Twain' AS apellido_autor
    UNION ALL SELECT '9781234560485' AS isbn, 'Herman' AS nombre_autor, 'Melville' AS apellido_autor
    UNION ALL SELECT '9781234560492' AS isbn, 'Edgar Allan' AS nombre_autor, 'Poe' AS apellido_autor
    UNION ALL SELECT '9781234560508' AS isbn, 'Ray' AS nombre_autor, 'Bradbury' AS apellido_autor
) AS asignacion ON asignacion.isbn = l.isbn
JOIN autor AS a
  ON a.nombre = asignacion.nombre_autor
 AND a.apellido = asignacion.apellido_autor;

-- Verificación: deben aparecer 50 libros asociados a este set de ISBN.
SELECT COUNT(*) AS libros_cargados
FROM libro
WHERE isbn BETWEEN '9781234560010' AND '9781234560508';

-- Verificación de las asociaciones: deben existir 50 relaciones libro-autor para este set.
SELECT COUNT(*) AS asociaciones_libro_autor
FROM libro_autor AS la
JOIN libro AS l ON l.id_libro = la.id_libro
WHERE l.isbn BETWEEN '9781234560010' AND '9781234560508';

COMMIT;
