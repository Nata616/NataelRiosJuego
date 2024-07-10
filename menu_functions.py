import pygame
from settings import *
from pygame.locals import *
import json 
import csv

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Fuentes
fuente = pygame.font.Font("./source/fuentes/ARKANOID.TTF", 74)
menu_fuente = pygame.font.Font("./source/fuentes/ARKANOID.TTF", 50)
fuente_pequeña = pygame.font.Font("./source/fuentes/ARKANOID.TTF", 36)
fuente_bienvenida = pygame.font.Font("./source/fuentes/ARKANOID.TTF", 26)
fuente_tutorial = pygame.font.Font("./source/fuentes/ARKANOID.TTF", 20)
fuente_opciones = pygame.font.SysFont(None, 50)
fuente_numero = pygame.font.SysFont(None, 36)

with open("./source/images.json", "r") as archivo_images:
    images_data = json.load(archivo_images)
images = {}
activate_key(images_data, images, pygame.image.load, "./source/images/{}.jpg")

with open("./source/music.json", 'r') as archivo_music:
    music = json.load(archivo_music)

with open("./source/sounds.json", "r") as archivo_sounds:
    sounds_data = json.load(archivo_sounds)
sounds = {}
activate_key(sounds_data, sounds, pygame.mixer.Sound, "./source/audios/{}.mp3")

# menu principal
screen = pygame.display.set_mode(SCREEN_SIZE)


def draw_stage_menu(selected_stage):
    """
    Dibuja el menú de selección de escenario.

    Args:
        selected_stage (int): Índice del escenario seleccionado.
    """
    screen.fill(BLACK)
    mostrar_texto(screen, "Seleccionar Escenario", menu_fuente, (SCREEN_CENTER[0], 50))
    mostrar_texto(screen, "Rocky Field", fuente_pequeña, (225, 125))
    mostrar_texto(screen, "Space", fuente_pequeña, (575, 125))
    rocky_field_scaled = pygame.transform.scale(images["rocky_field"], (360, 300))
    space_scaled = pygame.transform.scale(images["space"], (350, 300))
    screen.blit(rocky_field_scaled, (50, 150))
    screen.blit(space_scaled, (400, 150))
    if selected_stage == 0:
        pygame.draw.rect(screen, RED, (45, 145, 360, 310), 5)
    else:
        pygame.draw.rect(screen, RED, (395, 145, 360, 310), 5)
    mostrar_texto(screen, "Use LEFT KEY and RIGHT KEY to Navigate and ENTER to Select", fuente_tutorial, (SCREEN_CENTER[0], HEIGHT - 30), WHITE)
    mostrar_texto(screen, "Press ESC to Return", fuente_tutorial, (SCREEN_CENTER[0], HEIGHT - 60), WHITE)
    pygame.display.flip()


def draw_music_menu(selected_music):
    """Dibuja el menú de selección de música.

    Args:
        selected_music (int): Índice de la música seleccionada.
    """
    screen.fill(BLACK)
    mostrar_texto(screen, "Seleccionar Musica", menu_fuente, (SCREEN_CENTER[0], 50))
    music_items = list(music.keys())[:-2]
    pygame.mixer.music.set_volume(2)
    for i, item in enumerate(music_items):
        item_name = item.replace("_", " ")
        color = RED if i == selected_music else WHITE
        mostrar_texto(screen, item_name, fuente_pequeña, (SCREEN_CENTER[0], 150 + i * 40), color)
    mostrar_texto(screen, "Use UP KEY and DOWN KEY to Navigate and ENTER to Select", fuente_tutorial, (SCREEN_CENTER[0], HEIGHT - 30), WHITE)
    mostrar_texto(screen, "Press ESC to Return", fuente_tutorial, (SCREEN_CENTER[0], HEIGHT - 60), WHITE)
    
    pygame.display.flip()

