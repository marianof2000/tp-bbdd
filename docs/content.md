## TFI Fundamentos de Bases de Datos

TFI Fundamentos de Bases de Datos.   
Parte 1 · Selección del proyecto e identificación del problema. 2   
1.1. Caso de negocio. 2   
1.2. Entidades, propiedades y tipos de datos. 2   
1.3. Justificación de los tipos de datos. .3   
1.4. Relaciones identificadas. .4   
1.5. Reglas del negocio para dejar asentadas. . 4   
1.6 Preguntas de negocio. . 5   
Parte 2 · Modelado en DrawDB con asistencia de IA. . 6   
2.1. Objetivo. . 6   
2.2. Entidades del modelo. .6   
2.3. Relaciones, cardinalidad y participación. . 7   
2.4. Prompts utilizados para el modelado. . 8   
Prompt 1 · Crear las entidades y sus atributos. . 8   
Prompt 2 · Incorporar las relaciones. . 8   
Prompt 3 · Revisar críticamente el diagrama. . 9   
2.5. Revisión humana y decisiones. .10   
2.6. Diagrama del modelo inicial. 10   
Parte 3 - Refactorización del modelo. . 11   
3.1. Revisión de claves primarias, candidatas y alternativas. 11   
3.2. Revisión y resolución de la jerarquía. 13   
3.2.1 Estructura propuesta. . 13   
3.2.2 Restricciones de la jerarquía. .14   
3.2.3 Relaciones con el resto del modelo. 14   
3.2.4 Representación en DrawDB. ..14   
3.3. Normalización del modelo hasta tercera forma normal. ..14   
3.3.1. Primera forma normal. ..15   
3.3.2. Segunda forma normal. ..15   
3.3.3. Tercera forma normal. 15   
3.3.4. Conservación de información histórica.. 16   
3.4. Reglas de integridad y borrado. . 17   
3.4.1. Reglas de borrado.. ..17   
3.4.2. Otras reglas de integridad. . 18   
3.5. Auditoría del modelo con IA y decisiones adoptadas. ..18   
3.5.1. Prompt de auditoría. .18   
3.5.2. Hallazgos y revisión humana. 19   
3.6. Diagrama definitivo y síntesis de las decisiones de diseño. 20   
3.6.1. Esquema de referencia para el diagrama. 20   
3.6.2. Síntesis de las decisiones. . 22   
Parte 4 · Creación de la base en DBeaver. 23   
4.1. Objetivo. . 23   
4.2. Preparación del script.. .23   
4.3. Restricciones e integridad.. .23   
4.4. Orden y ejecución en DBeaver. 24   
4.5. Verificación de la estructura.. . 24   
4.6. Uso de IA y correcciones.. 25   
4.7. Resultado y controles pendientes. 26

## Parte 1 · Selección del proyecto e identificación del problema

## 1.1. Caso de negocio

El proyecto consiste en diseñar una base de datos para la biblioteca. La biblioteca posee libros registrados con ninguno, uno o más ejemplares físicos. Por lo que puede registrarse un libro antes de incorporar sus copias a la biblioteca.

También registra a sus socios y administra los préstamos. Un bibliotecario registra cada préstamo y su devolución.

El problema que se busca resolver es la dispersión de la información sobre el catálogo, los ejemplares y la circulación de libros. La base de datos deberá permitir identificar qué ejemplar se prestó, a quién, cuándo debe devolverse y si ya fue devuelto, además de consultar autores y editoriales.

Cuando un libro ingresa a la biblioteca, se registra su información bibliográfica, editorial y autores. Cada copia física se registra como un ejemplar con un código de inventario único. Los socios pueden solicitar ejemplares disponibles; un bibliotecario registra cada préstamo, su fecha y su vencimiento. Al devolver el ejemplar, se registra la fecha de devolución. Si se renueva el plazo, se actualiza el vencimiento actual y se conserva el vencimiento inicial. Un ejemplar no puede estar prestado simultáneamente a dos socios.

Alcance: cada préstamo corresponde a un ejemplar. Si un socio retira tres ejemplares al mismo tiempo, se registran tres préstamos. Esta regla mantiene sencillo el modelo inicial.

