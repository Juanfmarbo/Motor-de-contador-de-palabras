#Librerias usadas para el funcionamiento de la app
from pathlib import Path
from array import array
import time

def Cargar_Archivo():
    """
    Lee un archivo .txt y construye las estructuras de datos
    necesarias para realizar búsquedas eficientes.

    Retorna:
        Un diccionario con las estructuras del archivo.
        None si ocurre un error durante la carga.
    """

    # Solicitar el nombre o la ruta del archivo
    entrada = input(
        "Nombre del archivo .txt (en Archivos) o ruta: "
    ).strip()

    # Validar que se haya ingresado una ruta
    if not entrada:
        print("Error: debe ingresar un nombre o una ruta.")
        return None

    ruta = Path(entrada).expanduser()

    # Validar la extensión
    if ruta.suffix.lower() != ".txt":
        print("Error: el archivo debe tener extensión .txt.")
        return None

    # Construir la ruta del archivo
    if not ruta.is_absolute():

        carpeta_proyecto = Path(__file__).resolve().parent

        # Si solamente ingresó el nombre del archivo
        if len(ruta.parts) == 1:
            ruta = carpeta_proyecto / "Archivos" / ruta

        # Si ingresó una ruta relativa
        else:
            ruta = carpeta_proyecto / ruta

    # ------------------------------------------------
    # ESTRUCTURAS DE DATOS
    # ------------------------------------------------

    # Almacena cada palabra diferente una sola vez
    vocabulario = []

    # Guarda temporalmente las palabras normalizadas
    normalizadas = []

    # Almacena los identificadores en orden de aparición
    orden_ids = array("I")

    # Almacena el número de línea de cada aparición
    lineas = array("I")

    # Índice Hash para búsqueda exacta
    indice_exacto = {}

    # Índice Hash para búsqueda sin distinguir mayúsculas
    indice_simple = {}

    # ------------------------------------------------
    # LECTURA DEL ARCHIVO
    # ------------------------------------------------

    try:

        with ruta.open("r", encoding="utf-8-sig") as archivo:

            # Recorrer el archivo línea por línea
            for numero_linea, linea in enumerate(archivo, 1):

                # Separar las palabras de la línea
                for palabra in linea.split():

                    # Posición que ocupará la palabra
                    posicion = len(orden_ids)

                    # Consultar si la palabra ya existe
                    registro = indice_exacto.get(palabra)

                    # --------------------------------
                    # PALABRA NUEVA
                    # --------------------------------

                    if registro is None:

                        # Asignar identificador
                        identificador = len(vocabulario)

                        # Guardar la palabra original
                        vocabulario.append(palabra)

                        # Normalizar una sola vez
                        normalizada = palabra.casefold()

                        normalizadas.append(normalizada)

                        # [ID, cantidad, primera línea, última línea]
                        indice_exacto[palabra] = [
                            identificador,
                            1,
                            numero_linea,
                            numero_linea
                        ]

                    # --------------------------------
                    # PALABRA REPETIDA
                    # --------------------------------

                    else:

                        # Recuperar su identificador
                        identificador = registro[0]

                        # Recuperar su versión normalizada
                        normalizada = normalizadas[identificador]

                        # Aumentar el contador
                        registro[1] += 1

                        # Actualizar la última línea
                        registro[3] = numero_linea

                    # --------------------------------
                    # GUARDAR LA APARICIÓN
                    # --------------------------------

                    orden_ids.append(identificador)

                    lineas.append(numero_linea)

                    # --------------------------------
                    # ÍNDICE PARA BÚSQUEDA SIMPLE
                    # --------------------------------

                    posiciones = indice_simple.get(normalizada)

                    # Si la palabra normalizada no existe
                    if posiciones is None:

                        posiciones = array("I")

                        indice_simple[normalizada] = posiciones

                    # Guardar la posición de esta aparición
                    posiciones.append(posicion)

        # ------------------------------------------------
        # VALIDAR EL CONTENIDO
        # ------------------------------------------------

        if len(orden_ids) == 0:

            print("Error: el archivo está vacío o no contiene palabras.")

            return None

        # ------------------------------------------------
        # PREPARAR BÚSQUEDAS POR PREFIJO
        # ------------------------------------------------

        # Ordenar solamente las palabras diferentes
        claves_ordenadas = sorted(indice_simple)

        # ------------------------------------------------
        # DEVOLVER LOS DATOS
        # ------------------------------------------------

        return {
            "vocabulario": vocabulario,
            "orden_ids": orden_ids,
            "lineas": lineas,
            "indice_exacto": indice_exacto,
            "indice_simple": indice_simple,
            "claves_ordenadas": claves_ordenadas
        }

    # ------------------------------------------------
    # MANEJO DE ERRORES
    # ------------------------------------------------

    except FileNotFoundError:
        print("Error: no se encontró el archivo.")

    except PermissionError:
        print("Error: no tiene permisos para leer el archivo.")

    except UnicodeDecodeError:
        print("Error: el archivo no tiene una codificación UTF-8 válida.")

    except MemoryError:
        print("Error: no hay memoria suficiente para procesar este archivo.")

    except OSError as error:
        print(f"Error: no se pudo abrir el archivo ({error}).")

    return None
    

