#Eine pygame Methode wird benutzt um Rechtecke für das Spiel zu zeichnen. Dies ist auch eine Hilfsklasse, welche die Rendering Methoden des Spiels enthält-

#A pygame method is used to draw rectangles for the game, this is a helper class, containing the rendering methods of the game.

def render_object(object, pygame, screen):
    rectangle = pygame.Rect(object.x, object.y, object.width, object.height)
    pygame.draw.rect(screen, object.colour, rectangle)

def render_button(object, pygame, screen):
    colour = object.colour
    if object.hit:
        colour = object.colour_dark

    rectangle = pygame.Rect(object.x, object.y, object.width, object.height)
    pygame.draw.rect(screen, colour, rectangle)

    rectangle_text = object.text_rect
    text = object.text

    if object.hit:
        text = object.text_dark
        rectangle_text = object.text_rect_dark

    screen.blit(text, rectangle_text)

#Clears the screen. | Löscht den Bildschirm.
def clear_objects(pygame, screen, colour):
    w, h = pygame.display.get_surface().get_size()

    rectangle = pygame.Rect(0, 0, w, h)
    pygame.draw.rect(screen, colour, rectangle)

def render_text(pygame, screen, text, text_size, colour_text, colour_background, y, x):
    font = pygame.font.Font('freesansbold.ttf', text_size)
    
    text_font = font.render(text, True, colour_text,colour_background)
    text_rect = text_font.get_rect()

    text_rect.x = x - text_font.get_width()/2
    text_rect.y = y - text_font.get_height()/2
    
    screen.blit(text_font, text_rect)