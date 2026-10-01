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

def clear_objects(pygame, screen):
    w, h = pygame.display.get_surface().get_size()

    rectangle = pygame.Rect(0, 0, w, h)
    pygame.draw.rect(screen, [0,0,0], rectangle)