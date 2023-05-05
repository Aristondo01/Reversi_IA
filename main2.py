from minmax import Minimax
from minmax2 import Minimax2
from minimax3 import Minimax3
from Reversi import Reversi
import random
import numpy as np

minimax1 = Minimax()
minimax2 = Minimax2()
minimax3 = Minimax3()

turn = -1

letras = 'abcdefgh'

# board.make_move((4, 5), -1)
# board.make_move((3, 5), 1)
# print(board.getValidMoves(-1))


list = []
for i in range(1):
    board = Reversi()
    j = 0
    while board.winner_exist() == 0:
        # board.print_board()
        if turn == -1:
            move = minimax3.minimax(board.board.copy(), turn, turn, 0)
            # if move:
            #     # print(letras[move[0]], move[1] + 1, 'minimax')
            #     print(move[0], move[1], 'Minimax')
            # else:
            #     print('pass')
            board.make_move(move, turn)
        else:
            move = minimax2.minimax(board.board.copy(), turn, turn)
            # if move:
            #     # print(letras[move[0]], move[1] + 1, 'minimax')
            #     print(move[0], move[1], 'Minimax')
            # else:
            #     print('pass')
            board.make_move(move, turn)

        turn *= -1
        j += 1

    victoria="Empate"
    if board.winner_exist() == 1:
        victoria = "Blanco"
    elif board.winner_exist() == -1:
        victoria = "Negro"
    list.append(victoria)
    board.print_board()
    print(board.black, board.white)

list = np.array(list)
print("Cantidad de victorias")
print(np.count_nonzero(list == "Negro"))