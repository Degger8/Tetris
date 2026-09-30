import Game_Object as object
import pygame as pygame
import time
import Colission_Helper as collision_helper

class button_object(object.object):
    def __init__(self, x, y, width, height, colour, text_colour, text, text_size):
        super().__init__(x,y,colour,None)
        self.width = width
        self.height = height

        self.last_pressed = 0
        self.wait = 500
        self.time_to_millis = 1000

        pygame.init()
        font = pygame.font.Font('freesansbold.ttf', text_size)
        self.text = font.render(text, True, text_colour)
        self.text_rect = self.text.get_rect()

        self.x_text = x + (width-self.text.get_width())/2
        self.y_text = y + (height-self.text.get_height())/2

        self.text_rect.x = self.x_text
        self.text_rect.y = self.y_text

        self.text_colour = text_colour

    def press(self,object_mouse):
        if collision_helper.AABB(self,object_mouse) and self.last_pressed + self.wait < time.time() * self.time_to_millis:
            self.last_pressed = time.time() * self.time_to_millis
            return True
        else:
            return False

    def get_x_text(self):
        return self.x_text

    def get_y_text(self):
        return self.y_text

    def get_text(self):
        return self.text

    def get_text_rect(self):
        return self.text_rect

    def get_text_colour(self):
        return self.text_colour