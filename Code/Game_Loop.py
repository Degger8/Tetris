import pygame
import numpy
import random
import time
import Renderer as renderer
import Resource_Loader as resource
import Game_Object as game_object
import Colission_Helper as colission_helper
import Keyboard_Helper as keyboard_helper
import Button as button
import Button_Enums as button_enum
import Menu_Enums as menu_enum
import File_Helper as file_helper

#TODO: If the !!game is done!! Make comments explaining the why and how in German + English

# Blocks next/hold:
# 1 -> I shape (long)
# 2 -> block
# 3 -> L left
# 4 -> L right
# 5 -> T shape
# 6 -> Z left
# 7 -> Z right

# Grid
# 1 -> Wall
# 2 -> Block
# 3 -> Player block
# 4 -> Turn point of MOVING block!

blocks_min_max = [1,7]

block_next = 0
block_current = 0
block_held = 0

block_size = 25

rows = 20
columns = 15

if columns % 2 != 0:
    columns = columns - 1

extra_width = 600
extra_height = 250

button_press_buffer = 100
timer_conversion = 1000
timer_go_down = 0
buffer_go_down = 750
buffer_go_down_og = buffer_go_down
decrease = 100

button_height = 80
button_width = 200
button_colour = [255,255,255]
text_title_colour = [255,255,255]
text_colour = [0,0,0]
screen_colour = [0,0,0]
text_size = 20
text_size_title = 100
speed_level = 1

text_game_over_buttons = [button_enum.Button_Text.RESTART.value, button_enum.Button_Text.MENU.value, button_enum.Button_Text.EXIT.value]
text_pause_buttons = [button_enum.Button_Text.RESUME.value, button_enum.Button_Text.MENU.value, button_enum.Button_Text.EXIT.value]

text_main_menu_buttons = [button_enum.Button_Text.START.value, button_enum.Button_Text.HIGHSCORE.value,
                          button_enum.Button_Text.OPTIONS.value, button_enum.Button_Text.EXIT.value]

text_options_buttons = [button_enum.Button_Text.MUSIC_ON.value, button_enum.Button_Text.SFX_ON.value, button_enum.Button_Text.MENU.value]
text_highscore_buttons = [button_enum.Button_Text.MENU.value]

points = 0
points_faster_down = 2500
points_faster_down_og = points_faster_down

not_in_main_menu = False
block_is_placed = False
started = False

music_play = True
sfx_play = True

width = columns * block_size
height = columns * block_size
show_buttons = False
game_state = menu_enum.Menu.MAINMENU.value

screen_width = width + extra_width
screen_height = height + extra_height

width_walls_total = block_size * columns
height_walls_total = block_size * rows
grid = numpy.zeros((rows,columns))
i = 0
j = 0

width_center = (screen_width - width_walls_total)/2
height_center = (screen_height - height_walls_total)/2

walls = []
buttons = []

running = True
fps = 60

player_block = None
block_held_active = False
next_object = None
hold_object = None
block_next = random.randint(blocks_min_max[0],blocks_min_max[1])

pygame.init()
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_icon(resource.icon)

def calculate_grid_cords(cord, is_x):
    global width_center, height_center, block_size
    if is_x:
        return (int)((cord - width_center) / block_size)
    else:
        return (int)((cord - height_center) / block_size)

def calculate_world_cords(cord, is_x):
    global width_center, height_center, block_size
    if is_x:
        return cord * block_size + width_center
    else:
        return cord * block_size + height_center

# x_w = cord * block_size + width_center
# (x_w - width_center) / block_size = cord

def create_walls():
    global walls, block_size, grid

    for i in range(rows):
        for j in range(columns):
            grid[i][j] = 0
    
    walls.clear()
    for i in range(rows):
        for j in range(columns):
            if j - 1 < 0 or j + 1 >= columns or i + 1 >= rows:
                x = calculate_world_cords(j,True)
                y = calculate_world_cords(i,False)

                grey_scale = 100
                wall_colour = [grey_scale,grey_scale,grey_scale]

                object = game_object.object(x,y,wall_colour,block_size)
                walls.append(object)

                grid[i][j] = 1

def print_grid():
    global columns, rows
    for i in range(rows):
        for j in range(columns):
            print(grid[i][j],end=" ")
        print()

