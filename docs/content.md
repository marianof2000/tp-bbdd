## TFI Fundamentos de Bases de Datos

TFI Fundamentos de Bases de Datos.   
Parte 1 · Selección del proyecto e identificación del problema. .3   
1.1. Caso de negocio. 3   
1.2. Entidades, propiedades y tipos de datos. 3   
1.3. Justificación de los tipos de datos. .4   
1.4. Relaciones identificadas. .4   
1.5. Reglas del negocio para dejar asentadas. .. 5   
1.6 Preguntas de negocio. . 5   
Parte 2 · Modelado en DrawDB con asistencia de IA. . 7   
2.1. Objetivo. 7   
2.2. Entidades del modelo. .7   
2.3. Relaciones, cardinalidad y participación. 7   
2.4. Prompts utilizados para el modelado. 8   
Prompt 1 · Crear las entidades y sus atributos. . 8   
Prompt 2 · Incorporar las relaciones. . 9   
Prompt 3 · Revisar críticamente el diagrama. . 9   
2.5. Revisión humana y decisiones. .10   
2.6. Diagrama del modelo inicial. 10   
Parte 3 - Refactorización del modelo. . 12   
3.1. Revisión de claves primarias, candidatas y alternativas. 12   
3.2. Revisión y resolución de la jerarquía. 13   
3.2.1 Estructura propuesta. . 14   
3.2.2 Restricciones de la jerarquía. .14   
3.2.3 Relaciones con el resto del modelo. 14   
3.2.4 Representación en DrawDB. ..14   
3.3. Normalización del modelo hasta tercera forma normal. ..15   
3.3.1. Primera forma normal. ..15   
3.3.2. Segunda forma normal. .15   
3.3.3. Tercera forma normal. 16   
3.3.4. Conservación de información histórica.. 17   
3.4. Reglas de integridad y borrado. 17   
3.4.1. Reglas de borrado.. ..17   
3.4.2. Otras reglas de integridad. . 18   
3.5. Auditoría del modelo con IA y decisiones adoptadas. ..19   
3.5.1. Prompt de auditoría. ..19   
3.5.2. Hallazgos y revisión humana. 19   
3.6. Diagrama definitivo y síntesis de las decisiones de diseño. 20   
3.6.1. Esquema de referencia para el diagrama. 20   
3.6.2. Síntesis de las decisiones. . 22   
Parte 4 · Creación de la base en DBeaver. 23   
4.1. Objetivo. . 23   
4.2. Preparación del script.. .23   
4.3. Restricciones e integridad.. .23   
4.4. Orden y ejecución en DBeaver. 24   
4.5. Verificación de la estructura. . 24   
4.6. Uso de IA y correcciones.. 25   
4.7. Resultado y controles pendientes. 26   
Parte 5 · Carga de datos de prueba y consultas de negocio.. . 29   
5.1 Observación de verificación. . 30   
5.2 Consultas a la base de datos. .30   
Parte 6 · Consultas de negocio y análisis de resultados. 33   
6.1. Relación entre las preguntas iniciales y las consultas de prueba. .33   
6.2. Informes que relacionan tres o más tablas. 34   
6.3. Verificación de resultados. 37   
6.4. Análisis del plan de ejecución y optimización. 38   
6.5. Comparación de consultas propias y asistidas por IA.. ..39   
Parte 7 · Integración de la base de datos con Python e inteligencia artificial.. . 41   
7.1. Integración mediante MCP. .41   
7.2. Conexión de Python con MySQL y ejecución de consultas.. .42   
7.3. Consultas parametrizadas e inyección SQL 42   
7.4. Interfaz gráfica de gestión. .43   
7.5. Usuarios, roles y permisos.. .43   
7.6. Resultado de la integración. .43   
Parte 8 · Resumen y conclusión general del trabajo. 44   
8.1. Resumen del proyecto. 44   
8.2. La inteligencia artificial como herramienta de apoyo.. 44   
8.3. Conclusión general.. ..44

## Parte 1 · Selección del proyecto e identificación del problema

## 1.1. Caso de negocio

El proyecto consiste en diseñar una base de datos para la biblioteca. La biblioteca posee libros registrados con ninguno, uno o más ejemplares físicos. Por lo que puede registrarse un libro antes de incorporar sus copias a la biblioteca.

También registra a sus socios y administra los préstamos. Un bibliotecario registra cada préstamo y su devolución.

El problema que se busca resolver es la dispersión de la información sobre el catálogo, los ejemplares y la circulación de libros. La base de datos deberá permitir identificar qué ejemplar se prestó, a quién, cuándo debe devolverse y si ya fue devuelto, además de consultar autores y editoriales.

Cuando un libro ingresa a la biblioteca, se registra su información bibliográfica, editorial y autores. Cada copia física se registra como un ejemplar con un código de inventario único. Los socios pueden solicitar ejemplares disponibles; un bibliotecario registra cada préstamo, su fecha y su vencimiento. Al devolver el ejemplar, se registra la fecha de devolución. Si se renueva el plazo, se actualiza el vencimiento actual y se conserva el vencimiento inicial. Un ejemplar no puede ser prestado simultáneamente a dos socios.

Alcance: cada préstamo corresponde a un ejemplar. Si un socio retira tres ejemplares al mismo tiempo, se registran tres préstamos. Esta regla mantiene sencillo el modelo inicial.

1.2. Entidades, propiedades y tipos de datos
<table><tr><td colspan="1" rowspan="1">Entidad</td><td colspan="1" rowspan="1">Propiedades propuestas</td><td colspan="1" rowspan="1">Clave primaria (PK) y motivo</td></tr><tr><td colspan="1" rowspan="1">Socio</td><td colspan="1" rowspan="1">id_socio INT, nombre VARCHAR(80), apellidoVARCHAR(80), documento VARCHÀR(20), emailVARCHAR(254), fecha_alta DATE</td><td colspan="1" rowspan="1">id_socio: identifica de formaestable al socio aunque cambiesu correo o se corrija sudocumento.</td></tr><tr><td colspan="1" rowspan="1">Bibliotecario</td><td colspan="1" rowspan="1">id_bibliotecario INT, nombre VARCHAR(80), apellidoVARCHAR(80), legajo VARCHAR(30)</td><td colspan="1" rowspan="1">id_bibliotecario: mantiene laidentidad del empleado aunquecambie su legajo.</td></tr><tr><td colspan="1" rowspan="1">Editorial</td><td colspan="1" rowspan="1">id_editorial INT, nombre VARCHAR(120)</td><td colspan="1" rowspan="1">id_editorial: distingue editorialesaunque   existannombressimilares   0  cambiendedenominación.</td></tr><tr><td colspan="1" rowspan="1">Autor</td><td colspan="1" rowspan="1">id_autor INT, nombre VARCHAR(80), apellidoVARCHAR(80)</td><td colspan="1" rowspan="1">id_autor: distingue personasque pueden compartir nombre yapellido.</td></tr><tr><td colspan="1" rowspan="1">Libro</td><td colspan="1" rowspan="1">id_libro   INT,    titulo   VARCHAR(200),   isbnVARCHAR(17),     anio_publicacion    SMALLINT,id_editorial INT</td><td colspan="1" rowspan="1">id_libro: identifica el registrobibliográfico;el  ISBN esobligatorio.</td></tr><tr><td colspan="1" rowspan="1">Ejemplar</td><td colspan="1" rowspan="1">id_ejemplar INT, id_libro INT, codigo_inventarioVARCHAR(40), fecha_incorporacion DATE</td><td colspan="1" rowspan="1">id_ejemplar: identifica una copiafísica      específica.      Dos</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">ejemplares del mismo librotienen identificadores distintos.</td></tr><tr><td colspan="1" rowspan="1">Prestamo</td><td colspan="1" rowspan="1">id_prestamo INT, id_socio INT, id_ejemplar INT,id bibliotecarioINT,fecha_prestamo   DATE,fecha vencimiento inicial                       DATE,fecha_vencimiento_actual DATE, fecha_devolucionDATE</td><td colspan="1" rowspan="1">id_prestamo:distinguelassucesivas ocasiones en que sepresta un mismo ejemplar.</td></tr><tr><td colspan="1" rowspan="1">LibroAutor</td><td colspan="1" rowspan="1">id_libro INT, id_autor INT, orden_autoria SMALLINT</td><td colspan="1" rowspan="1">PK    compuesta    (id_libro,id_autor): evita asociar dosveces al mismo autor con elmismo libro.</td></tr><tr><td colspan="1" rowspan="1">TelefonoSocio</td><td colspan="1" rowspan="1">id_socioINT,   numero   VARCHAR(25),  tipoVARCHAR(20)</td><td colspan="1" rowspan="1">PK   compuesta   (id_socio,numero):permite    variosteléfonos por socio sin repetir elmismo número para ese socio.</td></tr></table>

Los campos id\_... que apuntan a otra entidad serán claves foráneas (FK). Por ejemplo, Ejemplar.id\_libro referencia a Libro.id\_libro.

## 1.3. Justificación de los tipos de datos

● INT: identificadores enteros positivos; no representan cantidades del negocio.

VARCHAR: textos de longitud variable. El documento, el ISBN, el legajo, el código de inventario y el teléfono se almacenan como texto porque son identificadores: no tiene sentido sumarlos y pueden contener ceros iniciales, letras o separadores.

● DATE: fechas para las que, en este alcance, no es necesario registrar la hora.

SMALLINT: valores enteros no negativos y acotados, como el año de publicación y el orden de autoría.

fecha\_devolucion podrá quedar vacía mientras el ejemplar no haya sido devuelto. El dato histórico será fecha\_vencimiento\_inicial: si se concede una renovación, se modifica fecha\_vencimiento\_actual, pero se conserva la fecha acordada originalmente.

## 1.4. Relaciones identificadas

La participación se expresa como 0..N (cero o muchos), 1..N (uno o muchos) y 1..1 (exactamente uno).

<table><tr><td colspan="1" rowspan="1">Relación expresadacon verbo</td><td colspan="1" rowspan="1">Cardinalidad y participación</td></tr><tr><td colspan="1" rowspan="1">Una editorial publicalibros.</td><td colspan="1" rowspan="1">Una editorial puede publicar 0..N libros registrados; cada librocorresponde a 1..1 editorial.</td></tr><tr><td colspan="1" rowspan="1">Un    libro    poseeejemplares.</td><td colspan="1" rowspan="1">Un libro puede tener 0..N ejemplares registrados; cada ejemplarcorresponde a 1..1 libro.</td></tr><tr><td colspan="1" rowspan="1">Un autor escribelibros.</td><td colspan="1" rowspan="1">Un autor puede estar asociado a 0..N libros; un libro tiene 1..Nautores. Es una relación N:M resuelta mediante LibroAutor, queademás registra el orden de autoría.</td></tr><tr><td colspan="1" rowspan="1">Un socio  solicitapréstamos.</td><td colspan="1" rowspan="1">Un socio puede realizar 0..N préstamos; cada préstamocorresponde a 1..1 socio.</td></tr><tr><td colspan="1" rowspan="1">Un        bibliotecarioregistra préstamos.</td><td colspan="1" rowspan="1">Un bibliotecario puede registrar 0..N préstamos; cada préstamoes registrado por 1..1 bibliotecario.</td></tr><tr><td colspan="1" rowspan="1">Un ejemplar participaen préstamos.</td><td colspan="1" rowspan="1">Un ejemplar puede tener 0..N préstamos a lo largo del tiempo;cada préstamo corresponde a 1..1 ejemplar.</td></tr><tr><td colspan="1" rowspan="1">Un socio registrateléfonos.</td><td colspan="1" rowspan="1">Un socio puede registrar 0..N teléfonos; cada registro de teléfonopertenece a 1..1 socio.</td></tr></table>

## 1.5. Reglas del negocio para dejar asentadas

1. codigo\_inventario debe ser único: identifica cada copia física dentro de la biblioteca.

2. Un mismo ejemplar no puede tener dos préstamos sin devolver al mismo tiempo, aunque sí puede acumular muchos préstamos a lo largo de su historia y debe estar operativo.

3. Un libro debe tener al menos un autor para considerarse completo en el catálogo. Esa exigencia deberá controlarse al cargar los datos.

4. La disponibilidad de un ejemplar se obtiene de sus préstamos sin fecha\_devolucion; no hace falta duplicarla en un campo que pueda quedar desactualizado.

