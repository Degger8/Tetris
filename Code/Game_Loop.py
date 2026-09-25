import pygame
import numpy
import random
import time
import Renderer as renderer
import Resource_Loader as resource
import Game_Object as game_object
import Colission_Helper as colission_helper
import Keyboard_Helper as keyboard_helper

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
button_press_buffer_more = 500
timer_conversion = 1000
timer_go_down = 0
buffer_go_down = 750

points = 0

block_is_placed = False

width = columns * block_size
height = columns * block_size
not_game_over = True

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
walls_bottom = []

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

def block_spawn(value):
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

    return blocks

running = True
fps = 60

player_block = None

pygame.init()
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

def move_blocks_down():
    global grid, walls, columns, rows

    i = rows - 1

    while i >= 0:
        j = columns - 1
        while j >= 0:
            if j > 0 and j + 1 < columns and i + 1 < rows:
                if grid[i][j] == 2:
                    y = i + 1
                    not_touched = True
                    while not_touched:
                        if grid[y][j] == 1 or grid[y][j] == 2:
                            not_touched = False
                        else:
                            y = y + 1
                            if y >= rows:
                                break

                    y = y - 1
                    x_world_cords_origin = calculate_world_cords(j,True)
                    y_world_cords_origin = calculate_world_cords(i,False)
                    y_world_cords = calculate_world_cords(y,False)

                    for k in range(len(walls)):
                        if walls[k].get_y() == y_world_cords_origin and walls[k].get_x() == x_world_cords_origin:
                            walls[k].set_y(y_world_cords)
                            grid[i][j] = 0
                            grid[y][j] = 2

            j = j - 1

        i = i - 1
    print_grid()

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

block_held_active = False
next_object = None
hold_object = None
block_next = random.randint(blocks_min_max[0],blocks_min_max[1])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keyInput = pygame.key.get_pressed()

    if player_block is not None:
        keyboard_helper.set_outside_variables(block_held_active,block_is_placed)
        placeSkip = keyboard_helper.player(pygame,player_block,
                                           walls, button_press_buffer_more, block_next, timer_conversion,
                                           button_press_buffer, keyInput, block_size)

        block_held_active = keyboard_helper.get_block_held()
        block_is_placed = keyboard_helper.get_block_is_placed()
        block_fast_down = keyboard_helper.get_block_fast_down()

        if block_fast_down:
            timer_go_down = time.time() * timer_conversion

        if timer_go_down + buffer_go_down < time.time() * timer_conversion or placeSkip:
            timer_go_down = time.time() * timer_conversion
            place = False

            for l in range(len(player_block)):
                y = player_block[l].get_y()
                y_og = y
                y = y + block_size
                player_block[l].set_y(y)

                for i in range(len(walls)):
                    if colission_helper.AABB(player_block[l], walls[i]):
                        place = True

            if place:
                for l in range(len(player_block)):
                    y = player_block[l].get_y() - block_size
                    player_block[l].set_y(y)

                for l in range(len(player_block)):
                    walls.append(player_block[l])
                    block_is_placed = True

                    x_array = calculate_grid_cords(player_block[l].get_x(),True)
                    y_array = calculate_grid_cords(player_block[l].get_y(),False)

                    if x_array >= columns:
                       x_array = columns - 1
                    elif x_array < 0:
                        x_array = 0

                    if y_array >= rows:
                       y_array = rows - 1
                    elif y_array < 0:
                        y_array = 0

                    grid[y_array][x_array] = 2

            for i in range(rows):
                row_done = True
                blocks = []
                for j in range(columns):
                    if j > 0 and j + 1 < columns:
                        if grid[i][j] == 0 or grid[i][j] == 1:
                            row_done = False
                        else:
                            x = j * block_size + width_center
                            y = i * block_size + height_center

                            for k in range(len(walls)):
                                if walls[k].get_x() == x and walls[k].get_y() == y:
                                    blocks.append(walls[k])

                if row_done:
                    for j in range(len(blocks)):
                        walls.remove(blocks[j])

                        x_array = calculate_grid_cords(blocks[j].get_x(),True)
                        y_array = calculate_grid_cords(blocks[j].get_y(),False)

                        grid[y_array][x_array] = 0

                    move_blocks_down()

                blocks.clear()

    if block_is_placed or player_block is None or block_held_active:
        block_is_placed = False

        block_drop_in = block_next
        if block_held_active:
            if block_held != 0:
                block_drop_in = block_held
            block_held_storage = block_held

            block_held = block_current

            block_current = block_held_storage

            hold_object = block_spawn(block_held)

            for i in range(len(hold_object)):
                new_x = hold_object[i].get_x() - width_walls_total/2
                hold_object[i].set_x(new_x)

            widthToMove = 0
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

            x_extra = x_away(hold_object,True)
            for k in range(len(hold_object)):
                new_x = hold_object[k].get_x() - (hold_object[k].get_width() * x_extra)
                hold_object[k].set_x(new_x)

        else:
            block_current = block_next

        player_block = block_spawn(block_drop_in)

        if block_held_active:
            block_held_active = False
        else:
            block_next = random.randint(blocks_min_max[0],blocks_min_max[1])

        next_object = block_spawn(block_next)

        x_extra = x_away(next_object,False)

        for i in range(len(next_object)):
            new_x = next_object[i].get_x() + (x_extra * next_object[i].get_width()) + width_walls_total/2
            next_object[i].set_x(new_x)

    if player_block is not None:
        renderer.clear_objects(pygame,screen)
        for i in range(len(walls)):
            renderer.render_object(walls[i], pygame, screen)

        for i in range(len(player_block)):
            renderer.render_object(player_block[i], pygame, screen)

        if next_object is not None:
            for i in range(len(next_object)):
                renderer.render_object(next_object[i], pygame, screen)

        if hold_object is not None:
            for i in range(len(hold_object)):
                renderer.render_object(hold_object[i], pygame, screen)

        pygame.display.flip()
    clock.tick(fps)