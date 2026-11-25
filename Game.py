import Constants


class Game:
    def __init__(self, turn_player):
        self.turn_player = turn_player
        self.board = None
        self.current_clue = None
        self.current_num_guesses = None

    def update_board(self, word):
        for w in self.board:
            if w.word == word:
                w.word = w.tile
                w.status = True

    def get_word_tile(self, word):
        for w in self.board:
            if w.word == word:
                return w
        return None