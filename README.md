# Buscador eficiente de palabras en archivos de texto

Proyecto final de **Estructura de Datos** · Universidad de La Sabana · 2026  
Profesor: **Arley Calderón**  
Equipo: **Juan, Daniel y Sara**

## ¿De qué trata el proyecto?

Desarrollamos un programa de consola en Python que permite cargar un archivo `.txt` y consultar su contenido de diferentes maneras: encontrar palabras exactas, ignorar mayúsculas, buscar por prefijo, revisar estadísticas, recuperar una palabra por su posición y comparar dos estrategias de búsqueda.

Nuestro objetivo fue **evitar recorrer el archivo completo cada vez que hacemos una consulta**. Para lograrlo, durante la carga construimos estructuras que conservan tanto el orden del texto como índices para encontrar palabras rápidamente.

La solución combina **diccionarios hash, listas, arreglos compactos y búsqueda binaria**. No utilizamos paquetes externos.

## Requisitos

- **Python 3.10 o superior**, porque el menú utiliza `match/case`.
- Un archivo de texto con extensión `.txt` y codificación **UTF-8** (también se admite UTF-8 con BOM).
- Windows, macOS o Linux.

Las bibliotecas utilizadas (`pathlib`, `array`, `time`, `bisect` y `heapq`) forman parte de la biblioteca estándar de Python. **No es necesario ejecutar `pip install`**.

## Estructura del proyecto

```text
Proyecto/
├── main.py          # Menú principal y control del programa
├── librerias.py      # Carga, estructuras de datos y búsquedas
├── Archivos/         # Aquí ubicamos los .txt que queremos analizar
├── README.md
└── .gitignore
```

Los archivos de texto pueden guardarse en `Archivos/` o cargarse mediante una ruta válida. La carpeta del proyecto se puede copiar completa a otro computador sin necesidad de modificar rutas dentro del código.

## ¿Cómo ejecutar el programa?

1. Descargamos o clonamos el proyecto y conservamos juntos `main.py`, `librerias.py` y la carpeta `Archivos`.
2. Colocamos el archivo `.txt` que queremos estudiar dentro de `Archivos`.
3. Abrimos una terminal en la carpeta del proyecto.
4. Ejecutamos el programa:

   **Windows**

   ```powershell
   py main.py
   ```

   **macOS o Linux**

   ```bash
   python3 main.py
   ```

5. Elegimos **1) Cargar Archivo** e ingresamos el nombre del archivo, por ejemplo `texto.txt`.
6. Cuando la carga termina correctamente, se habilitan las demás operaciones.

También podemos ingresar una ruta relativa, como `Archivos/texto.txt`, o una ruta absoluta del computador donde se esté ejecutando el programa. Si ya tenemos un archivo cargado, el menú pregunta si queremos reemplazarlo.

> **Importante:** para llevar el programa a otro computador, no debemos copiar únicamente `main.py`. También necesitamos `librerias.py` y los archivos de texto que vayamos a utilizar. No hay que instalar dependencias adicionales.

## Menú de opciones

| Opción | Función | ¿Qué permite hacer? |
|:---:|---|---|
| **1** | Cargar archivo | Leer el `.txt`, validar su contenido y construir los índices. |
| **2** | Búsqueda exacta | Encontrar una palabra completa, respetando mayúsculas y minúsculas. |
| **3** | Búsqueda simple | Encontrar una palabra completa sin distinguir mayúsculas y minúsculas. |
| **4** | Búsqueda por prefijo | Mostrar todas las apariciones de palabras que comienzan por un prefijo. |
| **5** | Estadísticas | Mostrar el total, la primera palabra, la central y la última. |
| **6** | Buscar palabra N.º X | Recuperar la palabra y su línea a partir de una posición válida. |
| **7** | Análisis comparativo | Comparar una búsqueda lineal con una búsqueda por diccionario. |
| **0** | Salir | Cerrar el programa. |

Las opciones **2 a 7** requieren que el archivo se haya cargado correctamente.

### ¿Qué consideramos una palabra?

Siguiendo el taller, una palabra es cualquier secuencia de caracteres separada por **espacios en blanco o saltos de línea**. Por eso, `casa` y `casa,` son palabras distintas: la puntuación no se elimina automáticamente.