5. Los teléfonos múltiples se separan en TelefonoSocio para evitar columnas repetidas como telefono\_1 y telefono\_2.

## 1.6 Preguntas de negocio

Las siguientes preguntas permiten verificar que el modelo almacena la información necesaria para gestionar el catálogo, los ejemplares, los socios y la circulación de libros.

1. ¿Qué libros integran el catálogo y quiénes son sus autores, en el orden de autoría registrado?

2. ¿Qué libros pertenecen a una editorial determinada?

3. ¿Cuántos ejemplares tiene registrados la biblioteca de cada libro?

4. ¿Qué ejemplares están disponibles para prestar, considerando su estado y la ausencia de préstamos pendientes?

5. ¿Qué ejemplares se encuentran en reparación y a qué libros corresponden?

6. ¿Qué socios tienen préstamos pendientes de devolución?

7. ¿Qué préstamos están vencidos y pendientes de devolución a la fecha de consulta?

8. ¿Qué préstamos pendientes vencen dentro de los próximos siete días?

9. ¿Cuál es el historial de préstamos de un socio determinado?

10. ¿Cuál es el historial de préstamos de un ejemplar determinado?

11. $\dot { \iota } \mathsf { Q u } \dot { \epsilon }$ préstamos registró un bibliotecario durante un período determinado?

12. $\dot { c }$ Cuántos préstamos se registraron por mes durante un año determinado?

13. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ libros fueron los más prestados durante un período determinado?

14. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ socios realizaron la mayor cantidad de préstamos durante un período determinado?

15. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ socios nunca realizaron un préstamo?

16. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ libros con ejemplares registrados nunca fueron prestados?

17. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ préstamos se devolvieron después de su fecha de vencimiento vigente y cuántos días de atraso tuvieron?

18. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ préstamos tienen una fecha de vencimiento actual posterior a la inicial, indicando una extensión del plazo?

19. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ personas están registradas simultáneamente como socios y bibliotecarios?

20. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ socios no tienen ningún teléfono de contacto registrado?

## Parte 2 · Modelado en DrawDB con asistencia de IA

## 2.1. Objetivo

A partir del caso de la biblioteca definido en la Parte 1, se construye en DrawDB un diagrama que represente las entidades, sus atributos y las relaciones del negocio. En esta etapa se verifica especialmente qué representa cada entidad, cómo se vincula con las demás y cuántas instancias pueden participar en cada relación.

La Clase 2 propone trabajar en este orden: entidades y atributos, relaciones con cardinalidad y participación, y revisión del modelo con IA. El SQL exportado y su ejecución corresponden a una etapa posterior.

## 2.2. Entidades del modelo

El diagrama debe contener exactamente estas nueve entidades:
<table><tr><td rowspan=1 colspan=1>Entidad</td><td rowspan=1 colspan=1>Significado e identificador</td></tr><tr><td rowspan=1 colspan=1>socio</td><td rowspan=1 colspan=1>Persona que puede solicitar préstamos. Identificador: id_socio.</td></tr><tr><td rowspan=1 colspan=1>telefono_socio</td><td rowspan=1 colspan=1>Número de contacto informado por un socio. Identificador:id_telefono_socio.</td></tr><tr><td rowspan=1 colspan=1>bibliotecario</td><td rowspan=1 colspan=1>Persona que registra el préstamo. Identificador: id_bibliotecario.</td></tr><tr><td rowspan=1 colspan=1>editorial</td><td rowspan=1 colspan=1>Editorial que publica libros. Identificador: id_editorial.</td></tr><tr><td rowspan=1 colspan=1>autor</td><td rowspan=1 colspan=1>Persona autora de libros. Identificador: id_autor.</td></tr><tr><td rowspan=1 colspan=1>libro</td><td rowspan=1 colspan=1>Registro bibliográfico, independiente de sus copias físicas.Identificador: id_libro.</td></tr><tr><td rowspan=1 colspan=1>libro_autor</td><td rowspan=1 colspan=1>Asociación entre un libro y un autor; guarda orden_autoria.Identificador compuesto: id_libro e id_autor.</td></tr><tr><td rowspan=1 colspan=1>ejemplar</td><td rowspan=1 colspan=1>Copia física identificada por un código de inventario. Identificador:id_ejemplar.</td></tr><tr><td rowspan=1 colspan=1>prestamo</td><td rowspan=1 colspan=1>Entrega de un ejemplar a un socio. Identificador: id_prestamo.</td></tr></table>

libro\_autor resuelve la relación N:M: un libro puede tener varios autores y un autor puede participar en varios libros. Su atributo propio, orden\_autoria, expresa la posición que ocupa un autor en un libro determinado.

## 2.3. Relaciones, cardinalidad y participación

<table><tr><td>Relación</td><td>Lectura del negocio</td></tr><tr><td></td><td></td></tr><tr><td colspan="1" rowspan="1">socio          registratelefono_socio</td><td colspan="1" rowspan="1">Un socio puede registrar 0..N teléfonos. Cada teléfonoregistrado pertenece a 1..1 socio.</td></tr><tr><td colspan="1" rowspan="1">editorial — publica — libro</td><td colspan="1" rowspan="1">Una editorial puede tener 0..N libros registrados. Cada libropertenece a 1..1 editorial.</td></tr><tr><td colspan="1" rowspan="1">libro — posee — ejemplar</td><td colspan="1" rowspan="1">Un libro puede tener 0..N ejemplares registrados. Cadaejemplar corresponde a 1..1 libro.</td></tr><tr><td colspan="1" rowspan="1">libro — tiene — libro_autor</td><td colspan="1" rowspan="1">Un libro debe asociarse con 1..N autores según la regla delnegocio. Cada fila de libro_autor corresponde a 1..1 libro.</td></tr><tr><td colspan="1" rowspan="1">autor — participa enlibro_autor</td><td colspan="1" rowspan="1">Un autor puede asociarse con 0..N libros. Cada fila delibro_autor corresponde a 1..1 autor.</td></tr><tr><td colspan="1" rowspan="1">socio           realizaprestamo</td><td colspan="1" rowspan="1">Un socio puede realizar 0..N préstamos. Cada préstamocorresponde a 1..1 socio.</td></tr><tr><td colspan="1" rowspan="1">ejemplar — participa en —prestamo</td><td colspan="1" rowspan="1">Un ejemplar puede tener 0..N préstamos a lo largo deltiempo. Cada préstamo corresponde a 1..1 ejemplar.</td></tr><tr><td colspan="1" rowspan="1">bibliotecario — registra —prestamo</td><td colspan="1" rowspan="1">Un bibliotecario puede registrar 0..N préstamos. Cadapréstamo es registrado por 1..1 bibliotecario.</td></tr></table>

La relación entre ejemplar y prestamo describe el historial: que un ejemplar tenga muchos préstamos no significa que pueda estar prestado a varias personas al mismo tiempo.

## 2.4. Prompts utilizados para el modelado

## Prompt 1 · Crear las entidades y sus atributos

Objetivo: obtener las nueve entidades del diseño acordado, sin permitir que la IA amplíe el alcance.

Actuá como especialista en modelado de datos. Sobre el proyecto de biblioteca abierto en DrawDB, representá exactamente las siguientes nueve entidades, con los atributos indicados. No agregues otras entidades ni relaciones en esta etapa.

socio: id\_socio, nombre, apellido, documento, email, fecha\_alta.

telefono\_socio: id\_telefono\_socio, id\_socio, numero, tipo.

bibliotecario: id\_bibliotecario, nombre, apellido, legajo.

editorial: id\_editorial, nombre.

autor: id\_autor, nombre, apellido.

libro: id\_libro, titulo, isbn, anio\_publicacion, id\_editorial.

libro\_autor: id\_libro, id\_autor, orden\_autoria. Su identificador es la combinación de id\_libro e id\_autor. orden\_autoria es un atributo propio de la asociación.

ejemplar: id\_ejemplar, id\_libro, codigo\_inventario, fecha\_incorporacion, estado.

prestamo: id\_prestamo, id\_socio, id\_ejemplar, id\_bibliotecario, fecha\_prestamo, fecha\_vencimiento\_inicial, fecha\_vencimiento\_actual, fecha\_devolucion.

Contexto del negocio:

\- Un libro describe una obra; un ejemplar es una copia física.

\- Cada préstamo corresponde a un único ejemplar.

\- No hay bajas, multas, pagos ni historial de renovaciones.

\- Los ejemplares pueden estar operativos o en reparación.

\- Se conserva el vencimiento inicial y el actual.

Verificá que el resultado tenga exactamente nueve entidades. Si encontrás una ambigüedad, informala; no cambies el alcance por tu cuenta.

## Prompt 2 · Incorporar las relaciones

Objetivo: vincular las entidades ya dibujadas y representar cardinalidad y participación.

Sobre el diagrama de nueve entidades de la biblioteca que ya está abierto en DrawDB, incorporá únicamente estas ocho relaciones:

1. socio registra telefono\_socio: socio 0..N; cada telefono\_socio pertenece a 1..1 socio.

2. editorial publica libro: editorial 0..N; cada libro pertenece a 1..1 editorial.

3. libro posee ejemplar: libro 0..N; cada ejemplar corresponde a 1..1 libro.

4. libro tiene libro\_autor: según el negocio, libro 1..N asociaciones de autor; cada fila de libro\_autor corresponde a 1..1 libro.

5. autor participa en libro\_autor: autor 0..N asociaciones con libros; cada fila de libro\_autor corresponde a 1..1 autor.

6. socio realiza prestamo: socio 0..N; cada prestamo corresponde a 1..1 socio.

7. ejemplar participa en prestamo: ejemplar 0..N préstamos históricos; cada prestamo corresponde a 1..1 ejemplar.

8. bibliotecario registra prestamo: bibliotecario 0..N; cada prestamo corresponde a   
1..1 bibliotecario.

Mostrá las relaciones y sus cardinalidades en el diagrama.

Mantené las nueve entidades y todos sus atributos sin cambios.

No agregues relaciones directas entre libro y autor: la relación N:M se representa mediante libro\_autor.

Si la herramienta no puede mostrar alguno de los mínimos de participación, indicá cuál quedó documentado fuera del dibujo. Al finalizar, enumerá las ocho relaciones que efectivamente creaste.

## Prompt 3 · Revisar críticamente el diagrama

Objetivo: detectar problemas antes de dar por terminado el modelo. La revisión no debe modificarlo automáticamente.

Actuá como revisor senior de modelos de datos. Revisá el diagrama de la biblioteca actualmente abierto en DrawDB. No lo modifiques.

Contrastalo con estas reglas:

\- Debe haber exactamente nueve entidades y ocho relaciones.

\- Cada entidad tiene el identificador definido.

\- libro y ejemplar son entidades diferentes.

\- libro\_autor resuelve la relación N:M y tiene el atributo propio orden\_autoria.

\- Cada relación expresa un verbo, cardinalidad y participación.

\- Un préstamo corresponde a un solo ejemplar.

\- Un libro tiene editorial e ISBN.

\- No se gestionan bajas, multas, pagos ni historial de renovaciones.

\- Un ejemplar en reparación no puede prestarse.

\- Un ejemplar puede tener muchos préstamos históricos, pero no dos préstamos pendientes de devolución al mismo tiempo.

Respondé en cinco secciones:

1. Entidades o atributos faltantes o sobrantes.

2. Relaciones incorrectas, faltantes o sobrantes.

3. Cardinalidades y participaciones dudosas, con explicación.

4. Datos redundantes y reglas que el diagrama no puede garantizar por sí solo.

## 2.5. Revisión humana y decisiones

La respuesta de la IA debe contrastarse con la descripción del negocio. Para este caso, las decisiones que deben conservarse son:

● libro y ejemplar representan conceptos distintos.

● libro\_autor resuelve la N:M y conserva orden\_autoria.

● No se agregan procesos de bajas, multas ni pagos.

● La disponibilidad de un ejemplar no se confunde con su estado físico: debe estar operativo y no tener un préstamo pendiente.

El mínimo de un autor por libro es una regla del negocio. La relación dibujada puede expresarla conceptualmente, pero las claves foráneas por sí solas no aseguran que ya exista una fila en libro\_autor.

● Impedir préstamos simultáneos de un ejemplar y préstamos de ejemplares en reparación requerirá controles adicionales al implementar el sistema.

