# Práctica 1 - Complejidad computacional
# Autores: 
#   - Javier Alejandro Rivera Zavala
#   - Ulises Rodríguez García
#   - Zurisadai Uribe García
import random


"""
Esta función lee el contenido del archivo de entrada y retorna una cadena de caracteres.
:param nombreArchEnt: Ruta del archivo de entrada.
:return str: Contenido del archivo de entrada en formato cadena.
"""
def leerArchivoEntrada(nombreArchEnt):
    with open(nombreArchEnt, 'r') as archivoEnt:
        cadenaRepresentacion = archivoEnt.read().strip()
    return cadenaRepresentacion

"""
Esta función escribe el contenido de un arreglo como una cadena en un archivo de texto plano.
:param nombreArchivo: Ruta del archivo de salida.
"""
def escribeCertificado(arreglo, nombreArchivo):
    with open(nombreArchivo, 'w') as archivo:
        cadena = ''.join(map(str, arreglo))            
        archivo.write(cadena)


#################################### De la práctica anterior  ###########################################
"""
Esta función transforma la representación binaria de un ejemplar del problema a una matriz de adyacencia.
:param cadenaBinaria: Representación binaria del ejemplar del problema.
:return tuple: Contiene el valor de K, el número de vértices, el número de aristas y la matriz de adyacencia.
"""
def transformaRepresentacion(cadenaBinaria):
    longitudK = 0
    longitudN = 0
    i = 0    
    #Obteniendo las longitudes en digitos de K y n 
    while cadenaBinaria[i] == '0':           
        longitudK += 1
        i += 1
       
    if not cadenaBinaria[i] == '1':
        print("Entrada no válida, la representación sólo debe de consistir de 0's y 1's\n")
        return None
    i += 1 
                    
    while cadenaBinaria[i] == '0':           
        longitudN += 1
        i += 1
    
    if not cadenaBinaria[i] == '1':
        print("Entrada no válida, la representación sólo debe de consistir de 0's y 1's\n")
        return None
    i += 1

    # Verificando que las longitudes m y h sean válidas
    if longitudK <= 0 or longitudN <= 0:
        print("La dimensión del parámetro K ó del indicador para el número vértices, no se \n" +
              "especificaron debidamente.\n")
        return None
    #Verificando que haya suficientes digitos para buscar a n y a  K    
    if len(cadenaBinaria) < (2*(longitudK+longitudN+1)):
        return None
    # Obteniendo los valores de K y n    
    k = int(cadenaBinaria[i:i+longitudK], 2)
    i += longitudK
    
    n = int(cadenaBinaria[i:i+longitudN], 2)
    i += longitudN
   
    # Verificando que K y n sean válidos
    if k > n:
        print("Entrada no válida, el valor de K ha de ser menor o igual al número de vértices\n")
        return None   

    # Verificando la longitud total de la cadena
    if len(cadenaBinaria) != i + n*n:
        print("La longitud de la subcadena que representa la gráfica no es consistente con los valores de K y n.\n")
        return None     

    # Construyendo la matriz de adyacencia y contando el número de aristas   
    matriz = []
    contadorAristas = 0

    for j in range(n):
        filaMatriz = []

        for _ in range(n):            
                    
            if cadenaBinaria[i] not in '01':
                print("Entrada no válida, la entrada debe consistir únicamente de unos y ceros\n")
                return None
                    
            if cadenaBinaria[i] == '1':
                contadorAristas += 1
            if (i-(2*(longitudK+longitudN+1))) % n == j and cadenaBinaria[i] != '0' : #Quitar para aceptar lazos
                print("Sólo se aceptan gráficas sin lazos\n")
                return None
                    
            filaMatriz.append(int(cadenaBinaria[i]))
            i += 1
        matriz.append(filaMatriz) 

    # Verificación de que la matriz de adyacencia represente una gráfica no dirigida
    #for x in range(n):
     #   for y in range(x + 1, n):
      #      if matriz[x][y] != matriz[y][x]:
       #         print("Sólo se aceptan gráficas no dirigidas\n")
        #        return None 
    cociente = contadorAristas//2
    residuo = contadorAristas%2
    if residuo == 1:
        contadorAristas = cociente+1
    else:
        contadorAristas = cociente                 

    return k, n, contadorAristas, matriz