def block_spawn(value, is_player_spawn):
    global walls, game_state

    blocks = []

    y = height_center
    x = (columns/2) * block_size + width_center

    if value == 1:
        colour = [0,255,255]

        for i in range(4):
            obj = game_object.object(x, y + block_size * i, colour, block_size)
            blocks.append(obj)
    elif value == 2:
        colour = [255, 255, 0]

        for i in range(2):
            for j in range(2):
                obj = game_object.object(x + block_size * j, y + block_size * i, colour, block_size)
                blocks.append(obj)
    elif value == 3:
        colour = [0, 0, 255]

        for i in range(3):
            obj = game_object.object(x, y + block_size * i, colour, block_size)
            blocks.append(obj)
            if i == 2:
                obj = game_object.object(x + block_size, y + block_size * i, colour, block_size)
                blocks.append(obj)
    elif value == 4:
        colour = [255, 165, 0]

        for i in range(3):
            obj = game_object.object(x, y + block_size * i, colour, block_size)
            blocks.append(obj)
            if i == 2:
                obj = game_object.object(x - block_size, y + block_size * i, colour, block_size)
                blocks.append(obj)
    elif value == 5:
        colour = [128, 0, 128]

        for i in range(3):
            obj = game_object.object(x + block_size * i, y, colour, block_size)
            blocks.append(obj)
            if i == 1:
                obj = game_object.object(x + block_size * i, y + block_size, colour, block_size)
                blocks.append(obj)
    elif value == 6:
        colour = [255, 0, 0]

        for i in range(2):
            obj = game_object.object(x + block_size * i + block_size, y, colour, block_size)
            blocks.append(obj)

        for i in range(2):
            obj = game_object.object(x + block_size * i, y + block_size, colour, block_size)
            blocks.append(obj)
    elif value == 7:
        colour = [0, 255, 0]

        for i in range(2):
            obj = game_object.object(x + block_size * i - block_size, y, colour, block_size)
            blocks.append(obj)

        for i in range(2):
            obj = game_object.object(x + block_size * i, y + block_size, colour, block_size)
            blocks.append(obj)

    if is_player_spawn:
        for i in range(len(walls)):
            for j in range(len(blocks)):
                if colission_helper.AABB(walls[i],blocks[j]):
                    game_state = menu_enum.Menu.GAME_OVER.value

    return blocks

def move_blocks_down(rows_removed, y_lowest):
    global grid, walls, columns, rows, block_size, sfx_play

    if sfx_play:
        resource.row_cleared.stop()
        resource.row_cleared.play()

    y_move_down = rows_removed * block_size

    i = rows - 1
    while i >= 0:
        j = columns - 1
        while j >= 0:
            if j > 0 and j + 1 < columns and i + 1 < rows:
                if grid[i][j] == 2:
                    x_world_cords_origin = calculate_world_cords(j,True)
                    y_world_cords_origin = calculate_world_cords(i,False)
                    y_new = y_move_down + y_world_cords_origin

                    for k in range(len(walls)):
                        if walls[k].get_y() == y_world_cords_origin and walls[k].get_x() == x_world_cords_origin and walls[k].get_y() < y_lowest:
                            walls[k].set_y(y_new)
                            
                            y_new_pos = calculate_grid_cords(y_new,False)

                            grid[i][j] = 0
                            grid[y_new_pos][j] = 2
            j = j - 1

        i = i - 1

def rows_done_count():
    global grid, columns, rows

    total_rows = 0
    for i in range(rows):
        row_done = True
        for j in range(columns):
            if j > 0 and j + 1 < columns: 
                if grid[i][j] == 0 or grid[i][j] == 1:
                    row_done = False
        if row_done:
            total_rows = total_rows + 1

    return total_rows

def lowest_done_row():
    global grid, columns, rows

    lowest_y = 0
    for i in range(rows):
        row_done = True
        for j in range(columns):
            if j > 0 and j + 1 < columns: 
                if grid[i][j] == 0 or grid[i][j] == 1:
                    row_done = False
        if row_done:
            if i > lowest_y:
                lowest_y = i

    return_y = calculate_world_cords(lowest_y,False)
    return return_y

def restart():
    global player_block, block_held, block_next, block_held_active, next_object, hold_object, block_is_placed, game_state, points, speed_level, buffer_go_down, buffer_go_down_og, points_faster_down, points_faster_down_og, speed_level
    create_walls()
    player_block = None
    block_held = 0
    block_next = random.randint(blocks_min_max[0],blocks_min_max[1])
    block_held_active = False
    next_object = None
    hold_object = None
    points = 0
    speed_level = 1
    block_is_placed = False
    game_state = menu_enum.Menu.GAME.value
    keyboard_helper.set_game_active(True)
    buffer_go_down = buffer_go_down_og
    points_faster_down = points_faster_down_og
    speed_level = 1

