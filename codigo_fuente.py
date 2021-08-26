"""
Proyecto del Curso Introducción a la Computación - Grupo 010

Estudiantes:
Daniel Fallas Sibaja - B66831
Freddy Calvo Avendaño - B61334

Descripción del programa:
El siguiente es el codigo de un juego funcional tipo Same.
El juego crea una cuadricula el tamaño deseado por el usuario en la cual se muestran bloques
de distintos colores que se pueden eliminar al clickearlos si cumplen con la condicion de que hayan 3
o mas cuadros del mismo color de manera adyacente (no diagonal). El objetivo del juego es terminar el
juego con la puntuacion mas alta posible. Esta puntuacion incrementa a lo largo del juego en dependencia
de la cantidad de bloques eliminados por el jugador En un area a la derecha de la ventana se muestra un menu
que en tiempo real señala el puntaje del jugador, la cantidad de movimientos posibles en todo momento,
botones para poder controlar el juego desde la misma ventana junto con instrucciones de como controlar ciertas
funciones desde el teclado. En la ventana del menu tambien se indica cuando el juego ha terminado y la misma
cambia de color a rojo con el fin de llamar la atencion del jugador en caso de que este se encuentre muy concentrado
en la cuadricula de colores.


Division de trabajo:

Trabajo realizado de manera conjunta por ambos estudiantes

Lista de frases aleatorias en el menu con el fin de entretenimiento
Ajustes del tamaño de la ventana y posicion de los elementos de la misma
Codigo para guardar el click del mouse y poder jugar con el mismo a lo largo de la partida
Codigo que cuenta el numero de movimientos y el puntaje del en tiempo real a lo largo de la partida
Codigo que permite crear una nueva partida y regresar el puntaje a cero
Botones del menu y sus respuestas al utilizarlos

Trabajo realizado especificamente por Daniel
Paleta de colores
Codigo que crea una matriz de respaldo para hacer posible el reinicio de partidas
Codigo que dibuja los botones del menu
Codigo que escoge una frase aleatoria y la muestra en el menu con el fin de entretener al jugador
Posicion de los elementos del menu
Codigo que permite reiniciar la partida actual y su respectivo puntaje a cero

Freddy
Codigo que revisa los adyacentes y mueve los bloques en caso de que una jugada sea valida
Codigo para crear la matriz con los bloques aleatorios
Codigo para que se muestre por defecto una matriz simetrica al inicio del juego
Limites del tamaño de la cuadricula para que el juego se ejecute sin pesar mucho
Codigo que dibuja los bloques de la cuadricula

Algunos recursos online de los que se hizo uso para entender funciones
o para esocoger la paleta de colores que se uso en el juego son los siguientes:

Detalles sobre el dibujo de superficies en pygame
https://realpython.com/pygame-a-primer/
Se utilizo al principio cuando no teniamos muy claro como empezar

Tabla de colores y su respectivo codigo valor rgb
https://htmlcolorcodes.com/es/tabla-de-colores/
Se utilizo al inicio cuando decidimos usar colores mas atractivos a la vista
y que una persona con problemas de daltonismo pudiese jugar

Pagina dedicada a pygame para explicar diferentes funciones y como utlizarlas
https://www.pygame.org/docs/
Se utilizo a lo largo de todo el proyecto cuando haciamos pruebas utilizando diferentes
funciones o no estabamos seguros sobre como se utlizaba alguna en especifico

Foro dedicado a resolver dudas sobre codigo
https://stackoverflow.com/
Se utilizo cuando buscabamos un error especifico sobre alguna funcion
y alguien ya habia anteriormente cual era el error en el foro y como resolverlo
"""

import pygame
import random

#Paleta de colores principal
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (155, 155, 155)
AZUL = (80, 180, 216)
ROJO = (255, 96, 96)
AMARILLO = (247, 229, 183)
VERDE = (167, 217, 201)
VIOLETA = (194, 155, 163)

