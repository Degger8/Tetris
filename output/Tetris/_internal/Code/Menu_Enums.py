from enum import Enum

#Enums werden als exakter Identifikator benutzt, anstatt als etwas Fehleranfälliges wie ein String. Sie werden benutzt um bestimmte Zustände zu merken im Code z.B. ist das Spiel aktiv?

#Enums are used to have an exact identifier, instead of something as error prone as using a string as an identificator. They are used to hard check stuff e.g. is the game active?

class Menu(Enum):
    NOT_SPECIFIED = "NaN"
    GAME_OVER = "GAME OVER"
    PAUSE = "PAUSE"
    GAME = "GAME"
    MAINMENU = "MAIN MENU"
    OPTIONS = "OPTIONS"
    HIGHSCORE = "HIGHSCORE"