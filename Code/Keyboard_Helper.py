import time
import Colission_Helper as colission_helper
import Resource_Loader as resource
import Game_Object as object
from copy import deepcopy

timer = 0
block_held = False
block_is_placed = False
block_fast_down = False
block_hold_already_hit = False
game_active = True

def set_outside_variables(block_heldN,block_is_placedN):
    global block_held, block_is_placed
    block_held = block_heldN
    block_is_placed = block_is_placedN

#Holt die X und Y, es erstellt eine kleines lokales grid für player_blocks.

#gets the x or y, a small local grid for the player_blocks.
def blocks_on_y_or_x(return_x,player_blocks):
    blocks_before = []
    x = 0
    y = 0
    for i in range(len(player_blocks)):
        player_block = player_blocks[i]

        add_x = True
        add_y = True

        for j in range(len(blocks_before)):
            block_before = blocks_before[j]
            if player_block.x == block_before.x:
                add_x = False
            if player_block.y == block_before.y:
                add_y = False

        if add_x:
            x = x + 1
        if add_y:
            y = y + 1

        blocks_before.append(player_block)

    if return_x:
        return x
    else:
        return y

#Holt das erste X oder Y, also das Kleinste.

#gets the first x or y, so the smallest one
def get_first_x_or_y(player_blocks,return_x):
    x_first = None
    y_first = None

    for i in range(len(player_blocks)):
        player_block = player_blocks[i]
        if x_first is not None and y_first is not None:
            if x_first > player_block.x:
                x_first = player_block.x

            if y_first > player_block.y:
                y_first = player_block.y
        else:
            x_first = player_block.x
            y_first = player_block.y

    if return_x:
        return x_first
    else:
        return y_first

#Holt das letzte X oder Y, also das Größte.

#gets the last x or y, so the biggest one
def get_last_x_or_y(player_blocks, return_x):
    x_first = None
    y_first = None

    for i in range(len(player_blocks)):
        player_block = player_blocks[i]
        if x_first is not None and y_first is not None:
            if x_first < player_block.x:
                x_first = player_block.x

            if y_first < player_block.y:
                y_first = player_block.y
        else:
            x_first = player_block.x
            y_first = player_block.y

    if return_x:
        return x_first
    else:
        return y_first

#Dies dreht den Block um seine Achse. Es holt erst die x und y vom jetzigen Block und wechselt die x und y Koordinaten.
#Nachdem dies fertig ist, invertiert es die x Koordinaten. Wenn es keine Valide Position findet, kehrt es zur alten zurück.

#This turns the blocks around. By first getting the x and y of the current block, then switching the x and y around.
#After that is done, it inverts the x. If it fails to find a valid position, it returns to the old one.
def turn_block(player_blocks,walls):
    not_valid = False
    old = deepcopy(player_blocks)
    time_not_valid = 0.05

    blocks_total = len(player_blocks)
    y_length_before = blocks_on_y_or_x(False,player_blocks)

    x_first = get_first_x_or_y(player_blocks,True)
    y_first = get_first_x_or_y(player_blocks,False)
    width = None
    height = None

    for i in range(len(player_blocks)):
        player_block = player_blocks[i]

        width = player_block.width
        height = player_block.height
        break

    if width and height is not None:
        for i in range(len(player_blocks)):
            player_block = player_blocks[i]

            x_to_cord = 0
            y_to_cord = 0

            x_now = x_first
            y_now = y_first

            for j in range(blocks_total):
                if x_now != player_block.x:
                    x_now = x_now + player_block.width
                    x_to_cord = x_to_cord + 1

                if y_now != player_block.y:
                    y_now = y_now + player_block.height
                    y_to_cord = y_to_cord + 1

            x_inverse = y_to_cord - blocks_total
            y_inverse = x_to_cord

            if x_inverse < 0:
                x_inverse *= -1

            y_pos = y_inverse * player_block.height + y_first
            x_pos = x_inverse * player_block.width + x_first

            move_back = y_length_before * player_block.width
            x_pos = x_pos - move_back

            player_block.y = y_pos
            player_block.x = x_pos

        collision = True
        timer = time.time()
        while collision:
            no_collision = True

            for i in range(len(player_blocks)):
                player_block = player_blocks[i]
                for j in range(len(walls)):
                    wall = walls[j]
                    if colission_helper.AABB(wall, player_block):
                        no_collision = False

                        direction = 1

                        if x_first < wall.x:
                            direction = -1

                        is_free_x = True
                        for k in range(len(player_blocks)):
                            player_block = player_blocks[k]

                            object_direction_free = object.object(player_block.x,player_block.y,None,None)

                            object_direction_free.width = player_block.width
                            object_direction_free.height = player_block.height

                            for t in range(len(player_blocks)):
                                x_new = object_direction_free.x + player_block.width * direction
                                object_direction_free.x = x_new

                            for l in range(len(walls)):
                                if colission_helper.AABB(object_direction_free,walls[l]):
                                    is_free_x = False

                        for k in range(len(player_blocks)):
                            new = player_blocks[k]
                            if is_free_x:
                                x_new = new.x + new.width * direction
                                new.x = x_new
                            else:
                                y_new = new.y - new.height
                                new.y = y_new

            if timer + time_not_valid < time.time():
                collision = False
                not_valid = True

            if no_collision:
                collision = False

    if not_valid:
        player_blocks[:] = old