#Valores posibles de los elementos de la matriz
VACIO = 0
BLOQ_AZUL = 1
BLOQ_ROJO = 2
BLOQ_AMARILLO = 3
BLOQ_VERDE = 4
BLOQ_VIOLETA = 5

#Frases del menu para que muestre algo mientras se juega
frase1 = "Lean Chainsaw Man"
frase2 = "Bañense regularmente"
frase3 = "Lean un manga"
frase4 = "Pidan una pizza"
frase5 = "Hagan ejercicio"
frase6 = "Hagan la cama"
frase7 = "Miren Steins;Gate"
frase8 = "Tomen te frio"
frase9 = "Lean un libro"
frase10 = "Usen desodorante"
frase11 = "Estirense"
frase12 = "Un ko-fi para los devs"
frase13 = "Limpien su pc"
frase14 = "Preparen un tang"
frase15 = "Miren Kimi no Na Wa"
frase16 = "Que venga la beca"

#Se inicia pygame
pygame.init()

pantalla = pygame.display.set_mode([1000, 600])
pygame.display.set_caption("Same")
fuente = pygame.font.SysFont("arial", 25)
fuente_fin = pygame.font.SysFont("arial", 30)

#Medidas predeterminadas
filas = 8
columnas = 8
tamano = 8

#Funciona sobre la creación de la matriz del juego y la matriz de respaldo

"""Retorna un valor aleatorio de una lista de valores.
El valor retornado será usado para determinar el color del bloque de la cuadrícula
más adelante."""
def elegir_bloque():
    bloques = [BLOQ_AZUL, BLOQ_ROJO, BLOQ_AMARILLO, BLOQ_VERDE, BLOQ_VIOLETA]
    return bloques[random.randint(0, len(bloques) - 1)]

#Crea una matriz a partir de bloques aleatorios. Retorna la matriz.
def crear_matriz():
    matriz = []
    for fila in range(filas):
        matriz.append([])
        for columna in range(columnas):
            matriz[fila].append(elegir_bloque())
    return matriz

"""Retorna una matriz con filas y columnas iguales.
Recibe como parámetro una matriz, y si la matriz no tiene filas y columnas iguales le
agrega valores específicos a sus filas y/o columnas hasta que la matriz sea simétrica.
Dicho valor se considera un valor 'vacío'"""
def matriz_simetrica(matriz):
    if filas < tamano:
        for fila in range(filas, tamano):
            matriz.append([])
            for columna in range(tamano):
                matriz[fila].append(VACIO)
    if columnas < tamano:
        for fila in range(tamano):
            for columna in range(columnas, tamano):
                matriz[fila].append(VACIO)
    return matriz

"""Retorna una copia de una matriz creada inicialmente.
Recibe como parámetro una matriz y copia cada elemento en una nueva matriz. Dicha matriz
será una matriz de respaldo y es una matriz independiente, por tanto no cambia a menos que se empiece un nuevo juego."""
def matriz_respaldo(matriz):
    matrizb = []
    for fila in range (tamano):
        matrizb.append([])
        for columna in range(tamano):
            matrizb[fila].append(matriz[fila][columna])
    return matrizb

"""Retorna una matriz.
La matriz retornada tiene como elementos a los de una matriz de respaldo creada
anteriormente."""
def cargar_matriz():
    for fila in range(tamano):
        for columna in range(tamano):
            matriz[fila][columna] = matrizb[fila][columna]
    return matriz

#Funciones sobre el dibujo de la matriz como una cuadrícula y de los botones del menú

"""Calcula el lado de cada bloque. Retorna el lado.
Dependiendo del número de filas y columnas, el tamaño del lado varía."""
def obtener_lado():
    lado = pantalla.get_height() // tamano
    return lado