1.2. Entidades, propiedades y tipos de datos
<table><tr><td colspan="1" rowspan="1">Entidad</td><td colspan="1" rowspan="1">Propiedades propuestas</td><td colspan="1" rowspan="1">Clave primaria (PK) y motivo</td></tr><tr><td colspan="1" rowspan="1">Socio</td><td colspan="1" rowspan="1">id_socio     BIGINT     UNSIGNED,    nombreVARCHAR(80),     apellido      VARCHAR(80),documento          VARCHAR(20),         emailVARCHAR(254),fecha_alta DATEIME</td><td colspan="1" rowspan="1">id_socio: identifica de formaestable al socio aunque cambiesu correo o se corrija sudocumento.</td></tr><tr><td colspan="1" rowspan="1">Bibliotecario</td><td colspan="1" rowspan="1">id_bibliotecario BIGINT UNSIGNED, nombreVARCHAR(80), apellido VARCHAR(80), legajoVARCHAR(30)</td><td colspan="1" rowspan="1">id_bibliotecario: mantienela identidad del empleadoaunque cambie su legajo.</td></tr><tr><td colspan="1" rowspan="1">Editorial</td><td colspan="1" rowspan="1">id_editorial   BIGINT   UNSIGNED,nombreVARCHAR(120)</td><td colspan="1" rowspan="1">id_editorial:      distingueeditorialesaunque  existannombres similares o cambiende denominación.</td></tr><tr><td colspan="1" rowspan="1">Autor</td><td colspan="1" rowspan="1">id_autor     BIGINT     UNSIGNED,    nombreVARCHAR(80), apellido VARCHAR(80)</td><td colspan="1" rowspan="1">id_autor: distingue personasque pueden compartir nombre yapellido.</td></tr><tr><td colspan="1" rowspan="1">Libro</td><td colspan="1" rowspan="1">id_libro     BIGINT     UNSIGNED,    tituloVARCHAR(200),       isbn        VARCHAR(17),anio_publicacion SMALLBIGINT  UNSIGNED,id_editorial BIGINT UNSIGNED</td><td colspan="1" rowspan="1">id_libro: identifica el registrobibliográfico; el ISBN puedefaltar o requerir corrección.</td></tr><tr><td colspan="1" rowspan="1">Ejemplar</td><td colspan="1" rowspan="1">id_ejemplar  BIGINT   UNSIGNED, id_libroBIGINT      UNSIGNED,     codigo_inventarioVARCHAR(40),fecha_incorporacion DATEIME</td><td colspan="1" rowspan="1">id_ejemplar: identifica unacopia física específica. Dosejemplares del mismo librotienen identificadores distintos.</td></tr><tr><td colspan="1" rowspan="1">Prestamo</td><td colspan="1" rowspan="1">id_prestamo  BIGINT  UNSIGNED,id_socioBIGINT   UNSIGNED,id_ejemplar   BIGINTUNSIGNED,      id_bibliotecario       BIGINTUNSIGNED,      fecha_prestamo       DATEIME,fecha_vencimiento_inicial          DATEIME,fecha vencimiento actual            DATEIME,fecha devolucion DATEIME</td><td colspan="1" rowspan="1">id_prestamo: distingue lassucesivas ocasiones en que sepresta un mismo ejemplar.</td></tr><tr><td colspan="1" rowspan="1">LibroAutor</td><td colspan="1" rowspan="1">id_libro    BIGINT    UNSIGNED,  id_autorBIGINT         UNSIGNED,        orden_autoriaSMALLBIGINT UNSIGNED</td><td colspan="1" rowspan="1">PK compuesta (id_libro,id_autor): evita asociar dosveces al mismo autor con elmismo libro.</td></tr><tr><td colspan="1" rowspan="1">TelefonoSocio</td><td colspan="1" rowspan="1">id_socio     BIGINT     UNSIGNED,    numeroVARCHAR(25),tipo VARCHAR(20)</td><td colspan="1" rowspan="1">PK compuesta (id_socio,numero):permite  variosteléfonos por socio sin repetir elmismo número para ese socio.</td></tr></table>

Los campos id\_... que apuntan a otra entidad serán claves foráneas (FK). Por ejemplo, Ejemplar.id\_libro referencia a Libro.id\_libro.

## 1.3. Justificación de los tipos de datos

BIGINT UNSIGNED: identificadores enteros positivos; no representan cantidades del negocio.

VARCHAR: textos de longitud variable. El documento, el ISBN, el legajo, el código de inventario y el teléfono se almacenan como texto porque son identificadores: no tiene sentido sumarlos y pueden contener ceros iniciales, letras o separadores.

DATEIME: fechas para las que, en este alcance, no es necesario registrar la hora.

SMALLBIGINT UNSIGNED: valores enteros no negativos y acotados, como el año de publicación y el orden de autoría.

fecha\_devolucion podrá quedar vacía mientras el ejemplar no haya sido devuelto. El dato histórico será fecha\_vencimiento\_inicial: si se concede una renovación, se modifica fecha\_vencimiento\_actual, pero se conserva la fecha acordada originalmente.

## 1.4. Relaciones identificadas

La participación se expresa como 0..N (cero o muchos), 1..N (uno o muchos) y 1..1 (exactamente uno).

<table><tr><td rowspan=1 colspan=1>Relación expresadacon verbo</td><td rowspan=1 colspan=1>Cardinalidad y participación</td></tr><tr><td rowspan=1 colspan=1>Una           editorialpublica libros.</td><td rowspan=1 colspan=1>Una editorial puede publicar 0. .N libros registrados; cada librocorresponde a 1 . .1 editorial.</td></tr><tr><td rowspan=1 colspan=1>Un   libro   poseeejemplares.</td><td rowspan=1 colspan=1>Un libro puede tener 0. .N ejemplares registrados; cada ejemplarcorresponde a 1 . .1 libro.</td></tr><tr><td rowspan=1 colspan=1>Un autor escribelibros.</td><td rowspan=1 colspan=1>Un autor puede estar asociado a 0 . .N libros; un libro tiene 1 . .Nautores. Es una relación N:M resuelta mediante LibroAutor,que además registra el orden de autoría.</td></tr><tr><td rowspan=1 colspan=1>Un socio solicitapréstamos.</td><td rowspan=1 colspan=1>Un socio puede realizar 0..N préstamos; cada préstamocorresponde a 1. .1 socio.</td></tr><tr><td rowspan=1 colspan=1>Un      bibliotecarioregistra préstamos.</td><td rowspan=1 colspan=1>Un bibliotecario puede registrar 0 . .N préstamos; cada préstamoes registrado por 1 . .1 bibliotecario.</td></tr><tr><td rowspan=1 colspan=1>Un            ejemplarparticipa            enpréstamos.</td><td rowspan=1 colspan=1>Un ejemplar puede tener 0. .N préstamos a lo largo del tiempo;cada préstamo corresponde a 1 . .1 ejemplar.</td></tr><tr><td rowspan=1 colspan=1>Un socio registrateléfonos.</td><td rowspan=1 colspan=1>Un socio puede registrar 0..N teléfonos; cada registro deteléfono pertenece a 1 . .1 socio.</td></tr></table>

## 1.5. Reglas del negocio para dejar asentadas

