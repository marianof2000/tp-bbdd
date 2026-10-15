-- Carga de 30 editoriales reales para la base biblioteca.
-- Ejecutar una sola vez para evitar duplicados.
USE biblioteca;

START TRANSACTION;

INSERT INTO editorial (nombre) VALUES
    ('Editorial Sudamericana'),
    ('Emecé Editores'),
    ('Alfaguara'),
    ('Penguin Random House Grupo Editorial'),
    ('Planeta'),
    ('Editorial Anagrama'),
    ('Seix Barral'),
    ('Siglo XXI Editores'),
    ('Fondo de Cultura Económica'),
    ('Editorial Losada'),
    ('Eudeba'),
    ('Ediciones Colihue'),
    ('Editorial Acme Agency'),
    ('Editorial Universitaria de Buenos Aires'),
    ('Ediciones de la Flor'),
    ('Editorial Atlántida'),
    ('Editorial Kapelusz'),
    ('Ediciones Paidós'),
    ('Editorial Tusquets'),
    ('Editorial Siruela'),
    ('Editorial Anaya'),
    ('Editorial SM'),
    ('Editorial Kalandraka'),
    ('Editorial Salamandra'),
    ('HarperCollins'),
    ('Simon & Schuster'),
    ('Macmillan Publishers'),
    ('Hachette Livre'),
    ('Scholastic'),
    ('Oxford University Press');

-- Verificación: debe devolver 30 si la tabla estaba vacía antes de la carga.
SELECT COUNT(*) AS editoriales_cargadas FROM editorial;

COMMIT;