## 2.6. Diagrama del modelo inicial

Modelo inicial de la biblioteca, con entidades, atributos y relaciones. La relación N:M entre libros y autores se resuelve mediante LIBRO\_AUTOR

![](images/01a6d152e67749ae041ac79837875fb2ea73dd308c6abeea0f1bcecd30f80e85.jpg)

## Parte 3 - Refactorización del modelo

## 3.1. Revisión de claves primarias, candidatas y alternativas

Se revisan las claves del modelo según los cinco criterios desarrollados en la Clase 3: unicidad garantizada, presencia obligatoria, estabilidad en el tiempo, representación corta y simple, y ausencia de significado de negocio.

Se adoptan identificadores numéricos subrogados de tipo INT, generados automáticamente. Los datos naturales que deben ser únicos se conservan como atributos y se protegen mediante restricciones de unicidad.

SOCIO y BIBLIOTECARIO constituyen una excepción a la generación de identificadores independientes: utilizan la clave de PERSONA como PK y FK, porque representan roles de una misma identidad.

<table><tr><td colspan="1" rowspan="1">Entidad</td><td colspan="1" rowspan="1">Clave         primariaadoptada</td><td colspan="1" rowspan="1">Claves alternativas orestricciones         deunicidad</td><td colspan="1" rowspan="1">Justificación</td></tr><tr><td colspan="1" rowspan="1">PERSONA</td><td colspan="1" rowspan="1">id_persona</td><td colspan="1" rowspan="1">documento obligatorio yúnico</td><td colspan="1" rowspan="1">El identificador permaneceestable aunque se corrijan losdatos     personales.    Eldocumento permite controlarregistros duplicados.</td></tr><tr><td colspan="1" rowspan="1">SOCIO</td><td colspan="1" rowspan="1">id_persona,  tambiénFK hacia PERSONA</td><td colspan="1" rowspan="1">No se identifica otraclave candidata</td><td colspan="1" rowspan="1">Permite una sola afiliaciónpor persona y conserva laidentidad de la entidadgeneral.</td></tr><tr><td colspan="1" rowspan="1">BIBLIOTECARIO</td><td colspan="1" rowspan="1">id_persona,  tambiénFK hacia PERSONA</td><td colspan="1" rowspan="1">legajo  obligatorio  yúnico</td><td colspan="1" rowspan="1">La identidad se comparte conPERSONA;    el    legajoidentifica ai empleado dentrode la institución.</td></tr><tr><td colspan="1" rowspan="1">EDITORIAL</td><td colspan="1" rowspan="1">id_editorial</td><td colspan="1" rowspan="1">No se identifica otraclave candidata</td><td colspan="1" rowspan="1">El nombre no garantizaunicidad y puede cambiar.</td></tr><tr><td colspan="1" rowspan="1">AUTOR</td><td colspan="1" rowspan="1">id_autor</td><td colspan="1" rowspan="1">No se identifica otraclave candidata</td><td colspan="1" rowspan="1">Dos     autores     puedencompartir nombre y apellido.</td></tr><tr><td colspan="1" rowspan="1">LIBRO</td><td colspan="1" rowspan="1">id_libro</td><td colspan="1" rowspan="1">ISBN único cuando estáinformado</td><td colspan="1" rowspan="1">El registro bibliográfico debepoder identificarse y debetener ISBN.</td></tr><tr><td colspan="1" rowspan="1">EJEMPLAR</td><td colspan="1" rowspan="1">id_ejemplar</td><td colspan="1" rowspan="1">codigo_inventarioobligatorio y único</td><td colspan="1" rowspan="1">El identificador distingue cadacopia física; el código deinventario   conserva   sufunción   dentro   de   labiblioteca.</td></tr><tr><td colspan="1" rowspan="1">PRÉSTAMO</td><td colspan="1" rowspan="1">id_prestamo</td><td colspan="1" rowspan="1">No se identifica otraclave candidata</td><td colspan="1" rowspan="1">Un mismo socio puede recibirelmismo ejemplar  endistintas ocasiones.</td></tr><tr><td colspan="1" rowspan="1">LIBRO_AUTOR</td><td colspan="1" rowspan="1">id_libro_autor</td><td colspan="1" rowspan="1">UNIQUE       (id_libro,id_autor),       ambosobligatorios</td><td colspan="1" rowspan="1">La clave subrogada simplificala      identificación;      lacombinación impide repetir la</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">asociación entre un libro y unautor.</td></tr><tr><td colspan="1" rowspan="1">TELÉFONO_SOCIO</td><td colspan="1" rowspan="1">id_telefono_socio</td><td colspan="1" rowspan="1">UNIQUE      (id_socio,numero),        ambosobligatorios</td><td colspan="1" rowspan="1">Cada registro tiene unidentificador estable y no seadmite repetir un númeropara el mismo socio.</td></tr></table>

Las combinaciones obligatorias y únicas de LIBRO\_AUTOR y TELÉFONO\_SOCIO son claves candidatas compuestas que se conservan como alternativas a las PK subrogadas.

El correo electrónico no se considera clave candidata, porque puede faltar o ser compartido por distintas personas.

Los nombres y apellidos no se utilizan como claves: no garantizan unicidad ni estabilidad.

Respecto del modelo inicial, se documentan tres cambios:

● SOCIO y BIBLIOTECARIO reemplazan sus identificadores independientes por id\_persona.

● LIBRO\_AUTOR incorpora id\_libro\_autor y conserva la unicidad de la combinación libro–autor.

TELÉFONO\_SOCIO adopta id\_telefono\_socio y conserva la unicidad de la combinación socio–número.

## 3.2. Revisión y resolución de la jerarquía.

En el modelo inicial de biblioteca, las entidades SOCIO y BIBLIOTECARIO representan personas que desempeñan diferentes roles. Ambas contienen los atributos nombre y apellido, mientras que cada una tiene información propia: SOCIO registra documento, email y fecha\_alta; BIBLIOTECARIO registra legajo.

Se evaluaron dos alternativas:

Mantener las entidades independientes: simplifica las consultas, pero obliga a duplicar los datos personales cuando un bibliotecario también es socio. Una actualización podría dejar nombres o apellidos diferentes para la misma persona.

Crear una entidad general PERSONA: permite registrar una única identidad y asociarle los roles que desempeña, manteniendo los atributos específicos en cada especialización.

Se adopta la segunda alternativa porque permite que un bibliotecario también sea socio sin duplicar sus datos personales.

3.2.1 Estructura propuesta
<table><tr><td rowspan=1 colspan=1>Entidad</td><td rowspan=1 colspan=1>Atributos</td><td rowspan=1 colspan=1>Función</td></tr><tr><td rowspan=1 colspan=1>PERSONA</td><td rowspan=1 colspan=1>id_persona, nombre, apellido,documento, email</td><td rowspan=1 colspan=1>Contiene la identidad y los datospersonales comunes.</td></tr><tr><td rowspan=1 colspan=1>SOCIO</td><td rowspan=1 colspan=1>id_persona, fecha_alta</td><td rowspan=1 colspan=1>Contiene los datos propios de laafiliación a la biblioteca.</td></tr><tr><td rowspan=1 colspan=1>BIBLIOTECARIO</td><td rowspan=1 colspan=1>id_persona, legajo</td><td rowspan=1 colspan=1>Contiene los datos propios delpersonal de la biblioteca.</td></tr></table>

En PERSONA, id\_persona es la clave primaria subrogada. El documento se establece como obligatorio y único para identificar a una persona y evitar que sea registrada nuevamente al incorporar otro rol. El correo electrónico es opcional y no se considera una clave candidata, porque no se garantiza que sea único.

En SOCIO y BIBLIOTECARIO, id\_persona cumple simultáneamente las funciones de clave primaria y clave foránea hacia PERSONA. Las especializaciones no generan identificadores independientes: utilizan la identidad asignada por la entidad general.

## 3.2.2 Restricciones de la jerarquía

Para este diseño se adoptan las siguientes reglas de negocio:

Especialización total: toda persona registrada debe desempeñar al menos uno de los dos roles: socio o bibliotecario. El sistema no registra personas sin un rol definido.

● Especialización superpuesta: una misma persona puede ser socio y bibliotecario simultáneamente.

Estas reglas se documentan en el diagrama como “Jerarquía PERSONA: total y superpuesta”.

## 3.2.3 Relaciones con el resto del modelo

PRÉSTAMO mantiene relaciones diferenciadas con SOCIO y BIBLIOTECARIO: la primera identifica a quien recibe el ejemplar y la segunda a quien registra la operación. Ambas relaciones deben apuntar a la especialización correspondiente, porque la existencia de una PERSONA no garantiza por sí sola que tenga el rol requerido.

La entidad TELÉFONO\_SOCIO conserva su relación con SOCIO, ya que, dentro del alcance actual, se registran teléfonos de contacto de los socios.

AUTOR permanece como entidad independiente. Compartir nombre y apellido no justifica incorporarlo a esta jerarquía: el registro de autoría tiene una finalidad bibliográfica y no requiere gestionar la identidad de los autores junto con los usuarios y el personal de la biblioteca.

## 3.2.4 Representación en DrawDB

Se incorpora PERSONA y se trasladan a ella los datos personales. En SOCIO y BIBLIOTECARIO se utiliza id\_persona como PK/FK, vinculándolo con PERSONA mediante relaciones que permiten cero o una fila de cada especialización por persona.

La condición de totalidad debe quedar expresada en una nota: las claves foráneas garantizan que cada socio o bibliotecario tenga una persona asociada, pero no garantizan que toda persona tenga al menos un rol. Su control deberá resolverse al implementar el sistema.

La decisión permite mantener una única identidad por persona y actualizar sus datos en un solo lugar. Como consecuencia, las consultas que necesiten los datos personales de un socio o bibliotecario deberán relacionar su especialización con PERSONA.

## 3.3. Normalización del modelo hasta tercera forma normal

Se analiza el modelo para evitar anomalías de inserción, actualización y borrado. La revisión considera el significado de los atributos y sus dependencias funcionales, sin agregar entidades que no sean necesarias para el alcance del proyecto.

## 3.3.1. Primera forma normal

Cada atributo almacena un único valor dentro del dominio definido. No se utilizan listas de autores o teléfonos dentro de una celda ni columnas repetidas como telefono\_1, telefono\_2 o autor\_1.

Los teléfonos de un socio se representan mediante filas independientes en TELÉFONO\_SOCIO. La relación entre libros y autores se representa mediante LIBRO\_AUTOR, con una fila por asociación.

Nombre y apellido se almacenan por separado porque el sistema necesita tratarlos como atributos diferenciados.

La disponibilidad del ejemplar se calcula: requiere que su estado sea operativo y que no exista un préstamo pendiente de devolución. No se almacena una columna adicional de disponibilidad que pueda contradecir esos datos.

## 3.3.2. Segunda forma normal

Los atributos no clave deben depender de la totalidad de cada clave candidata, incluidas las claves compuestas alternativas.

En LIBRO\_AUTOR, la dependencia relevante es:

## (id\_libro, id\_autor) → orden\_autoria

El orden expresa la posición de un autor en un libro determinado. No depende únicamente del autor, porque puede ocupar posiciones diferentes en otros libros; tampoco depende únicamente del libro, porque este puede tener varios autores.

En TELÉFONO\_SOCIO se adopta la siguiente regla:

## (id\_socio, numero) → tipo

El atributo tipo describe el número de contacto informado por ese socio. No se supone que un número determine globalmente su clasificación para todas las personas.

No se almacenan el título del libro ni el nombre del autor en LIBRO\_AUTOR. Tampoco se almacenan los datos personales del socio en TELÉFONO\_SOCIO. Esos atributos pertenecen a sus respectivas entidades.

La incorporación de una PK subrogada no sustituye esta revisión: también deben analizarse las dependencias respecto de las claves candidatas compuestas.

## 3.3.3. Tercera forma normal

Se verifica que los atributos no clave no dependan transitivamente de otros atributos no clave.

