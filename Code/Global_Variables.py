#Geteil von Game_Loop.py, um es mehr organisiert aussehen zu lassen und damit nicht so viele Globale Variablen in einer großen Datei sind

#Seperated from Game_Loop.py, to make it look more organized, and to not have so many globals inside of one big file.


#Globale Variablen, um den Spielzustand festzuhalten

#Global variables, to keep track of the game state.
blocks_min_max = [1,7]

block_next = 0
block_current = 0
block_held = 0

#Kontrolliert die Blockgröße. Wenn die Höhe oder Länge außerhalb dieser Variable geändert werden, bricht die Spiellogik.

#Controls the block sizes. If the widht or height is messed with, it breaks the game.
block_size = 25
block_size_og = block_size

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
button_height_og = button_height
button_width_og = button_width

button_colour = [255,255,255]
text_title_colour = [255,255,255]
text_colour = [0,0,0]
screen_colour = [0,0,0]

text_size = 20
text_size_title = 100
text_size_og = text_size
text_size_title_og = text_size_title

speed_level = 1

points = 0
points_faster_down = 2500
points_faster_down_og = points_faster_down

not_in_main_menu = False
block_is_placed = False
started = False

music_play = True
sfx_play = True
show_buttons = False