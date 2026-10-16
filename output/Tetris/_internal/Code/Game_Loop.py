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
import Global_Variables as globals
import math
from copy import deepcopy

#TODO: Add Window resizing.

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

#Die Menü Knöpfe für Start, Pause und Game Over Menü. Die Werte sind mit ein Enum gesetzt. Mit .value holt man den Wert des Enums, ist nötig für die Knopftexte!

#The menu buttons for the start menu, pause menu and game over menu. The values are set via an enum. With .value you can get the values these enums contains (Necessary to display the text in this case!)
text_game_over_buttons = [button_enum.Button_Text.RESTART.value, button_enum.Button_Text.MENU.value, button_enum.Button_Text.EXIT.value]
text_pause_buttons = [button_enum.Button_Text.RESUME.value, button_enum.Button_Text.MENU.value, button_enum.Button_Text.EXIT.value]

text_main_menu_buttons = [button_enum.Button_Text.START.value, button_enum.Button_Text.HIGHSCORE.value,
                          button_enum.Button_Text.OPTIONS.value, button_enum.Button_Text.EXIT.value]

text_options_buttons = [button_enum.Button_Text.MUSIC_ON.value, button_enum.Button_Text.SFX_ON.value, button_enum.Button_Text.MENU.value]
text_highscore_buttons = [button_enum.Button_Text.MENU.value]

width = globals.columns * globals.block_size
height = globals.columns * globals.block_size

game_state = menu_enum.Menu.MAINMENU.value

screen_width = width + globals.extra_width
screen_height = height + globals.extra_height

diagonal_start = math.sqrt((screen_width*screen_width)+(screen_height*screen_height))

width_walls_total = globals.block_size * globals.columns
height_walls_total = globals.block_size * globals.rows
grid = numpy.zeros((globals.rows,globals.columns))
i = 0
j = 0

width_center = (screen_width - width_walls_total)/2
height_center = (screen_height - height_walls_total)/2

#Wände und Knopf Liste. Es beinhaltet die Welt Koordinaten zum Rendern.
#Ich habe nicht daran gedacht, die Wände und Blöcke NUR in ein grid so machen, also ist es geblieben.

#Walls and Buttons list. It contains the world coordinates for rendering and such.
#I first did not consider having the walls and blocks just in a grid, so it stuck around.
walls = []
buttons = []

running = True
fps = 60

player_block = None
block_held_active = False
next_object = None
hold_object = None
globals.block_next = random.randint(globals.blocks_min_max[0],globals.blocks_min_max[1])

pygame.init()
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_icon(resource.icon)

#Konvertiert Fenster/Welt Koordinaten zu Grid Koordinaten

#Converts the window/world cords to grid cords.
def calculate_grid_cords(cord, is_x):
    global width_center, height_center
    if is_x:
        return (int)((cord - width_center) / globals.block_size)
    else:
        return (int)((cord - height_center) / globals.block_size)

#Konvertiert Grid Koordinaten zu Fenster/Welt Koordinaten

#Converts the grid cords to window/world cords.
def calculate_world_cords(cord, is_x):
    global width_center, height_center
    if is_x:
        return cord * globals.block_size + width_center
    else:
        return cord * globals.block_size + height_center

# x_w = cord * block_size + width_center
# (x_w - width_center) / block_size = cord

#Erstellt die Wände

#creates the walls
def create_walls():
    global walls, grid

    for i in range(globals.rows):
        for j in range(globals.columns):
            grid[i][j] = 0
    
    walls.clear()
    for i in range(globals.rows):
        for j in range(globals.columns):
            if j - 1 < 0 or j + 1 >= globals.columns or i + 1 >= globals.rows:
                x = calculate_world_cords(j,True)
                y = calculate_world_cords(i,False)

                grey_scale = 100
                wall_colour = [grey_scale,grey_scale,grey_scale]

                object = game_object.object(x,y,wall_colour,globals.block_size)
                walls.append(object)

                grid[i][j] = 1

def print_grid():
    global columns
    for i in range(globals.rows):
        for j in range(columns):
            print(grid[i][j],end=" ")
        print()

#Definiert die Farbe und wie der Block aussieht wenn er reingespawnt wird. Es wird auf die Spieler liste übertragen am Ende.

#Defines what colour and how the blocks look when spawned in. Assigns it to the player list too.
def block_spawn(value, is_player_spawn):
    global walls, game_state, height_center, screen_width

    blocks = []

    block_size = globals.block_size

    y = height_center
    x = screen_width/2

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

#Bewegt die Blöcke runter