Las principales dependencias del modelo son:
<table><tr><td rowspan=1 colspan=1>Entidad</td><td rowspan=1 colspan=1>Dependencia funcional</td></tr><tr><td rowspan=1 colspan=1>PERSONA</td><td rowspan=1 colspan=1>id_persona → nombre, apellido, documento, email</td></tr><tr><td rowspan=1 colspan=1>SOCIO</td><td rowspan=1 colspan=1>id_persona → fecha_alta</td></tr><tr><td rowspan=1 colspan=1>BIBLIOTECARIO</td><td rowspan=1 colspan=1>id_persona → legajo</td></tr><tr><td rowspan=1 colspan=1>EDITORIAL</td><td rowspan=1 colspan=1>id_editorial → nombre</td></tr><tr><td rowspan=1 colspan=1>AUTOR</td><td rowspan=1 colspan=1>id_autor → nombre, apellido</td></tr><tr><td rowspan=1 colspan=1>LIBRO</td><td rowspan=1 colspan=1>id_libro → titulo, isbn, anio_publicacion, id_editorial</td></tr><tr><td rowspan=1 colspan=1>EJEMPLAR</td><td rowspan=1 colspan=1>id_ejemplar → id_libro, codigo_inventario, fecha_incorporacion, estado</td></tr><tr><td rowspan=1 colspan=1>PRÉSTAMO</td><td rowspan=1 colspan=1>id prestamo → id socio, id ejemplar, id bibliotecario y fechas de la operación</td></tr><tr><td rowspan=1 colspan=1>LIBRO AUTOR</td><td rowspan=1 colspan=1>id_libro_autor → id_libro, id_autor, orden_autoria</td></tr><tr><td rowspan=1 colspan=1>TELÉFONO_SOCIO</td><td rowspan=1 colspan=1>id_telefono_socio → id_socio, numero, tipo</td></tr></table>

Por ejemplo, el nombre de la editorial no se almacena en LIBRO. Si se incluyera, aparecería la dependencia transitiva:  
id\_libro → id\_editorial → nombre\_editorial

La separación entre LIBRO y EDITORIAL evita esa redundancia. Del mismo modo, EJEMPLAR no repite el título del libro y PRÉSTAMO no repite los nombres del socio o del bibliotecario.

No se detecta una dependencia transitiva adicional que exija otra separación en el modelo definido. Se documenta este resultado sin introducir entidades artificiales para producir una corrección innecesaria.

La jerarquía PERSONA permite, además, centralizar los datos personales de quienes desempeñan ambos roles. Esta decisión evita duplicaciones entre entidades, aunque la repetición entre tablas no constituye por sí sola una violación de 3FN.

## 3.3.4. Conservación de información histórica

fecha\_vencimiento\_inicial y fecha\_vencimiento\_actual representan hechos diferentes.

La primera conserva el plazo acordado al registrar el préstamo y no se modifica durante una renovación. La segunda representa el plazo vigente y puede actualizarse.

Aunque inicialmente coincidan, ninguna determina necesariamente a la otra. Su conservación no constituye una redundancia ni una desnormalización deliberada. No se registra el historial completo de renovaciones, porque queda fuera del alcance del proyecto.

## 3.4. Reglas de integridad y borrado

La integridad del modelo se establece mediante claves primarias, claves foráneas, obligatoriedad, unicidad y reglas del negocio.

Las relaciones obligatorias requieren FK no nulas. fecha\_devolucion admite NULL mientras el préstamo permanezca pendiente. El correo electrónico es opcional y el ISBN es obligatorio.

## 3.4.1. Reglas de borrado

Se prioriza la conservación del historial de préstamos. El sistema no incluye un proceso funcional de bajas; las siguientes reglas definen qué debe ocurrir si se intenta eliminar un registro.

<table><tr><td colspan="1" rowspan="1">Registro que seintenta eliminar</td><td colspan="1" rowspan="1">Registros relacionados</td><td colspan="1" rowspan="1">Regla</td><td colspan="1" rowspan="1">Fundamento</td></tr><tr><td colspan="1" rowspan="1">PERSONA</td><td colspan="1" rowspan="1">SOCIO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">No se elimina una identidad mientrasconserve el rol de socio.</td></tr><tr><td colspan="1" rowspan="1">PERSONA</td><td colspan="1" rowspan="1">BIBLIOTECARIO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">No se elimina una identidad mientrasconserve el rol de bibliotecario.</td></tr><tr><td colspan="1" rowspan="1">SOCIO</td><td colspan="1" rowspan="1">PRÉSTAMO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">Se preserva la identificación de quienrecibió cada ejemplar.</td></tr><tr><td colspan="1" rowspan="1">BIBLIOTECARIO</td><td colspan="1" rowspan="1">PRÉSTAMO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">Se preserva la identificación de quienregistró la operación.</td></tr><tr><td colspan="1" rowspan="1">EJEMPLAR</td><td colspan="1" rowspan="1">PRÉSTAMO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">Se conserva la referencia a la copiafísica prestada.</td></tr><tr><td colspan="1" rowspan="1">LIBRO</td><td colspan="1" rowspan="1">EJEMPLAR</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">No se elimina un registro bibliográficoque todavía tiene copias registradas.</td></tr><tr><td colspan="1" rowspan="1">EDITORIAL</td><td colspan="1" rowspan="1">LIBRO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">No se dejan libros sin su editorialobligatoria.</td></tr><tr><td colspan="1" rowspan="1">AUTOR</td><td colspan="1" rowspan="1">LIBRO_AUTOR</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">Se evita eliminar una autoríamediante el borrado del autor.</td></tr><tr><td colspan="1" rowspan="1">LIBRO</td><td colspan="1" rowspan="1">LIBRO_AUTOR</td><td colspan="1" rowspan="1">CASCADE</td><td colspan="1" rowspan="1">Si puede eliminarse el libro, susasociaciones de autoría carecen deexistencia independiente.</td></tr><tr><td colspan="1" rowspan="1">SOCIO</td><td colspan="1" rowspan="1">TELÉFONO_SOCIO</td><td colspan="1" rowspan="1">CASCADE</td><td colspan="1" rowspan="1">Si puede eliminarse el socio, tambiénse eliminan sus registros de contacto.</td></tr></table>

CASCADE solo actúa cuando el borrado del registro principal está permitido. Por ejemplo, un socio con préstamos registrados no puede eliminarse, por lo que tampoco se ejecuta el borrado en cascada de sus teléfonos.

No se utiliza SET NULL en estas relaciones porque sus referencias son obligatorias.

## 3.4.2. Otras reglas de integridad

Se establecen las siguientes condiciones:

● Un ejemplar debe pertenecer a un libro existente.

● Un préstamo debe identificar un socio, un bibliotecario y un ejemplar existentes.

● Un ejemplar no puede tener dos préstamos pendientes de devolución simultáneamente.

● Un ejemplar en reparación no puede prestarse.

● estado solo admite los valores operativo y en\_reparacion.

● Las fechas de vencimiento y devolución no pueden ser anteriores a fecha\_prestamo.

● Una renovación no modifica fecha\_vencimiento\_inicial.

● orden\_autoria debe ser mayor que cero.

● Un libro completo debe tener al menos un autor.

● Toda PERSONA debe pertenecer al menos a SOCIO o BIBLIOTECARIO.

Las PK, FK y restricciones de columna no garantizan por sí solas todas estas condiciones. La totalidad de la jerarquía, la presencia de autores y el control de préstamos simultáneos requieren mecanismos adicionales al implementar el sistema. El control de simultaneidad deberá contemplar operaciones concurrentes.

## 3.5. Auditoría del modelo con IA y decisiones adoptadas

Se realiza una auditoría documental con ChatGPT sobre las entidades, atributos, claves y reglas descritas. La revisión analiza el diseño y no acredita por sí sola que los cambios ya estén aplicados en DrawDB.

## 3.5.1. Prompt de auditoría

Actuá como revisor de modelos de datos, especialista en normalización hasta tercera forma normal.

## CONTEXTO:

Modelo de biblioteca con las entidades PERSONA, SOCIO, BIBLIOTECARIO, EDITORIAL, AUTOR, LIBRO, EJEMPLAR, PRÉSTAMO, LIBRO\_AUTOR y TELÉFONO\_SOCIO. Utilizá el esquema de atributos y claves del apartado 3.6.

## REGLAS DEL NEGOCIO:

● La especialización PERSONA es total y superpuesta.

● SOCIO y BIBLIOTECARIO utilizan id\_persona como PK y FK.

● Cada préstamo corresponde a un único ejemplar.

● LIBRO\_AUTOR registra orden\_autoria y no admite repetir la combinación libro–autor.

Un socio puede registrar varios teléfonos, sin repetir el mismo número para ese socio.

● El ISBN es obligatorio y único

● El correo electrónico es opcional y puede compartirse.

● El vencimiento inicial se conserva; el actual puede cambiar por renovación.

● Un ejemplar debe estar operativo y sin préstamos pendientes para poder prestarse.

● No se gestionan multas, pagos, bajas ni historial completo de renovaciones.

## TAREA:

1. Detectá posibles violaciones de 1FN.

2. Revisá dependencias parciales respecto de todas las claves candidatas, no solo de las PK.

3. Revisá dependencias transitivas, indicando su cadena completa.

4. Señalá inconsistencias entre atributos, claves y relaciones.

5. Diferenciá errores del diseño de reglas que requieren controles adicionales.

## RESTRICCIONES:

No reescribas el modelo completo, no amplíes el alcance y no propongas formas normales superiores a 3FN.

## FORMATO:

Tabla con hallazgo, fundamento, corrección propuesta e impacto. Identificá los supuestos que no puedan comprobarse con la información suministrada.

## 3.5.2. Hallazgos y revisión humana

<table><tr><td rowspan=1 colspan=1>Hallazgo u observación</td><td rowspan=1 colspan=1>Clasificación</td><td rowspan=1 colspan=1>Decisión y fundamento</td></tr><tr><td rowspan=1 colspan=1>TELÉFONO SOCIO tenía identificadoresdiferentes  entree las partes deldocumento.</td><td rowspan=1 colspan=1>Correcto</td><td rowspan=1 colspan=1>Se adopta id_telefono_socio y se conservaUNIQUE (id_socio, numero).</td></tr><tr><td rowspan=1 colspan=1>Los datos personales se duplicarían si unbibliotecario también fuera socio.</td><td rowspan=1 colspan=1>Correcto</td><td rowspan=1 colspan=1>Se acepta PERSONA como entidad general yse mantienen los atributos específicos en cadarol.</td></tr><tr><td rowspan=1 colspan=1>Las FK de préstamos y teléfonos debenadecuarse a los identificadores de lasespecializaciones.</td><td rowspan=1 colspan=1>Correcto</td><td rowspan=1 colspan=1>Se mantienen los nombres que expresan el rol,pero se referencian las PK id_persona deSOCIO y BIBLIOTECARIO.</td></tr><tr><td rowspan=1 colspan=1>Conviene reemplazar la PK compuestade LIBRO_AUTOR por una subrogada.</td><td rowspan=1 colspan=1>Discutible</td><td rowspan=1 colspan=1>Ambas opciones son válidas. Se adopta lasubrogada para seguir el criterio del curso,conservando UNIQUE (id_libro, id_autor).</td></tr><tr><td rowspan=1 colspan=1>Falta definir las reglas de borrado.</td><td rowspan=1 colspan=1>Correcto</td><td rowspan=1 colspan=1>Se incorporan reglas explícitas que preservanel historial y eliminan únicamente registrosdependientes cuando corresponde.</td></tr><tr><td rowspan=1 colspan=1>El atributo estado aparece en losprompts, pero no en la descripción inicialde EJEMPLAR.</td><td rowspan=1 colspan=1>Correcto</td><td rowspan=1 colspan=1>Se incorpora al esquema y se limita a operativoy en_reparacion.</td></tr><tr><td rowspan=1 colspan=1>El ISBN se presenta con obligatoriedadambigua.</td><td rowspan=1 colspan=1>Correcto</td><td rowspan=1 colspan=1>Se establece que es obligatorio y único</td></tr><tr><td rowspan=1 colspan=1>Debe comprobarse 2FN aunque las PKsean simples.</td><td rowspan=1 colspan=1>Correcto</td><td rowspan=1 colspan=1>Se revisan también las claves candidatascompuestas de las tablas asociativas.</td></tr></table>

Se descartan dos posibles correcciones que perjudicarían el diseño: eliminar fecha\_vencimiento\_inicial por coincidir inicialmente con el vencimiento actual, y dirigir los préstamos exclusivamente a PERSONA. La primera perdería información histórica; la segunda no garantizaría los roles de socio y bibliotecario.