La búsqueda exacta también distingue `casa` de `Casa`. La búsqueda simple y la de prefijo ignoran esa diferencia usando normalización de texto.

## ¿Cómo organizamos los datos?

Al cargar el archivo una sola vez, construimos estas estructuras:

| Estructura | Tipo | Información que almacena | Utilidad |
|---|---|---|---|
| `vocabulario` | Lista | Cada palabra original diferente, una sola vez. | Recuperar la palabra a partir de su identificador. |
| `orden_ids` | `array('I')` | Identificadores de **todas** las apariciones, en el orden del archivo. | Consultar posiciones sin repetir las cadenas. |
| `lineas` | `array('I')` | Número de línea de cada aparición. | Recuperar la ubicación de una palabra. |
| `indice_exacto` | Diccionario | Palabra original → identificador, conteo, primera y última línea. | Búsqueda exacta rápida. |
| `indice_simple` | Diccionario | Palabra normalizada → arreglo de posiciones donde aparece. | Búsqueda sin distinguir mayúsculas. |
| `claves_ordenadas` | Lista | Claves normalizadas diferentes, ordenadas alfabéticamente. | Búsqueda binaria por prefijo. |

El proceso de carga también utiliza una lista temporal de palabras normalizadas para evitar normalizar repetidamente una palabra original. Esta lista temporal no se incluye en el diccionario de datos devuelto al menú.

### ¿Por qué usamos `array('I')`?

Cada aparición necesita guardar números (identificadores, líneas o posiciones), pero **no necesita guardar otra copia completa de la palabra**. Un arreglo de enteros sin signo almacena esos números de forma compacta; normalmente cada elemento de tipo `I` ocupa 4 bytes, aunque el tamaño depende de la plataforma. Esto reduce la sobrecarga frente a almacenar millones de objetos `int` en listas de Python.

Además, los arreglos permiten recuperar un elemento por su posición en **O(1)**.

## Funciones implementadas

### 1. `Cargar_Archivo()`

Lee el texto línea por línea, identifica palabras nuevas, cuenta sus repeticiones, registra posiciones y líneas, construye los dos diccionarios y ordena las claves necesarias para la búsqueda por prefijo.

**Decisión:** invertir trabajo al cargar el archivo para evitar repetirlo en las consultas posteriores. También permite trabajar con rutas relativas al proyecto y manejar errores de apertura y lectura.

### 2. `Busqueda(datos)` — exacta

Consulta `indice_exacto` con la palabra tal como la ingresamos. Obtiene el número de apariciones y las líneas de la primera y la última coincidencia. No acepta coincidencias parciales.

**Decisión:** el diccionario hash permite encontrar el registro directamente, en lugar de recorrer todas las palabras.

### 3. `Busqueda_simple(datos)` — sin distinguir mayúsculas

Normaliza la palabra buscada con `casefold()` y consulta `indice_simple`. Las posiciones registradas permiten obtener el conteo y las líneas extremas sin recorrer el archivo.

**Decisión:** normalizamos una sola vez las claves durante la carga; así no tenemos que transformar y comparar cada aparición en cada búsqueda.

### 4. `Busqueda_prefijo(datos)`

Utiliza búsqueda binaria sobre `claves_ordenadas` para encontrar el inicio de las palabras que comparten el prefijo. Después recupera las coincidencias y une sus posiciones en el orden original mediante una mezcla de secuencias ordenadas (`heapq.merge`). Muestra todas las apariciones con sus líneas.

**Decisión:** buscamos primero entre palabras **diferentes**, en lugar de revisar las **N apariciones**. La mezcla evita crear y ordenar otra lista gigante de resultados.

### 5. `Estadisticas(datos)`

Obtiene directamente el total de palabras, la primera, la última y la central. Para esta última aplicamos la regla del taller: si la mitad da decimal, elegimos la posición inmediatamente superior.

**Decisión:** como `orden_ids` conserva las posiciones originales, no necesitamos recorrer el texto para calcular estos datos.

### 6. `palabra_numero(datos)`

