def render_object(object, pygame, screen):
    rectangle = pygame.Rect(object.get_x(), object.get_y(), object.get_width(), object.get_height())
    pygame.draw.rect(screen, object.get_colour(), rectangle)

def render_button(object, pygame, screen):
    colour = object.get_colour()
    if object.get_hit():
        colour = object.get_colour_dark()

    rectangle = pygame.Rect(object.get_x(), object.get_y(), object.get_width(), object.get_height())
    pygame.draw.rect(screen, colour, rectangle)

    rectangle_text = object.get_text_rect()
    text = object.get_text()

    screen.blit(text, rectangle_text)

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