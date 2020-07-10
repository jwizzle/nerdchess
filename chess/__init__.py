import game
from tabulate import tabulate


def main():
    name_1 = input('What is the name of player 1?')
    name_1_color = input(
        "With which color should {} start, (w)hite, (b)lack or (r)andom?\
        ".format(name_1))
    name_2 = input('What is the name of player 2?')

    chessgame = game.ChessGame(name_1, name_2, name_1_color)
    print(chessgame.player_white, chessgame.player_black)
    print(tabulate(chessgame.board.matrix()))

    move = input("What's your move, {}?: ".format(name_1))
    chessgame.move(move)
    print(tabulate(chessgame.board.matrix()))


if __name__ == '__main__':
    main()
