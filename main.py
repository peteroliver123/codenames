import random
from WordTile import WordTile
from Game import Game
import Constants
from colorama import just_fix_windows_console

import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def setup_game(game_state):
    print("Welcome to Codenames!")
    print()

    tiles = prepare_tiles(game_state)
    words = prepare_words()
    board = pair_words_with_tiles(words, tiles)
    game_state.board = board

    output_public_board_state(board)
    print()

def output_public_board_state(board):
    print("Here is the public board state:")
    print()
    for i in range (0,5):
        for j in range (0,5):
            board[j + (i * 5)].display_word(False)
            print(" ", end="")
        print("\n", end="")

def output_spymaster_card(board):
    print("Here is the secret board state: ")
    print()

    for i in range (0,5):
        for j in range (0,5):
            board[j + (i * 5)].display_word(True)
            print(" ", end="")
        print("\n", end="")

def prepare_tiles(game_state):
    # prepare tiles
    tiles = [Constants.ASSASSIN]
    if game_state.turn_player == 0:
        tiles.append(Constants.BLUE_AGENT)
    else:
        tiles.append(Constants.RED_AGENT)
    for i in range (0, 8):
        tiles.append(Constants.BLUE_AGENT)
        tiles.append(Constants.RED_AGENT)
        tiles.append(Constants.INNOCENT_BYSTANDER)

    tiles.remove(Constants.INNOCENT_BYSTANDER)

    random.shuffle(tiles)

    return tiles

def prepare_words():
    # fetch random words
    with open(Constants.CODENAMES_WORDS_FILE, "r") as f:
        lines = [line.strip() for line in f]

    return random.sample(lines, 25)

def pair_words_with_tiles(board_words, board_tiles):
    combined = []
    for word,tile in zip(board_words, board_tiles):
        if tile == Constants.BLUE_AGENT:
            color = Constants.BLUE
        elif tile == Constants.RED_AGENT:
            color = Constants.RED
        elif tile == Constants.INNOCENT_BYSTANDER:
            color = Constants.PEACH
        else :
            color = Constants.BLACK
        c = WordTile(word, tile, color)
        combined.append(c)
    return combined

def launch_spymaster(game_state):
    turn_player = "BLUE" if game_state.turn_player else "RED"
    print(f"{turn_player} Players Turn!")
    print()
    print(f"Launching for {turn_player} Spymaster")
    input("Press ENTER key to reveal hidden board: \n")
    output_spymaster_card(game_state.board)
    game_state.current_clue = input("Enter clue: ").upper()
    game_state.current_num_guesses = int(input("Enter num guesses: "))

def launch_operative(game_state):
    turn_player = "BLUE" if game_state.turn_player else "RED"
    print(f"Launching for {turn_player} Operative(s)")
    print()
    print(f"##### CURENT CLUE: {game_state.current_clue} #######")
    print()
    output_public_board_state(game_state.board)

    num_guess_made = 0
    words = []
    for word_tile in game_state.board:
        words.append(word_tile.word)
    while num_guess_made < game_state.current_num_guesses:
        guess = input(f"Enter guess {num_guess_made + 1}: ").upper().strip()
        if words.__contains__(guess) and guess != Constants.RED_AGENT and guess != Constants.BLUE_AGENT and guess != Constants.INNOCENT_BYSTANDER:
            # remove word from board, replace with its tile
            # keep color
            # perform appropriate outcome

            skip_turn = False
            word_tile = game_state.get_word_tile(guess)
            if game_state.turn_player:
                if word_tile.tile != Constants.BLUE_AGENT:
                    skip_turn = True
            else :
                if word_tile.tile != Constants.RED_AGENT:
                    skip_turn = True
            game_state.update_board(guess)
            output_public_board_state(game_state.board)
            if check_game_over(game_state):
                return True
            if skip_turn:
                break
            num_guess_made += 1
        else:
            print("Guess not in Grid guess again")
    return False

def check_game_over(game_state):
    turn_player = "BLUE" if game_state.turn_player else "RED"

    red_wins = True
    blue_wins = True
    for word_tile in game_state.board:
        if word_tile.tile == Constants.ASSASSIN and word_tile.status:
            print(f"{turn_player} loses!")
            return True
        if word_tile.tile == Constants.RED_AGENT and not word_tile.status:
            red_wins = False
        if word_tile.tile == Constants.BLUE_AGENT and not word_tile.status:
            blue_wins = False

    if red_wins:
        print(f"RED Wins!")
        return True
    if blue_wins:
        print(f"BLUE Wins!")
        return True
    return False

def main():
    just_fix_windows_console()
    turn_player = random.randint(0,1)
    game_state = Game(turn_player)
    setup_game(game_state)
    run = True
    while run:
        launch_spymaster(game_state)
        print("Hiding Spymaster Board")
        clear_terminal()
        if launch_operative(game_state):
            run = False
        game_state.turn_player = 0 if game_state.turn_player else 1
    print("Game Over!")

if __name__ == "__main__":
    main()