#Metodo Principal de Busqueda
def Busqueda(datos):
    palabra = input("Ingrese la palabra que desea buscar: ").strip()
    #time.perf_counter() es el metodo que usamos para medir el tiempo de ejecucion de nuestro programa
    inicio = time.perf_counter()
    #Accedemos al dic que habiamos creado antes y pedimos solo los indices_exactos
    indice = datos["indice_exacto"]
    # .get() es una funcion de los dic en py que nos permite ver si existe lo que estamos buscando
    registro = indice.get(palabra)
    fin = time.perf_counter()
    tiempo_ms = (fin-inicio)*1000

    if registro is None:
        print("La palabra no se encuentra en el .txt")
    else:
        print("--------- Metodo Dic ----------")
        print(f"""Palabra encontrada: {palabra}
Cantidad de apariciones: {registro[1]}
Primera linea donde se encontro: {registro[2]}
Ultima Linea donde se vio: {registro[3]}""")
        print("")
        

    print("-----------Resultados------------")
    print(f"tiempo buscando: {tiempo_ms:.6f} milisegundos")
    enter = input("Presione enter para continuar: ")



def Busqueda_simple(datos):
    palabra = input("Ingrese la palabra que desea buscar: ").strip()

    if not palabra:
        print("Error: debe ingresar una palabra.")
        return

    inicio = time.perf_counter()

    palabra_normalizada = palabra.casefold()

    indice = datos["indice_simple"]

    posiciones = indice.get(palabra_normalizada)

    if posiciones is None:
        fin = time.perf_counter()
        tiempo_ms = (fin - inicio) * 1000

        print("\nLa palabra no se encuentra en el archivo.")
        print(f"Tiempo de búsqueda: {tiempo_ms:.6f} ms")
        input("Presione enter para continuar: ")
        return

    cantidad = len(posiciones)

    primera_posicion = posiciones[0]
    ultima_posicion = posiciones[-1]

    lineas = datos["lineas"]

    primera_linea = lineas[primera_posicion]
    ultima_linea = lineas[ultima_posicion]

    fin = time.perf_counter()
    tiempo_ms = (fin - inicio) * 1000

    print("\n--------- BÚSQUEDA SIMPLE ---------")
    print(f"Palabra buscada: {palabra}")
    print(f"Cantidad de apariciones: {cantidad}")
    print(f"Primera línea: {primera_linea}")
    print(f"Última línea: {ultima_linea}")

    print("----------------------------------")
    print(f"Tiempo de búsqueda: {tiempo_ms:.6f} ms")
    input("Presione enter para continuar: ")