"""Dibuja un bloque de un color aleatorio.
Recibe una pantalla, una matriz, y la fila y la columna de un elemento de la respectiva
matriz. Dependiendo del valor del elemento, dibujará el bloque del color con el que se
relaciona dicho valor."""
def dibujar_bloque(pantalla, fila, columna, matriz):
    celda = matriz[fila][columna]
    lado = obtener_lado()
    
    lado_borde = lado
    pos_x_borde = columna * lado_borde
    pos_y_borde = fila * lado_borde
    
    lado_bloque = 0.9 * lado
    pos_x_bloque = (columna + 0.05) * lado
    pos_y_bloque = (fila + 0.05) * lado
    
    if celda == VACIO:
        pygame.draw.rect(pantalla, NEGRO,
                     (pos_x_borde, pos_y_borde, lado_borde, lado_borde))
        pygame.draw.rect(pantalla, NEGRO,
                     (pos_x_bloque, pos_y_bloque, lado_bloque, lado_bloque))
    elif celda == BLOQ_AZUL:
        pygame.draw.rect(pantalla, NEGRO,
                     (pos_x_borde, pos_y_borde, lado_borde, lado_borde))
        pygame.draw.rect(pantalla, AZUL,
                     (pos_x_bloque, pos_y_bloque, lado_bloque, lado_bloque))
    elif celda == BLOQ_ROJO:
        pygame.draw.rect(pantalla, NEGRO,
                     (pos_x_borde, pos_y_borde, lado_borde, lado_borde))
        pygame.draw.rect(pantalla, ROJO,
                     (pos_x_bloque, pos_y_bloque, lado_bloque, lado_bloque))
    elif celda == BLOQ_AMARILLO:
        pygame.draw.rect(pantalla, NEGRO,
                     (pos_x_borde, pos_y_borde, lado_borde, lado_borde))
        pygame.draw.rect(pantalla, AMARILLO,
                     (pos_x_bloque, pos_y_bloque, lado_bloque, lado_bloque))
    elif celda == BLOQ_VERDE:
        pygame.draw.rect(pantalla, NEGRO,
                     (pos_x_borde, pos_y_borde, lado_borde, lado_borde))
        pygame.draw.rect(pantalla, VERDE,
                     (pos_x_bloque, pos_y_bloque, lado_bloque, lado_bloque))
    elif celda == BLOQ_VIOLETA:
        pygame.draw.rect(pantalla, NEGRO,
                     (pos_x_borde, pos_y_borde, lado_borde, lado_borde))
        pygame.draw.rect(pantalla, VIOLETA,
                     (pos_x_bloque, pos_y_bloque, lado_bloque, lado_bloque))
    
"""Dibuja una cuadrícula de bloques en la pantalla.
Recibe una pantalla y una matriz como parámetros."""
def dibujar_cuadricula(pantalla, matriz):
    for fila in range(tamano):
        for columna in range(tamano):
            dibujar_bloque(pantalla, fila, columna, matriz)
 
