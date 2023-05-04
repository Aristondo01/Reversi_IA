from minmax import Minimax
from Reversi import Reversi
import random
import numpy as np

minimax = Minimax()

turn = -1

letras = 'abcdefgh'

# board.make_move((4, 5), -1)
# board.make_move((3, 5), 1)
# print(board.getValidMoves(-1))
list = []
# TODO: arreglar los movimientos
for i in range(1):
    board = Reversi()
    while board.winner_exist() == 0:
        board.print_board()
        if turn == -1:
            move = minimax.minimax(board.board.copy(), turn, turn, 0)
            if move:
                print(letras[move[0]], move[1] + 1, 'minimax')
                # print(move[0], move[1], 'Minimax')
            else:
                print('pass')
            board.make_move(move, turn)
        else:
            possible_moves = board.getValidMoves(turn)
            move = ()
            # if possible_moves:
            #     move = random.choice(possible_moves)
            # move = minimax.minimax(board.board.copy(), turn, turn, 0)
            # if move:
            #     print(letras[move[0]], move[1] + 1, 'minimax2')
            # board.make_move(move, turn)
            if possible_moves:
                move = input("Ingrese su movimiento> ")
                move = eval(move)
                if move:
                    move = (letras.index(move[0]), int(move[1]) - 1)
                    pass
            board.make_move(move, 1)

        turn *= -1

    victoria="Empate"
    if board.winner_exist() == 1:
        victoria = "Blanco"
    elif board.winner_exist() == -1:
        victoria = "Negro"
    list.append(victoria)

list = np.array(list)
print("Cantidad de victorias")
print(np.count_nonzero(list == "Negro"))

# print("Gano:", victoria)
# board.print_board()