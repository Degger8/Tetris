def render_object(object, pygame, screen):
    rectangle = pygame.Rect(object.get_x(), object.get_y(), object.get_width(), object.get_height())
    pygame.draw.rect(screen, object.get_colour(), rectangle)

def render_button(object, pygame, screen):
    rectangle = pygame.Rect(object.get_x(), object.get_y(), object.get_width(), object.get_height())
    pygame.draw.rect(screen, object.get_colour(), rectangle)

def clear_objects(pygame, screen):
    w, h = pygame.display.get_surface().get_size()

    rectangle = pygame.Rect(0, 0, w, h)
    pygame.draw.rect(screen, [0,0,0], rectangle)