from enum import Enum

#Enums werden als exakter Identifikator benutzt, anstatt als etwas Fehleranfälliges wie ein String. Sie werden benutzt um bestimmte Zustände zu merken im Code z.B. ist das Spiel aktiv?

#Enums are used to have an exact identifier, instead of something as error prone as using a string as an identificator. They are used to hard check stuff e.g. is the game active?

class Button_Text(Enum):
    EXIT = "Exit Game"
    MENU = "Main Menu"
    
    RESTART = "Restart"
    
    RESUME = "Resume"

    START = "Start"
    OPTIONS = "Options"

    MUSIC_OFF = "Music Off"
    SFX_OFF = "Sfx Off"
    MUSIC_ON = "Music On"
    SFX_ON = "Sfx On"
    
    HIGHSCORE = "Show Highscores"