"""Dibuja los botones de la parte del menú.
Recibe el número de movimientos disponibles de la cuadrícula, dibuja un fondo color
rojo al menú si no hay movimientos disponibles, y dibuja un fondo color gris en el caso
contrario."""
def dibujar_botones(movimientos):
    #Color del fondo del menú
    if movimientos > 0:   
        pygame.draw.rect(pantalla, NEGRO, (600, 0, 300, 600))
        pygame.draw.rect(pantalla, GRIS, (605, 10, 385, 580))
    else:
        pygame.draw.rect(pantalla, NEGRO, (600, 0, 300, 600))
        pygame.draw.rect(pantalla, ROJO, (605, 10, 385, 580))
        
    #botones centro derecha
    pygame.draw.rect(pantalla, NEGRO, (940, 225, 45, 45))
    pygame.draw.rect(pantalla, VERDE, (943, 228, 39, 39))
    pygame.draw.rect(pantalla, NEGRO, (940, 275, 45, 45))
    pygame.draw.rect(pantalla, VERDE, (943, 278, 39, 39))
        
    #botones centro centro
    pygame.draw.rect(pantalla, NEGRO, (890, 225, 45, 45))
    pygame.draw.rect(pantalla, BLANCO, (893, 228, 39, 39))
    pygame.draw.rect(pantalla, NEGRO, (890, 275, 45, 45))
    pygame.draw.rect(pantalla, BLANCO, (893, 278, 39, 39))
        
    #botones centro izquierda
    pygame.draw.rect(pantalla, NEGRO, (840, 225, 45, 45))
    pygame.draw.rect(pantalla, ROJO, (843, 228, 39, 39))
    pygame.draw.rect(pantalla, NEGRO, (840, 275, 45, 45))
    pygame.draw.rect(pantalla, ROJO, (843, 278, 39, 39))
    
    #botones abajo
    pygame.draw.rect(pantalla, NEGRO, (940, 440, 45, 45))
    pygame.draw.rect(pantalla, AMARILLO, (943, 443, 39, 39))
    pygame.draw.rect(pantalla, NEGRO, (940, 490, 45, 45))
    pygame.draw.rect(pantalla, AZUL, (943, 493, 39, 39))
    pygame.draw.rect(pantalla, NEGRO, (940, 540, 45, 45))
    pygame.draw.rect(pantalla, ROJO, (943, 543, 39, 39))

#Funciones sobre el análisis de elementos adyacentes, su conteo, eliminación y reposición

"""Retorna el número de fila y columna.
Recibe como parámetro la posición del click del usuario, y calcula la fila y columna con
la que se relaciona dicha posición en la cuadrícula en pantalla."""
def obtener_fila_columna(pos_click):
    pos_x, pos_y = pos_click
    fila = pos_y // obtener_lado()
    columna = pos_x // obtener_lado()
    return int(fila), int(columna)

"""Retorna un tipo booleano.
Recibe como parámetros una coordenada en términos de filas y columnas, y una lista con
posiblemente coordenadas guardadas. Si la coordenada se encuentra entre los elementos de
la lista, el tipo booleano se vuelve True. El tipo booleano es False inicialmente."""
def se_repite(coordenada, coords_guardadas):
    se_repite = False
    for i in range(len(coords_guardadas)):
        if coordenada == coords_guardadas[i]:
            se_repite = True
    return se_repite

"""Retorna el número de elemetnos adyacentes totales desde una posición en la matriz.
Recibe como parámetros una matriz, la fila y la columna del elemento de dicha matriz, y
las coordenadas guardadas. Analiza los alrededores de un elemento seleccionado, y si son
iguales la función cuenta los elementos y pasa a analizar los elementos adyacentes. Para
evitar la recursividad infinita la funcion guarda las coordenadas de los elementos en
una lista inicialmente vacía llamada 'coords_guardadas'."""
def obtener_adyacentes(fila, columna, matriz, coords_guardadas):
    bloque = matriz[fila][columna]
    alto_matriz = tamano - 1
    largo_matriz = tamano - 1
    numero_bloques = 1
    coord = [fila, columna]
    coords_guardadas.append(coord)
    if fila != 0:
        ady_sup = matriz[fila - 1][columna]
        coord_sup = [fila - 1, columna]
        if bloque == ady_sup and not se_repite(coord_sup, coords_guardadas):
            numero_bloques = numero_bloques + obtener_adyacentes(fila - 1, columna, matriz, coords_guardadas)
    if fila != alto_matriz:
        ady_inf = matriz[fila + 1][columna]
        coord_inf = [fila + 1, columna]
        if bloque == ady_inf and not se_repite(coord_inf, coords_guardadas):
            numero_bloques = numero_bloques + obtener_adyacentes(fila + 1, columna, matriz, coords_guardadas)
    if columna != 0:
        ady_izq = matriz[fila][columna - 1]
        coord_izq = [fila, columna - 1]
        if bloque == ady_izq and not se_repite(coord_izq, coords_guardadas):
            numero_bloques = numero_bloques + obtener_adyacentes(fila, columna - 1, matriz, coords_guardadas)
    if columna != largo_matriz:
        ady_der = matriz[fila][columna + 1]
        coord_der = [fila, columna + 1]
        if bloque == ady_der and not se_repite(coord_der, coords_guardadas):
            numero_bloques = numero_bloques + obtener_adyacentes(fila, columna + 1, matriz, coords_guardadas)
    if bloque == VACIO:
        numero_bloques = 0
    return numero_bloques