#Dies akzeptiert und verwertet den Spieler input. Diese Methode kontrolliert die Bewegung, links und rechts, runter, wenn man es dreht oder hält.

#This accepts and uses the keyboard inputs. This Method controls the movement (left, right and down), wether you can spin or hold the object.
def player(pygame, player_blocks, walls, timer_conversion,
           button_press_buffer, sfx_play,
           keyInput):
    global timer, block_held, block_is_placed, block_fast_down, game_active, block_hold_already_hit
    placeSkip = False
    r_pressed = False

    block_fast_down = False
    if button_press_buffer + timer < time.time() * timer_conversion:
        key_pressed = False
        space_pressed = False

        x_originals = []
        y_originals = []

        for l in range(len(player_blocks)):
            x_originals.append(player_blocks[l].x)
            y_originals.append(player_blocks[l].y)

        for l in range(len(player_blocks)):
            player_block = player_blocks[l]

            width = player_block.width
            height = player_block.height
            x = player_block.x
            x_og = x
            y = player_block.y

            if keyInput[pygame.K_d]:
                key_pressed = True
                x = x + width
            elif keyInput[pygame.K_a]:
                key_pressed = True
                x = x - width
            
            if keyInput[pygame.K_s]:
                y = y + height
                key_pressed = True
                block_fast_down = True
            elif keyInput[pygame.K_SPACE]:
                space_pressed = True
                key_pressed = True
                
            if keyInput[pygame.K_e] and not block_hold_already_hit:
                block_held = True
                key_pressed = True
                block_hold_already_hit = True
            if keyInput[pygame.K_r]:
                r_pressed = True
                key_pressed = True

            if keyInput[pygame.K_q]:
                game_active = False
                key_pressed = True

            player_block.x = x
            player_block.y = y

            collided = False
            if space_pressed:
                placeSkip = True
                block_is_placed = True
                block_fast_down = True
                player_block.x = x_og

                j = len(player_blocks) - 1
                y_farthest_up = None
                y_farthest_up_start_y = None

                while j >= 0:
                    collided = False
                    player_block_here = player_blocks[j]
                    y_start = player_block_here.y

                    #Schaut welche die Höhste Y Position ist wenn es mit etwas aus der Wand Liste Kollidiert

                    #checked what the highest y position is when it collides with something from the wall list.
                    while not collided:
                        y_og = player_block_here.y
                        y = y_og + player_block_here.height
                        player_block_here.y = y
                        for i in range(len(walls)):
                            if colission_helper.AABB(player_block_here, walls[i]) and not collided:
                                collided = True
                                if not y_farthest_up is None:
                                    if y_farthest_up > y_og:
                                        y_farthest_up = y_og
                                        y_farthest_up_start_y = y_start
                                else:
                                    y_farthest_up_start_y = y_start
                                    y_farthest_up = y_og
                                
                                player_block_here.y = y_start

                            if collided:
                                break
                    j = j - 1

                #Dies berechnet wie weit nach unten die Blöcke zu fallen haben, und bewegt die Blöcke danach runter

                #This now moves calculates how far the blocks has to fall and moves the blocks down
                if y_farthest_up_start_y is not None:
                    try:
                        y_distance = y_farthest_up - y_farthest_up_start_y

                        for l in range(len(player_blocks)):
                            y_fall = player_blocks[l].y + y_distance
                            player_blocks[l].y = y_fall

                        collision = True

                        while collision:
                            collision = False
                            for l in range(len(player_blocks)):
                                for i in range(len(walls)):
                                    while colission_helper.AABB(player_blocks[l],walls[i]):
                                        collision = True
                                        for m in range(len(player_blocks)):
                                            y_move_out = player_blocks[m].y - player_blocks[m].height
                                            player_blocks[m].y = y_move_out
                    except KeyError as e:
                        print("an error occured!",e)
                else:
                    print("is none!")

                if sfx_play:
                    resource.block_down_fast.stop()
                    resource.block_down_fast.play()
            else:
                #Falls es mit Wändern kollidiert, schiebt es den Block direkt zurück.

                #If it collides with a wall, it pushes the block directly back.
                for i in range(len(walls)):
                    if colission_helper.AABB(player_block, walls[i]) and not collided:
                        for m in range(len(player_blocks)):
                            player_blocks[m].x = x_originals[m]
                            player_blocks[m].y = y_originals[m]
                            collided = True

            if collided:
                break

        if key_pressed:
            timer = time.time() * timer_conversion

            if not space_pressed and sfx_play and not collided:
                resource.button_pressed.stop()
                resource.button_pressed.play()

    if r_pressed:
        turn_block(player_blocks,walls)

    return placeSkip