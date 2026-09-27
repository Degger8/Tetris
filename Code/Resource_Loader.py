import os
import pygame

pygame.mixer.init()

current_dir = os.path.dirname(__file__)
directory_path = current_dir + "/../Resources/Music/"

print("dir:", directory_path)

main_theme = pygame.mixer.Sound(os.path.join(directory_path, "Tetris.mp3"))