Valida que la posición ingresada sea un entero entre **1 y N**. Luego obtiene el identificador, la palabra original y su línea mediante accesos directos a los arreglos.

**Decisión:** recuperar la palabra N.º X debe costar lo mismo aunque esté al principio o al final del archivo.

### 7. `Comparacion(datos)`

Busca la misma palabra exacta de dos formas:

1. **Búsqueda lineal:** recorre `orden_ids` y compara cada palabra, con complejidad **O(N)**.
2. **Búsqueda optimizada:** consulta `indice_exacto`, con complejidad **O(1) promedio** respecto al número de palabras.

El programa mide los tiempos en milisegundos, identifica el método más rápido en esa ejecución y verifica que ambos métodos produzcan el mismo conteo y las mismas líneas, incluso si la palabra no aparece.

## Análisis de complejidad Big O

Definimos las variables usadas para analizar el rendimiento:

- **C:** cantidad de caracteres del archivo.
- **N:** cantidad total de apariciones de palabras.
- **U:** cantidad de palabras diferentes.
- **K:** cantidad de palabras diferentes que coinciden con un prefijo.
- **M:** cantidad total de apariciones que coinciden con ese prefijo.
- **L:** longitud de la palabra o prefijo ingresado.

| Operación | Tiempo | Memoria adicional por operación |
|---|---|---|
| Cargar archivo | **O(C + U log U)** aprox. | **O(N + U)** para conservar los índices y arreglos. |
| Búsqueda exacta | **O(1) promedio** para palabras de longitud acotada | **O(1)** |
| Búsqueda simple | **O(L)** promedio por la normalización de la consulta | **O(L)** por la cadena normalizada |
| Búsqueda por prefijo | **O(log U + K + M log K)** aprox. | **O(K)** |
| Estadísticas | **O(1)** | **O(1)** |
| Palabra N.º X | **O(1)** | **O(1)** |
| Comparación: recorrido lineal | **O(N)** | **O(1)** |
| Comparación: diccionario | **O(1) promedio**, con L acotada | **O(1)** |

**Cómo interpretar esta tabla:**

- La memoria **O(1)** de una consulta se refiere a sus **variables auxiliares**, no a toda la memoria del programa. Los índices ya cargados siguen ocupando espacio.
- El espacio **O(N + U)** resume los identificadores, las posiciones y los registros. Si las palabras tienen longitudes variables, también debemos contabilizar los caracteres de las **U palabras diferentes** y la sobrecarga propia de las estructuras de Python.
- El tiempo de búsqueda exacta se considera **O(1) promedio respecto a N** por el acceso hash; calcular o comparar cadenas de longitud variable también tiene un costo asociado a **L**.
- En la carga y la búsqueda por prefijo, las comparaciones de cadenas pueden añadir factores según su longitud; la tabla resume el caso habitual de palabras relativamente cortas.
- En prefijos, generar **M resultados** exige trabajo proporcional a la cantidad de resultados. Ninguna estructura puede mostrar miles de coincidencias sin procesarlas.
- El peor caso teórico de una tabla hash puede ser peor que el promedio; **O(1)** no significa que una consulta demore siempre exactamente el mismo número de milisegundos.

## ¿Por qué no utilizamos una sola estructura?

| Alternativa | Ventaja | Desventaja en nuestro problema |
|---|---|---|
| Recorrer el archivo para cada búsqueda | Requiere pocos índices adicionales. | Repetiríamos un recorrido **O(N)** en cada consulta por contenido. |
| Listas tradicionales para todos los números | Son sencillas y permiten acceso directo. | Una lista de muchos enteros de Python tiene más sobrecarga que `array('I')`. |
| Árbol de prefijos (**Trie**) | Muy útil para consultar prefijos. | Puede requerir numerosos nodos, referencias y más memoria. |
| Árbol de búsqueda balanceado | Mantiene claves ordenadas y permite consultas **O(log U)**. | La búsqueda exacta sería menos rápida que el promedio de un diccionario hash. |
| **Diccionarios + arreglos + claves ordenadas** | Exacta rápida, acceso por posición y búsqueda por prefijo. | Necesita una carga inicial y memoria para mantener los índices. |