No se identifican violaciones adicionales de 1FN, 2FN o 3FN bajo las reglas declaradas. Este resultado deberá contrastarse con el diagrama actualizado para verificar que su representación coincida con el diseño documentado.

## 3.6. Diagrama definitivo y síntesis de las decisiones de diseño

El modelo refactorizado queda definido por diez entidades. Las nueve entidades iniciales se conservan y se incorpora PERSONA como generalización de SOCIO y BIBLIOTECARIO.

## 3.6.1. Esquema de referencia para el diagrama

<table><tr><td rowspan=1 colspan=1>Entidad</td><td rowspan=1 colspan=1>Atributos definitivos</td></tr><tr><td rowspan=1 colspan=1>PERSONA</td><td rowspan=1 colspan=1>id_persona PK, nombre, apellido, documento UNIQUE y obligatorio, emailopcional</td></tr><tr><td rowspan=1 colspan=1>SOCIO</td><td rowspan=1 colspan=1>id_persona PK/FK hacia PERSONA, fecha_alta</td></tr><tr><td rowspan=1 colspan=1>BIBLIOTECARIO</td><td rowspan=1 colspan=1>id_persona PK/FK hacia PERSONA, legajo UNIQUE y obligatorio</td></tr><tr><td rowspan=1 colspan=1>EDITORIAL</td><td rowspan=1 colspan=1>id_editorial PK, nombre</td></tr><tr><td rowspan=1 colspan=1>AUTOR</td><td rowspan=1 colspan=1>id_autor PK, nombre, apellido</td></tr><tr><td rowspan=1 colspan=1>LIBRO</td><td rowspan=1 colspan=1>id_libro PK, titulo, isbn obligatorio y UNIQUE, anio_publicacion, id_editorial FK</td></tr><tr><td rowspan=1 colspan=1>EJEMPLAR</td><td rowspan=1 colspan=1>id_ejemplar PK, id_libro FK, codigo_inventario UNIQUE y obligatorio,fecha incorporacion, estado</td></tr><tr><td rowspan=1 colspan=1>PRÉSTAMO</td><td rowspan=1 colspan=1>id_prestamo PK, id_socio FK hacia SOCIO.id_persona, id_ejemplar FK,id bibliotecario FK hacia BIBLIOTECARIO.id persona, fecha prestamo,fecha vencimiento inicial, fecha vencimiento actual, fecha devolucion opcional</td></tr><tr><td rowspan=1 colspan=1>LIBRO AUTOR</td><td rowspan=1 colspan=1>id_libro_autor PK, id_libro FK, id_autor FK, orden_autoria; UNIQUE (id_libro,id_autor)</td></tr><tr><td rowspan=1 colspan=1>TELÉFONO_SOCIO</td><td rowspan=1 colspan=1>id_telefono_socio PK, id_socio FK hacia SOCIO.id_persona, numero, tipo;UNIQUE (id_socio, numero)</td></tr></table>

El diagrama mantiene las ocho relaciones de la Parte 2 y agrega las dos relaciones de especialización. Cada PERSONA puede tener cero o una fila en cada especialización, pero debe tener al menos uno de los dos roles. Esta condición conjunta se documenta mediante la nota “Especialización total y superpuesta”.

Cada relación debe mostrar su cardinalidad y obligatoriedad. La exigencia de al menos un autor por libro debe quedar documentada aunque la herramienta no permita representarla completamente.

Modelo refactorizado de la biblioteca, con la jerarquía PERSONA, las claves revisadas y las decisiones de normalización

![](images/e5224cacab155f53498b65867408b2273c848bdc3b112e13b3e027cf1cab6aaf.jpg)

## 3.6.2. Síntesis de las decisiones

El diseño distingue el registro bibliográfico de cada copia física y registra un préstamo por ejemplar. La relación N:M entre libros y autores se resuelve mediante LIBRO\_AUTOR, que conserva el atributo propio orden\_autoria.

PERSONA centraliza la identidad y los datos personales de socios y bibliotecarios. Las operaciones se vinculan con las especializaciones para garantizar que cada participante tenga el rol requerido.

Los teléfonos se representan en una entidad independiente. Las claves subrogadas simplifican la identificación y las restricciones de unicidad conservan las reglas naturales del negocio.

La disponibilidad se calcula a partir del estado del ejemplar y de sus préstamos pendientes. El vencimiento inicial se conserva como información histórica y el actual representa el plazo vigente.

Las reglas de borrado protegen el historial de circulación. Las condiciones que requieren controles adicionales quedan documentadas para su implementación posterior.

La imagen incorporada deberá coincidir con este esquema y con las decisiones registradas en los apartados anteriores.

## Parte 4 · Creación de la base en DBeaver

## 4.1. Objetivo

Implementar en MySQL el modelo de biblioteca refactorizado en la parte 3, mediante un script SQL de definición de datos (DDL), y verificar la estructura creada utilizando DBeaver.

## 4.2. Preparación del script

Se tomó como punto de partida el script exportado desde DrawDB. Se revisaron sus instrucciones y se incorporaron los ajustes necesarios para crear la base de datos y sus tablas.

El esquema quedó compuesto por diez tablas:

● persona

● socio

● bibliotecario

● telefono\_socio

● editorial

● autor

libro

● ejemplar

● prestamo

● libro\_autor

Se agregó la creación de la base biblioteca y su selección mediante USE. En todas las tablas se declaró el motor InnoDB, que permite implementar claves foráneas, y el juego de caracteres utf8mb4.

Se conservaron las decisiones del modelo anterior: la identidad común en persona, los roles de socio y bibliotecario mediante claves que son simultáneamente PK y FK, la separación entre libro y ejemplar, y la relación N:M entre libros y autores resuelta mediante libro\_autor.

## 4.3. Restricciones e integridad

El script incorpora claves primarias, claves foráneas, restricciones de obligatoriedad y unicidad, e índices sobre columnas utilizadas en las relaciones.

Entre las restricciones implementadas se destacan:

● Documento, legajo, ISBN y código de inventario obligatorios y únicos en sus respectivas tablas.

● Unicidad de la combinación socio–número de teléfono.

● Unicidad de la combinación libro–autor.

● Orden de autoría mayor que cero.

● Vencimiento inicial igual o posterior a la fecha del préstamo.

● Vencimiento actual igual o posterior al vencimiento inicial, considerando que las renovaciones extienden el plazo.

● Fecha de devolución nula mientras el préstamo esté pendiente, o igual o posterior a la fecha del préstamo.

Todas las claves foráneas recibieron nombres explícitos y reglas de actualización y borrado. Se utilizó principalmente RESTRICT para impedir eliminaciones que dejarían registros relacionados sin referencia. Se definió CASCADE para los teléfonos de un socio y las asociaciones de autoría de un libro cuando se elimina su registro principal.

Estas reglas de integridad referencial no incorporan un circuito funcional de bajas al alcance del proyecto.

## 4.4. Orden y ejecución en DBeaver

Las instrucciones se organizaron respetando sus dependencias:

1. Creación y selección de la base.

2. Creación de las tablas y sus índices.

3. Incorporación de las claves foráneas, una vez existentes todas las tablas referenciadas.

4. Incorporación de las restricciones CHECK.

La ejecución se realizó progresivamente desde el editor SQL de DBeaver. Durante el proceso se presentó un error de permisos del usuario de conexión sobre la base biblioteca, que debió resolverse para continuar.

En la revisión del script también se detectó la duplicación de las dos claves foráneas de libro\_autor. Se indicó eliminar las declaraciones repetidas y conservar las restricciones nombradas.

## 4.5. Verificación de la estructura

Para inspeccionar la base se utilizaron las instrucciones de verificación propuestas en clase: SHOW TABLES para listar las tablas y DESCRIBE para examinar sus columnas, tipos de datos, nulabilidad y claves.

La comprobación se complementó con el diagrama generado por DBeaver a partir de la estructura existente en MySQL. En él se observaron las diez tablas y las diez relaciones esperadas, correspondientes al modelo refactorizado.

Se verificaron visualmente las relaciones de persona con sus roles, las referencias de prestamo a socio, bibliotecario y ejemplar, la vinculación de ejemplar con libro y editorial, y la tabla intermedia libro\_autor.

![](images/209a96733bd0fe989861ba15bbbe9d3222a100ea1e82eb521c05be1aa6c4ad87.jpg)

La inspección mediante SHOW CREATE TABLE permite completar la revisión de las reglas de borrado y de los CHECK, cuyos detalles no se muestran en el diagrama.

## 4.6. Uso de IA y correcciones

La IA se utilizó como apoyo para revisar el SQL exportado, interpretar errores y orientar la ejecución y la verificación. Las consultas abordaron la comparación con los errores frecuentes de DDL, los elementos faltantes y el orden de ejecución.

La revisión permitió identificar y corregir:

● La ausencia de las instrucciones de creación y selección de la base.

● La falta de declaración explícita del motor y del juego de caracteres.

● La inconsistencia entre la obligatoriedad del ISBN y su comentario.

● La ausencia de validaciones del orden de autoría y de las fechas.

● La falta de nombres explícitos en las claves foráneas.

● La duplicación de restricciones en libro\_autor.

Las sugerencias se contrastaron con las decisiones del proyecto antes de incorporarlas al script.

## 4.7. Resultado y controles pendientes

Se obtuvo la base biblioteca con sus tablas y relaciones, cuya estructura pudo visualizarse en DBeaver. El script del esquema se incorpora a la entrega como 01\_esquema.sql.

