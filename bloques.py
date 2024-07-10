import pygame
from random import randrange, randint
from settings import *
import json

pygame.init()
pygame.mixer.init()

with open("./source/sounds.json", "r") as archivo_sounds:
    sounds_data = json.load(archivo_sounds)
sounds = {}
activate_key(sounds_data, sounds, pygame.mixer.Sound, "./source/audios/{}.mp3")

def create_block(imagen = None, left=0, top=0, width=50, height=50, color=(255, 255, 255), dir=3, borde=0, radio=-1) -> dict[pygame.Rect, tuple[int, int, int], int, int, int]:
    return {
        "rect": pygame.Rect(left, top, width, height), 
        "color": color, 
        "dir": dir, 
        "borde": borde, 
        "radio": radio, 
        "img": imagen
        }

def create_player(imagen = None) :
    if imagen :
        imagen = pygame.transform.scale(imagen, (PLAYER_WIDTH, PLAYER_HEIGHT)) 
    return (create_block(imagen, randint(0, WIDTH - PLAYER_WIDTH), randint(0, HEIGHT - PLAYER_HEIGHT), PLAYER_WIDTH, PLAYER_HEIGHT, dir = direcciones[randrange(len(direcciones))], color = RED))


# player

player = create_player()
player_rect = player["rect"]
player_rect.x = (WIDTH - PLAYER_WIDTH) // 2  
player_rect.y = HEIGHT - PLAYER_HEIGHT - 10  


# Ball 
ball = {
    "rect": pygame.Rect(WIDTH // 2 - 5, HEIGHT // 2 - 5, 10, 10),
    "color": WHITE,
    "speed_x": 3,
    "speed_y": 3
}

# Bricks 
bricks = []
brick_width = 50
brick_height = 20
for _ in range(3):  
    brick_x = randint(20, WIDTH - brick_width)
    brick_y = randint(20, HEIGHT // 2 - brick_height)
    brick = {
        "rect": pygame.Rect(brick_x, brick_y, brick_width, brick_height),
        "color": colors[randint(0, len(colors) - 1)],
        "speed_x": randint(1, 3) * (-1 if randint(0, 1) else 1),
        "speed_y": 0,
        "img": None,
        "destroyed": False
    }
    bricks.append(brick)


def draw_blocks(screen, blocks):
    """
    Dibuja los bloques en la pantalla.

    Args:
        screen (pygame.Surface): La superficie de la pantalla.
        blocks (list): Lista de diccionarios que representan los bloques.
    """
    for block in blocks:
        if block['img']:
            screen.blit(block['img'], block['rect'])
        else:
            pygame.draw.rect(screen, block['color'], block['rect'])

def move_ball(ball, player, bricks, score, life):
    """
    Mueve la pelota y maneja las colisiones con el jugador, los bloques y los límites de la pantalla.

    Args:
        ball (dict): Diccionario que representa la pelota.
        player (dict): Diccionario que representa al jugador.
        bricks (list): Lista de diccionarios que representan los bloques.
        score (int): Puntuación actual del jugador.
        life (int): Vidas restantes del jugador.

    Returns:
        tuple: Tupla que contiene la puntuación actualizada y las vidas restantes.
    """
    ball['rect'].x += ball['speed_x']
    ball['rect'].y += ball['speed_y']
    
    if ball['rect'].left <= 0 or ball['rect'].right >= WIDTH:
        ball['speed_x'] = -ball['speed_x']
    if ball['rect'].top <= 0:
        ball['speed_y'] = -ball['speed_y']
    
    
    if ball['rect'].colliderect(player['rect']):
        if ball['rect'].bottom > player['rect'].top:
            ball['rect'].bottom = player['rect'].top  
            ball['speed_y'] = -ball['speed_y']
            ball['speed_y'] += 0.1 if ball['speed_y'] > 0 else -0.1
            
            
            if ball['rect'].centerx < player['rect'].centerx:
                ball['speed_x'] = -abs(ball['speed_x'])
            else:
                ball['speed_x'] = abs(ball['speed_x'])
            ball['speed_x'] += 0.1 if ball['speed_x'] > 0 else -0.1
    
            sounds["golpe_paleta"].play()
    
    for brick in bricks[:]:
        if ball['rect'].colliderect(brick['rect']):
            ball['speed_y'] = -ball['speed_y']
            ball['speed_y'] += 0.2 if ball['speed_y'] > 0 else -0.2
            ball['speed_x'] += 0.2 if ball['speed_x'] > 0 else -0.2
            
            brick['rect'].width //= 2
            brick['rect'].height //= 2
            score += 1  

            sounds["explosion"].play()

            if brick['rect'].width < 10 or brick['rect'].height < 10:
                bricks.remove(brick)
    
    
    if ball['rect'].top >= HEIGHT:
        life -= 1
        sounds["caida"].play() 
        ball['rect'].center = (WIDTH // 2, HEIGHT // 2)
    
    return score, life 

def draw_ball(screen, ball):
    """
    Dibuja la pelota en la pantalla.

    Args:
        screen (pygame.Surface): La superficie de la pantalla.
        ball (dict): Diccionario que representa la pelota.
    """
    pygame.draw.ellipse(screen, ball['color'], ball['rect'])

def move_bricks(bricks):
    """
    Mueve los bloques y maneja las colisiones con los límites de la pantalla.

    Args:
        bricks (list): Lista de diccionarios que representan los bloques.
    """
    for brick in bricks:
        brick['rect'].x += brick['speed_x']
        if brick['rect'].left <= 0 or brick['rect'].right >= WIDTH:
            brick['speed_x'] = -brick['speed_x']