1. codigo\_inventario debe ser único: identifica cada copia física dentro de la biblioteca.

2. Un mismo ejemplar no puede tener dos préstamos sin devolver al mismo tiempo, aunque sí puede acumular muchos préstamos a lo largo de su historia.

3. Un libro debe tener al menos un autor para considerarse completo en el catálogo. Esa exigencia deberá controlarse al cargar los datos.

4. La disponibilidad de un ejemplar se obtiene de sus préstamos sin fecha\_devolucion; no hace falta duplicarla en un campo que pueda quedar desactualizado.

5. Los teléfonos múltiples se separan en TelefonoSocio para evitar columnas repetidas como telefono\_1 y telefono\_2.

## 1.6 Preguntas de negocio

Las siguientes preguntas permiten verificar que el modelo almacena la información necesaria para gestionar el catálogo, los ejemplares, los socios y la circulación de libros.

1. ¿Qué libros integran el catálogo y quiénes son sus autores, en el orden de autoría registrado?

2. ¿Qué libros pertenecen a una editorial determinada?

3. ¿Cuántos ejemplares tiene registrados la biblioteca de cada libro?

4. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ ejemplares están disponibles para prestar, considerando su estado y la ausencia de préstamos pendientes?

5. ¿Qué ejemplares se encuentran en reparación y a qué libros corresponden?

6. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ socios tienen préstamos pendientes de devolución?

7. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ préstamos están vencidos y pendientes de devolución a la fecha de consulta?

8. ¿Qué préstamos pendientes vencen dentro de los próximos siete días?

9. ¿Cuál es el historial de préstamos de un socio determinado?

10. ¿Cuál es el historial de préstamos de un ejemplar determinado?

11. $\therefore \angle u \dot { \boldsymbol { \Theta } }$ préstamos registró un bibliotecario durante un período determinado?

12. ¿Cuántos préstamos se registraron por mes durante un año determinado?

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

<table><tr><td colspan="1" rowspan="1">Entidad</td><td colspan="1" rowspan="1">Significado e identificador</td></tr><tr><td colspan="1" rowspan="1">socio</td><td colspan="1" rowspan="1">Persona que puede solicitar préstamos. Identificador: id_socio.</td></tr><tr><td colspan="1" rowspan="1">telefono_socio</td><td colspan="1" rowspan="1">Número de contacto informado por un socio. Identificador:id_telefono_socio.</td></tr><tr><td colspan="1" rowspan="1">bibliotecari0</td><td colspan="1" rowspan="1">Persona que registra el préstamo. Identificador: id_bibliotecario.</td></tr><tr><td colspan="1" rowspan="1">editorial</td><td colspan="1" rowspan="1">Editorial que publica libros. Identificador: id_editorial.</td></tr><tr><td colspan="1" rowspan="1">autor</td><td colspan="1" rowspan="1">Persona autora de libros. Identificador: id_autor.</td></tr><tr><td colspan="1" rowspan="1">libro</td><td colspan="1" rowspan="1">Registro bibliográfico, independiente de sus copias físicas.Identificador: id_libro.</td></tr><tr><td colspan="1" rowspan="1">libro_autor</td><td colspan="1" rowspan="1">Asociación entre un libro y un autor; guarda orden_autoria.Identificador compuesto: id_libro e id_autor.</td></tr><tr><td>ejemplar</td><td>Copia física identificada por un código de inventario. Identificador: id_ejemplar.</td></tr><tr><td>prestamo</td><td>Entrega de un ejemplar a un socio. Identificador: id_prestamo.</td></tr></table>

libro\_autor resuelve la relación N:M: un libro puede tener varios autores y un autor puede participar en varios libros. Su atributo propio, orden\_autoria, expresa la posición que ocupa un autor en un libro determinado.

## 2.3. Relaciones, cardinalidad y participación

<table><tr><td colspan="1" rowspan="1">Relación</td><td colspan="1" rowspan="1">Lectura del negocio</td></tr><tr><td colspan="1" rowspan="1">socio — registratelefono_socio</td><td colspan="1" rowspan="1">Un socio puede registrar 0..N teléfonos. Cada teléfonoregistrado pertenece a 1..1 socio.</td></tr><tr><td colspan="1" rowspan="1">editorial — publica —libro</td><td colspan="1" rowspan="1">Una editorial puede tener 0.N libros registrados. Cada libropertenece a 1..1 editorial.</td></tr><tr><td colspan="1" rowspan="1">libro一  poseeejemplar</td><td colspan="1" rowspan="1">Un libro puede tener 0..N ejemplares registrados. Cadaejemplar corresponde a 1..1 libro.</td></tr><tr><td colspan="1" rowspan="1">libro           tienelibro_autor</td><td colspan="1" rowspan="1">Un libro debe asociarse con 1..N autores según la regla delnegocio. Cada fila de libro_autor corresponde a 1..1libro.</td></tr><tr><td colspan="1" rowspan="1">autor — participa en —libro_autor</td><td colspan="1" rowspan="1">Un autor puede asociarse con 0..N libros. Cada fila delibro_autor corresponde a 1..1 autor.</td></tr><tr><td colspan="1" rowspan="1">socio         realizaprestamo</td><td colspan="1" rowspan="1">Un socio puede realizar 0..N préstamos. Cada préstamocorresponde a 1..1 socio.</td></tr><tr><td colspan="1" rowspan="1">ejemplar — participa en—prestamo</td><td colspan="1" rowspan="1">Un ejemplar puede tener 0..N préstamos a lo largo deltiempo. Cada préstamo corresponde a 1..1 ejemplar.</td></tr><tr><td>bibliotecario registra —prestamo</td><td>Un bibliotecario puede registrar 0..N préstamos. Cada préstamo es registrado por 1..1 bibliotecario.</td></tr></table>

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

