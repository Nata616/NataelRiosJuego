import pygame
import sys
import json
import csv
from random import *
from settings import *
from bloques import *
from pygame.locals import *
from menu_functions import *


pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

# pantalla principal por default
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Natanoid")


# Fuentes
fuente = pygame.font.Font("./source/fuentes/ARKANOID.TTF", 74)
menu_fuente = pygame.font.Font("./source/fuentes/ARKANOID.TTF", 50)
fuente_pequeña = pygame.font.Font("./source/fuentes/ARKANOID.TTF", 36)
fuente_bienvenida = pygame.font.Font("./source/fuentes/ARKANOID.TTF", 26)
fuente_tutorial = pygame.font.Font("./source/fuentes/ARKANOID.TTF", 20)
fuente_opciones = pygame.font.SysFont(None, 50)
fuente_numero = pygame.font.SysFont(None, 36)


with open("./source/sounds.json", "r") as archivo_sounds:
    sounds_data = json.load(archivo_sounds)
sounds = {}
activate_key(sounds_data, sounds, pygame.mixer.Sound, "./source/audios/{}.mp3")

with open("./source/images.json", "r") as archivo_images:
    images_data = json.load(archivo_images)
images = {}
activate_key(images_data, images, pygame.image.load, "./source/images/{}.jpg")

with open("./source/music.json", 'r') as archivo_music:
    music = json.load(archivo_music)

pygame.mixer.music.set_volume(0.1)

# score
score = 0
lives = 5
brick_break_counter = 0 

# menu