def Busqueda_prefijo(datos):
    from bisect import bisect_left
    from heapq import merge

    prefijo = input("Ingrese el prefijo que desea buscar: ").strip()

    if not prefijo:
        print("Error: debe ingresar al menos un carácter.")
        return

    prefijo = prefijo.casefold()

    claves = datos["claves_ordenadas"]
    indice = datos["indice_simple"]

    orden_ids = datos["orden_ids"]
    vocabulario = datos["vocabulario"]
    lineas = datos["lineas"]

    inicio = time.perf_counter()

    # ---------------------------------
    # 1. BUSQUEDA BINARIA
    # ---------------------------------

    posicion = bisect_left(claves, prefijo)

    coincidencias = []

    while posicion < len(claves):

        palabra = claves[posicion]

        if not palabra.startswith(prefijo):
            break

        coincidencias.append(palabra)

        posicion += 1

    # ---------------------------------
    # 2. VALIDAR RESULTADOS
    # ---------------------------------

    if not coincidencias:

        fin = time.perf_counter()
        tiempo_ms = (fin - inicio) * 1000

        print("\nNo se encontraron palabras con ese prefijo.")
        print(f"Tiempo de búsqueda: {tiempo_ms:.6f} ms")
        input("Presione enter para continuar: ")
        return

    # ---------------------------------
    # 3. CALCULAR ESTADISTICAS
    # ---------------------------------

    cantidad = 0
    primera_posicion = None
    ultima_posicion = None

    for palabra in coincidencias:

        posiciones = indice[palabra]

        cantidad += len(posiciones)

        primera = posiciones[0]

        ultima = posiciones[-1]

        if primera_posicion is None or primera < primera_posicion:
            primera_posicion = primera

        if ultima_posicion is None or ultima > ultima_posicion:
            ultima_posicion = ultima

    primera_palabra = vocabulario[
        orden_ids[primera_posicion]
    ]

    ultima_palabra = vocabulario[
        orden_ids[ultima_posicion]
    ]

    primera_linea = lineas[primera_posicion]
    ultima_linea = lineas[ultima_posicion]

    fin = time.perf_counter()
    tiempo_ms = (fin - inicio) * 1000

    # ---------------------------------
    # 4. MOSTRAR TODAS LAS APARICIONES
    # ---------------------------------

    print("\n--------- BÚSQUEDA POR PREFIJO ---------")

    print(f"Prefijo buscado: {prefijo}")
    print(f"Palabras diferentes encontradas: {len(coincidencias)}")
    print(f"Total de apariciones: {cantidad}")

    print("\nApariciones en el orden original:\n")

    posiciones_ordenadas = merge(
        *(indice[palabra] for palabra in coincidencias)
    )

    for posicion in posiciones_ordenadas:

        identificador = orden_ids[posicion]

        palabra_original = vocabulario[identificador]

        numero_linea = lineas[posicion]

        print(f"{palabra_original} - Línea {numero_linea}")

    # ---------------------------------
    # 5. RESULTADOS FINALES
    # ---------------------------------

    print("\n--------- RESULTADOS ---------")

    print(f"Primera palabra: {primera_palabra}")
    print(f"Primera línea: {primera_linea}")

    print(f"Última palabra: {ultima_palabra}")
    print(f"Última línea: {ultima_linea}")

    print(f"Total de apariciones: {cantidad}")

    print("----------------------------------")
    print(f"Tiempo de búsqueda: {tiempo_ms:.6f} ms")
    print("(No incluye el tiempo de impresión de resultados)")
    input("Presione enter para continuar: ")


def Estadisticas(datos):
    vocabulario=datos["vocabulario"]
    orden_ids=datos["orden_ids"]
    lineas=datos["lineas"]

    #Cantidad total de palabras
    N=len(orden_ids)

    #Primera palabra
    primera=vocabulario[orden_ids[0]]
    linea_primera=lineas[0]
    #Ultima palabra
    ultima=vocabulario[orden_ids[N-1]]
    linea_ultima=lineas[N-1]

    #Posicion central
    centro=(N+1)//2
    #Concierte posicion a indice
    indice_centro=centro-1
    palabra_central = vocabulario[orden_ids[indice_centro]]
    linea_central = lineas[indice_centro]

    print("\n===== ESTADÍSTICAS DEL ARCHIVO =====")

    print(f"Cantidad total de palabras: {N}")

    print(f"Primera palabra: {primera}")
    print(f"Posición: 1 | Línea: {linea_primera}")

    print(f"Última palabra: {ultima}")
    print(f"Posición: {N} | Línea: {linea_ultima}")

    print(f"Palabra central: {palabra_central}")
    print(f"Posición: {centro} | Línea: {linea_central}")    