prestamo: id\_prestamo, id\_socio, id\_ejemplar, id\_bibliotecario, fecha\_prestamo,

fecha\_vencimiento\_inicial, fecha\_vencimiento\_actual, fecha\_devolucion.

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

8. bibliotecario registra prestamo: bibliotecario 0..N; cada prestamo corresponde a 1..1 bibliotecario.

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

5. Preguntas que todavía habría que resolver con el responsable de la biblioteca.

Para cada hallazgo, citá la entidad o relación afectada y explicá por qué es un problema. Diferenciá entre un error comprobado y una regla que DrawDB simplemente no permite verificar. No reescribas el modelo: proponé observaciones para que yo decida cuáles aceptar.

## 2.5. Revisión humana y decisiones

La respuesta de la IA debe contrastarse con la descripción del negocio. Para este caso, las decisiones que deben conservarse son:

● libro y ejemplar representan conceptos distintos.

● libro\_autor resuelve la N:M y conserva orden\_autoria.

● No se agregan procesos de bajas, multas ni pagos.

● La disponibilidad de un ejemplar no se confunde con su estado físico: debe estar operativo y no tener un préstamo pendiente.

El mínimo de un autor por libro es una regla del negocio. La relación dibujada puede expresarla conceptualmente, pero las claves foráneas por sí solas no aseguran que ya exista una fila en libro\_autor.

Impedir préstamos simultáneos de un ejemplar y préstamos de ejemplares en reparación requerirá controles adicionales al implementar el sistema.

## 2.6. Diagrama del modelo inicial

Modelo inicial de la biblioteca, con entidades, atributos y relaciones. La relación N:M entre libros y autores se resuelve mediante LIBRO\_AUTOR

![](images/67a8ab7f12ccf6062d4a845dc4c8aabd4ddca40d5a15e520a3e508d862c8ce89.jpg)

## Parte 3 - Refactorización del modelo

## 3.1. Revisión de claves primarias, candidatas y alternativas

Se revisan las claves del modelo según los cinco criterios desarrollados en la Clase 3: unicidad garantizada, presencia obligatoria, estabilidad en el tiempo, representación corta y simple, y ausencia de significado de negocio.

Se adoptan identificadores numéricos subrogados de tipo BIGINT UNSIGNED, generados automáticamente. Los datos naturales que deben ser únicos se conservan como atributos y se protegen mediante restricciones de unicidad.

SOCIO y BIBLIOTECARIO constituyen una excepción a la generación de identificadores independientes: utilizan la clave de PERSONA como PK y FK, porque representan roles de una misma identidad.

<table><tr><td colspan="1" rowspan="1">Entidad</td><td colspan="1" rowspan="1">Clave primariaadoptada</td><td colspan="1" rowspan="1">Clavesalternativas orestricciones deunicidad</td><td colspan="1" rowspan="1">Justificación</td></tr><tr><td colspan="1" rowspan="1">PERSONA</td><td colspan="1" rowspan="1">id_persona</td><td colspan="1" rowspan="1">documentoobligatorio y único</td><td colspan="1" rowspan="1">El            identificadorpermanece       estableaunque se corrijan losdatos personales. Eldocumento       permitecontrolar        registrosduplicados.</td></tr><tr><td colspan="1" rowspan="1">SOCIO</td><td colspan="1" rowspan="1">id_persona,también FK haciaPERSONA</td><td colspan="1" rowspan="1">No se identifica otraclave candidata</td><td colspan="1" rowspan="1">Permite     una    solaafiliación por persona yconserva la identidad dela entidad general.</td></tr><tr><td colspan="1" rowspan="1">BIBLIOTECARIO</td><td colspan="1" rowspan="1">id_persona,también FK haciaPERSONA</td><td colspan="1" rowspan="1">legajo obligatorio yúnico</td><td colspan="1" rowspan="1">La     identidad     secomparte              conPERSONA; el legajoidentifica al empleadodentro de la institución.</td></tr><tr><td colspan="1" rowspan="1">EDITORIAL</td><td colspan="1" rowspan="1">id_editorial</td><td colspan="1" rowspan="1">No se identifica otraclave candidata</td><td colspan="1" rowspan="1">El nombre no garantizaunicidad   y  puedecambiar.</td></tr><tr><td colspan="1" rowspan="1">AUTOR</td><td colspan="1" rowspan="1">id_autor</td><td colspan="1" rowspan="1">No se identifica otraclave candidata</td><td colspan="1" rowspan="1">Dos autores puedencompartir nombre yapellido.</td></tr><tr><td colspan="1" rowspan="1">LIBRO</td><td colspan="1" rowspan="1">id_libro</td><td colspan="1" rowspan="1">ISBN único cuandoestá informado</td><td colspan="1" rowspan="1">El registro bibliográficodebe poder identificarseaunque   carezca  deISBN.</td></tr><tr><td colspan="1" rowspan="1">EJEMPLAR</td><td colspan="1" rowspan="1">id_ejemplar</td><td colspan="1" rowspan="1">codigo_inventarioobligatorio y único</td><td colspan="1" rowspan="1">El identificador distinguecada copia física; elcódigo de inventarioconserva su funcióndentro de la biblioteca.</td></tr><tr><td colspan="1" rowspan="1">PRÉSTAMO</td><td colspan="1" rowspan="1">id_prestamo</td><td colspan="1" rowspan="1">No se identifica otraclave candidata</td><td colspan="1" rowspan="1">Un mismo socio puederecibir     el     mismoejemplar endistintasocasiones.</td></tr><tr><td colspan="1" rowspan="1">LIBRO_AUTOR</td><td colspan="1" rowspan="1">id_libro_autor</td><td colspan="1" rowspan="1">UNIQUE(id_libro,id_autor),   ambosobligatorios</td><td colspan="1" rowspan="1">La clave  subrogadasimplifica                 laidentificación;           lacombinación     impiderepetir la asociaciónentre un libro y un autor.</td></tr><tr><td colspan="1" rowspan="1">TELÉFONO_SOCI0</td><td colspan="1" rowspan="1">id_telefono_socio</td><td colspan="1" rowspan="1">UNIQUE (id_socio,numero),    ambosobligatorios</td><td colspan="1" rowspan="1">Cada registro tiene unidentificador estable yno se admite repetir unnúmero para el mismosocio.</td></tr></table>