"""Retorna una matriz con algunos elementos cambiados por elementos 'vacíos'.
Recibe como parámetros una matriz, la fila y la columna del elemento de dicha matriz, y
las coordenadas guardadas. Analiza los alrededores de un elemento seleccionado, y si son
iguales la función cambia los elementos por elemenots 'vacíos' y pasa a analizar los
elementos adyacentes. Para evitar la recursividad infinita la funcion guarda las
coordenadas de los elementos en una lista inicialmente vacía llamada 'coords_guardadas'."""
def eliminar_bloques(fila, columna, matriz, coords_guardadas):
    bloque = matriz[fila][columna]
    alto_matriz = tamano - 1
    largo_matriz = tamano - 1
    numero_bloques = 1
    coord = [fila, columna]
    coords_guardadas.append(coord)
    
    if fila != 0:
        ady_sup = matriz[fila - 1][columna]
        coord_sup = [fila - 1, columna]
        if bloque == ady_sup and not se_repite(coord_sup, coords_guardadas):
            eliminar_bloques(fila - 1, columna, matriz, coords_guardadas)
    if fila != alto_matriz:
        ady_inf = matriz[fila + 1][columna]
        coord_inf = [fila + 1, columna]
        if bloque == ady_inf and not se_repite(coord_inf, coords_guardadas):
            eliminar_bloques(fila + 1, columna, matriz, coords_guardadas)
    if columna != 0:
        ady_izq = matriz[fila][columna - 1]
        coord_izq = [fila, columna - 1]
        if bloque == ady_izq and not se_repite(coord_izq, coords_guardadas):
            eliminar_bloques(fila, columna - 1, matriz, coords_guardadas)
    if columna != largo_matriz:
        ady_der = matriz[fila][columna + 1]
        coord_der = [fila, columna + 1]
        if bloque == ady_der and not se_repite(coord_der, coords_guardadas):
            eliminar_bloques(fila, columna + 1, matriz, coords_guardadas)
    if bloque != VACIO:
        matriz[fila][columna] = VACIO
    return matriz

"""Retorna una lista con coordeandas guardadas.
Recibe como parámetros una matriz, la fila y la columna del elemento de dicha matriz, y
las coordenadas guardadas. Analiza los alrededores de un elemento seleccionado, y si son
iguales la función guarda las coordenadas de dichos elementos y pasa a analizar los
elementos adyacentes."""
def coords_adyacentes(fila, columna, matriz, coords_guardadas):
    bloque = matriz[fila][columna]
    alto_matriz = tamano - 1
    largo_matriz = tamano - 1
    coord = [fila, columna]
    coords_guardadas.append(coord)
    if bloque != VACIO:
        if fila != 0:
            ady_sup = matriz[fila - 1][columna]
            coord_sup = [fila - 1, columna]
            if bloque == ady_sup and not se_repite(coord_sup, coords_guardadas):
                coords_adyacentes(fila - 1, columna, matriz, coords_guardadas)
        if fila != alto_matriz:
            ady_inf = matriz[fila + 1][columna]
            coord_inf = [fila + 1, columna]
            if bloque == ady_inf and not se_repite(coord_inf, coords_guardadas):
                coords_adyacentes(fila + 1, columna, matriz, coords_guardadas)
        if columna != 0:
            ady_izq = matriz[fila][columna - 1]
            coord_izq = [fila, columna - 1]
            if bloque == ady_izq and not se_repite(coord_izq, coords_guardadas):
                coords_adyacentes(fila, columna - 1, matriz, coords_guardadas)
        if columna != largo_matriz:
            ady_der = matriz[fila][columna + 1]
            coord_der = [fila, columna + 1]
            if bloque == ady_der and not se_repite(coord_der, coords_guardadas):
                coords_adyacentes(fila, columna + 1, matriz, coords_guardadas)
    return coords_guardadas

