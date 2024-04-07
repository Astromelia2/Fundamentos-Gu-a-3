############################################################
############## BIBLIOTECA PERSONAL DE METODOS ##############
### AUTORES:FLOR ALBA TOVAR PEREA
GERALDIN PAOLA PALACIO MÁRQUEZ
JULIO MARIO RAMOS LOPEZ
### VERSIÓN: 1.0 
############################################################
#######    Aquí se incluyen los métodos más usados  ########
############################################################

def limpiar_consola():
    """
    Desc: Limpia la consola de comandos.
    Pre : La consola tiene texto o está vacía.
    Pos : La consola queda limpia sin texto visible.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def leer_letras(archivo):
    """
    Desc: Lee un archivo que contiene la configuración de las letras en la matriz del juego y las asigna a la matriz.
    Pre : El archivo existe y tiene el formato correcto (fila, columna, valor).
    Pos : La matriz del juego se actualiza con las letras leídas del archivo.
    """
    with open(archivo, 'r') as file:
        for line in file:
            fila, columna, valor = line.split()
            matrix[int(fila)][int(columna)] = valor

def leer_Serpientes_Escaleras(archivo):
    """
    Desc: Lee un archivo que contiene la configuración de las serpientes y escaleras en el juego y las asigna a la matriz y al diccionario escaleras_serpientes.
    Pre : El archivo existe y tiene el formato correcto (tipo_inicio, inicio_fila, inicio_columna, tipo_fin, fin_fila, fin_columna).
    Pos : La matriz del juego y el diccionario escaleras_serpientes se actualizan con la configuración de serpientes y escaleras.
    """
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

def leer_adivinanzas(archivo):
    """
    Desc: Lee un archivo que contiene adivinanzas y las almacena en el diccionario adivinanzas.
    Pre : El archivo existe y tiene el formato correcto (letra; animal; adivinanza).
    Pos : El diccionario adivinanzas se actualiza con las adivinanzas leídas del archivo.
    """
    with open(archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split(";")
            if len(partes) == 3:
                letra, animal, adivinanza = partes
                adivinanzas[letra] = (animal, adivinanza)
            else:
                print(f"Advertencia: la línea '{linea.strip()}' no tiene el formato esperado.")

def mover_jugador(posicion, pasos, valor_anterior):
    """
    Desc: Mueve al jugador en la matriz del juego según el número de pasos dados.
    Pre : La posición actual del jugador es válida y los pasos son un número entero no negativo.
    Pos : La posición del jugador se actualiza en la matriz del juego, y se devuelve la nueva posición junto con el valor anterior de la casilla a la que se movió.
    """
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
    """
    Desc: Verifica si la casilla en la que cae el jugador contiene una adivinanza y, en caso afirmativo, muestra la adivinanza y solicita una respuesta.
    Pre : La posición del jugador es válida y la matriz contiene posibles adivinanzas.
    Pos : Si la casilla contiene una adivinanza y el jugador responde correctamente, se actualiza la posición del jugador y se devuelve la nueva posición. Si la respuesta es incorrecta, se mantiene la posición actual.
    """
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
    """
    Desc: Actualiza el archivo de puntajes con el nombre y puntaje del jugador, manteniendo solo los 5 mejores puntajes.
    Pre : El archivo de puntajes existe y el nuevo puntaje es un número entero.
    Pos : El archivo de puntajes se actualiza con el nuevo puntaje y nombre del jugador, si corresponde, y se mantienen solo los 5 mejores puntajes.
    """
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