Las combinaciones obligatorias y únicas de LIBRO\_AUTOR y TELÉFONO\_SOCIO son claves candidatas compuestas que se conservan como alternativas a las PK subrogadas.

El ISBN es opcional. Por ese motivo, su restricción de unicidad cuando está informado no lo convierte en una clave candidata válida para identificar todos los registros de LIBRO. El correo electrónico tampoco se considera clave candidata, porque puede faltar o ser compartido por distintas personas.

Los nombres y apellidos no se utilizan como claves: no garantizan unicidad ni estabilidad.

Respecto del modelo inicial, se documentan tres cambios:

● SOCIO y BIBLIOTECARIO reemplazan sus identificadores independientes por id\_persona.

● LIBRO\_AUTOR incorpora id\_libro\_autor y conserva la unicidad de la combinación libro–autor.

● TELÉFONO\_SOCIO adopta id\_telefono\_socio y conserva la unicidad de la combinación socio–número.

En las tablas que referencian los roles se mantienen nombres que expresan su función: PRÉSTAMO.id\_socio referencia SOCIO.id\_persona y PRÉSTAMO.id\_bibliotecario referencia BIBLIOTECARIO.id\_persona. TELÉFONO\_SOCIO.id\_socio también referencia SOCIO.id\_persona. Estos campos contienen identificadores de PERSONA, pero sus FK verifican además la existencia del rol correspondiente.

## 3.2. Revisión y resolución de la jerarquía.

En el modelo inicial de biblioteca, las entidades SOCIO y BIBLIOTECARIO representan personas que desempeñan diferentes roles. Ambas contienen los atributos nombre y apellido, mientras que cada una tiene información propia: SOCIO registra documento, email y fecha\_alta; BIBLIOTECARIO registra legajo.

Se evaluaron dos alternativas:

Mantener las entidades independientes: simplifica las consultas, pero obliga a duplicar los datos personales cuando un bibliotecario también es socio. Una actualización podría dejar nombres o apellidos diferentes para la misma persona.

Crear una entidad general PERSONA: permite registrar una única identidad y asociarle los roles que desempeña, manteniendo los atributos específicos en cada especialización.

Se adopta la segunda alternativa porque permite que un bibliotecario también sea socio sin duplicar sus datos personales.

## 3.2.1 Estructura propuesta

<table><tr><td rowspan=1 colspan=1>Entidad</td><td rowspan=1 colspan=1>Atributos</td><td rowspan=1 colspan=1>Función</td></tr><tr><td rowspan=1 colspan=1>PERSONA</td><td rowspan=1 colspan=1>id_persona,            nombre,apellido, documento, email</td><td rowspan=1 colspan=1>Contiene la identidad y los datospersonales comunes.</td></tr><tr><td rowspan=1 colspan=1>SOCIO</td><td rowspan=1 colspan=1>id_persona, fecha_alta</td><td rowspan=1 colspan=1>Contiene los datos propios de laafiliación a la biblioteca.</td></tr><tr><td rowspan=1 colspan=1>BIBLIOTECARIO</td><td rowspan=1 colspan=1>id_persona, legajo</td><td rowspan=1 colspan=1>Contiene los datos propios delpersonal de la biblioteca.</td></tr></table>

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

<table><tr><td rowspan=1 colspan=1>Entidad</td><td rowspan=1 colspan=1>Dependencia funcional</td></tr><tr><td rowspan=1 colspan=1>PERSONA</td><td rowspan=1 colspan=1>id_persona → nombre, apellido, documento, email</td></tr><tr><td rowspan=1 colspan=1>SOCIO</td><td rowspan=1 colspan=1>id_persona → fecha_alta</td></tr><tr><td rowspan=1 colspan=1>BIBLIOTECARIO</td><td rowspan=1 colspan=1>id_persona → legajo</td></tr><tr><td rowspan=1 colspan=1>EDITORIAL</td><td rowspan=1 colspan=1>id_editorial → nombre</td></tr><tr><td rowspan=1 colspan=1>AUTOR</td><td rowspan=1 colspan=1>id_autor → nombre, apellido</td></tr><tr><td rowspan=1 colspan=1>LIBRO</td><td rowspan=1 colspan=1>id_libro → titulo, isbn, anio_publicacion, id_editorial</td></tr><tr><td rowspan=1 colspan=1>EJEMPLAR</td><td rowspan=1 colspan=1>id_ejemplar → id_libro, codigo_inventario, fecha_incorporacion, estado</td></tr><tr><td rowspan=1 colspan=1>PRÉSTAMO</td><td rowspan=1 colspan=1>id_prestamo → id_socio, id_ejemplar, id_bibliotecario y fechas de la operación</td></tr><tr><td rowspan=1 colspan=1>LIBRO_AUTOR</td><td rowspan=1 colspan=1>id_libro_autor → id_libro, id_autor, orden_autoria</td></tr><tr><td rowspan=1 colspan=1>TELÉFONO_SOCIO</td><td rowspan=1 colspan=1>id_telefono_socio → id_socio, numero, tipo</td></tr></table>

