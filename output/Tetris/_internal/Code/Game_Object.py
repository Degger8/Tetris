#Die Basis Klasse des Spiels (für z.B. Wände). Es ist die Elternklasse von Button.py

#The base class of the game. It is the parent class of Button.py

class object:
    #Dies ist ein Konstruktor, es wird benutzt um Variablen beim start des Objektes weiter zugeben.

    #This is a constructor, it is used to pass over variables at the initalization off the object.
    def __init__(self, x, y, colour, block_size):
        self.x = x
        self.y = y
        # first colour is red, second is green, third is blue.
        self.colour = colour
        self.width = block_size
        self.height = block_size

    def to_string(self):
        return "x:",self.x,"y:",self.y,"width:",self.width,"height:",self.height,"colour:",self.colour