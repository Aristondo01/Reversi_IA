from Reversi import Reversi
from Agent import Agent
REVERSI = Reversi()


Blanco = Agent(1)
Negro = Agent(-1)


REVERSI.print_board()
movimiento = Negro.my_turn(REVERSI.board, REVERSI.getValidMoves(-1)) 
REVERSI.make_move(movimiento, Negro.color)
REVERSI.print_board()
movimiento = Blanco.my_turn(REVERSI.board, REVERSI.getValidMoves(1)) 
REVERSI.make_move(movimiento, Blanco.color)
REVERSI.print_board()


# print(REVERSI.getValidMoves(1))