def x_away(list, check_right):
    x_extra = 1

    for i in range(len(list)):
        hit = False
        for j in range(len(list)):
            for k in range(len(walls)):
                if not hit:
                    x_now = list[i].get_x() + list[i].get_width() + width_walls_total / 2

                    direction = 1
                    if check_right:
                        direction = -1
                        x_now = list[i].get_x() - list[i].get_width() - width_walls_total / 2

                    test_object = game_object.object(x_now - list[j].get_width() * direction,
                                                     list[j].get_y(), list[j].get_colour(), block_size)

                    hit = colission_helper.AABB(test_object, walls[k])
                    if hit:
                        x_extra = x_extra + 1

                if hit:
                    break

            if hit:
                break
    return x_extra

def game_logic():
    global player_block, block_held_active, block_next, block_held_active, block_is_placed, block_held, block_current, timer_go_down, next_object, hold_object, game_state, sfx_play, points, speed_level, points_faster_down, points_faster_down_og, decrease, buffer_go_down, speed_level

    if player_block is not None:
        keyboard_helper.set_outside_variables(block_held_active, block_is_placed)
        placeSkip = keyboard_helper.player(pygame, player_block,
                                           walls, timer_conversion,
                                           button_press_buffer, sfx_play, keyInput)

        block_held_active = keyboard_helper.get_block_held()
        block_is_placed = keyboard_helper.get_block_is_placed()
        block_fast_down = keyboard_helper.get_block_fast_down()

        if not keyboard_helper.get_game_active():
            game_state = menu_enum.Menu.PAUSE.value

        if block_fast_down:
            timer_go_down = time.time() * timer_conversion

        if timer_go_down + buffer_go_down < time.time() * timer_conversion or placeSkip:
            timer_go_down = time.time() * timer_conversion
            place = False

            for l in range(len(player_block)):
                y = player_block[l].get_y()
                y = y + block_size
                player_block[l].set_y(y)

                for i in range(len(walls)):
                    if colission_helper.AABB(player_block[l], walls[i]):
                        place = True

            if place:
                keyboard_helper.set_block_hold_already_hit(False)
                
                for l in range(len(player_block)):
                    y = player_block[l].get_y() - block_size
                    player_block[l].set_y(y)

                for l in range(len(player_block)):
                    walls.append(player_block[l])
                    block_is_placed = True

                    x_array = calculate_grid_cords(player_block[l].get_x(), True)
                    y_array = calculate_grid_cords(player_block[l].get_y(), False)

                    if x_array >= columns:
                        x_array = columns - 1
                    elif x_array < 0:
                        x_array = 0

                    if y_array >= rows:
                        y_array = rows - 1
                    elif y_array < 0:
                        y_array = 0

                    grid[y_array][x_array] = 2

            rows_removed = rows_done_count()

            if rows_removed == 1:
                points = points + (100 * speed_level)
            if rows_removed == 2:
                points = points + (300 * speed_level)
            if rows_removed == 3:
                points = points + (500 * speed_level)
            if rows_removed == 4:
                points = points + (800 * speed_level)

            if points > points_faster_down:
                points_faster_down = points_faster_down + points_faster_down_og
                buffer_go_down = buffer_go_down - decrease
                speed_level = speed_level + 1
                if buffer_go_down < 0:
                    buffer_go_down = decrease

            y_lowest = lowest_done_row()
            rows_move_down = False
            for i in range(rows):
                row_done = True
                blocks = []

                for j in range(columns):
                    if j > 0 and j + 1 < columns:
                        if grid[i][j] == 0 or grid[i][j] == 1:
                            row_done = False
                        else:
                            x = calculate_world_cords(j, True)
                            y = calculate_world_cords(i, False)

                            for k in range(len(walls)):
                                if walls[k].get_x() == x and walls[k].get_y() == y:
                                    blocks.append(walls[k])

                if row_done:
                    for j in range(len(blocks)):
                        x_array = calculate_grid_cords(blocks[j].get_x(), True)
                        y_array = calculate_grid_cords(blocks[j].get_y(), False)

                        grid[y_array][x_array] = 0
                        walls.remove(blocks[j])

                    rows_move_down = True

                blocks.clear()

            if rows_move_down:
                move_blocks_down(rows_removed, y_lowest)

    if block_is_placed or player_block is None or block_held_active:
        block_is_placed = False

        block_drop_in = block_next
        if block_held_active:
            if block_held != 0:
                block_drop_in = block_held
            block_held_storage = block_held

            block_held = block_current

            block_current = block_held_storage

            hold_object = block_spawn(block_held, False)

            for i in range(len(hold_object)):
                new_x = hold_object[i].get_x() - width_walls_total / 2
                hold_object[i].set_x(new_x)

            collision = True
            while collision:
                collision = False
                for i in range(len(hold_object)):
                    for j in range(len(walls)):
                        if colission_helper.AABB(hold_object[i], walls[j]) and not collision:
                            for k in range(len(hold_object)):
                                new_x = hold_object[k].get_x() - hold_object[k].get_width()
                                hold_object[k].set_x(new_x)
                            collision = True

            x_extra = x_away(hold_object, True)
            for k in range(len(hold_object)):
                new_x = hold_object[k].get_x() - (hold_object[k].get_width() * x_extra)
                hold_object[k].set_x(new_x)
        else:
            block_current = block_next

        player_block = block_spawn(block_drop_in, True)

        if block_held_active:
            block_held_active = False
        else:
            block_next = random.randint(blocks_min_max[0], blocks_min_max[1])

        next_object = block_spawn(block_next, False)

        x_extra = x_away(next_object, False)

        for i in range(len(next_object)):
            new_x = next_object[i].get_x() + (x_extra * next_object[i].get_width()) + width_walls_total / 2
            next_object[i].set_x(new_x)

