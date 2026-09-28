import os
import pygame

pygame.mixer.init()

current_dir = os.path.dirname(__file__)
directory_path_music = current_dir + "/../Resources/Music/"
directory_path_graphics = current_dir + "/../Resources/Graphics/"

main_theme = pygame.mixer.Sound(os.path.join(directory_path_music, "Tetris.mp3"))
icon = pygame.image.load(os.path.join(directory_path_graphics,"Tetris Logo.png"))