#Move the blocks down the needed row
def move_blocks_down(indexes_removed,y_lowest):
    global grid, walls

    if globals.sfx_play:
        resource.row_cleared.stop()
        resource.row_cleared.play()

    columns = globals.columns

    i = globals.rows - 1
    while i >= 0:
        j = columns - 1
        while j >= 0:
            if j > 0 and j + 1 < columns and i + 1 < globals.rows:
                if grid[i][j] == 2:
                    rows_removed = 0

                    for l in range(len(indexes_removed)):
                        number = indexes_removed[l]
                        if number > i:
                            rows_removed = rows_removed + 1

                    y_move_down = rows_removed * globals.block_size

                    x_world_cords_origin = calculate_world_cords(j,True)
                    y_world_cords_origin = calculate_world_cords(i,False)
                    y_new = y_move_down + y_world_cords_origin

                    for k in range(len(walls)):
                        if walls[k].y == y_world_cords_origin and walls[k].x == x_world_cords_origin and walls[k].y < y_lowest:
                            walls[k].y = y_new
                            
                            y_new_pos = calculate_grid_cords(y_new,False)

                            grid[i][j] = 0
                            y_current = len(grid)

                            while y_new_pos + 1 >= len(grid):
                                y_current = y_current - 1
                                y_new_pos = y_current

                                y_new = y_new - walls[k].height
                                walls[k].y = y_new

                            grid[y_new_pos][j] = 2
            j = j - 1

        i = i - 1

def rows_done_count():
    global grid

    total_rows = 0
    for i in range(globals.rows):
        row_done = True
        for j in range(globals.columns):
            if j > 0 and j + 1 < globals.columns: 
                if grid[i][j] == 0 or grid[i][j] == 1:
                    row_done = False
        if row_done:
            total_rows = total_rows + 1

    return total_rows

def lowest_done_row():
    global grid

    lowest_y = 0
    for i in range(globals.rows):
        row_done = True
        for j in range(globals.columns):
            if j > 0 and j + 1 < globals.columns: 
                if grid[i][j] == 0 or grid[i][j] == 1:
                    row_done = False
        if row_done:
            if i > lowest_y:
                lowest_y = i

    return_y = calculate_world_cords(lowest_y,False)
    return return_y

def restart():
    global player_block, block_held_active, next_object, hold_object, game_state
    create_walls()
    player_block = None
    globals.block_held = 0
    globals.block_next = random.randint(globals.blocks_min_max[0],globals.blocks_min_max[1])
    block_held_active = False
    next_object = None
    hold_object = None
    globals.points = 0
    globals.speed_level = 1
    globals.block_is_placed = False
    game_state = menu_enum.Menu.GAME.value
    keyboard_helper.game_active = True
    globals.buffer_go_down = globals.buffer_go_down_og
    globals.points_faster_down = globals.points_faster_down_og
    globals.speed_level = 1

#schaut ob links oder rechts etwas frei ist

#checks wether there are free tiles left or right
def x_away(list, check_right):
    x_extra = 1

    for i in range(len(list)):
        hit = False
        for j in range(len(list)):
            for k in range(len(walls)):
                if not hit:
                    x_now = list[i].x + list[i].width + width_walls_total / 2

                    direction = 1
                    if check_right:
                        direction = -1
                        x_now = list[i].x - list[i].width - width_walls_total / 2

                    test_object = game_object.object(x_now - list[j].width * direction,
                                                     list[j].y, list[j].colour, globals.block_size)

                    hit = colission_helper.AABB(test_object, walls[k])
                    if hit:
                        x_extra = x_extra + 1

                if hit:
                    break

            if hit:
                break
    return x_extra

#Spie Logik

