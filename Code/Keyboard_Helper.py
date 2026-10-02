import time
import Colission_Helper as colission_helper

timer = 0
block_held = False
block_is_placed = False
block_fast_down = False
game_active = True

def get_game_active():
    global game_active
    return game_active

def set_game_active(value):
    global game_active
    game_active = value

def get_block_held():
    global block_held
    return block_held

def get_block_is_placed():
    global block_is_placed
    return block_is_placed

def get_block_fast_down():
    global block_fast_down
    return block_fast_down

def set_outside_variables(block_heldN,block_is_placedN):
    global block_held, block_is_placed
    block_held = block_heldN
    block_is_placed = block_is_placedN

def player(pygame, player_blocks, walls, button_press_buffer_more, block_next,
           timer_conversion, button_press_buffer,
           keyInput):
    global timer, block_held, block_is_placed, block_fast_down, game_active
    placeSkip = False

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

            width = player_block.get_width()
            height = player_block.get_height()
            x = player_block.get_x()
            x_og = x
            y = player_block.get_y()

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
                
            if keyInput[pygame.K_e]:
                block_held = True
                key_pressed = True
            if keyInput[pygame.K_r] and button_press_buffer_more + timer < time.time() * timer_conversion:
                print("Rotate")
                key_pressed = True

            if keyInput[pygame.K_q]:
                game_active = False
                key_pressed = True

            player_block.set_x(x)
            player_block.set_y(y)

            collided = False
            if space_pressed:
                placeSkip = True
                block_is_placed = True
                block_fast_down = True
                player_block.set_x(x_og)

                j = len(player_blocks) - 1
                y_farthest_up = None
                y_farthest_up_start_y = None

                while j >= 0:
                    collided = False
                    player_block_here = player_blocks[j]
                    y_start = player_block_here.get_y()

                    while not collided:
                        y_og = player_block_here.get_y()
                        y = y_og + player_block_here.get_height()
                        player_block_here.set_y(y)
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
                                
                                player_block_here.set_y(y_start)

                            if collided:
                                break
                    j = j - 1

                if y_farthest_up_start_y is not None:
                    try:
                        y_distance = y_farthest_up - y_farthest_up_start_y

                        for l in range(len(player_blocks)):
                            y_fall = player_blocks[l].get_y() + y_distance
                            player_blocks[l].set_y(y_fall)

                        for l in range(len(player_blocks)):
                            for i in range(len(walls)):
                                while colission_helper.AABB(player_blocks[l],walls[i]):
                                    for m in range(len(player_blocks)):
                                        y_move_out = player_blocks[m].get_y() - player_blocks[m].get_height()
                                        player_blocks[m].set_y(y_move_out)
                    except KeyError as e:
                        print("an error occured!",e)
                else:
                    print("is none!")
            else:
                for i in range(len(walls)):
                    if colission_helper.AABB(player_block, walls[i]) and not collided:
                        for m in range(len(player_blocks)):
                            player_blocks[m].set_x(x_originals[m])
                            player_blocks[m].set_y(y_originals[m])
                            collided = True

            if collided:
                break

        if key_pressed:
            timer = time.time() * timer_conversion


    return placeSkip