Por ejemplo, el nombre de la editorial no se almacena en LIBRO. Si se incluyera, aparecería la dependencia transitiva:

## id\_libro → id\_editorial → nombre\_editorial

La separación entre LIBRO y EDITORIAL evita esa redundancia. Del mismo modo, EJEMPLAR no repite el título del libro y PRÉSTAMO no repite los nombres del socio o del bibliotecario.

No se detecta una dependencia transitiva adicional que exija otra separación en el modelo definido. Se documenta este resultado sin introducir entidades artificiales para producir una corrección innecesaria.

La jerarquía PERSONA permite, además, centralizar los datos personales de quienes desempeñan ambos roles. Esta decisión evita duplicaciones entre entidades, aunque la repetición entre tablas no constituye por sí sola una violación de 3FN.

## 3.3.4. Conservación de información histórica

fecha\_vencimiento\_inicial y fecha\_vencimiento\_actual representan hechos diferentes.

La primera conserva el plazo acordado al registrar el préstamo y no se modifica durante una renovación. La segunda representa el plazo vigente y puede actualizarse.

Aunque inicialmente coincidan, ninguna determina necesariamente a la otra. Su conservación no constituye una redundancia ni una desnormalización deliberada. No se registra el historial completo de renovaciones, porque queda fuera del alcance del proyecto.

## 3.4. Reglas de integridad y borrado

La integridad del modelo se establece mediante claves primarias, claves foráneas, obligatoriedad, unicidad y reglas del negocio.

Las relaciones obligatorias requieren FK no nulas. fecha\_devolucion admite NULL mientras el préstamo permanezca pendiente. El correo electrónico y el ISBN también son opcionales.

## 3.4.1. Reglas de borrado

Se prioriza la conservación del historial de préstamos. El sistema no incluye un proceso funcional de bajas; las siguientes reglas definen qué debe ocurrir si se intenta eliminar un registro.

<table><tr><td colspan="1" rowspan="1">Registro que seintenta eliminar</td><td colspan="1" rowspan="1">Registros relacionados</td><td colspan="1" rowspan="1">Regla</td><td colspan="1" rowspan="1">Fundamento</td></tr><tr><td colspan="1" rowspan="1">PERSONA</td><td colspan="1" rowspan="1">SOCIO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">No se elimina una identidad mientrasconserve el rol de socio.</td></tr><tr><td colspan="1" rowspan="1">PERSONA</td><td colspan="1" rowspan="1">BIBLIOTECARIO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">No se elimina una identidad mientrasconserve el rol de bibliotecario.</td></tr><tr><td colspan="1" rowspan="1">SOCIO</td><td colspan="1" rowspan="1">PRÉSTAMO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">Se preserva la identificación de quienrecibió cada ejemplar.</td></tr><tr><td colspan="1" rowspan="1">BIBLIOTECARIO</td><td colspan="1" rowspan="1">PRÉSTAMO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">Se preserva la identificación de quienregistró la operación.</td></tr><tr><td colspan="1" rowspan="1">EJEMPLAR</td><td colspan="1" rowspan="1">PRÉSTAMO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">Se conserva la referencia a la copiafísica prestada.</td></tr><tr><td colspan="1" rowspan="1">LIBRO</td><td colspan="1" rowspan="1">EJEMPLAR</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">No se elimina un registro bibliográficoque todavía tiene copias registradas.</td></tr><tr><td colspan="1" rowspan="1">EDITORIAL</td><td colspan="1" rowspan="1">LIBRO</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">No se dejan libros sin su editorialobligatoria.</td></tr><tr><td colspan="1" rowspan="1">AUTOR</td><td colspan="1" rowspan="1">LIBRO_AUTOR</td><td colspan="1" rowspan="1">RESTRICT</td><td colspan="1" rowspan="1">Se evita eliminar una autoríamediante el borrado del autor.</td></tr><tr><td colspan="1" rowspan="1">LIBRO</td><td colspan="1" rowspan="1">LIBRO AUTOR</td><td colspan="1" rowspan="1">CASCADE</td><td colspan="1" rowspan="1">Si puede eliminarse el libro, susasociaciones de autoría carecen deexistencia independiente.</td></tr><tr><td colspan="1" rowspan="1">SOCIO</td><td colspan="1" rowspan="1">TELÉFONO_SOCIO</td><td colspan="1" rowspan="1">CASCADE</td><td colspan="1" rowspan="1">Si puede eliminarse el socio, tambiénse eliminan sus registros de contacto.</td></tr></table>

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

CONTEXTO:

Modelo de biblioteca con las entidades PERSONA, SOCIO, BIBLIOTECARIO, EDITORIAL,

AUTOR, LIBRO, EJEMPLAR, PRÉSTAMO, LIBRO\_AUTOR y TELÉFONO\_SOCIO. Utilizá el esquema de atributos y claves del apartado 3.6.

## REGLAS DEL NEGOCIO:

● La especialización PERSONA es total y superpuesta.

● SOCIO y BIBLIOTECARIO utilizan id\_persona como PK y FK.

● Cada préstamo corresponde a un único ejemplar.

LIBRO\_AUTOR registra orden\_autoria y no admite repetir la combinación libro–autor.

Un socio puede registrar varios teléfonos, sin repetir el mismo número para ese socio.

● El ISBN es opcional; cuando está informado, debe ser único.

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