Nuestra elección se adapta especialmente bien a un escenario donde **cargamos un archivo una vez y consultamos muchas veces**. Para una única búsqueda en un texto pequeño, el costo de construir los índices podría no compensarse.

## Medición de tiempos

Utilizamos `time.perf_counter()`, que devuelve el tiempo en segundos, y lo convertimos a milisegundos multiplicando por 1000.

Las mediciones implementadas corresponden a la **operación interna de búsqueda**, una vez recibida la entrada del usuario. No incluyen el tiempo que la persona tarda escribiendo ni la construcción inicial de los índices; tampoco incluyen la impresión de los resultados. Esta distinción es importante al interpretar la comparación entre **O(N)** y **O(1) promedio**.

Los tiempos reales pueden variar según el computador, el tamaño del texto y las condiciones de ejecución. Por eso no presentamos una medición aislada como prueba matemática de Big O: la complejidad se justifica por el algoritmo y los tiempos sirven para observar su comportamiento.

## Pruebas realizadas

Probamos la lógica del programa con un archivo generado específicamente para comprobar casos normales y extremos:

| Característica | Resultado |
|---|---:|
| Apariciones totales | **2.000.001** |
| Palabras originales diferentes | **50.020** |
| Líneas | **80.001** |

Algunos casos de verificación fueron:

- **Exacta:** `casa` y `Casa` se contabilizan por separado.
- **Simple:** `cAsA` reúne las variantes de mayúsculas y minúsculas.
- **Prefijo:** un prefijo poco frecuente devuelve sus coincidencias y líneas en orden original.
- **Estadísticas:** la primera, central y última palabras coinciden con marcadores colocados en esas posiciones.
- **Palabra N.º X:** se verificaron posiciones al inicio, al centro y al final.
- **Comparación:** el recorrido y el diccionario entregan el mismo conteo y las mismas líneas.
- **Casos sin resultados:** las búsquedas informan cuando no encuentran coincidencias.

También contemplamos casos de error como archivo inexistente, vacío, sin permisos, codificación inválida, posiciones fuera de rango y entradas no numéricas.

## Manejo de errores y portabilidad

- Verificamos que el nombre ingresado no esté vacío y que el archivo tenga extensión `.txt`.
- Controlamos errores de archivo inexistente, permisos insuficientes, codificación, memoria y errores del sistema de archivos.
- Mantenemos los datos anteriores cuando una nueva carga no se completa correctamente.
- Las rutas relativas se resuelven tomando como referencia la carpeta de `librerias.py`, no una ruta fija del computador donde programamos.
- Las opciones de búsqueda solo pueden usarse después de una carga válida.
- Trabajamos únicamente con bibliotecas estándar de Python, lo que facilita ejecutar el proyecto en distintos equipos.

## Limitaciones conocidas

- El texto debe estar codificado en UTF-8 o UTF-8 con BOM.
- La separación de palabras depende de espacios en blanco; **no eliminamos signos de puntuación**, porque así se define la palabra en el taller.
- Los índices permanecen en memoria mientras el archivo está cargado. En textos muy grandes, la memoria disponible del equipo puede limitar la carga.
- El tipo `array('I')` tiene un rango entero máximo dependiente de la plataforma; para cantidades de apariciones extraordinariamente grandes habría que revisar ese límite.
- En una búsqueda por prefijo muy común, mostrar cada aparición puede producir una salida extensa en consola.
- Las comparaciones de tiempos no consideran el costo de preprocesamiento; esa inversión se aprovecha cuando hacemos consultas repetidas.

## Conclusión

El proyecto nos permitió comprobar que **la estructura de datos correcta depende de la operación que queremos resolver**. Los diccionarios nos ayudan a buscar palabras rápidamente, los arreglos conservan el orden y permiten consultar posiciones directamente, y las claves ordenadas hacen posible buscar por prefijo sin revisar todas las apariciones.

Nuestra solución prioriza **rapidez en consultas repetidas y un uso razonable de memoria**, reconociendo el costo de construir los índices y las limitaciones propias de cada alternativa.

---

**Proyecto final de Estructura de Datos — Universidad de La Sabana, 2026.**
