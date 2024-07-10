import pygame
import sys
from random import randint,randrange

# pantalla

WIDTH = 800
HEIGHT = 600
SCREEN_SIZE = (WIDTH, HEIGHT)
SCREEN_CENTER = (WIDTH // 2, HEIGHT // 2)
ORIGIN = (0, 0)

# colores

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CUSTOM = (200, 255, 255)

colors = [RED, BLUE, GREEN, MAGENTA, BLACK, WHITE]

FPS = 60

UR = 0
DR = 0
DL = 0
UL = 0

direcciones = (UR, DR, DL, UL)

PLAYER_WIDTH = 100
PLAYER_HEIGHT = 20
PLAYER_SPEED = 5

BRICK_WIDTH = 60
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLUMNS = WIDTH // BRICK_WIDTH


def mostrar_texto(superficie, texto, fuente, coordenada, color = WHITE, color_fondo = BLACK) :
    """
    Muestra texto en la pantalla.

    Args:
        surface (pygame.Surface): La superficie de la pantalla.
        texto (str): El texto a mostrar.
        fuente (pygame.font.Font): La fuente del texto.
        pos (tuple): La posición del texto.
        color (tuple): El color del texto.
    """
    sticker = fuente.render(texto, True, color, color_fondo)
    rect = sticker.get_rect()
    rect.center = coordenada
    superficie.blit(sticker, rect)

def wait_user(tecla) :
    """
    Espera a que el usuario presione una tecla específica.

    Args:
        tecla (int): La tecla de pygame que debe ser presionada para continuar.
    """
    continuar = True
    while continuar :
        for evento in pygame.event.get() :
            if evento.type == pygame.KEYDOWN:
                if evento.key == tecla:
                    continuar = False


def activate_key(data:dict, name:str, function, path:str) :
    """
    Activa una clave en un diccionario cargando los datos correspondientes.

    Args:
        data (dict): Datos a activar.
        dictionary (dict): Diccionario donde almacenar los datos activados.
        func (function): Función para cargar los datos.
        ruta (str): Ruta de los archivos.
    """
    for key, path in data.items():
        name[key] = function(path)