```sql
CREATE DATABASE IF NOT EXISTS biblioteca
CHARACTER SET utf8mb4;
USE biblioteca;
CREATE TABLE IF NOT EXISTS `persona` (
`id_persona` INT NOT NULL AUTO_INCREMENT,
`nombre` VARCHAR(80) NOT NULL,
`apellido` VARCHAR(80) NOT NULL,
`documento` VARCHAR(20) NOT NULL UNIQUE COMMENT 'Obligatorio y único según el alcance
del proyecto.',
`email` VARCHAR(254) COMMENT 'Opcional; puede compartirse. No es clave candidata.',
PRIMARY KEY(`id_persona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Identidad común de socios y bibliotecarios.
Especialización total y superpuesta.';
CREATE TABLE IF NOT EXISTS `socio` (
`id_persona` INT NOT NULL COMMENT 'PK/FK a persona.id_persona; no genera identidad
independiente.',
`fecha_alta` DATE NOT NULL,
PRIMARY KEY(`id_persona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Rol que habilita a recibir préstamos. Persona
0..1 socio; todo socio tiene 1 persona.';
CREATE TABLE IF NOT EXISTS `bibliotecario` (
`id_persona` INT NOT NULL COMMENT 'PK/FK a persona.id_persona; no genera identidad
independiente.',
`legajo` VARCHAR(30) NOT NULL UNIQUE,
PRIMARY KEY(`id_persona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Rol que habilita a registrar préstamos.
Persona 0..1 bibliotecario; todo bibliotecario tiene 1 persona.';
CREATE TABLE IF NOT EXISTS `telefono_socio` (
`id_telefono_socio` INT NOT NULL AUTO_INCREMENT,
`id_socio` INT NOT NULL COMMENT 'FK hacia socio.id_persona. Identifica el rol socio.',
`numero` VARCHAR(25) NOT NULL,
`tipo` VARCHAR(20) COMMENT 'Clasificación del contacto informado por este socio.',
PRIMARY KEY(`id_telefono_socio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Cada socio puede registrar 0..N teléfonos.
Número único dentro de cada socio.';
CREATE UNIQUE INDEX `uq_telefono_socio_numero
ON `telefono_socio` (`id_socio`, `numero`);
CREATE TABLE IF NOT EXISTS `editorial` (
`id_editorial` INT NOT NULL AUTO_INCREMENT,
```

```sql
`nombre` VARCHAR(120) NOT NULL,
PRIMARY KEY(`id_editorial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Editorial que publica libros. No se presupone
unicidad del nombre.';
CREATE TABLE IF NOT EXISTS `autor` (
`id_autor` INT NOT NULL AUTO_INCREMENT,
`nombre` VARCHAR(80) NOT NULL,
`apellido` VARCHAR(80) NOT NULL,
PRIMARY KEY(`id_autor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Identidad bibliográfica independiente de la
jerarquía persona. Puede asociarse a 0..N libros.';
CREATE TABLE IF NOT EXISTS `libro` (
`id_libro` INT NOT NULL AUTO_INCREMENT,
`titulo` VARCHAR(200) NOT NULL,
`isbn` VARCHAR(17) NOT NULL UNIQUE COMMENT 'Obligatorio y único según el alcance del
proyecto.',
`anio_publicacion` SMALLINT,
`id_editorial` INT NOT NULL,
PRIMARY KEY(`id_libro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registro bibliográfico independiente de las
copias. Cada libro tiene 1 editorial, 0..N ejemplares y 1..N autores para considerarse completo.';
CREATE INDEX `ix_libro_editorial
ON `libro` (`id_editorial`);
CREATE TABLE IF NOT EXISTS `ejemplar` (
`id_ejemplar` INT NOT NULL AUTO_INCREMENT,
`id_libro` INT NOT NULL,
`codigo_inventario` VARCHAR(40) NOT NULL UNIQUE,
`fecha_incorporacion` DATE NOT NULL,
`estado` ENUM('operativo', 'en_reparacion') NOT NULL COMMENT 'Estado físico, diferente de
disponibilidad.',
PRIMARY KEY(`id_ejemplar`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Copia física de un libro. Disponibilidad
derivada: operativo y sin préstamo pendiente. No se almacena disponibilidad.';
CREATE INDEX `ix_ejemplar_libro
ON `ejemplar` (`id_libro`);
CREATE TABLE IF NOT EXISTS `prestamo` (
`id_prestamo` INT NOT NULL AUTO_INCREMENT,
`id_socio` INT NOT NULL COMMENT 'FK hacia socio.id_persona; receptor del ejemplar.',
`id_ejemplar` INT NOT NULL,
`id_bibliotecario` INT NOT NULL COMMENT 'FK hacia bibliotecario.id_persona; responsable del
registro.',
`fecha_prestamo` DATE NOT NULL
`fecha_vencimiento_inicial` DATE NOT NULL COMMENT 'Dato histórico inmutable ante
renovaciones.',
`fecha_vencimiento_actual` DATE NOT NULL COMMENT 'Plazo vigente; puede cambiar por
renovación.',
`fecha_devolucion` DATE COMMENT 'NULL indica pendiente de devolución.',
PRIMARY KEY(`id_prestamo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Una operación por ejemplar. No se repiten
datos personales ni bibliográficos. Reglas de fechas y simultaneidad en notas.';
CREATE INDEX `ix_prestamo_socio
ON `prestamo` (`id_socio`);
CREATE INDEX `ix_prestamo_ejemplar_devolucion
ON `prestamo` (`id_ejemplar`, `fecha_devolucion`);
CREATE INDEX `ix_prestamo_bibliotecario
ON `prestamo` (`id_bibliotecario`);
CREATE TABLE IF NOT EXISTS `libro_autor` (
`id_libro_autor` INT NOT NULL AUTO_INCREMENT,
```

```sql
`id_libro` INT NOT NULL
`id_autor` INT NOT NULL,
`orden_autoria` SMALLINT NOT NULL COMMENT 'Posición del autor en este libro; depende de la
combinación libro-autor.',
PRIMARY KEY(`id_libro_autor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Entidad asociativa que resuelve libro N:M
autor y conserva orden_autoria. No debe repetirse libro-autor.';
CREATE UNIQUE INDEX `uq_libro_autor
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
ADD CONSTRAINT `fk_telefono_socio_socio
FOREIGN KEY (`id_socio`) REFERENCES `socio` (`id_persona`)
ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE `libro
ADD CONSTRAINT `fk_libro_editorial
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
ADD CONSTRAINT `fk_prestamo_ejemplar
FOREIGN KEY (`id_ejemplar`) REFERENCES `ejemplar` (`id_ejemplar`)
ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE `prestamo
ADD CONSTRAINT `fk_prestamo_bibliotecario
FOREIGN KEY (`id_bibliotecario`)
REFERENCES `bibliotecario` (`id_persona`)
ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE `libro_autor
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
```

CHECK (orden\_autoria > 0);

## Parte 5 · Carga de datos de prueba y consultas de negocio

Con el esquema de la base de datos de biblioteca creado en la etapa anterior, se preparó un conjunto de datos ficticios para probar las restricciones y las consultas del sistema. La carga se organizó mediante scripts SQL independientes para facilitar su ejecución y revisión.

A partir de estos datos se formularon 20 preguntas de negocio relacionadas con la gestión de socios, el catálogo, las editoriales, los autores y el inventario. Entre ellas se incluyeron consultas para contar registros, filtrar títulos, agrupar libros por año de publicación, identificar editoriales sin libros asociados, verificar libros sin autor o sin ejemplares y conocer la distribución de ejemplares por estado. Para cada pregunta se definió un resultado esperado, que sirve como referencia para evaluar la consulta.

## 5.1 Observación de verificación

Durante la comprobación de la pregunta sobre editoriales sin libros asociados, la consulta devolvió 41 registros, cuando el resultado esperado era 11. La revisión permitió detectar que las 30 editoriales se habían cargado nuevamente, generando registros duplicados. Se preparó un script para identificar y eliminar las últimas 30 filas duplicadas que no estén asociadas a libros. La limpieza y la nueva ejecución de la consulta deben confirmarse antes de presentar 11 como resultado observado.

Esta etapa deja preparados el conjunto de datos, las preguntas de negocio y sus consultas SQL para verificar el funcionamiento de la base. La comparación de las consultas manuales con las generadas mediante IA deberá documentarse una vez que ambas versiones se ejecuten sobre la misma base cargada y depurada.

Los scripts de carga y consultas SQL elaborados para esta etapa se encuentran en el directorio SQL del proyecto, junto con los demás archivos SQL utilizados en su desarrollo. Allí se organizan las cargas de personas, autores, editoriales, libros, teléfonos y ejemplares, además del script con las 20 consultas de negocio.

## 5.2 Consultas a la base de datos

Las preguntas se plantean sobre la base de datos de la biblioteca y el set de prueba preparado. Los resultados indicados suponen que se ejecutaron correctamente los scripts

de personas, teléfonos, autores, editoriales, libros y ejemplares. En esta etapa se define qué queremos consultar y qué esperamos encontrar.
<table><tr><td colspan="1" rowspan="1">N.°</td><td colspan="1" rowspan="1">Pregunta de negocio</td><td colspan="1" rowspan="1">Resultado esperado y análisis</td></tr><tr><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">¿Cuántas personas estánregistradas en la biblioteca?</td><td colspan="1" rowspan="1">50 personas. Corresponden a las 45 personas con rolde socio y las 5 con rol de bibliotecario.</td></tr><tr><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">¿Cuántas personas tienenrol de socio?</td><td colspan="1" rowspan="1">45 socios. Permite verificar la carga de personas y latabla de roles. Requiere relacionar persona consocio.</td></tr><tr><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">¿Cuántas personas trabajancomo bibliotecarias?</td><td colspan="1" rowspan="1">5 bibliotecarios. Requiere relacionar persona conbibliotecario.</td></tr><tr><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">¿Hay personas sin correoelectrónico registrado?</td><td colspan="1" rowspan="1">Ninguna. Las 50 personas del set tienen correo deprueba.</td></tr><tr><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">¿Cuántos   teléfonos    seregistraron y cuántos sociostienen al menos uno?</td><td colspan="1" rowspan="1">55 teléfonos para 45 socios. Cada socio tiene unteléfono principal; 10 tienen además uno alternativo.Requiere relacionar telefono_socio, socio y persona.</td></tr><tr><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">¿Cuántos socios tienen unteléfono y cuántos tienendos?</td><td colspan="1" rowspan="1">35 socios tienen uno y 10 tienen dos. La consultapermite comprobar que se contemplan variosteléfonos por socio.</td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">¿Cuántos  autores  estánregistrados?</td><td colspan="1" rowspan="1">110 autores. Se espera ese total si la tabla estabavacía antes de ejecutar la carga.</td></tr><tr><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">¿Cuántos autores tienen almenos un libro asociado ycuántos todavía no tienenninguno?</td><td colspan="1" rowspan="1">50 autores tienen un libro asociado y 60 no tienenlibros asociados. La carga actual asigna un autor acada uno de los 50 libros. Requiere relacionar autor,libro_autor y libro.</td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">¿Cuántas editoriales estánregistradas?</td><td colspan="1" rowspan="1">30 editoriales.</td></tr><tr><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">¿Cuántas editoriales todavíano publican libros en elcatálogo de prueba?</td><td colspan="1" rowspan="1">11 editoriales. De las 30 cargadas, 19 se asignaron alos libros.</td></tr><tr><td colspan="1" rowspan="1">11</td><td colspan="1" rowspan="1">¿Cuántos libros integran elcatálogo?</td><td colspan="1" rowspan="1">50 libros.</td></tr><tr><td colspan="1" rowspan="1">12</td><td colspan="1" rowspan="1">¿Cuántos títulos comienzancon “El”?</td><td colspan="1" rowspan="1">18 títulos. La búsqueda debe considerar el comienzodel título, no las apariciones de “el” en otrasposiciones.</td></tr><tr><td colspan="1" rowspan="1">13</td><td colspan="1" rowspan="1">¿Cuántos      libros      sepublicaron en cada año delset?</td><td colspan="1" rowspan="1">Se esperan estos resultados: 2017: 4; 2018: 7; 2019:7;2020: 9; 2021: 8; 2022: 6; 2023: 5; 2024:4. Lasuma debe ser 50.</td></tr><tr><td colspan="1" rowspan="1">14</td><td colspan="1" rowspan="1">¿Qué editoriales tienen máslibros en este catálogo deprueba?</td><td colspan="1" rowspan="1">Alfaguara y HarperCollins, con 5 libros cada una. Esel máximo del set.</td></tr><tr><td colspan="1" rowspan="1">15</td><td colspan="1" rowspan="1">¿Hay libros sin autorasociado?</td><td colspan="1" rowspan="1">Ninguno. Cada libro tiene una asociación con unautor en libro_autor.</td></tr><tr><td colspan="1" rowspan="1">16</td><td colspan="1" rowspan="1">¿Hay libros sin ejemplaresregistrados?</td><td colspan="1" rowspan="1">Ninguno. Cada uno de los 50 libros recibió entre 1 y 3ejemplares.</td></tr><tr><td colspan="1" rowspan="1">17</td><td colspan="1" rowspan="1">¿Cuántos libros tienen uno,dos o tres ejemplares?</td><td colspan="1" rowspan="1">16 libros tienen uno; 17 tienen dos; 17 tienen tres. Entotal deben ser 50 libros. Requiere agrupar losejemplares por libro.</td></tr><tr><td colspan="1" rowspan="1">18</td><td colspan="1" rowspan="1">¿Cuántos ejemplares estánoperativos y cuántos enreparación?</td><td colspan="1" rowspan="1">97 operativos y 4 en reparación, sobre un total de101 ejemplares.</td></tr><tr><td colspan="1" rowspan="1">19</td><td colspan="1" rowspan="1">¿Qué      títulos      tienenejemplares en reparación?</td><td colspan="1" rowspan="1">El último tren de la memoria, Pequeño atlas de lanoche, Los nombres del bosque profundo y El mapade los pájaros azules. Cada uno tiene un ejemplar enreparación y conserva al menos uno operativo.</td></tr><tr><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">¿Qué libros tienen menosde tres ejemplares, paraevaluar si conviene ampliarel inventario?</td><td colspan="1" rowspan="1">33 libros: los 16 que tienen un ejemplar y los 17 quetienen dos. Los otros 17 ya cuentan con tresejemplares.</td></tr></table>

## Parte 6 · Consultas de negocio y análisis de resultados

Para resolverlas se utilizaron operaciones de selección y filtrado, combinaciones mediante JOIN y LEFT JOIN, funciones de agregación como COUNT, agrupamientos con GROUP BY, condiciones sobre grupos mediante HAVING y subconsultas. También se utilizaron EXISTS y NOT EXISTS para detectar registros relacionados o sin relación, como las editoriales sin libros asociados. Algunas consultas emplean tablas derivadas o subconsultas escalares para calcular cantidades intermedias.

Los resultados esperados del script corresponden al conjunto de pruebas cargadas. Entre ellos se encuentran 50 personas —45 socios y 5 bibliotecarios—, 55 teléfonos, 110 autores, 30 editoriales, 50 libros y 101 ejemplares. También se prevé identificar 11 editoriales sin libros, una distribución de ejemplares de 16 libros con una copia, 17 con dos y 17 con tres, y 33 libros con menos de tres ejemplares. Estos valores se utilizaron como referencia para revisar la salida de las consultas.

Durante esa validación, la consulta sobre editoriales sin libros devolvió inicialmente 41 registros, aunque el resultado esperado era 11. La revisión permitió detectar 30 registros de editoriales duplicados. Para tratarlos se preparó el archivo 08\_eliminar\_editoriales\_duplicadas.sql: selecciona las filas duplicadas más recientes, muestra previamente cuántos libros están asociados a cada una y elimina únicamente las que no tienen libros vinculados. El procedimiento incluye una comprobación posterior de la cantidad de registros, los nombres distintos y los posibles duplicados. Así, la corrección contempla tanto la calidad de los datos como la conservación de las relaciones existentes.

La revisión de los resultados tuvo en cuenta que los JOIN pueden multiplicar filas cuando intervienen relaciones de uno a muchos. Por eso, en las consultas que cuentan autores, libros o ejemplares se consideró qué entidad debía contarse y cuándo correspondía utilizar DISTINCT, una agregación previa o una subconsulta. Esta comprobación es necesaria para que los totales representen los registros de negocio y no las filas intermedias producidas por la combinación de tablas.

## 6.1. Relación entre las preguntas iniciales y las consultas de prueba

Las preguntas formuladas en la Parte 1 expresan las necesidades de información del negocio, incluyendo disponibilidad, circulación de ejemplares, vencimientos e historial de préstamos. Las veinte consultas de la Parte 5 se concentran en verificar la carga inicial, las asociaciones entre entidades y la composición del catálogo.

Ambos conjuntos cumplen funciones complementarias: las consultas de prueba permiten comprobar la consistencia de los datos, mientras que las preguntas iniciales orientan los informes de gestión. Las preguntas relacionadas con préstamos requieren contar con datos que representen operaciones pendientes, devueltas, vencidas y renovadas.

## 6.2. Informes que relacionan tres o más tablas

Para ampliar el análisis se definen los siguientes cinco informes, que requieren combinar información de tres o más tablas:

<table><tr><td rowspan=1 colspan=1>Informe</td><td rowspan=1 colspan=1>Tablas involucradas</td><td rowspan=1 colspan=1>Información que permite obtener</td></tr><tr><td rowspan=1 colspan=1>Catálogo con autores yeditoriales</td><td rowspan=1 colspan=1>libro,libro_autor, autor yeditorial</td><td rowspan=1 colspan=1>Identificar los autores de cada libro,respetando el orden de autoría, y su editorial.</td></tr><tr><td rowspan=1 colspan=1>Ejemplares disponibles porlibro y editorial</td><td rowspan=1 colspan=1>ejemplar, libro, editorial yprestamo</td><td rowspan=1 colspan=1>Identificar ejemplares operativos que notengan préstamos pendientes</td></tr><tr><td rowspan=1 colspan=1>Préstamos pendientes porsocio</td><td rowspan=1 colspan=1>prestamo,socio, persona,ejemplar y libro</td><td rowspan=1 colspan=1>Conocer quién tiene cada ejemplar, su títuloy la fecha de vencimiento vigente.</td></tr><tr><td rowspan=1 colspan=1>Préstamos registrados porbibliotecario</td><td rowspan=1 colspan=1>prestamo,         bibliotecario,persona, ejemplar y libro</td><td rowspan=1 colspan=1>Consultar las operaciones registradas porcada bibliotecario durante un período.</td></tr><tr><td rowspan=1 colspan=1>Librosmás prestadosdurante un período</td><td rowspan=1 colspan=1>prestamo, ejemplar, libro yeditorial</td><td rowspan=1 colspan=1>Contar los préstamos por libro e identificarlos títulos con mayor circulación.</td></tr></table>

En los informes de disponibilidad, la ausencia de préstamos pendientes debe comprobarse sin excluir los ejemplares que nunca fueron prestados. En los informes de circulación, los filtros temporales deben indicar expresamente el período analizado.

Cuando se incorporan autores a un informe de préstamos, un mismo préstamo puede aparecer en varias filas si el libro tiene varios autores. Por ello, los conteos deben realizarse sobre la entidad que se desea medir, utilizando una agregación previa o COUNT(DISTINCT id\_prestamo), según corresponda.

Se definieron cinco informes de negocio que combinan al menos tres tablas del modelo. Sus consultas permiten relacionar los datos bibliográficos, los ejemplares físicos, las personas y los préstamos. Para los informes que dependen de préstamos se debe indicar el período consultado y comprobar los resultados sobre los datos efectivamente cargados.

Informe 1. Catálogo con autores y editoriales. Permite conocer la editorial y los autores de cada libro. GROUP\_CONCAT presenta a los autores según orden\_autoria sin repetir el libro en la salida.

SELECT

```sql
l.id_libro,
l.titulo,
e.nombre AS editorial,
GROUP_CONCAT(
CONCAT(a.apellido, ', ', a.nombre)
ORDER BY la.orden_autoria
SEPARATOR '; '
) AS autores
FROM libro AS l
JOIN editorial AS e ON e.id_editorial = l.id_editorial
JOIN libro_autor AS la ON la.id_libro = l.id_libro
JOIN autor AS a ON a.id_autor = la.id_autor
GROUP BY l.id_libro, l.titulo, e.id_editorial, e.nombre
ORDER BY l.titulo;
```

Informe 2. Ejemplares disponibles por libro y editorial. Un ejemplar está disponible si se encuentra operativo y no posee un préstamo pendiente. La condición sobre prestamo se coloca en el JOIN para conservar los ejemplares que nunca fueron prestados.

Informe 3. Préstamos pendientes por socio. Muestra el socio, el ejemplar prestado, el título y la fecha de vencimiento vigente.

SELECT pr.id\_prestamo, pe.documento, pe.apellido,

pe.nombre, ej.codigo\_inventario, l.titulo, pr.fecha\_prestamo, pr.fecha\_vencimiento\_actual FROM prestamo AS pr JOIN socio AS s ON s.id\_persona = pr.id\_socio JOIN persona AS pe ON pe.id\_persona = s.id\_persona JOIN ejemplar AS ej ON ej.id\_ejemplar = pr.id\_ejemplar JOIN libro AS l ON l.id\_libro = ej.id\_libro WHERE pr.fecha\_devolucion IS NULL ORDER BY pr.fecha\_vencimiento\_actual, pe.apellido; Para los dos informes siguientes se establece el período mediante variables de sesión: SET @desde = '2026-01-01'; SET @hasta = '2026-12-31';

Informe 4. Bibliotecarios que registraron al menos dos préstamos durante el período. La   
agrupación cuenta operaciones de préstamo, y HAVING selecciona a quienes alcanzaron el   
mínimo definido. SELECT b.id\_persona AS id\_bibliotecario, pe.apellido, pe.nombre, COUNT(pr.id\_prestamo) AS prestamos\_registrados FROM prestamo AS pr JOIN bibliotecario AS b ON b.id\_persona = pr.id\_bibliotecario JOIN persona AS pe ON pe.id\_persona = b.id\_persona JOIN ejemplar AS ej ON ej.id\_ejemplar = pr.id\_ejemplar JOIN libro AS l ON l.id\_libro = ej.id\_libro WHERE pr.fecha\_prestamo BETWEEN @desde AND @hasta GROUP BY b.id\_persona, pe.apellido, pe.nombre HAVING COUNT(pr.id\_prestamo) >= 2 ORDER BY prestamos\_registrados DESC, pe.apellido;   
Informe 5. Libros más prestados durante el período. Cuenta los préstamos por libro y   
ordena los títulos según su circulación. La combinación utilizada no incluye la tabla de   
autores, que podría multiplicar las filas correspondientes a un préstamo. SELECT l.id\_libro,

l.titulo,

ed.nombre AS editorial,

COUNT(pr.id\_prestamo) AS cantidad\_prestamos

FROM prestamo AS pr

JOIN ejemplar AS ej ON ej.id\_ejemplar = pr.id\_ejemplar

JOIN libro AS l ON l.id\_libro = ej.id\_libro

JOIN editorial AS ed ON ed.id\_editorial = l.id\_editorial

WHERE pr.fecha\_prestamo BETWEEN @desde AND @hasta

GROUP BY l.id\_libro, l.titulo, ed.id\_editorial, ed.nombre

ORDER BY cantidad\_prestamos DESC, l.titulo;

Resultado esperado de cada informe: (1) una fila por libro que tenga autores asociados, con su editorial y la lista ordenada de autores; (2) una fila por ejemplar operativo sin préstamo activo; (3) una fila por préstamo activo, con su socio, ejemplar y vencimiento; (4) una fila por bibliotecario que haya registrado al menos dos préstamos entre @desde y @hasta; (5) una fila por libro con préstamos en ese período, ordenada de mayor a menor circulación. Los informes 4 y 5 usan las fechas definidas antes de sus sentencias.

Si la tabla prestamo permanece vacía, los informes 3, 4 y 5 no devolverán filas. Esa salida representa la ausencia de operaciones en el conjunto de prueba y no un error de las consultas.

## 6.3. Verificación de resultados

Verificación de resultados

Se ejecutó la siguiente consulta

```sql
SELECT concepto, esperado, obtenido,
IF(esperado = obtenido, 'Coincide', 'Revisar') AS conclusion
FROM (
SELECT 'Personas registradas' AS concepto, 50 AS esperado,
(SELECT COUNT(*) FROM persona) AS obtenido
UNION ALL
SELECT 'Socios registrados', 45, (SELECT COUNT(*) FROM socio)
```

```sql
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
```

Se ejecutaron las consultas de control sobre la base de datos luego de la carga de prueba y de la limpieza de editoriales. Los resultados obtenidos coincidieron con los valores esperados: 50 personas, 45 socios, 5 bibliotecarios, 30 editoriales, 11 editoriales sin libros, 50 libros, 101 ejemplares y 4 ejemplares en reparación.

La verificación específica de editoriales mostró 30 registros, 30 nombres distintos y ningún nombre repetido en el conjunto de prueba. Al ejecutar nuevamente la consulta de editoriales sin libros, el resultado fue 11. De esta manera, la diferencia inicial de 41 registros quedó resuelta mediante la eliminación de las 30 filas duplicadas sin libros asociados.

Estos controles comprueban la concordancia de las cantidades generales del conjunto de prueba. No sustituyen la revisión individual de las relaciones y de las reglas de negocio que el esquema SQL no garantiza por sí solo.

## 6.4. Análisis del plan de ejecución y optimización

La evaluación del rendimiento se documenta mediante EXPLAIN sobre una consulta seleccionada. Se compara su plan de ejecución antes y después de aplicar una modificación justificada, manteniendo el mismo conjunto de datos y verificando que ambas versiones produzcan resultados equivalentes.

EXPLAIN permite observar el orden de acceso a las tablas, los índices considerados y utilizados, el tipo de acceso y la estimación de filas examinadas. Estas estimaciones permiten fundamentar una optimización, pero no constituyen por sí solas una medición del tiempo real de ejecución.

La modificación aplicada debe responder al plan observado: por ejemplo, ajustar un filtro o incorporar un índice adecuado a las condiciones de búsqueda y combinación. Antes de crear un índice se revisan los ya existentes para evitar duplicaciones.

Con una base pequeña, el optimizador puede preferir recorrer una tabla completa. Por ese motivo, la conclusión debe describir lo que muestra la evidencia, sin afirmar una mejora de rendimiento únicamente por haber agregado un índice.

Conclusión de la comparación: Se analizó el plan de ejecución de la consulta que identifica los libros con ejemplares en reparación. Después de incorporar el índice "ix\_ejemplar\_estado", el plan utilizó ese índice para localizar los ejemplares cuyo estado es "en\_reparacion" y estimó examinar menos filas que en el plan inicial. La consulta mantuvo el mismo resultado: cuatro ejemplares en reparación asociados a los mismos títulos. La comparación evidencia un cambio favorable en el acceso a los datos, pero no demuestra por sí sola una reducción del tiempo de ejecución. Dado el tamaño reducido del conjunto de prueba, esa mejora requeriría mediciones adicionales sobre un volumen mayor de datos.

## 6.5. Comparación de consultas propias y asistidas por IA

Se tomó como consulta propia la incluida en 07\_consultas\_20\_preguntas\_biblioteca.sql para contar las editoriales que no tienen libros asociados. La consulta utiliza NOT EXISTS:

```sql
SELECT COUNT(*) AS editoriales_sin_libros
FROM editorial AS e
WHERE NOT EXISTS (
SELECT 1
FROM libro AS l
WHERE l.id_editorial = e.id_editorial
);
```

Como alternativa elaborada con asistencia de IA, se propuso resolver la misma pregunta mediante LEFT JOIN:

SELECT COUNT(\*) AS editoriales\_sin\_libros

FROM editorial AS e

LEFT JOIN libro AS l ON l.id\_editorial = e.id\_editorial

WHERE l.id\_libro IS NULL;

Este caso mostró que revisar una consulta exige distinguir la lógica de la sentencia de la calidad de los datos. La diferencia inicial entre 41 y 11 se resolvió corrigiendo la carga duplicada, no reemplazando NOT EXISTS por otra forma de consulta.

## Parte 7 · Integración de la base de datos con Python e inteligencia artificial

En esta etapa se integró la base de datos de la biblioteca con componentes de software que permiten consultarla desde Python y desde una interfaz gráfica. El trabajo comprende la incorporación de un servidor MCP, la ejecución de consultas SQL desde el código, el uso de consultas parametrizadas y la definición de permisos diferenciados para los usuarios.

## 7.1. Integración mediante MCP

El proyecto incorpora un servidor MCP en mcp\_server.py, implementado con FastMCP y denominado Biblioteca. Su finalidad es ofrecer a un cliente compatible un conjunto definido de herramientas de consulta. El servidor se inicia mediante mcp.run(transport="stdio"), por lo que se comunica con el cliente a través de la entrada y salida estándar del proceso.

El servidor registra seis herramientas:
<table><tr><td rowspan=1 colspan=1>Herramienta MCP</td><td rowspan=1 colspan=1>Operación delegada</td><td rowspan=1 colspan=1>Respuesta</td></tr><tr><td rowspan=1 colspan=1>buscar_libros(titulo)</td><td rowspan=1 colspan=1>search_books</td><td rowspan=1 colspan=1>Cantidad y lista de libros cuyos títuloscoinciden con el criterio.</td></tr><tr><td rowspan=1 colspan=1>buscar_libros_por_autor(autor)</td><td rowspan=1 colspan=1>search books by author</td><td rowspan=1 colspan=1>Cantidad y lista de libros encontrados porautor.</td></tr><tr><td rowspan=1 colspan=1>buscar_socios(criterio)</td><td rowspan=1 colspan=1>search_members</td><td rowspan=1 colspan=1>Cantidad y lista de socios encontrados.</td></tr><tr><td rowspan=1 colspan=1>consultar_disponibilidad(id_libro)</td><td rowspan=1 colspan=1>get_book_availability</td><td rowspan=1 colspan=1>Cantidades de ejemplares de un libro segúnsu disponibilidad y estado.</td></tr><tr><td rowspan=1 colspan=1>listar_prestamos_vencidos()</td><td rowspan=1 colspan=1>list_overdue_loans</td><td rowspan=1 colspan=1>Cantidad y lista de préstamos activosvencidos.</td></tr><tr><td rowspan=1 colspan=1>obtener_estadisticas_biblioteca()</td><td rowspan=1 colspan=1>get_library_statistics</td><td rowspan=1 colspan=1>Cantidades generales de libros, ejemplares,socios y préstamos.</td></tr></table>

El servidor está planteado como una interfaz de solo lectura: no expone una herramienta para enviar SQL arbitrario ni registra operaciones de alta, modificación o eliminación. Además, cada herramienta se anuncia con anotaciones de lectura (readOnlyHint) y como no destructiva. Estas anotaciones describen su propósito al cliente; la garantía efectiva depende también de lo que hagan las funciones de consulta invocadas y de los permisos de la conexión a la base de datos.

En el tratamiento de errores, \_read devuelve el mensaje de los errores de validación (ValueError) y una respuesta genérica ante errores de SQLAlchemy u otras excepciones. La configuración mask\_error\_details=True evita exponer detalles internos del servidor al cliente.

Los roles admin y user de la interfaz web no aparecen aplicados en mcp\_server.py. Por ello, el acceso al servidor MCP debe analizarse como una vía de acceso distinta de la interfaz web, especialmente porque la herramienta buscar\_socios consulta datos de personas.

## 7.2. Conexión de Python con MySQL y ejecución de consultas

La función "get\_db()" entrega una sesión y garantiza su cierre mediante un bloque "finally". El servidor MCP utiliza esa misma fábrica de sesiones dentro de un bloque "with", por lo que cada operación cierra su sesión al terminar.

Las consultas se implementan en "library\_queries.py" mediante expresiones de SQLAlchemy. El programa permite buscar libros por título o autor, buscar socios, consultar la disponibilidad de ejemplares, listar préstamos vencidos y obtener estadísticas generales. Por ejemplo, "list\_overdue\_loans()" relaciona préstamos, socios, personas, ejemplares y libros para mostrar los préstamos activos cuya fecha de vencimiento ya pasó. "get\_book\_availability()" calcula los ejemplares totales, disponibles, prestados y en reparación de un libro.

Así, las operaciones de consulta se ejecutan desde Python y devuelven datos estructurados que pueden utilizarse desde el servidor MCP. El código examinado acredita estas consultas implementadas en la aplicación; no permite afirmar que se hayan reproducido desde Python todas las consultas del archivo SQL de la parte 6.

## 7.3. Consultas parametrizadas e inyección SQL

La inyección SQL ocurre cuando un dato ingresado por una persona se incorpora como parte de una sentencia SQL y llega a modificar su estructura. Por ejemplo, concatenar directamente el texto de una búsqueda dentro de una consulta puede permitir que ese texto altere las condiciones previstas por el programa.

Las búsquedas por título, autor y socio también utilizan "autoescape=True". Esto hace que caracteres especiales de los patrones de búsqueda, como "%" y "\_", se traten como caracteres literales cuando aparecen en el criterio ingresado. Además, esas funciones eliminan espacios al comienzo y al final y rechazan criterios vacíos con "ValueError".

## 7.4. Interfaz gráfica de gestión

El proyecto incorpora una interfaz gráfica básica para operar sobre la base de datos de la biblioteca. La aplicación permite realizar altas y consultas y, según el perfil habilitado, otras operaciones de gestión. La interfaz se comunica con el servidor de la aplicación, que ejecuta las operaciones correspondientes sobre MySQL.

La separación entre interfaz, lógica de aplicación y base de datos permite que los datos no se modifiquen directamente desde la página. El servidor recibe las solicitudes, aplica las reglas de acceso y utiliza la conexión a MySQL para completar la operación.

## 7.5. Usuarios, roles y permisos

El acceso a las funciones se organiza mediante dos roles:

<table><tr><td rowspan=1 colspan=1>Usuario</td><td rowspan=1 colspan=1>Permisos</td></tr><tr><td rowspan=1 colspan=1>admin</td><td rowspan=1 colspan=1>Acceso completo a las funciones de gestión, incluidas las operaciones de alta, consulta,modificación y eliminación.</td></tr><tr><td rowspan=1 colspan=1>user</td><td rowspan=1 colspan=1>Acceso de consulta. Puede visualizar información, pero no crear, modificar ni eliminar registros.</td></tr></table>

La aplicación utiliza el rol para determinar qué operaciones puede realizar cada usuario. Las funciones de escritura deben quedar restringidas tanto en la interfaz como en la lógica del servidor, de modo que ocultar un botón no sea la única medida de protección. Así, una solicitud de modificación enviada directamente al servidor también debe ser rechazada cuando proviene de un usuario con permisos de solo lectura.

## 7.6. Resultado de la integración

La integración reúne en un mismo proyecto la base de datos MySQL, las consultas SQL, la aplicación Python, la interfaz gráfica y el servidor MCP. Esto permite consultar y gestionar la información de la biblioteca desde la aplicación y exponer operaciones seleccionadas a clientes compatibles con MCP.

El desarrollo también permite observar la importancia de separar responsabilidades: MySQL conserva y relaciona los datos; Python implementa la lógica de acceso; la interfaz presenta las funciones a las personas usuarias; el control de roles limita las operaciones; y MCP ofrece una vía estandarizada para que una aplicación de inteligencia artificial utilice las herramientas expuestas por el sistema.

## Parte 8 · Resumen y conclusión general del trabajo

## 8.1. Resumen del proyecto

El trabajo integrador abordó el desarrollo de un sistema de gestión de biblioteca, desde el análisis de las necesidades del caso hasta la implementación de una base de datos relacional y su integración con una aplicación en Python.

En las primeras etapas se definieron las reglas de negocio y se identificaron las entidades, sus atributos y sus relaciones. A partir de este análisis se elaboró el diagrama entidad-relación en DrawDB, estableciendo claves primarias y foráneas, cardinalidades y restricciones de integridad.

Luego se revisó y refactorizó el modelo para reducir redundancias y representar adecuadamente los datos. Entre las decisiones centrales se destacó la distinción entre libro y ejemplar, necesaria para diferenciar la información bibliográfica de las unidades físicas disponibles para préstamo. Las relaciones de muchos a muchos se resolvieron mediante entidades asociativas.

El modelo se implementó en MySQL mediante scripts SQL y se verificó utilizando DBeaver. Posteriormente, se incorporaron datos de prueba y se formularon veinte preguntas de negocio, que permitieron relacionar las necesidades de información de la biblioteca con consultas sobre la base de datos. Se trabajó con filtros, relaciones entre tablas, funciones de agregación, agrupamientos y subconsultas.

Finalmente, se integró la base de datos con una aplicación en Python, utilizando FastAPI y una interfaz web básica. Esta etapa incluyó operaciones de gestión y consulta, consultas parametrizadas para prevenir la inyección SQL y controles de acceso que distinguen las acciones permitidas para el administrador y para el usuario de consulta. También se incorporó un servidor MCP como mecanismo para exponer funciones del proyecto a herramientas de inteligencia artificial compatibles.

## 8.2. La inteligencia artificial como herramienta de apoyo

La inteligencia artificial acompañó distintas etapas del proceso: interpretación del caso, revisión del modelo, elaboración de consultas, asistencia en la programación y redacción de la documentación.

Su utilización requirió contrastar las propuestas con las reglas de negocio, el esquema implementado y los resultados obtenidos. Esto permitió reconocer que una respuesta generada por IA puede ser útil como punto de partida, pero necesita revisión técnica antes de incorporarse al proyecto.

El trabajo también mostró la importancia de formular instrucciones precisas, proporcionar contexto y verificar las modificaciones sugeridas. La responsabilidad sobre las decisiones de diseño y la validez de los resultados corresponde a quienes desarrollan el sistema.

## 8.3. Conclusión general

El proyecto permitió integrar los contenidos de la asignatura mediante un caso práctico que vinculó el análisis de un problema, el modelado de datos, la implementación en SQL y el desarrollo de una aplicación.

Uno de los principales aprendizajes fue comprender que la calidad de un sistema depende de la coherencia entre sus reglas de negocio, su modelo de datos y las operaciones que ofrece. Las claves, las relaciones y las restricciones contribuyen a preservar la integridad de la información, mientras que las consultas permiten transformar los datos almacenados en respuestas útiles para la gestión.

La conexión con Python permitió observar cómo una base de datos se integra en una aplicación y por qué resulta necesario controlar tanto la ejecución de las consultas como los permisos de los usuarios. Asimismo, la incorporación de MCP permitió explorar una forma de interacción entre el sistema y herramientas de inteligencia artificial.

Como resultado, se obtuvo una implementación académica que reúne las principales etapas del desarrollo de un sistema basado en datos. Su evaluación debe apoyarse en evidencias reproducibles: scripts, consultas, resultados y pruebas de funcionamiento. Las mejoras de rendimiento, en particular, requieren comparar planes de ejecución y mediciones antes de afirmar que una optimización fue efectiva.

El trabajo consolidó una metodología de desarrollo basada en analizar, modelar, implementar, verificar y documentar, utilizando la inteligencia artificial como apoyo y manteniendo el criterio técnico como fundamento de las decisiones.