pygame.mixer.music.load(music["intro_musica"])
pygame.mixer.music.play(-1) 
screen.fill(BLACK)
pygame.time.delay(1500)
mostrar_texto(screen, "Bienvenidos al juego de Natanael Rios", fuente_bienvenida, SCREEN_CENTER, WHITE)
mostrar_texto(screen, "Presione SPACE para continuar", fuente_pequeña, (WIDTH // 2, HEIGHT - 50), WHITE)
pygame.display.flip()

wait_user(K_SPACE)


menu_items = ["Arcade", "Options", "Exit"]
def draw_main_menu():
    """Dibuja el menu de seleccion de escenario
    """
    screen.fill(BLACK)
    mostrar_texto(screen, "Natanoid", fuente, (SCREEN_CENTER[0], 100))
    scores = read_scores()
    highest_score = max(scores, key=lambda x: x[1])[1] if scores else 0
    mostrar_texto(screen, f"High Score: {highest_score}", fuente_numero, (SCREEN_CENTER[0], 200), WHITE)
    for i, item in enumerate(menu_items):
        color = RED if i == selected_item else WHITE
        mostrar_texto(screen, item, menu_fuente, (SCREEN_CENTER[0], 250 + i * 60), color)
    mostrar_texto(screen, "Use UP KEY and DOWN KEY to Navigate and ENTER to Select", fuente_tutorial, (SCREEN_CENTER[0], HEIGHT - 30), WHITE)
    pygame.display.flip()


# bucle principal
is_running = True
in_main_menu = True
in_stage_menu = False
in_music_menu = False
in_options_menu = False
selected_item = 0
selected_stage = 0
selected_music = 0
selected_option = 0
music_volume = 0.1
sound_volume = 0.1
ready_sound_played = False
go_sound_played = False
game_started = False
game_finished = False
game_over = False
mute = False
pausa = False


while is_running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            is_running = False

        if evento.type == pygame.KEYDOWN:
            if in_main_menu:
                if evento.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                    sounds["option_select"].play()
                elif evento.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                    sounds["option_select"].play()
                elif evento.key == pygame.K_RETURN:
                    sounds["option_selected"].play()
                    if selected_item == 0:
                        sounds["arcade_select"].play()
                        pygame.time.delay(1500)
                        pygame.mixer.music.stop()  
                        in_main_menu = False
                        in_stage_menu = True
                        sounds["select_stage"].play()
                    elif selected_item == 1:
                        in_main_menu = False
                        in_options_menu = True
                    elif selected_item == 2:
                        is_running = False                   

            elif in_options_menu:
                if evento.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 2
                    sounds["option_select"].play()
                elif evento.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 2
                    sounds["option_select"].play()
                elif evento.key == pygame.K_LEFT:
                    if selected_option == 0:  
                        music_volume = (music_volume - 0.1) if music_volume > 0 else 1.0
                        pygame.mixer.music.set_volume(music_volume)
                    elif selected_option == 1:  
                        sound_volume = (sound_volume - 0.1) if sound_volume > 0 else 1.0
                        for sound in sounds.values():
                            sound.set_volume(sound_volume)
                    sounds["option_select"].play()
                elif evento.key == pygame.K_RIGHT:
                    if selected_option == 0:  
                        music_volume = (music_volume + 0.1) if music_volume < 1.0 else 0.0
                        pygame.mixer.music.set_volume(music_volume)
                    elif selected_option == 1:  
                        sound_volume = (sound_volume + 0.1) if sound_volume < 1.0 else 0.0
                        for sound in sounds.values():
                            sound.set_volume(sound_volume)
                    sounds["option_select"].play()
                elif evento.key == pygame.K_ESCAPE:
                    sounds["menu_close"].play()
                    in_options_menu = False
                    in_main_menu = True

            elif in_stage_menu:
                if evento.key == pygame.K_LEFT:
                    selected_stage = (selected_stage - 1) % 2
                    sounds["option_select"].play()                   
                elif evento.key == pygame.K_RIGHT:
                    selected_stage = (selected_stage + 1) % 2
                    sounds["option_select"].play()                    
                elif evento.key == pygame.K_RETURN:
                    sounds["option_selected"].play()
                    
                    if selected_stage == 0:
                        sounds["rocky_field_stage_select"].play()                      
                        background_image = images["rocky_field"]
                    else:
                        sounds["space_stage_select"].play()                       
                        background_image = images["space"]                      
                    pygame.time.delay(1500)
                    in_stage_menu = False
                    in_music_menu = True
                    sounds["select_music"].play()   
                elif evento.key == pygame.K_ESCAPE:
                    sounds["menu_close"].play()                   
                    pygame.mixer.music.load(music["intro_musica"])
                    pygame.mixer.music.play(-1) 
                    in_stage_menu = False
                    in_main_menu = True
            elif in_music_menu:
                if evento.key == pygame.K_DOWN:
                    selected_music = (selected_music + 1) % (len(music) - 2)
                    pygame.mixer.music.load(music[list(music.keys())[selected_music]])
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1) 
                    sounds["option_select"].play()
                elif evento.key == pygame.K_UP:
                    selected_music = (selected_music - 1) % (len(music) - 2)
                    pygame.mixer.music.load(music[list(music.keys())[selected_music]])
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)   
                    sounds["option_select"].play()
                elif evento.key == pygame.K_RETURN:
                    selected_music_key = list(music.keys())[selected_music]
                    pygame.mixer.music.load(music[selected_music_key])
                    pygame.mixer.music.play(-1)
                    sounds["option_selected"].play()
                    in_music_menu = False
                elif evento.key == pygame.K_ESCAPE:
                    sounds["menu_close"].play()
                    
                    in_music_menu = False
                    in_stage_menu = True

    
    if in_main_menu:
        draw_main_menu()
    elif in_options_menu:
        draw_options_menu(selected_option, music_volume, sound_volume)
    elif in_stage_menu:
        draw_stage_menu(selected_stage)
    elif in_music_menu:
        draw_music_menu(selected_music)
    else:
        background_image = pygame.transform.scale(background_image,(SCREEN_SIZE))
        screen.blit(background_image, (0, 0)) 

        if not game_started:
            if not ready_sound_played:
                sounds["ready_fondo"].play()
                sounds["ready"].play()
                ready_sound_played = True
            screen.fill(BLACK)
            mostrar_texto(screen, "READY", fuente, SCREEN_CENTER, BLUE)
            pygame.display.flip()
            pygame.time.delay(2000)  
            if not go_sound_played:
                sounds["go"].play()
                go_sound_played = True
            screen.fill(BLACK)
            mostrar_texto(screen, "GO", fuente, SCREEN_CENTER, BLUE)
            pygame.display.flip()
            pygame.time.delay(1000)  
            game_started = True

        if game_started:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    is_running = False
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_p:
                        pausa = not pausa  
                        if pausa:
                            mostrar_texto(screen, "PAUSE", fuente, SCREEN_CENTER, WHITE)
                        pygame.display.flip()
                        pygame.time.delay(500)
                    elif evento.key == pygame.K_m:
                        mute = not mute    
                        if mute:
                            pygame.mixer.music.set_volume(0)  
                            for sound in sounds.values():
                                sound.set_volume(0)
                            mostrar_mute_texto = True
                        else:
                            pygame.mixer.music.set_volume(music_volume)  
                            for sound in sounds.values():
                                sound.set_volume(sound_volume)
                            mostrar_mute_texto = False
        if not pausa:
            if evento.type == MOUSEMOTION:
                pygame.mouse.set_visible(0)
                player['rect'].x = evento.pos[0]
            if player['rect'].left < 0:
                player['rect'].left = 0
            if player['rect'].right > WIDTH:
                player['rect'].right = WIDTH
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Detectar clic izquierdo
                shoot_laser()
        
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.set_volume(sound_volume)
        score, lives = move_ball(ball, player, bricks, score, lives)
        move_and_draw_lasers(screen, lasers, bricks)
        move_bricks(bricks)
        draw_blocks(screen, [player])
        draw_blocks(screen, bricks)
        draw_ball(screen, ball)
        mostrar_texto(screen, "Score:", fuente_pequeña, (80, 20), WHITE)
        mostrar_texto(screen, f"{score}",fuente_numero, (180, 20), WHITE) 
        mostrar_texto(screen, "Lives:", fuente_pequeña, (WIDTH - 100, 20), WHITE)
        mostrar_texto(screen, f"{lives}", fuente_numero, (WIDTH - 10, 20), WHITE)       
        
        if check_win_condition(bricks):
            screen.fill(BLACK)
            sounds["win"].play()
            sounds["you_win"].play()
            pygame.time.delay(1000)
            pygame.mixer.music.load(music["intro_musica"])
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1) 
            name = ask_for_name(screen)
            save_score(name, score)
            read_scores()
            show_top_scores(screen)
            in_main_menu = True
            in_stage_menu = False
            game_started = False
            ready_sound_played = False
            go_sound_played = False
            score = 0
            lives = 1

        if lives <= 0:
                pygame.mixer.music.load(music["yo_antes_era_como_tu"])
                pygame.mixer.music.set_volume(music_volume)
                pygame.mixer.music.play(-1) 
                game_over_sequence(screen, score, sound_volume)
                option = show_options(screen, score, sound_volume)
                if option == "YES":
                    pygame.mixer.music.stop()
                    sounds["select_stage"].play()
                    in_stage_menu = True
                    game_started = False
                    ready_sound_played = False
                    go_sound_played = False
                    score = 0
                    lives = 3
                else:
                    game_over_img = pygame.transform.scale(images["git_gud"], SCREEN_SIZE)
                    screen.blit(game_over_img, (0, 0))
                    pygame.mixer.music.load(music["intro_musica"])
                    pygame.mixer.music.set_volume(music_volume)
                    pygame.mixer.music.play(-1) 
                    name = ask_for_name(screen)
                    save_score(name, score)
                    read_scores()
                    show_top_scores(screen)
                    in_main_menu = True
                    score = 0
                    lives = 1

    pygame.display.flip()
    clock.tick(FPS)

pygame.mixer.music.set_volume(music_volume)
pygame.mixer.music.set_volume(sound_volume)
       
screen.fill(BLACK)
mostrar_texto(screen, "GAME OVER", fuente, SCREEN_CENTER, WHITE)
mostrar_texto(screen, "Presione SPACE para finalizar", fuente_pequeña, (WIDTH // 2, HEIGHT - 50), WHITE)
pygame.display.flip()
clock.tick(FPS)
sounds["game_over"].play() 

wait_user(K_SPACE)

pygame.quit()
sys.exit()
    