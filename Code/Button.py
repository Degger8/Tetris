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

        self.darker_by = 50

        self.colour_dark = [colour[0]-self.darker_by,colour[1]-self.darker_by,colour[2]-self.darker_by]

        pygame.init()
        font = pygame.font.Font('freesansbold.ttf', text_size)
        self.text = font.render(text, True, text_colour,colour)
        self.text_rect = self.text.get_rect()

        self.text_dark = font.render(text, True, text_colour,self.colour_dark)
        self.text_rect_dark = self.text_dark.get_rect()

        self.x_text = x + (width-self.text.get_width())/2
        self.y_text = y + (height-self.text.get_height())/2

        self.text_rect.x = self.x_text
        self.text_rect.y = self.y_text

        self.text_rect_dark.x = self.x_text
        self.text_rect_dark.y = self.y_text

        self.text_colour = text_colour

        self.hit = False

    def set_hit(self, value):
        self.hit = value

    def get_hit(self):
        return self.hit

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
        if not self.hit:
            return self.text
        else:
            return self.text_dark

    def get_text_rect(self):
        if not self.hit:
            return self.text_rect
        else:
            return self.text_rect_dark

    def get_text_colour(self):
        return self.text_colour

    def get_colour_dark(self):
        return self.colour_dark