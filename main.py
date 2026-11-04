import librerias as lb

#Variables
Activo = True # bandera que controla el bucle
Archivo_cargado = False #bandera que indica cuando el archivo ya este cargado

#Bucle que mantiene funcionando el codigo
while Activo:
    try:
        print("""    Menu     
1) Cargar Archivo
2) Búsqueda Exacta 
3) Búsqueda Simple 
4) Búsqueda por Prefijo 
5) Estadísticas 
6) Buscar Palabra No
7) Análisis Comparativo 

0) Salir""")
        
        print("")
        elec = int(input("Eleccion: "))

        if elec <0 or elec >7:
            print("Error, numero fuera de rango.")

        elif elec == 0:
            sali = input("Seguro de querer salir(s/n):").lower()
            if sali == "s":
                print("Saliendo")
                Activo = False

        elif elec != 1 and Archivo_cargado:
            match elec:
                case 2:
                    lb.Busqueda(datos)
                case 3:
                    lb.Busqueda_simple(datos)
                case 4:
                    lb.Busqueda_prefijo(datos)
                case 5:
                    lb.Estadisticas(datos)
                case 6:
                    lb.palabra_numero(datos)
                case 7:
                    lb.Comparacion(datos)
        elif elec != 1 and not(Archivo_cargado):
            print("No puede acceder a esta funcion hasta que el archivo sea cargado.")
            enter = input("""
Presione enter para continuar: """)
        else:
            if Archivo_cargado:
                des = input("ya tienes un archivo cargado, deseas cambiarlo? (s/n): ").lower()

                if des != "s":
                    continue

            nuevo = lb.Cargar_Archivo()

            if nuevo is not None:

                datos = nuevo

                Archivo_cargado = True

                print("Archivo cargado con éxito.")

                print("Total de palabras:", len(datos["orden_ids"]))

                print("Palabras diferentes:", len(datos["vocabulario"]))

                enter = input("Presione enter para continuar: ")
                
            else:
                print("error, Archivo no fue cargado.")
                enter = input("""
Presione enter para continuar: """)

        
        
    except Exception as e:
        print(e)