3.5.2. Hallazgos y revisión humana
<table><tr><td colspan="1" rowspan="1">Hallazgo u observación</td><td colspan="1" rowspan="1">Clasificación</td><td colspan="1" rowspan="1">Decisión y fundamento</td></tr><tr><td colspan="1" rowspan="1">TELÉFONO_SOCIO          teníaidentificadores diferentes entrelas partes del documento.</td><td colspan="1" rowspan="1">Correcto</td><td colspan="1" rowspan="1">Se adopta id_telefono_socio y seconserva UNIQUE (id_socio, numero).</td></tr><tr><td colspan="1" rowspan="1">Los   datos   personales   seduplicarían si un bibliotecariotambién fuera socio.</td><td colspan="1" rowspan="1">Correcto</td><td colspan="1" rowspan="1">Se acepta PERSONA como entidadgeneral y se mantienen los atributosespecíficos en cada rol.</td></tr><tr><td colspan="1" rowspan="1">Las FK de préstamos y teléfonosdeben    adecuarse    a    losidentificadores        de       lasespecializaciones.</td><td colspan="1" rowspan="1">Correcto</td><td colspan="1" rowspan="1">Se mantienen los nombres queexpresan el rol, pero se referencianlas PK id_persona de SOCIO yBIBLIOTECARIO.</td></tr><tr><td colspan="1" rowspan="1">Conviene reemplazar la PKcompuesta de LIBRO_AUTORpor una subrogada.</td><td colspan="1" rowspan="1">Discutible</td><td colspan="1" rowspan="1">Ambas opciones son válidas. Seadopta la subrogada para seguir elcriterio del curso, conservandoUNIQUE (id_libro, id_autor).</td></tr><tr><td colspan="1" rowspan="1">Falta definir las reglas deborrado.</td><td colspan="1" rowspan="1">Correcto</td><td colspan="1" rowspan="1">Se incorporan reglas explícitas quepreservan el historial y eliminanúnicamente registros dependientescuando corresponde.</td></tr><tr><td colspan="1" rowspan="1">El atributo estado aparece en losprompts, pero no en ladescripción inicial de EJEMPLAR.</td><td colspan="1" rowspan="1">Correcto</td><td colspan="1" rowspan="1">Se incorpora al esquema y se limita aoperativo y en_reparacion.</td></tr><tr><td colspan="1" rowspan="1">EI ISBN se presentaconobligatoriedad ambigua.</td><td colspan="1" rowspan="1">Correcto</td><td colspan="1" rowspan="1">Se establece que es opcional y únicocuando está informado.</td></tr><tr><td colspan="1" rowspan="1">Debe comprobarse 2FN aunquelas PK sean simples.</td><td colspan="1" rowspan="1">Correcto</td><td colspan="1" rowspan="1">Se revisan también las clavescandidatas compuestas de las tablasasociativas.</td></tr></table>

Se descartan dos posibles correcciones que perjudicarían el diseño: eliminar fecha\_vencimiento\_inicial por coincidir inicialmente con el vencimiento actual, y dirigir los préstamos exclusivamente a PERSONA. La primera perdería información histórica; la segunda no garantizaría los roles de socio y bibliotecario.  
No se identifican violaciones adicionales de 1FN, 2FN o 3FN bajo las reglas declaradas. Este resultado deberá contrastarse con el diagrama actualizado para verificar que su representación coincida con el diseño documentado.

## 3.6. Diagrama definitivo y síntesis de las decisiones de diseño

El modelo refactorizado queda definido por diez entidades. Las nueve entidades iniciales se conservan y se incorpora PERSONA como generalización de SOCIO y BIBLIOTECARIO.

## 3.6.1. Esquema de referencia para el diagrama

<table><tr><td>Entidad</td><td>Atributos definitivos</td></tr><tr><td colspan="1" rowspan="1">PERSONA</td><td colspan="1" rowspan="1">id_persona PK, nombre, apellido, documento UNIQUE yobligatorio, email opcional</td></tr><tr><td colspan="1" rowspan="1">SOCIO</td><td colspan="1" rowspan="1">id_persona PK/FK hacia PERSONA, fecha_alta</td></tr><tr><td colspan="1" rowspan="1">BIBLIOTECARIO</td><td colspan="1" rowspan="1">id_persona PK/FK hacia PERSONA, legajo UNIQUE y obligatorio</td></tr><tr><td colspan="1" rowspan="1">EDITORIAL</td><td colspan="1" rowspan="1">id_editorial PK, nombre</td></tr><tr><td colspan="1" rowspan="1">AUTOR</td><td colspan="1" rowspan="1">id_autor PK, nombre, apellido</td></tr><tr><td colspan="1" rowspan="1">LIBRO</td><td colspan="1" rowspan="1">id_libro PK, titulo, isbn opcional y UNIQUE, anio_publicacion,id_editorial FK</td></tr><tr><td colspan="1" rowspan="1">EJEMPLAR</td><td colspan="1" rowspan="1">id_ejemplar PK, id_libro FK, codigo_inventario UNIQUE yobligatorio, fecha_incorporacion, estado</td></tr><tr><td colspan="1" rowspan="1">PRÉSTAMO</td><td colspan="1" rowspan="1">id_prestamo PK, id_socio FK hacia SOCIO.id_persona,id_ejemplar        FK,        id_bibliotecario        FK        haciaBIBLIOTECARIO.id_persona,                           fecha_prestamo,fecha_vencimiento_inicial,                  fecha_vencimiento_actual,fecha_devolucion opcional</td></tr><tr><td colspan="1" rowspan="1">LIBRO_AUTOR</td><td colspan="1" rowspan="1">id_libro_autor PK, id_libro FK, id_autor FK, orden_autoria;UNIQUE (id_libro, id_autor)</td></tr><tr><td colspan="1" rowspan="1">TELÉFONO_SOCIO</td><td colspan="1" rowspan="1">id_telefono_socio PK, id_socio FK hacia SOCIO.id_persona,numero, tipo; UNIQUE (id_socio, numero)</td></tr></table>