#################################### De la práctica anterior  ###########################################
    

"""
Genera un certificado para el problema de la ruta inducia a partir de una matriz de adyacencias, 
así como un entero positivo k.
:param matrizAdyacencias: Una matriz que representa las adyacencias entre vértices de la gráfica.
:param k: tamaño del subconjunto de vértices a considerar, 0<k<=|V|.
:return: una representación binaria del certificado generado.
"""

def generadorCertificado(matrizAdyacencias, k):
    # Verifica que el tamaño del subconjunto sea válido
    if k > len(matrizAdyacencias) or k < 1:
        print("Error: El tamaño del subconjunto no puede ser mayor que el número de vértices ni menor que 1.")
        return

    # Crea una lista de vértices disponibles y la mezcla de manera aleatoria    
    verticesDisponibles = list(range(len(matrizAdyacencias)))
    random.shuffle(verticesDisponibles)
    # Selecciona los primeros k vértices como parte del subconjunto
    subconjunto = verticesDisponibles[:k]

    representacionBinaria = [0] * len(matrizAdyacencias)
     # Marca con '1' los vértices seleccionados en el certificado
    for vertice in subconjunto:
        representacionBinaria[vertice] = 1       

    return representacionBinaria



"""
Verifica la validez de un certificado para el problema de la ruta inducida.
:param matrizAdyacencias: una matriz que representa las adyacencias entre vértices de la gráfica.
:param certificado: un certificado binario a verificar.
:param k: tamaño del subconjunto especificado en el certificado.
:return: True si el certificado es válido, False en caso contrario.
"""
def verificadorCertificados(matrizAdyacencias, certificado, k):
    
    numVertices = len(matrizAdyacencias)
    contadorUnos = 0
    # Verifica que el certificado tenga el tamaño correcto
    if len(certificado) < 1 or len(certificado) != numVertices:
        return False
    # Cuenta la cantidad de '1' en el certificado    
    for indice in range(numVertices):
        if certificado[indice] == '1':
            contadorUnos += 1

    if contadorUnos != k:
        return False

    gradoVertice = 0    
    contadorHojas = 0
    hojas = []
    # Itera sobre los vértices del certificado
    for indiceCertificado in range(numVertices):
        if certificado[indiceCertificado] == '0':
            continue

        elif certificado[indiceCertificado] == '1':
            # Itera sobre las columnas de una fia de la matriz de adyancencias
            for indiceColumna in range(numVertices):                                    
                # Si hay una adyacencia con otro vértice en el subconjunto
                if matrizAdyacencias[indiceCertificado][indiceColumna] == 1:                                     
                    if certificado[indiceColumna] == '1': 
                        gradoVertice += 1

            #Verificaciones de grado            
            if gradoVertice != 1 and gradoVertice != 2:
                return False

            if gradoVertice == 1:                
                contadorHojas += 1
                hojas += [indiceCertificado]


            if contadorHojas > 2:
                return False            
            
            gradoVertice = 0          

        else:
            print("Error, los certificados deben de constar de ceros y unos.")
            return False   
    #Verificación final de hojas                
    if contadorHojas != 2:
        return False 

    if k == 2:
        return True

    #Verificación si los vértices forman una trayectoria de longitud k    
    lista = [-1] * k
    
    lista[0] = hojas[0]
    lista[-1] = hojas[1]
    vecinoPrimero = hojas[0]
    vecinoSegundo = hojas[1]

    #Buscamos a los vecinos de las hojas
    for indiceCol in range(numVertices):
        if matrizAdyacencias[hojas[0]][indiceCol] == 1:
            if certificado[indiceCol] == '1':
                vecinoPrimero = indiceCol
                break

    for indiceCol in range(numVertices):
        if matrizAdyacencias[hojas[1]][indiceCol] == 1:
            if certificado[indiceCol] == '1':
                vecinoSegundo = indiceCol
                break

    # Si hay un único vecino para las hojas y ya contemplamos todos lo vértices, terminamos.        
    if vecinoPrimero == vecinoSegundo and k == 3:
        return True     

    # Si sólo las hojas son vecinas, devolvemos false
    if vecinoPrimero == hojas[1] or vecinoSegundo == hojas[0]:
        return False

    #Buscamos los vecinos de los vértices anteriores que no sean iguales a sus
    #inmediatos anteriores en una lista.
    
    lista[1] = vecinoPrimero
    lista[-2] = vecinoSegundo

    i = 0
    contador = 4
    while(True):    
        for indiceCol in range(numVertices):
            if matrizAdyacencias[vecinoPrimero][indiceCol] == 1 and lista[i] != indiceCol:
                if certificado[indiceCol] == '1': 
                    vecinoPrimero = indiceCol
                    break

        for indiceCol in range(numVertices):
            if matrizAdyacencias[vecinoSegundo][indiceCol] == 1 and lista[-(i + 1)] != indiceCol:
                if certificado[indiceCol] == '1': 
                    vecinoSegundo = indiceCol
                    break
          
        i += 1
        #Si ya se encontraron los vecinos, no añadimos nada y rompemos
        if vecinoSegundo == lista[i]:
            break
        lista[i+2] = vecinoPrimero
        lista[-(i + 3)] = vecinoSegundo
        
        if vecinoPrimero == vecinoSegundo:
            contador += 1
            break
        else:
            contador += 2

    if contador != k:
        return False      
   

    return True

   

