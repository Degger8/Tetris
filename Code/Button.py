import Game_Object as object
import pygame as pygame
import time
import Colission_Helper as collision_helper

#Eine Kind Klasse, ist eine Klasse welche Variablen und Funktionen vererbt. Es existieren auch z.B. interfaces und mehr.

#A child class, is a class which inherits the variables, aswell as the function of the parent class. There are also e.g. interfaces and more.
class button_object(object.object):
    #Dies ist ein Konstruktor, es wird benutzt um Variablen beim start des Objektes weiter zugeben.

    #This is a constructor, it is used to pass over variables at the initalization off the object.
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

        self.text_string = text

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

    #Ist der Knopf gedrückt worden und ist die Maus über den Knopf Objekt?

    #Was the button pressed and is the mouse over this button instance?
    def press(self,object_mouse):
        if collision_helper.AABB(self,object_mouse) and self.last_pressed + self.wait < time.time() * self.time_to_millis:
            self.last_pressed = time.time() * self.time_to_millis
            return True
        else:
            return False