"""Retorna un tipo booleano.
Recibe como parámetros una matriz y una columna seleccionada de dicha matriz. Si la
columna está conformada por solo elementos 'vacíos', entonces cambia el tipo booleano
inicialmente en False a True."""
def columna_vacia(matriz, columna):
    columna_vacia = False
    cantidad_vacios = 0
    for fila in range(tamano):
        if matriz[fila][columna] == VACIO:
            cantidad_vacios = cantidad_vacios + 1
    if cantidad_vacios == tamano:
        columna_vacia = True
    return columna_vacia

"""Retorna una matriz con algunos elementos cambiados de posición.
Recibe como parámetro una matriz, y si dicha matriz tiene un elemento 'vacío' cuyo
elemento adyacente superior es no 'vacío', entonces intercambia sus posiciones."""
def mover_bloques_abajo(matriz):
    for columna in range(tamano):
        for fila in range(tamano):
            if fila < tamano - 1:
                bloque_obj = matriz[fila][columna]
                bloque_inf = matriz[fila + 1][columna]
                if bloque_obj != VACIO and bloque_inf == VACIO:
                    matriz[fila + 1][columna] = matriz[fila][columna]
                    matriz[fila][columna] = VACIO
    return matriz

"""Retorna una matriz con algunos elementos cambiados de posición.
Recibe como parámetro una matriz, y si dicha matriz tiene columnas 'vacías' con columnas
no 'vacías' a su derecha, entonces intercambia la posición de dichas columnas."""
def mover_bloques_izquierda(matriz):
    for columna in range(tamano):
        if columna_vacia(matriz, columna):
            for fila in range(tamano):
                if columna < tamano - 1:
                    matriz[fila][columna] = matriz[fila][columna + 1]
                    matriz[fila][columna + 1] = VACIO
    return matriz

"""Retorna una matriz con algunos de elementos cambiados de posición.
Recibe como parámetro una matriz, y se encarga de organizar todos sus elementos de modo
que se acumulen en la parte inferior izquierda de la matriz siguiendo las reglas de las
funciones 'mover_bloques_abajo' y 'mover_bloques_izquierda' en ese orden."""
def mover_bloques(matriz):
    for bloques in range(tamano ** 2):
        matriz = mover_bloques_abajo(matriz)
        matriz = mover_bloques_izquierda(matriz)
    return matriz       

"""Retorna el número de movimientos en una matriz.
Recibe como parámetro una matriz, y calcula el número de movimientos posibles en la
configuración actual de la matriz."""
def numero_movimientos(matriz):
    numero_movimientos = 0
    lista_coords = []
    for fila in range(tamano):
        for columna in range(tamano):
            coord = [fila, columna]
            if not se_repite(coord, lista_coords):
                numero_adyacentes = obtener_adyacentes(fila, columna, matriz, [])
                if numero_adyacentes >= 3:
                    numero_movimientos = numero_movimientos + 1
                    coordenadas_adyacentes = coords_adyacentes(fila, columna, matriz, [])
                    for coordenada in range(len(coordenadas_adyacentes)):
                        lista_coords.append(coordenadas_adyacentes[coordenada])            
    return numero_movimientos

#Funciones sobre el inicio del juego y el reinicio del juego

