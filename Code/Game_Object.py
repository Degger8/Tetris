class object:
    def __init__(self, x, y, colour, block_size):
        self.x = x
        self.y = y
        # first colour is red, second is green, third is blue.
        self.colour = colour
        self.width = block_size
        self.height = block_size

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_colour(self):
        return self.colour

    def set_colour(self, colour):
        self.colour = colour

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def to_string(self):
        return "x:",self.x,"y:",self.y,"width:",self.width,"height:",self.height,"colour:",self.colour