def palabra_numero(datos):
    vocabulario=datos["vocabulario"]
    orden_ids=datos["orden_ids"]
    lineas=datos["lineas"]
    N=len(orden_ids)

    while True:
        try:
            num=int(input(f"Ingrese la posicion de la palabra dentro del rango 1-{N}: "))
            if num<1 or num>N:
                print(f"La posicion debe estar dentro del rango 1-{N}")
                num=int(input("Ingrese numero en el rango correcto"))
            else:
                break

        except ValueError:
            print("Error: debe ingresar un numero entero")

    indice=num-1
    #inicio del tiempo de busqueda
    inicio = time.perf_counter()

    identificador=orden_ids[indice]
    palabra=vocabulario[identificador]
    linea = lineas[indice]
    #fin del tiempo de busqueda
    fin = time.perf_counter()
    # Calcular tiempo en milisegundos
    tiempo = (fin - inicio) * 1000

    # Mostrar resultado
    print("\n===== RESULTADO DE LA BÚSQUEDA =====")

    print(f"Palabra: {palabra}")
    print(f"Posición: {num}")
    print(f"Línea: {linea}")
    print(f"Tiempo de búsqueda: {tiempo:.6f} ms")

def Comparacion(datos):
    palabra = input("Ingrese la palabra que desea buscar: ").strip()
    inicio_arreglo = time.perf_counter()
    orden = datos["orden_ids"]
    vocabulario = datos["vocabulario"]
    lineas = datos["lineas"]

    cantidad = 0
    primera_linea = None
    ultima_linea = None

    for posicion, identificador in enumerate(orden):
        if vocabulario[identificador] == palabra:
            cantidad +=1

            if primera_linea is None:
                primera_linea = lineas[posicion]
            ultima_linea = lineas[posicion]

    final_arreglo = time.perf_counter()
    tiempoms_arreglo = (final_arreglo-inicio_arreglo)*1000

    if cantidad == 0:
        print("palabra no encontrada")
    else:
        print("----Metodo Arreglo----")
        print(f"""Palabra encontrada: {palabra}
Cantidad de apariciones: {cantidad}
Primera linea donde se encontro: {primera_linea}
Ultima Linea donde se vio: {ultima_linea}""")
        print("""
""")

        enter = input("Presiona enter para continuar con el otro metodo: ")
    inicio = time.perf_counter()
    #Accedemos al dic que habiamos creado antes y pedimos solo los indices_exactos
    indice = datos["indice_exacto"]
    # .get() es una funcion de los dic en py que nos permite ver si existe lo que estamos buscando
    registro = indice.get(palabra)
    fin = time.perf_counter()
    tiempo_ms = (fin-inicio)*1000
        
    if registro is None:
        print("La palabra no se encuentra en el .txt")
    else:
        print("---Metodo Dic---")
        print(f"""Palabra encontrada: {palabra}
Cantidad de apariciones: {registro[1]}
Primera linea donde se encontro: {registro[2]}
Ultima Linea donde se vio: {registro[3]}""")
        print("")
        enter = input("presione enter para continuar: ")


        

    diferencia = abs(tiempoms_arreglo - tiempo_ms)   
    print("----------------------Resultados-------------------")
    print(f"Método Arreglo O(N): {tiempoms_arreglo:.6f} milisegundos ")
    print(f"Método Diccionario O(1): {tiempo_ms:.6f} milisegundos")
    print("")
    if tiempo_ms < tiempoms_arreglo: 
        print("Ganador: Metodo Diccionario O(1)")
        print(f"Diferencia: {diferencia:.6f} ms")
    elif tiempo_ms > tiempoms_arreglo:
        print("Ganador: Metodo Arreglo O(N)")
        print(f"Diferencia: {diferencia:.6f} ms")
    else:
        print("Ganador: Empate")
        print(f"Diferencia: {diferencia:.6f} ms")

    # Verificar que ambos algoritmos entreguen los mismos resultados
    if registro is None:
        if cantidad == 0 and primera_linea is None and ultima_linea is None:
            print("Verificación: ambos algoritmos coinciden. Palabra no encontrada.")
        else:
            print("Error: los algoritmos entregaron resultados diferentes.")
    else:
        if cantidad == registro[1] and primera_linea == registro[2] and ultima_linea == registro[3]:
            print("ambos algoritmos entregaron resultados identicos.")
        else:
            print("Verificacion: ambos algortimos entregaron resultados distintos.")

    enter = input("presione enter para continuar: ")
    
        
  
     
        
    