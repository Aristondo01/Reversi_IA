import numpy as np
from Reversi import Reversi

class Minimax(object):
    
    def __init__(self):
        self.search_depth = 3
        pass
    
    def reward(self, board, turn, number_of_shifts,factor):
        score = board.black if turn == -1 else board.white
        other_score = board.black if turn == 1 else board.white


        return (score - other_score) * factor 

    def minimax(self, board_array, turn, maximize, depth):
        if depth <= self.search_depth:
            board = Reversi()
            board.set_board(board_array.copy())

            winner = board.winner_exist()
            
            factor = 1 if maximize == turn else -1

            # Aca vamos a poner la funcion de recompensa en lugar de los valores dummy hay que incluir depth = 0.
            if winner == turn:
                return 1000 * factor
            if winner == -turn:
                return -1000 * factor
            if winner == 2:
                return 0
            

            number_of_shifts = np.count_nonzero(board != 0)-4
            
            possible_moves = board.getValidMoves(turn)
            rewards_for_moves = np.zeros(len(possible_moves))

            if not possible_moves:
                if depth == 0:
                    return ()
                return self.minimax(board_array.copy(), -turn, maximize, depth+1)
            
            for index_move in range(len(possible_moves)):
                move = possible_moves[index_move]
                board.make_move(move, turn)
                rewards_for_moves[index_move] += self.reward(board, turn, number_of_shifts,factor)
                rewards_for_moves[index_move] += self.minimax(board.board.copy(), -turn, maximize, depth+1)
                board.reset_last_move()
                
            
            if depth == 0:
                return possible_moves[np.argmax(rewards_for_moves)]
            
            if maximize == turn:
                return np.max(rewards_for_moves)
            else:
                return np.min(rewards_for_moves)
            
        else:
            return 0