"""Retorna una frase aleatoria de una lista de frases."""
def elegir_frase():
    frases = [frase1, frase2, frase3, frase4, frase5, frase6, frase7, frase8, frase9,
              frase10, frase11, frase12, frase13, frase14, frase15, frase16]
    return frases[random.randint(0, len(frases) - 1)]

"""Retorna una matriz y una matriz de respaldo nuevas.
Reinicia varias variables que serán usadas en el loop principal del juego."""
def nuevo_juego():
    global puntaje, movimientos_disponibles, textoarriba1, textoarriba2
    global textoarriba3, texto_centro1, texto_centro2, texto_centro3
    global textoabajo1, textoabajo2, textoabajo3, texto_aumentar
    global texto_disminuir, contador_filas, contador_columnas, juego_terminado
    matriz = matriz_simetrica(crear_matriz())
    matrizb = matriz_respaldo(matriz)
    puntaje = 0
    movimientos_disponibles = numero_movimientos(matriz)
    pantalla.fill(NEGRO)
    dibujar_botones(movimientos_disponibles)
    textoarriba1 = fuente.render("MENU", False, (0, 0, 0))
    textoarriba2 = fuente.render("Puntaje: " + str(puntaje), False, (0, 0, 0))
    textoarriba3 = fuente.render("Mov. disponibles: " + str(movimientos_disponibles), False, (0, 0, 0))
    texto_centro1 = fuente.render("No. Filas", False, (0, 0, 0))
    texto_centro2 = fuente.render("No. Columnas", False, (0, 0, 0))
    texto_centro3 = fuente.render(elegir_frase(), False, (0, 0, 0))
    textoabajo1 = fuente.render("Reiniciar (r): ", False, (0, 0, 0))
    textoabajo2 = fuente.render("Nuevo Juego (n): ", False, (0, 0, 0))
    textoabajo3 = fuente.render("Salir (esc): ", False, (0, 0, 0))
    texto_aumentar = fuente.render(">", False, (0, 0, 0))
    texto_disminuir = fuente.render("<", False, (0, 0, 0))
    contador_filas = fuente.render(str(filas), False, (0, 0, 0))
    contador_columnas = fuente.render(str(columnas), False, (0, 0, 0))
    juego_terminado = fuente_fin.render("Juego terminado :(", False, (0, 0, 0))
    return matriz, matrizb

"""Retorna una matriz cuyos elementos son iguales a los de una matriz de respaldo.
Recibe como parámetro una matriz, y se encarga de reiniciar varias variables que serán
usadas en el loop principal del juego."""
def reiniciar_juego(matriz):
    global puntaje, movimientos_disponibles, textoarriba2, textoarriba3
    global texto_centro3
    matriz = cargar_matriz()
    puntaje = 0
    movimientos_disponibles = numero_movimientos(matriz)
    dibujar_botones(movimientos_disponibles)
    textoarriba2 = fuente.render("Puntaje: " + str(0), False, (0, 0, 0))
    textoarriba3 = fuente.render("Mov. disponibles: " + str(movimientos_disponibles), False, (0, 0, 0))
    texto_centro3 = fuente.render(str(elegir_frase()), False, (0, 0, 0))
    return matriz

#Empieza el juego
matriz, matrizb = nuevo_juego()
jugando = True