#Entrada a main
if __name__ == "__main__":    

    while True:
    # Menú principal
        print("\nMenú:")
        print("1. Generar Certificado")
        print("2. Verificar Certificado")
        print("3. Salir")

        opcion = input("Selecciona una opción, ingresa el número: ")

        if opcion == "1":

            entrada = input("Nombre del archivo de entrada: ")
            salida = input("Nombre del archivo de salida: ")
            if (entrada == salida):
                print("El nombre de archivo de entrada y salida no puede ser el mismo.\n")
                continue
            try:
                cadenaBinRep = leerArchivoEntrada(entrada)
                if cadenaBinRep is None:
                    print("Debe de ingresarse algún ejemplar válido del problema\n")
                    continue
                k, n, aristas, matriz = transformaRepresentacion(cadenaBinRep) 
                certificadoGenerado = generadorCertificado(matriz,k)
                escribeCertificado(certificadoGenerado, salida)        
                print(f"Certificado escrito en el archivo {salida}")
            except ValueError as e:
                print("Verifica la representación de entrada\n")
            except TypeError as e:
                print("No fue posible efectuar la operación\n")
            except FileNotFoundError:
                print(f"El archivo {entrada} ó {salida} no han logrado abrise con éxito.\n")
            except FileNotFoundError:
                print(f"No se encontró el archivo {entrada} o {salida}.\n")    

        elif opcion == "2":
        
            archivoEjemplar = input("Nombre del archivo con el ejemplar: ")
            archivoCertificado = input("Nombre del archivo con el certificado: ")
            if (archivoEjemplar == archivoCertificado):
                print("El nombre de los archivos de entrada no puede ser el mismo.\n")
                continue
            try:
                ejemplar = leerArchivoEntrada(archivoEjemplar)
                certificado = leerArchivoEntrada(archivoCertificado)
                if ejemplar is None or certificado is None:
                    print("Las entradas no pueden ser nulas\n")
                    continue
                k, n, aristas, matriz = transformaRepresentacion(ejemplar)
                respuesta = verificadorCertificados(matriz,certificado,k)
                print(f"El valor de k es: {k}.\n")
                if respuesta == True:
                    print(f"El certificado es una solución al problema.\n") 
                else:
                    print(f"El certificado no es una solución al problema.\n")
                    continue             
            except ValueError as e:
                print("Verifica que hayas ingresado un par de entradas correctas\n")
            except TypeError as e:
                print("No fue posible efectuar la verificación\n")
            except FileNotFoundError:
                print(f"El archivo {archivoEjemplar} ó {archivoCertificado} no han logrado abrise con éxito.\n") 
            except FileNotFoundError:
                print(f"No se encontró el archivo {archivoEjemplar} o {archivoCertificado}.\n")   

        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elige 1, 2 o 3.")