#Game logic
def game_logic():
    global player_block, block_held_active, next_object, hold_object, game_state, screen

    if player_block is not None:
        keyboard_helper.set_outside_variables(block_held_active, globals.block_is_placed)
        placeSkip = keyboard_helper.player(pygame, player_block,
                                           walls, globals.timer_conversion,
                                           globals.button_press_buffer, globals.sfx_play, keyInput)

        block_held_active = keyboard_helper.block_held
        globals.block_is_placed = keyboard_helper.block_is_placed
        block_fast_down = keyboard_helper.block_fast_down

        if not keyboard_helper.game_active:
            game_state = menu_enum.Menu.PAUSE.value

        if block_fast_down:
            globals.timer_go_down = time.time() * globals.timer_conversion

        if globals.timer_go_down + globals.buffer_go_down < time.time() * globals.timer_conversion or placeSkip:
            globals.timer_go_down = time.time() * globals.timer_conversion
            place = False

            for l in range(len(player_block)):
                y = player_block[l].y
                y = y + globals.block_size
                player_block[l].y = y

                for i in range(len(walls)):
                    if colission_helper.AABB(player_block[l], walls[i]):
                        place = True

            if place:
                keyboard_helper.block_hold_already_hit = False
                
                for l in range(len(player_block)):
                    y = player_block[l].y - globals.block_size
                    player_block[l].y = y

                for l in range(len(player_block)):
                    walls.append(player_block[l])
                    globals.block_is_placed = True

                    x_array = calculate_grid_cords(player_block[l].x, True)
                    y_array = calculate_grid_cords(player_block[l].y, False)

                    if x_array >= globals.columns:
                        x_array = globals.columns - 1
                    elif x_array < 0:
                        x_array = 0

                    if y_array >= globals.rows:
                        y_array = globals.rows - 1
                    elif y_array < 0:
                        y_array = 0

                    grid[y_array][x_array] = 2

            rows_removed = rows_done_count()

            if rows_removed == 1:
                globals.points = globals.points + (100 * globals.speed_level)
            if rows_removed == 2:
                globals.points = globals.points + (300 * globals.speed_level)
            if rows_removed == 3:
                globals.points = globals.points + (500 * globals.speed_level)
            if rows_removed == 4:
                globals.points = globals.points + (800 * globals.speed_level)

            if globals.points > globals.points_faster_down:
                globals.points_faster_down = globals.points_faster_down + globals.points_faster_down_og
                globals.buffer_go_down = globals.buffer_go_down - globals.decrease
                globals.speed_level = globals.speed_level + 1
                if globals.buffer_go_down < 0:
                    globals.buffer_go_down = globals.decrease

            y_lowest = lowest_done_row()
            rows_move_down = False
            rows_removed_list = []

            for i in range(globals.rows):
                row_done = True
                blocks = []

                for j in range(globals.columns):
                    if j > 0 and j + 1 < globals.columns:
                        if grid[i][j] == 0 or grid[i][j] == 1:
                            row_done = False
                        else:
                            x = calculate_world_cords(j, True)
                            y = calculate_world_cords(i, False)

                            for k in range(len(walls)):
                                if walls[k].x == x and walls[k].y == y:
                                    blocks.append(walls[k])

                if row_done:
                    rows_removed_list.append(i)

                    for j in range(len(blocks)):
                        x_array = calculate_grid_cords(blocks[j].x, True)
                        y_array = calculate_grid_cords(blocks[j].y, False)

                        grid[y_array][x_array] = 0
                        walls.remove(blocks[j])

                    rows_move_down = True

                blocks.clear()

            if rows_move_down:
                move_blocks_down(rows_removed_list,y_lowest)

    if globals.block_is_placed or player_block is None or block_held_active:
        globals.block_is_placed = False

        block_drop_in = globals.block_next
        if block_held_active:
            if globals.block_held != 0:
                block_drop_in = globals.block_held
            block_held_storage = globals.block_held

            globals.block_held = globals.block_current

            globals.block_current = block_held_storage

            hold_object = block_spawn(globals.block_held, False)

            for i in range(len(hold_object)):
                new_x = hold_object[i].x - width_walls_total / 2
                hold_object[i].x = new_x

            collision = True
            while collision:
                collision = False
                for i in range(len(hold_object)):
                    for j in range(len(walls)):
                        if colission_helper.AABB(hold_object[i], walls[j]) and not collision:
                            for k in range(len(hold_object)):
                                new_x = hold_object[k].x - hold_object[k].width
                                hold_object[k].x = new_x
                            collision = True

            x_extra = x_away(hold_object, True)
            for k in range(len(hold_object)):
                new_x = hold_object[k].x - (hold_object[k].width * x_extra)
                hold_object[k].x = new_x
        else:
            globals.block_current = globals.block_next

        player_block = block_spawn(block_drop_in, True)

        if block_held_active:
            block_held_active = False
        else:
            globals.block_next = random.randint(globals.blocks_min_max[0], globals.blocks_min_max[1])

        next_object = block_spawn(globals.block_next, False)

        x_extra = x_away(next_object, False)

        for i in range(len(next_object)):
            new_x = next_object[i].x + (x_extra * next_object[i].width) + width_walls_total / 2
            next_object[i].x = new_x

#Render Logik, es zeichnet die Knöpfe und sonstiges.