def render_objects():
    global player_block, next_object, hold_object, walls, buttons, game_state, show_buttons, not_in_main_menu, screen_colour, text_size_title, text_title_colour, screen_width, screen_height, text_size, points

    if buttons is not None:
        for button in buttons:
            if colission_helper.AABB(button, mouse):
                button.set_hit(True)
            else:
                button.set_hit(False)

    renderer.clear_objects(pygame, screen, screen_colour)
    
    if not_in_main_menu:
        if walls is not None:
            for i in range(len(walls)):
                renderer.render_object(walls[i], pygame, screen)

        if player_block is not None:
            for i in range(len(player_block)):
                renderer.render_object(player_block[i], pygame, screen)

        if next_object is not None:
            for i in range(len(next_object)):
                renderer.render_object(next_object[i], pygame, screen)

        if hold_object is not None:
            for i in range(len(hold_object)):
                renderer.render_object(hold_object[i], pygame, screen)

    x = screen_width/2
    y = 50 + text_size_title/2
    
    y_score = screen_height - text_size - 5

    if game_state == menu_enum.Menu.MAINMENU.value or game_state == menu_enum.Menu.OPTIONS.value or game_state == menu_enum.Menu.HIGHSCORE.value:
        renderer.render_text(pygame,screen,"Tetris",text_size_title,text_title_colour,screen_colour,y,x)
    elif game_state == menu_enum.Menu.GAME_OVER.value:
        renderer.render_text(pygame,screen,"Game Over!",text_size_title,text_title_colour,screen_colour,y,x)
    elif game_state == menu_enum.Menu.GAME.value:
        text = "Points: "+str(points)
        renderer.render_text(pygame,screen,str(text),text_size,text_title_colour,screen_colour,y_score,x)

    if game_state == menu_enum.Menu.HIGHSCORE.value:
        show_scores()

    if show_buttons:
        if buttons is not None:
            for i in range(len(buttons)):
                renderer.render_button(buttons[i], pygame, screen)

def button_logic(mouse_object, button_up):
    global buttons

    if button_up:
        text_of_button = ""

        for button in buttons:
            if button.press(mouse_object):
                text_of_button = button.get_text_string()

        button_todo(text_of_button)

