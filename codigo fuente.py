import pygame
import random
import tkinter

#Colores, constanes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (155, 155, 155)
AZUL = (80, 180, 216)
ROJO = (255, 96, 96)
AMARILLO = (247, 229, 183)
VERDE = (167, 217, 201)
VIOLETA = (194, 155, 163)

#Elementos de matriz, constantes
VACIO = 0
BLOQ_AZUL = 1
BLOQ_ROJO = 2
BLOQ_AMARILLO = 3
BLOQ_VERDE = 4
BLOQ_VIOLETA = 5
NADA = 6

pygame.init()
pantalla = pygame.display.set_mode([900, 600])

ANCHO = 800
ALTO = 400
superficie_cuadricula = pygame.Surface((400, 400))
cuadro_superficie = superficie_cuadricula.get_rect()

tamano = 10

#A partir de este punto se definen funciones para dibujar una cuadrícula de bloques aleatorios

#Esta funión elige un bloque al azar de una lista con varios bloques y lo retorna
def elegir_bloque():
    bloques = [BLOQ_AZUL, BLOQ_ROJO,
               BLOQ_AMARILLO, BLOQ_VERDE, BLOQ_VIOLETA]
    return bloques[random.randint(0, len(bloques) - 1)]

#Esta función crea una matriz con bloques al azar de un tamaño n x n y la retorna
def crear_matriz():
    matriz = []
    for fila in range(tamano):
        matriz.append([])
        for columna in range(tamano):
            matriz[fila].append(elegir_bloque())
    return matriz

#Esta función determina la longitud del lado de los bloques y la retorna
def obtener_lado():
    lado = pantalla.get_height() // tamano
    return lado

#Esta función dibuja un bloque de un color al azar con borde negro en una
#posición que será determinada en la siguiente funcion
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
    
#Esta función dibuja una cuadrícula de bloques usando la función anterior
def dibujar_cuadricula(pantalla, matriz):
    for fila in range(tamano):
        for columna in range(tamano):
            dibujar_bloque(pantalla, fila, columna, matriz)

#A partir de este punto se definen funciones que servirán para eliminar bloques adyacentes
#de una cuadrícula de bloques

#Esta función retorna el equivalente del número de fila y columna de la posición
#del click usuario
def obtener_fila_columna(pos_click):
    pos_x, pos_y = pos_click
    fila = pos_y // obtener_lado()
    columna = pos_x // obtener_lado()
    return int(fila), int(columna)

#Esta función determina si una coordenada dada se repite entre una lista de
#coordenadas guardadas retornando un tipo de dato booleano
def se_repite(coordenada, coords_guardadas):
    se_repite = False
    for i in range(len(coords_guardadas)):
        if coordenada == coords_guardadas[i]:
            se_repite = True
    return se_repite

#Esta funcion determina y retorna el número de bloques adyacentes en total a partir de un bloque
#clickeado por el usuario, determinando primero los bloques adyacentes al bloque seleccionado,
#luego determinando los bloques adyacentes a esos bloques, y así sucesivamente; recibe como
#parámetro una lista vacía llamada "coords_guardadas" como auxiliar para evitar recursividad infinita
def obtener_adyacentes(fila, columna, matriz, coords_guardadas):
    bloque = matriz[fila][columna]
    longitud_matriz = len(matriz) - 1
    numero_bloques = 1
    coord = [fila, columna]
    coords_guardadas.append(coord)
    
    if fila != 0:
        ady_sup = matriz[fila - 1][columna]
        coord_sup = [fila - 1, columna]
        if bloque == ady_sup and not se_repite(coord_sup, coords_guardadas):
            numero_bloques = numero_bloques + obtener_adyacentes(
                fila - 1, columna, matriz, coords_guardadas)
    if fila != longitud_matriz:
        ady_inf = matriz[fila + 1][columna]
        coord_inf = [fila + 1, columna]
        if bloque == ady_inf and not se_repite(coord_inf, coords_guardadas):
            numero_bloques = numero_bloques + obtener_adyacentes(
                fila + 1, columna, matriz, coords_guardadas)
    if columna != 0:
        ady_izq = matriz[fila][columna - 1]
        coord_izq = [fila, columna - 1]
        if bloque == ady_izq and not se_repite(coord_izq, coords_guardadas):
            numero_bloques = numero_bloques + obtener_adyacentes(
                fila, columna - 1, matriz, coords_guardadas)
    if columna != longitud_matriz:
        ady_der = matriz[fila][columna + 1]
        coord_der = [fila, columna + 1]
        if bloque == ady_der and not se_repite(coord_der, coords_guardadas):
            numero_bloques = numero_bloques + obtener_adyacentes(
                fila, columna + 1, matriz, coords_guardadas)
    
    return numero_bloques

#Esta funcion determina si aún quedan movimientos disponibles y retorna el número de movimientos
#en la matriz recibida
def quedan_adyacentes(matriz):
    numero_movimientos = 0
    quedan_adyacentes = True
    for fila in range(len(matriz)):
        for columna in range(len(matriz)):
            numero_adyacentes = obtener_adyacentes(fila, columna,
                                                   matriz, coords_guardadas)
            if numero_adyacentes >= 3:
                numero_movimientos = numero_movimientos + 1
    if numero_movimientos == 0:
        quedan_adyacentes = False
    return quedan_adyacentes, numero_movimientos