def draw_options_menu(selected_option, music_volume, sound_volume):
    """Dibuja el menú de opciones.

    Args:
        selected_option (int): Índice de la opción seleccionada.
        music_volume (float): Volumen de la música.
        sound_volume (float): Volumen de los efectos de sonido.
    """
    screen.fill(BLACK)
    mostrar_texto(screen, "Options", fuente, (SCREEN_CENTER[0], 50))
    options_items = ["Music Volume", "Sound Volume"]
    for i, item in enumerate(options_items):
        color = RED if i == selected_option else WHITE
        volume = f"{int(music_volume * 100)}%" if item == "Music Volume" else f"{int(sound_volume * 100)}%"
        mostrar_texto(screen, f"{item}:", fuente_pequeña, (WIDTH // 2, 150 + i * 100), color)
        mostrar_texto(screen, f"{volume}", fuente_opciones, (WIDTH // 2, 200 + i * 100), color)
    mostrar_texto(screen, "Use UP KEY, DOWN KEY to Navigate and L KEY, R KEY for volume", fuente_tutorial, (SCREEN_CENTER[0], HEIGHT - 30), WHITE)
    mostrar_texto(screen, "Press ESC to Return", fuente_tutorial, (SCREEN_CENTER[0], HEIGHT - 60), WHITE)
    pygame.display.flip()

def game_over_sequence(screen, score, volume:float):
    """Ejecuta la secuencia de fin de juego.

    Args:
        screen (pygame.Surface): La superficie de la pantalla.
        score (int): La puntuación del jugador.
        volume (float): El volumen de la música.
    """
    pygame.mixer.music.set_volume(volume)
    game_over_img = pygame.transform.scale(images["git_gud"], SCREEN_SIZE)
    screen.blit(game_over_img, (0, 0))
    mostrar_texto(screen, "You lose", fuente, SCREEN_CENTER, RED)
    mostrar_texto(screen, f"Score: {score}", fuente_numero, (SCREEN_CENTER[0], SCREEN_CENTER[1] + 50), WHITE)
    pygame.display.flip()
    
    pygame.mixer.Sound.play(sounds["you_lose"])
    pygame.time.delay(3000)
    pygame.mixer.Sound.play(sounds["continue"])
    pygame.time.delay(2000) 


def save_score(player_name, score):
    """
    Guarda la puntuación del jugador en un archivo CSV.

    Args:
        player_name (str): Nombre del jugador.
        score (int): Puntuación del jugador.
    """
    with open("./source/scores.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([player_name, score])

def read_scores():
    """
    Lee las puntuaciones guardadas en un archivo CSV.

    Returns:
        list: Lista de tuplas con los nombres y puntuaciones de los jugadores.
    """
    scores = []
    try:
        with open("./source/scores.csv", mode='r') as file:
            reader = csv.reader(file)
            top_scores = scores[:7]
            for row in reader:
                scores.append((row[0], int(row[1])))
    except FileNotFoundError:
        return []
    scores.sort(key=lambda x: int(x[1]), reverse=True)
    
    return scores[:7]

def ask_for_name(screen):
    """
    Solicita al jugador que ingrese su nombre.

    Args:
        screen (pygame.Surface): La superficie de la pantalla.

    Returns:
        str: Nombre ingresado por el jugador.
    """

    name = ""
    asking = True
    while asking:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    asking = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        
        
        mostrar_texto(screen, "Enter your name:", fuente_pequeña, (SCREEN_CENTER[0], SCREEN_CENTER[1] - 50), WHITE)
        mostrar_texto(screen, name, fuente_pequeña, SCREEN_CENTER, WHITE)
        pygame.display.flip()
    return name

def show_options(screen, score, volume:float):
    """
    Muestra las opciones de continuar el juego.

    Args:
        screen (pygame.Surface): La superficie de la pantalla.
        score (int): Puntuación del jugador.
        volume (float): El volumen de la música.

    Returns:
        str: "YES" o "NO" dependiendo de la opción seleccionada.
    """
    pygame.mixer.music.set_volume(volume)
    options = ["YES", "NO"]
    selected_option = 0
    showing_options = True
    while showing_options:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                    sounds["option_select"].play()
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                    sounds["option_select"].play()
                elif event.key == pygame.K_RETURN:
                    sounds["option_selected"].play()
                    if selected_option == 0:
                        return "YES"
                    else:
                        return "NO"

        game_over_img = pygame.transform.scale(images["git_gud"], SCREEN_SIZE)
        screen.blit(game_over_img, (0, 0))
        mostrar_texto(screen, "continue?", fuente_pequeña, SCREEN_CENTER, WHITE)
        for i, option in enumerate(options):
            color = RED if i == selected_option else WHITE
            mostrar_texto(screen, option, menu_fuente, (SCREEN_CENTER[0], SCREEN_CENTER[1] + 50 + i * 50), color)
        pygame.display.flip()

def show_top_scores(screen):
    """
    Muestra las puntuaciones más altas.

    Args:
        screen (pygame.Surface): La superficie de la pantalla.
        scores (list): Lista de tuplas con los nombres y puntuaciones de los jugadores.
    """
    screen.fill(BLACK)
    scores = read_scores()
    mostrar_texto(screen, "TOP SCORES", fuente, (SCREEN_CENTER[0], 100), WHITE)
    for i, (name, score) in enumerate(scores):
        if i >= 7:
            break
        mostrar_texto(screen, f"{i + 1}. {name}: {score}", fuente_numero, (SCREEN_CENTER[0], 200 + i * 50), WHITE)
    mostrar_texto(screen, "Press SPACE to return to main menu", fuente_tutorial, (SCREEN_CENTER[0], HEIGHT - 30), WHITE)
    pygame.display.flip()
    wait_user(K_SPACE)
    return

def check_win_condition(bricks):
    """
    Verifica si se han destruido todos los bloques.

    Args:
        bricks (list): Lista de diccionarios que representan los bloques.

    Returns:
        bool: True si todos los bloques están destruidos, False en caso contrario.
    """
    for brick in bricks:
        if not brick['destroyed']:
            return False
    return True