def button_todo(text):
    global running, game_state, not_in_main_menu, sfx_play, text_options_buttons, started, music_play, points

    button_sfx_play = False
    if text == button_enum.Button_Text.RESTART.value:
        file_helper.set_score(points)

        button_sfx_play = True
        restart()
        not_in_main_menu = True

    elif text == button_enum.Button_Text.EXIT.value:
        button_sfx_play = True
        running = False

    elif text == button_enum.Button_Text.MENU.value:
        file_helper.set_score(points)

        button_sfx_play = True
        not_in_main_menu = False
        if game_state == menu_enum.Menu.PAUSE.value or game_state == menu_enum.Menu.GAME_OVER.value:
            started = False
        restart()
        game_state = menu_enum.Menu.MAINMENU.value

    elif text == button_enum.Button_Text.RESUME.value:
        button_sfx_play = True
        game_state = menu_enum.Menu.GAME.value
        keyboard_helper.set_game_active(True)
        not_in_main_menu = True

    elif text == button_enum.Button_Text.START.value:
        button_sfx_play = True
        game_state = menu_enum.Menu.GAME.value
        not_in_main_menu = True
        started = False

    elif text == button_enum.Button_Text.HIGHSCORE.value:
        game_state = menu_enum.Menu.HIGHSCORE.value

    elif text == button_enum.Button_Text.OPTIONS.value:
        button_sfx_play = True
        game_state = menu_enum.Menu.OPTIONS.value

    elif text == button_enum.Button_Text.SFX_OFF.value or text == button_enum.Button_Text.SFX_ON.value:
        button_sfx_play = True
        on_off_toggle(button_enum.Button_Text.SFX_ON.value,button_enum.Button_Text.SFX_OFF.value,text_options_buttons, "Sfx")

    elif text == button_enum.Button_Text.MUSIC_OFF.value or text == button_enum.Button_Text.MUSIC_ON.value:
        button_sfx_play = True
        on_off_toggle(button_enum.Button_Text.MUSIC_ON.value,button_enum.Button_Text.MUSIC_OFF.value,text_options_buttons, "Music")

    if button_sfx_play and sfx_play:
        resource.ui_button.stop()
        resource.ui_button.play()

def on_off_toggle(value1, value2, insert_into, play):
    global started, music_play, sfx_play, started

    music_toggle = None

    if play == "Sfx":
        music_toggle = sfx_play
    elif play == "Music":
        music_toggle = music_play

    pos = None

    for i in range(len(insert_into)):
        if insert_into[i] == value1 or insert_into[i] == value2:
            pos = i

    if music_toggle is not None:
        if not music_toggle:
            music_toggle = True
            text_insert = value1
        else:
            music_toggle = False
            text_insert = value2

        if pos is not None and text_insert is not None:
            insert_into[pos] = text_insert

            if play == "Sfx":
                sfx_play = music_toggle
            elif play == "Music":
                started = False
                music_play = music_toggle

def make_buttons(button_text):
    global buttons, screen_height, screen_width, button_height, button_width, button_colour, text_colour, text_size

    buttons.clear()
    center_game_over_x = (screen_width-button_width)/2
    center_game_over_y = (screen_height-button_height)/2
    size_inbetween_buttons = 5
    y_down = 0

    for text in button_text:
        button_append = button.button_object(center_game_over_x,center_game_over_y + y_down,button_width,button_height,button_colour,text_colour,text,text_size)
        buttons.append(button_append)

        y_down += button_height + size_inbetween_buttons

def menu_toggle():
    global game_state, text_pause_buttons, text_game_over_buttons, text_main_menu_buttons, text_options_buttons, text_highscore_buttons

    if game_state == menu_enum.Menu.PAUSE.value:
        make_buttons(text_pause_buttons)
    elif game_state == menu_enum.Menu.GAME_OVER.value:
        make_buttons(text_game_over_buttons)
    elif game_state == menu_enum.Menu.MAINMENU.value:
        make_buttons(text_main_menu_buttons)
    elif game_state == menu_enum.Menu.OPTIONS.value:
        make_buttons(text_options_buttons)
    elif game_state == menu_enum.Menu.HIGHSCORE.value:
        make_buttons(text_highscore_buttons)

def show_scores():
    global text_title_colour, screen_colour, screen_width, button_height, screen_height

    text_size_score = 50
    apart_extra = 10
    scores = file_helper.read()

    for i in range(len(scores)):
        score_text = str(i + 1) + ". " + str(scores[i])

        y = screen_height/2 + button_height + apart_extra + text_size_score * i
        x = screen_width / 2

        renderer.render_text(pygame,screen,str(score_text),text_size_score,text_title_colour,screen_colour,y,x)

mouse = game_object.object(0,0,[0,0,0],10)
create_walls()

while running:
    button_up = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            button_up = True

    keyInput = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse.set_x(mouse_pos[0])
    mouse.set_y(mouse_pos[1])

    if game_state == menu_enum.Menu.GAME.value:
        show_buttons = False
        game_logic()
    else:
        show_buttons = True
        menu_toggle()

        button_logic(mouse,button_up)

    if music_play:
        if not started:
            if not_in_main_menu:
                resource.menu_theme.stop()
                resource.main_theme.play()
            else:
                resource.main_theme.stop()
                resource.menu_theme.play()
            started = True
        else:
            if not pygame.mixer.get_busy():
                started = False
    else:
       resource.stop_music()

    render_objects()

    pygame.display.flip()
    clock.tick(fps)