while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False                    
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                jugando = False
            elif evento.key == pygame.K_n:
                matriz, matrizb = nuevo_juego()
            elif evento.key == pygame.K_r:
                matriz = reiniciar_juego(matriz)
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pos_click = pygame.mouse.get_pos()
            fila, columna = obtener_fila_columna(pos_click)
            pos_x, pos_y = pos_click
            #aumentar fila en 1
            if 943 < pos_x < 988 and 228 < pos_y < 273:
                if filas < 16:
                    filas = filas + 1
                if filas > columnas:
                    tamano = filas
                else:
                    tamano = columnas
                menu_activo = False
                matriz, matrizb = nuevo_juego()
           #disminuir fila en 1
            elif 843 < pos_x < 888 and 228 < pos_y < 273:
                if filas > 1:
                    filas = filas - 1
                if filas > columnas:
                    tamano = filas
                else:
                    tamano = columnas
                menu_activo = False
                matriz, matrizb = nuevo_juego()
           #aumentar columna en 1
            elif 943 < pos_x < 988 and 278 < pos_y < 323:
                if columnas < 16:
                    columnas = columnas + 1
                if filas > columnas:
                    tamano = filas
                else:
                    tamano = columnas
                menu_activo = False
                matriz, matrizb = nuevo_juego()
            #disminuir columna en 1
            elif 843 < pos_x < 888 and 278 < pos_y < 323:
                if columnas > 1:
                    columnas = columnas - 1
                if filas > columnas:
                    tamano = filas
                else:
                    tamano = columnas
                menu_activo = False
                matriz, matrizb = nuevo_juego()
            #Reiniciar (r)
            elif 940 <= pos_x <= 985 and 440 <= pos_y <= 485:
                matriz = reiniciar_juego(matriz)
            #Nuevo juego (n)
            elif 940 <= pos_x <= 985 and 490 <= pos_y <= 535:
                matriz, matrizb = nuevo_juego()
            #Salir del juego
            elif 940 <= pos_x <= 985 and 540 <= pos_y <= 585:
                jugando = False
            #Clicks sobre cuadrícula
            elif fila < tamano and columna < tamano:
                bloques_adyacentes = obtener_adyacentes(fila, columna, matriz, [])
                if bloques_adyacentes >= 3:
                    dibujar_botones(movimientos_disponibles)
                    matriz = mover_bloques(eliminar_bloques(fila, columna, matriz, []))
                    movimientos_disponibles = numero_movimientos(matriz)
                    puntaje = puntaje + bloques_adyacentes**2
                    if movimientos_disponibles > 0:
                        textoarriba2 = fuente.render("Puntaje: " + str(puntaje), False, (0, 0, 0))
                        textoarriba3 = fuente.render("Mov. disponibles: " + str(movimientos_disponibles), False, (0, 0, 0))
                        texto_centro3 = fuente.render(str(elegir_frase()), False, (0, 0, 0))
                    else:
                        dibujar_botones(movimientos_disponibles)
                        textoarriba2 = fuente.render("Puntaje final: " + str(puntaje), False, (0, 0, 0))
                        textoarriba3 = fuente.render("Mov. disponibles: " + str(movimientos_disponibles), False, (0, 0, 0))
                        texto_centro3 = fuente.render("Juego terminado :(", False, (0, 0, 0))
                            
    pantalla.blit(textoarriba1, (610, 25))
    pantalla.blit(textoarriba2, (610, 75))
    pantalla.blit(textoarriba3, (610, 125))
    pantalla.blit(texto_centro1, (610, 242))
    pantalla.blit(texto_centro2, (610, 292))
    pantalla.blit(texto_centro3, (610, 342))
    pantalla.blit(textoabajo1, (610, 450))
    pantalla.blit(textoabajo2, (610, 500))
    pantalla.blit(textoabajo3, (610, 550))
    pantalla.blit(texto_aumentar, (955, 233))
    pantalla.blit(texto_aumentar, (955, 283))
    pantalla.blit(texto_disminuir, (855, 233))
    pantalla.blit(texto_disminuir, (855, 283))
    
    if filas > 9:
        pantalla.blit(contador_filas, (898, 233))
    else:
        pantalla.blit(contador_filas, (905, 233))
    if columnas > 9:
        pantalla.blit(contador_columnas, (898, 283))
    else:
        pantalla.blit(contador_columnas, (905, 283))

    matriz = mover_bloques(matriz)
    dibujar_cuadricula(pantalla, matriz)
    pygame.display.update()
pygame.quit()