#Esta función 'elimina' los bloques adyacentes totales a partir de un bloque clickeado por el
#usuario, y funciona de manera similar a la función "obtener_adyacentes"; recibe como parámetro
#auxiliar la lista llamada "coords_guardadas" para evitar recursividad infinita
def eliminar_bloques(fila, columna, matriz, coords_guardadas):
    bloque = matriz[fila][columna]
    longitud_matriz = len(matriz) - 1
    numero_bloques = 1
    coord = [fila, columna]
    coords_guardadas.append(coord)
    
    if fila != 0:
        ady_sup = matriz[fila - 1][columna]
        coord_sup = [fila - 1, columna]
        if bloque == ady_sup and not se_repite(coord_sup, coords_guardadas):
            eliminar_bloques(fila - 1, columna, matriz, coords_guardadas)
    if fila != longitud_matriz:
        ady_inf = matriz[fila + 1][columna]
        coord_inf = [fila + 1, columna]
        if bloque == ady_inf and not se_repite(coord_inf, coords_guardadas):
            eliminar_bloques(fila + 1, columna, matriz, coords_guardadas)
    if columna != 0:
        ady_izq = matriz[fila][columna - 1]
        coord_izq = [fila, columna - 1]
        if bloque == ady_izq and not se_repite(coord_izq, coords_guardadas):
            eliminar_bloques(fila, columna - 1, matriz, coords_guardadas)
    if columna != longitud_matriz:
        ady_der = matriz[fila][columna + 1]
        coord_der = [fila, columna + 1]
        if bloque == ady_der and not se_repite(coord_der, coords_guardadas):
            eliminar_bloques(fila, columna + 1, matriz, coords_guardadas)
    if bloque != VACIO:
        matriz[fila][columna] = VACIO
    
    return matriz

#A partir de aquí se definen funciones para acomodar los bloques de modo que no hayan espacios
#vacíos entre los conjuntos de bloques

#Esta función detecta si hay una columna 'vacía' en la matriz
def columna_vacia(matriz, columna):
    columna_vacia = False
    cantidad_vacios = 0
    for fila in range(len(matriz)):
        if matriz[fila][columna] == VACIO:
            cantidad_vacios = cantidad_vacios + 1
    if cantidad_vacios == len(matriz):
        columna_vacia = True
    return columna_vacia

#Esta función mueve bloques hacia abajo si hay espacios 'vacíos' debajo de los
#bloques de la matriz
def mover_bloques_abajo(matriz):
    for columna in range(len(matriz)):
        for fila in range(len(matriz)):
            if fila < len(matriz) - 1:
                bloque_obj = matriz[fila][columna]
                bloque_inf = matriz[fila + 1][columna]
                if bloque_obj != VACIO and bloque_inf == VACIO:
                    matriz[fila + 1][columna] = matriz[fila][columna]
                    matriz[fila][columna] = VACIO
    return matriz

#Esta función mueve los bloques hacia la izquierda si hay una columna 'vacía' en
#la matriz
def mover_bloques_izquierda(matriz):
    for columna in range(len(matriz)):
        if columna_vacia(matriz, columna):
            for fila in range(len(matriz)):
                if columna < len(matriz) - 1:
                    matriz[fila][columna] = matriz[fila][columna + 1]
                    matriz[fila][columna + 1] = VACIO
    return matriz

#Esta función mueve los bloques hacia abajo y hacia la izquierda usando los
#métodos "mover_bloques_abajo" y "mover_bloques_izquierda"
def mover_bloques(matriz):
    matriz = mover_bloques_abajo(matriz)
    matriz = mover_bloques_izquierda(matriz)
    return matriz       

coords_guardadas = []
matriz = crear_matriz()
aun_quedan_adyacentes, numero_movimientos = quedan_adyacentes(matriz)
print("Número de movimientos: " + str(numero_movimientos))
jugando = True

while jugando:
    coords_guardadas = []
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                jugando = False
            if evento.key == pygame.K_r:
                matriz = crear_matriz()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pos_click = pygame.mouse.get_pos()
            fila, columna = obtener_fila_columna(pos_click)
            if fila < tamano and columna < tamano:
                bloques_adyacentes = obtener_adyacentes(fila, columna,
                                                        matriz, coords_guardadas)
                coords_guardadas = []
                if bloques_adyacentes >= 3:
                    matriz = eliminar_bloques(fila, columna,
                                              matriz, coords_guardadas)
                    aun_quedan_adyacentes, numero_movimientos = quedan_adyacentes(matriz)
                    if aun_quedan_adyacentes:
                        print("Número de movimientos: " + str(numero_movimientos))
                    else:
                        print("Juego terminado")
    matriz = mover_bloques(matriz)
    dibujar_cuadricula(pantalla, matriz)
    #pantalla.blit(superficie_cuadricula, (0, 0))
    pygame.display.update()
pygame.quit()