El diagrama mantiene las ocho relaciones de la Parte 2 y agrega las dos relaciones de especialización. Cada PERSONA puede tener cero o una fila en cada especialización, pero debe tener al menos uno de los dos roles. Esta condición conjunta se documenta mediante la nota “Especialización total y superpuesta”.

Cada relación debe mostrar su cardinalidad y obligatoriedad. La exigencia de al menos un autor por libro debe quedar documentada aunque la herramienta no permita representarla completamente.

Modelo refactorizado de la biblioteca, con la jerarquía PERSONA, las claves revisadas y las decisiones de normalización

![](images/29db57275e4b8870a65dc0a221bb81112a362e1cbee3d402fbe0f2bf382a37e6.jpg)

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

Se conservaron las decisiones del modelo anterior: la identidad común en persona, los roles de socio y bibliotecario mediante claves que son simultáneamente PK y FK, la separación entre libro y ejemplar, y la relación N entre libros y autores resuelta mediante libro\_autor.

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

![](images/9f07fb16cb8968d0f142d7b9fd72a02e501188ad326b0e8c1af9749131aa6347.jpg)

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

Quedan pendientes los controles operativos que impidan prestar ejemplares en reparación y registrar dos préstamos pendientes para un mismo ejemplar. También requieren control adicional la participación total de persona en sus roles, la existencia de al menos un autor por libro completo y la conservación del vencimiento inicial como dato histórico. Los comentarios del esquema documentan estas reglas, pero no garantizan su cumplimiento.

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

## Actividad 5 · Preguntas de negocio y resultados esperados

Las preguntas se plantean sobre la base de datos de biblioteca y el set de prueba preparado. Los resultados indicados suponen que se ejecutaron correctamente los scripts de personas, teléfonos, autores, editoriales, libros y ejemplares. En esta etapa se define qué queremos consultar y qué esperamos encontrar; las consultas SQL se resolverán después.

N.º Pregunta de negocio

Resultado esperado y análisis

1 ¿Cuántas personas están 50 personas. Corresponden a las 45 personas con rol de socio y registradas en la biblioteca? las 5 con rol de bibliotecario.

2 ¿Cuántas personas tienen rol de 45 socios. Permite verificar la carga de personas y la tabla de socio? roles. Requiere relacionar persona con socio.

3 ¿Cuántas personas trabajan como 5 bibliotecarios. Requiere relacionar persona con bibliotecarias? bibliotecario.

4 ¿Hay personas sin correo Ninguna. Las 50 personas del set tienen correo de prueba. electrónico registrado?

5 ¿Cuántos teléfonos se registraron 55 teléfonos para 45 socios. Cada socio tiene un teléfono y cuántos socios tienen al menos principal; 10 tienen además uno alternativo. Requiere relacionar uno? telefono\_socio, socio y persona.

6 ¿Cuántos socios tienen un 35 socios tienen uno y 10 tienen dos. La consulta permite teléfono y cuántos tienen dos? comprobar que se contemplan varios teléfonos por socio.

7 ¿Cuántos autores están 110 autores. Se espera ese total si la tabla estaba vacía antes de registrados? ejecutar la carga.

8 ¿Cuántos autores tienen al menos 50 autores tienen un libro asociado y 60 no tienen libros un libro asociado y cuántos asociados. La carga actual asigna un autor a cada uno de los 50 todavía no tienen ninguno? libros. Requiere relacionar autor, libro\_autor y libro.

9 ¿Cuántas editoriales están 30 editoriales. registradas?

10 ¿Cuántas editoriales todavía no 11 editoriales. De las 30 cargadas, 19 se asignaron a los libros. publican libros en el catálogo de prueba?

11 ¿Cuántos libros integran el 50 libros. catálogo?

12 ¿Cuántos títulos comienzan con 18 títulos. La búsqueda debe considerar el comienzo del título, “El”? no las apariciones de “el” en otras posiciones.

¿Cuántos libros se publicaron en cada año del set?

¿Qué editoriales tienen más libros en este catálogo de prueba?

15 ¿Hay libros sin autor asociado?

¿Hay libros sin ejemplares registrados?

17 ¿Cuántos libros tienen uno, dos o tres ejemplares?

¿Cuántos ejemplares están operativos y cuántos en reparación?

¿Qué títulos tienen ejemplares en reparación?

Se esperan estos resultados: 2017: 4; 2018: 7; 2019: 7; 2020: 9;   
2021: 8; 2022: 6; 2023: 5; 2024: 4. La suma debe ser 50.

Alfaguara y HarperCollins, con 5 libros cada una. Es el máximo del set.

Ninguno. Cada libro tiene una asociación con un autor en libro\_autor.

Ninguno. Cada uno de los 50 libros recibió entre 1 y 3 ejemplares.

16 libros tienen uno; 17 tienen dos; 17 tienen tres. En total deben ser 50 libros. Requiere agrupar los ejemplares por libro.

97 operativos y 4 en reparación, sobre un total de 101 ejemplares.

El último tren de la memoria, Pequeño atlas de la noche, Los nombres del bosque profundo y El mapa de los pájaros azules. Cada uno tiene un ejemplar en reparación y conserva al menos uno operativo.

20 ¿Qué libros tienen menos de tres 33 libros: los 16 que tienen un ejemplar y los 17 que tienen dos. ejemplares, para evaluar si Los otros 17 ya cuentan con tres ejemplares. conviene ampliar el inventario?

Varias preguntas requieren combinar tablas —por ejemplo, para relacionar socios con teléfonos o libros con autores—, por lo que se resolverán con JOIN, tema previsto para la Clase 6. Las preguntas sobre conteos, filtros, ordenamientos y años pueden trabajarse con los contenidos de la Clase 5.