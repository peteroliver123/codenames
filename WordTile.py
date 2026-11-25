import Constants
class WordTile:

    def __init__(self, word, tile, color):
        self.word = word
        self.tile = tile
        self.color = color
        self.status = False

    def display_word(self, with_colors):
        display = self.word
        while len(display) < 10 and len(display) < 9:
            display = " " + display + " "
        if len(display) == 9:
            display = " " + display
        if with_colors:
            print(f"{self.color}{display}{Constants.RESET}", end="")
        elif self.status:
            print(f"{self.color}{display}{Constants.RESET}", end="")
        else:
            print(f"{display}{Constants.RESET}", end="")