#Render Logic, it draws the buttons and others
def render_objects():
    global player_block, next_object, hold_object, walls, buttons, game_state, screen_width, screen_height

    if buttons is not None:
        for button in buttons:
            if colission_helper.AABB(button, mouse):
                button.hit = True
            else:
                button.hit = False

    renderer.clear_objects(pygame, screen, globals.screen_colour)
    
    if globals.not_in_main_menu:
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
    y = 50 + globals.text_size_title/2
    
    y_score = screen_height - globals.text_size - 5

    if game_state == menu_enum.Menu.MAINMENU.value or game_state == menu_enum.Menu.OPTIONS.value or game_state == menu_enum.Menu.HIGHSCORE.value:
        renderer.render_text(pygame,screen,"Tetris",globals.text_size_title,globals.text_title_colour,globals.screen_colour,y,x)
    elif game_state == menu_enum.Menu.GAME_OVER.value:
        renderer.render_text(pygame,screen,"Game Over!",globals.text_size_title,globals.text_title_colour,globals.screen_colour,y,x)
    elif game_state == menu_enum.Menu.GAME.value:
        text = "Points: "+str(globals.points)
        renderer.render_text(pygame,screen,str(text),globals.text_size,globals.text_title_colour,globals.screen_colour,y_score,x)

    if game_state == menu_enum.Menu.HIGHSCORE.value:
        show_scores()

    if globals.show_buttons:
        if buttons is not None:
            for i in range(len(buttons)):
                renderer.render_button(buttons[i], pygame, screen)

#Schaut welche Knopf Text die Knöpfe beinhaltet

#Checks what button text the button contains
def button_logic(mouse_object, button_up):
    global buttons

    if button_up:
        text_of_button = ""

        for button in buttons:
            if button.press(mouse_object):
                text_of_button = button.text_string

        button_todo(text_of_button)

#Ein "Listener", exekutiert die Knopf Funtkionen.

#"Listener", executes the buttons functions
def button_todo(text):
    global running, game_state, text_options_buttons

    button_sfx_play = False
    if text == button_enum.Button_Text.RESTART.value:
        file_helper.set_score(globals.points)

        button_sfx_play = True
        restart()
        globals.not_in_main_menu = True

    elif text == button_enum.Button_Text.EXIT.value:
        button_sfx_play = True
        running = False

    elif text == button_enum.Button_Text.MENU.value:
        file_helper.set_score(globals.points)

        button_sfx_play = True
        globals.not_in_main_menu = False
        if game_state == menu_enum.Menu.PAUSE.value or game_state == menu_enum.Menu.GAME_OVER.value:
            globals.started = False
        restart()
        game_state = menu_enum.Menu.MAINMENU.value

    elif text == button_enum.Button_Text.RESUME.value:
        button_sfx_play = True
        game_state = menu_enum.Menu.GAME.value
        keyboard_helper.game_active = True
        globals.not_in_main_menu = True

    elif text == button_enum.Button_Text.START.value:
        button_sfx_play = True
        game_state = menu_enum.Menu.GAME.value
        globals.not_in_main_menu = True
        globals.started = False
        restart()

    elif text == button_enum.Button_Text.HIGHSCORE.value:
        game_state = menu_enum.Menu.HIGHSCORE.value
        button_sfx_play = True

    elif text == button_enum.Button_Text.OPTIONS.value:
        button_sfx_play = True
        game_state = menu_enum.Menu.OPTIONS.value

    elif text == button_enum.Button_Text.SFX_OFF.value or text == button_enum.Button_Text.SFX_ON.value:
        button_sfx_play = True
        on_off_toggle(button_enum.Button_Text.SFX_ON.value,button_enum.Button_Text.SFX_OFF.value,text_options_buttons, "Sfx")

    elif text == button_enum.Button_Text.MUSIC_OFF.value or text == button_enum.Button_Text.MUSIC_ON.value:
        button_sfx_play = True
        on_off_toggle(button_enum.Button_Text.MUSIC_ON.value,button_enum.Button_Text.MUSIC_OFF.value,text_options_buttons, "Music")

    if button_sfx_play and globals.sfx_play:
        resource.ui_button.stop()
        resource.ui_button.play()

#Kontrolliert die sfx und Music an aus logik.

#Controls the sfx and music on off logic
def on_off_toggle(value1, value2, insert_into, play):
    music_toggle = None

    if play == "Sfx":
        music_toggle = globals.sfx_play
    elif play == "Music":
        music_toggle = globals.music_play

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
                globals.sfx_play = music_toggle
            elif play == "Music":
                globals.started = False
                globals.music_play = music_toggle

#Erstellt die Knöpfe per Text

