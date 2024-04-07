import os
import random
import time
# Crear una matriz vacía de 8x8
matrix = [[0 for j in range(8)] for i in range(8)]
# Crear un diccionario para almacenar las posiciones de escaleras y serpientes
escaleras_serpientes = {}
# Crear un diccionario para almacenar las adivinanzas
adivinanzas = {}
# Crear un diccionario para almacenar los paises
diccionario_paises = {}
# Llenar la matriz de abajo hacia arriba
contador = 1
for i in range(7, -1, -1):
    if (7 - i) % 2 == 0:  # Fila par en zigzag
        for j in range(8):
            matrix[i][j] = str(contador).zfill(2)
            contador += 1
    else:  # Fila impar en zigzag
        for j in range(7, -1, -1):
            matrix[i][j] = str(contador).zfill(2)
            contador += 1

def limpiar_consola():
    if os.name == 'posix':  # Para sistemas basados en Unix, como Linux y macOS
        os.system('clear')
    else:  # Para otros sistemas, como Windows
        os.system('cls')

# Leer datos del archivo y asignar valores a la matriz
def leer_letras(archivo):
    with open(archivo, 'r') as file:
        for line in file:
            fila, columna, valor = line.split()
            matrix[int(fila)][int(columna)] = valor

# Leer el archivo y guardar las posiciones
def leer_Serpientes_Escaleras(archivo):
    with open(archivo, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 6:
                tipo_inicio, inicio_fila, inicio_columna, tipo_fin, fin_fila, fin_columna = parts
                inicio = (int(inicio_fila), int(inicio_columna))
                fin = (int(fin_fila), int(fin_columna))
                if tipo_inicio.upper() == 'W':
                    escaleras_serpientes[inicio] = ('escalera', fin)
                    matrix[inicio[0]][inicio[1]] = tipo_inicio +" "
                    matrix[fin[0]][fin[1]] = tipo_fin+" "
                elif tipo_inicio.upper() == 'X':
                    escaleras_serpientes[inicio] = ('serpiente', fin)
                    matrix[inicio[0]][inicio[1]] = tipo_inicio+" "
                    matrix[fin[0]][fin[1]] = tipo_fin+" "

# Leer el archivo y guardar las adivinanzas
def leer_adivinanzas(archivo):   
    with open(archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split(";")
            if len(partes) == 3:
                letra, animal, adivinanza = partes
                adivinanzas[letra] = (animal, adivinanza)
            else:
                print(f"Advertencia: la línea '{linea.strip()}' no tiene el formato esperado.")

def lectura_normal(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            letra, paises = linea.strip().split(';')
            diccionario_paises[letra] = paises.split(', ')
    return diccionario_paises

menu = 0
while menu not in [1, 2]:
    menu = int(input("SELECCIONE UNA DIFICULTAD:\n1)NORMAL\n2)ADIVINANZAS\n3)INFORMACIÓN\n-"))
    if menu == 1:
        limpiar_consola()
        usuario_normal = input("Ingrese su NICKNAME: ")
        puntaje_normal = 0
        leer_letras("letras.txt")
        leer_Serpientes_Escaleras("normal_Serpientes_Escaleras.txt")
        lectura_normal("palabras_normal.txt")
        limpiar_consola()
        break  # Salir del bucle después de seleccionar una dificultad
    elif menu == 2:
        limpiar_consola()
        usuario_dificil = input("Ingrese su NICKNAME: ")
        puntaje_dificil = 0
        leer_letras("letras.txt")
        leer_Serpientes_Escaleras("dificil_Serpientes_Escaleras.txt")
        leer_adivinanzas("adivinanzas_dificil.txt")
        limpiar_consola()
        break  # Salir del bucle después de seleccionar una dificultad
    elif menu == 3:
        print("""
Piensa y Juega es un juego al estilo de Escaleras y Serpientes que te sorprenderá con algunos retos de palabras. En nuestro modo normal, necesitarás tener conocimiento sobre países o ciudades, y objetos para escribir la palabra correcta según la letra y la señalización: si la letra está precedida por un punto, significa que la palabra a colocar es un objeto; si el punto viene después, es un país o una ciudad.

Por otro lado, en nuestro modo de juego más difícil, Adivinanzas, tendrás que resolver acertijos cuya respuesta comienza con la letra en la que caíste.

Piensa y Juega es un juego muy competitivo, por lo que nuestro sistema de puntos beneficia a los jugadores más conocedores. En el modo normal, ganarás +1 si tomas una escalera y +1 si aciertas una palabra; no te preocupes, en este modo nada te quitará tus puntos. En el modo Adivinanzas, ganarás +1 si tomas una escalera y +1 si aciertas el acertijo, además de moverte una casilla adicional. Sin embargo, en este modo, perderás -1 si caes en una serpiente.

Piensa y Juega te brinda la posibilidad de crear tus propios mapas con tus propias combinaciones de escaleras, serpientes, letras, adivinanzas y palabras. Anímate a crear tus propias partidas y compite por entrar en uno de los mejores puntajes. ¡Disfruta del juego!
""")
        # No hay 'break' aquí, por lo que el bucle continuará
    else:
        print("Por favor, seleccione una opción válida.")

# Imprimir la matriz
for row in matrix:
    print(" | ".join(str(cell) for cell in row))

def lanzar_dado():
    return random.randint(1, 6)
 
def mostrar_adivinanza(letra):
    global puntaje_dificil
    if letra in adivinanzas:
        animal, adivinanza = adivinanzas[letra]
        print(f"Adivinanza: {adivinanza}")
        respuesta = input("¿Quién soy? ").strip()
        if respuesta.lower() == animal.lower():
            print("¡Correcto! Avanzas una casilla adicional.")
            time.sleep(2)
            puntaje_dificil+=1
            limpiar_consola()
            return True
        else:
            print("Incorrecto. Te quedas en la misma casilla.")
            time.sleep(2)
            puntaje_dificil-=1
            limpiar_consola()
            return False

def comprobar_palabra(diccionario, valor_casilla):
    global puntaje_normal
    letra = valor_casilla.strip('.')
    if valor_casilla.startswith('.'):
        print(f"La palabra debe ser un objeto que empiece por la letra {letra}")
    elif valor_casilla.endswith('.'):
        print(f"La palabra debe ser un país o ciudad que empiece por la letra {letra}")
    else:
        pass
    
    opciones = diccionario.get(valor_casilla)
    if opciones:
        respuesta = input("--").strip()
        opciones_minusculas = [opcion.lower() for opcion in opciones]
        if respuesta.lower() in opciones_minusculas:
            puntaje_normal += 1
            print("¡Correcto!")
            time.sleep(2)
            limpiar_consola()
        else:
            print("Incorrecto")
            time.sleep(2)
            limpiar_consola()
    else:
        pass

def mover_jugador(posicion, pasos, valor_anterior):
    fila, columna = posicion
    for _ in range(pasos):
        if fila == 0 and columna == 0:  # El jugador ya está en la meta
            break
        if (7 - fila) % 2 == 0:  # Fila par en zigzag
            if columna < 7:
                columna += 1
            else:
                fila -= 1
        else:  # Fila impar en zigzag
            if columna > 0:
                columna -= 1
            else:
                fila -= 1
    return fila, columna, valor_anterior

def verificar_casilla_adivinanza(posicion_jugador, matrix):
    fila, columna = posicion_jugador
    valor_casilla = matrix[fila][columna]
    if str(valor_casilla) in adivinanzas:
        print(f"Has caído en la casilla {valor_casilla}")
        if mostrar_adivinanza(str(valor_casilla)):
            # Mover al jugador una casilla adicional si responde correctamente
            fila, columna, _ = mover_jugador(posicion_jugador, 1, valor_anterior)
            posicion_jugador = (fila, columna)
            # Verificar si la nueva casilla también tiene una adivinanza
            if posicion_jugador == (0,0):
                return posicion_jugador
            else:
                posicion_jugador = verificar_casilla_adivinanza(posicion_jugador, matrix)
    return posicion_jugador

def actualizar_puntajes(nombre_archivo, nuevo_nombre, nuevo_puntaje):
    nombres = []
    puntajes = []

    # Leer los puntajes actuales del archivo
    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            nombre, puntaje = linea.strip().split("  ")
            nombres.append(nombre)
            puntajes.append(int(puntaje))

    # Insertar el nuevo puntaje en la posición correcta
    insertado = False
    for i, puntaje in enumerate(puntajes):
        if nuevo_puntaje > puntaje:
            nombres.insert(i, nuevo_nombre)
            puntajes.insert(i, nuevo_puntaje)
            insertado = True
            break

    # Si el nuevo puntaje no es mayor que ninguno existente, añadirlo al final
    if not insertado:
        nombres.append(nuevo_nombre)
        puntajes.append(nuevo_puntaje)

    # Asegurarse de que solo haya 5 puntajes en la lista
    nombres = nombres[:5]
    puntajes = puntajes[:5]

    # Volver a escribir los puntajes actualizados en el archivo
    with open(nombre_archivo, "w") as archivo:
        for nombre, puntaje in zip(nombres, puntajes):
            archivo.write(f"{nombre}  {puntaje}\n")

    # Mostrar los puntajes en la consola
    print("Mejores puntajes:")
    for nombre, puntaje in zip(nombres, puntajes):
        print(f"{nombre}: {puntaje}")

# Posición inicial del jugador y valor anterior
posicion_jugador = (7, 0)
valor_anterior = matrix[posicion_jugador[0]][posicion_jugador[1]]
matrix[posicion_jugador[0]][posicion_jugador[1]] = '* '

# Bucle de juego
game = True
while game:
    input("Presiona Enter para lanzar el dado...")
    limpiar_consola()
    dado = lanzar_dado()
    print(f"Has sacado un {dado}")

    # Calcular la nueva posición sin mover al jugador todavía
    nueva_fila, nueva_columna, _ = mover_jugador(posicion_jugador, dado, valor_anterior)

    # Verificar si el jugador se pasaría de la meta
    if nueva_fila < 0 or nueva_columna < 0:
        print("Te has pasado de la meta. Tira de nuevo.")
        continue  # El jugador tira de nuevo el dado sin moverse

    # Extraer el valor de la casilla donde caerá el jugador
    valor_casilla = matrix[nueva_fila][nueva_columna]

    # Restaurar el valor anterior en la posición actual del jugador
    matrix[posicion_jugador[0]][posicion_jugador[1]] = valor_anterior

    # Mover el jugador y obtener el valor anterior de la nueva posición
    fila, columna, valor_anterior = mover_jugador(posicion_jugador, dado, valor_anterior)
    posicion_jugador = (fila, columna)
    if(menu==1):
        comprobar_palabra(diccionario_paises,str(valor_casilla))
    elif(menu==2):
        posicion_jugador = verificar_casilla_adivinanza(posicion_jugador, matrix)

    # Marcar la nueva posición del jugador en la matriz y almacenar el valor anterior
    valor_anterior = matrix[posicion_jugador[0]][posicion_jugador[1]]
    matrix[posicion_jugador[0]][posicion_jugador[1]] = '* ' 

    print(f"Te mueves a la posición {posicion_jugador}")

    # Verificar si el jugador ha llegado a una escalera o serpiente
    if posicion_jugador in escaleras_serpientes:
        tipo, nueva_posicion = escaleras_serpientes[posicion_jugador]
        if(menu==1):
            if tipo =='W':
                puntaje_normal+=1
        elif(menu==2):
            if tipo =='W':
                puntaje_dificil+=1
            elif tipo == 'X':
                puntaje_dificil-=1    
        print(f"¡Has encontrado una {tipo}! Te mueves a la posición {nueva_posicion}")

        # Borrar la posición actual del jugador en la matriz
        matrix[posicion_jugador[0]][posicion_jugador[1]] = valor_anterior

        # Actualizar la posición del jugador y obtener el valor anterior de la nueva posición
        posicion_jugador = nueva_posicion
        valor_anterior = matrix[posicion_jugador[0]][posicion_jugador[1]]

        # Marcar la nueva posición del jugador en la matriz
        matrix[posicion_jugador[0]][posicion_jugador[1]] = '* '

    # Imprimir la matriz
    for row in matrix:
        print(" | ".join(str(cell) for cell in row))

    # Verificar si el jugador ha llegado al final
    if posicion_jugador == (0, 0):
        limpiar_consola()
        print("¡Felicidades! Has llegado al final")
        if(menu==1):
            print(f"Su puntaje total es:{puntaje_normal}")
            actualizar_puntajes("puntajes_normal.txt",usuario_normal,puntaje_normal)
        elif(menu==2):
            print(f"Su puntaje total es:{puntaje_dificil}")
            actualizar_puntajes("puntajes_dificil.txt",usuario_dificil,puntaje_dificil)
        game = False
        break

input("Presiona Enter para salir...")