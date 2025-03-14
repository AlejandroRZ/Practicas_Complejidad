# Práctica 1 - Complejidad computacional
# Autores: 
#   - Javier Alejandro Rivera Zavala
#   - Ulises Rodríguez García
#   - Zurisadai Uribe García



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
Esta función escribe la matriz de adyacencia en el archivo de salida junto con detalles adicionales.
:param matriz: Matriz de adyacencia.
:param nombreArchSal: Ruta del archivo de salida.
:param k: Valor del parámetro K.
"""
def escribeArchivoSalida(matriz, nombreArchSal, k):
    # Abre el archivo en modo escritura
    with open(nombreArchSal, 'w') as archivo:
        # Escribe el valor de k en binario con espacios entre dígitos en una línea
        kBinario = ' '.join(bin(k)[2:])
        archivo.write(kBinario + '\n')

        # Escribe cada fila de la matriz con espacios entre dígitos en el archivo
        for fila in matriz:
            filaStr = ' '.join(map(str, fila))
            archivo.write(filaStr + '\n')


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

    

   

#Entrada a main
if __name__ == "__main__":
    entrada = input("Nombre del archivo de entrada: ")
    salida = input("Nombre del archivo de salida: ")
    if (entrada == salida):
        raise ValueError("El nombre de archivo de entrada y salida no puede ser el mismo.\n")
    try:
        cadenaBinRep = leerArchivoEntrada(entrada)
        if cadenaBinRep is None:
            raise ValueError("Debe de ingresarse algún ejemplar válido del problema\n")
        k, n, aristas, matriz = transformaRepresentacion(cadenaBinRep)        
        print(f"El ejemplar es una gráfica G con {n} vértices y {aristas} aristas, así como una cota K = {k}\n")
        escribeArchivoSalida(matriz, salida, k)
        print(f"Se leyeron el parametro {k} y la representación de la gráfica G de {n} vértices \n" + \
              f"del archivo {entrada}, al final se escribió la matriz de adyacencias de G en el archivo {salida}\n")
    except ValueError as e:
        print("Verifica la representación de entrada\n")
    except TypeError as e:
        print("No fue posible efectuar la transformación\n")
    except FileNotFoundError:
        print(f"El archivo {entrada} ó {salida} no han logrado abrise con éxito.\n")