#Make the buttons per text
def make_buttons(button_text):
    global buttons, screen_height, screen_width

    buttons.clear()
    center_x = (screen_width-globals.button_width)/2
    center_y = (screen_height-globals.button_height)/2
    size_inbetween_buttons = 5
    y_down = 0

    for text in button_text:
        button_append = button.button_object(center_x,center_y + y_down,globals.button_width,globals.button_height,globals.button_colour,globals.text_colour,text,globals.text_size)
        buttons.append(button_append)

        y_down += globals.button_height + size_inbetween_buttons

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

#Zeigt den Score, erster, zweiter und dritte.

#Shows the scores, first, second and third.
def show_scores():
    global screen_width, screen_height

    text_size_score = 50
    apart_extra = 10
    scores = file_helper.read()

    for i in range(len(scores)):
        score_text = str(i + 1) + ". " + str(scores[i])

        y = screen_height/2 + globals.button_height + apart_extra + text_size_score * i
        x = screen_width / 2

        renderer.render_text(pygame,screen,str(score_text),text_size_score,globals.text_title_colour,globals.screen_colour,y,x)

width_walls_total_og = width_walls_total
height_walls_total_og = height_walls_total

#Vergrößert/Verkleinert die Blöcke, je nach Größe.

#Resizes the blocks, so they are the appropiate size.
def get_percentage():
    global diagonal_start, screen_height, screen_width

    diagonal_new = math.sqrt((screen_width*screen_width)+(screen_height*screen_height))
    percentage = diagonal_new/diagonal_start

    max = 1.5
    min = 0.75

    if percentage > max:
        percentage = max
    elif percentage < min:
        percentage = min

    return percentage

def resize_list(list):    
    for l in list:
        new_size = globals.block_size
        l.width = new_size
        l.height = new_size

#Skaliert eine Liste von Objekten (Spielerblock, Wände, platzierte Blöcke, Next, Hold) auf die neue Blockgröße.

#Rescales a list of objects (player block, walls, placed blocks, next, hold) to the new block size.
#Each object is converted to grid units with the OLD layout and placed again with the NEW layout.
def fit_resized_block(list, old_block_size, old_width_center, old_height_center):
    for obj in list:
        grid_x = round((obj.x - old_width_center) / old_block_size, 6)
        grid_y = round((obj.y - old_height_center) / old_block_size, 6)

        obj.width = globals.block_size
        obj.height = globals.block_size

        obj.x = calculate_world_cords(grid_x, True)
        obj.y = calculate_world_cords(grid_y, False)

#Damit es sich zentriert, muss es die extra Bildschirmgröße nutzen, welche mit der vergrößerung des Bildschirms kam.

#To make it go to the center, you need to add the extra screensize that came with the window resize
def center_objects(screen_size):
    global buttons, walls, player_block, screen_width, screen_height, width_center, height_center, width_walls_total, height_walls_total, hold_object, next_object, buttons

    # Remember the old layout so every object can be converted from old -> new
    old_block_size = globals.block_size
    old_width_center = width_center
    old_height_center = height_center

    screen_width = screen_size[0]
    screen_height = screen_size[1]

    perc = get_percentage()

    globals.block_size = globals.block_size_og * perc

    width_walls_total = width_walls_total_og * perc
    height_walls_total = height_walls_total_og * perc

    width_center = (screen_width - width_walls_total) / 2
    height_center = (screen_height - height_walls_total) / 2

    if buttons is not None:
        globals.button_height = int(globals.button_height_og * perc)
        globals.button_width = int(globals.button_width_og * perc)
        globals.text_size = int(globals.text_size_og * perc)
        globals.text_size_title = int(globals.text_size_title_og * perc)

    # The same function handles the player block, walls (including placed blocks), hold and next.
    for object_list in (player_block, walls, hold_object, next_object):
        if object_list is not None:
            fit_resized_block(object_list, old_block_size, old_width_center, old_height_center)

mouse = game_object.object(0,0,[0,0,0],10)

while running:
    button_up = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            button_up = True
        elif event.type == pygame.VIDEORESIZE:
            center_objects(screen.get_size())

    keyInput = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse.x = mouse_pos[0]
    mouse.y = mouse_pos[1]

    if game_state == menu_enum.Menu.GAME.value:
        globals.show_buttons = False
        game_logic()
    else:
        globals.show_buttons = True
        menu_toggle()

        button_logic(mouse,button_up)

    if globals.music_play:
        if not globals.started:
            if globals.not_in_main_menu:
                resource.menu_theme.stop()
                resource.main_theme.play()
            else:
                resource.main_theme.stop()
                resource.menu_theme.play()
            globals.started = True
        else:
            if not pygame.mixer.get_busy():
                globals.started = False
    else:
       resource.stop_music()

    render_objects()

    pygame.display.flip()
    clock.tick(fps)