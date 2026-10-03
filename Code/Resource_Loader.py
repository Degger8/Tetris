import os
import pygame

pygame.mixer.init()

current_dir = os.path.dirname(__file__)
directory_path_music = current_dir + "/../Resources/Music/"
directory_path_graphics = current_dir + "/../Resources/Graphics/"
directory_path_sfx = current_dir + "/../Resources/Sfx/"

main_theme = pygame.mixer.Sound(os.path.join(directory_path_music, "Tetris.mp3"))
menu_theme = pygame.mixer.Sound(os.path.join(directory_path_music, "Tetris Menu.mp3"))

button_pressed = pygame.mixer.Sound(os.path.join(directory_path_sfx, "button pressed.mp3"))
row_cleared = pygame.mixer.Sound(os.path.join(directory_path_sfx, "row cleared.mp3"))
block_down_fast = pygame.mixer.Sound(os.path.join(directory_path_sfx, "space bar pressed.mp3"))
ui_button = pygame.mixer.Sound(os.path.join(directory_path_sfx,"UI button press.mp3"))

icon = pygame.image.load(os.path.join(directory_path_graphics,"Tetris Logo.png"))

def stop_music():
    global main_theme, menu_theme

    main_theme.stop()
    menu_theme.stop()