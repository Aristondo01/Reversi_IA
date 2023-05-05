import numpy as np
from Reversi import Reversi
import math

class Minimax(object):
    
    def __init__(self):
        self.search_depth = 3
        self.corners = [[0,0], [0,7], [7,0], [7,7]]
        self.depth_stability = 2
        pass
    
    def reward_amount_movements(self,amount):
        if amount == 0:
            return 20
        elif amount == 1:
            return 5
        elif amount > 2 and amount < 3:
            return 0
        elif amount > 3 and amount < 5:
            return -50
        else:
            return -100
        
    def reward_corners(self,move,factor):
        reward_corner = 0
        if move in self.corners:
            if factor == 1:
                reward_corner += 100
            else:
                reward_corner += 200
            
            
        return reward_corner

    def is_stable_ap1(self, board, row, col):
        # Verificar si la pieza está en una esquina
        if (row == 0 and col == 0) or (row == 0 and col == 7) or (row == 7 and col == 0) or (row == 7 and col == 7):
            return True
        
        # Verificar si la pieza está en un borde
        if row == 0 or col == 0 or row == 7 or col == 7:
            # Verificar si la pieza está rodeada por otras piezas en el mismo borde
            for i in range(max(0, row-1), min(row+2, 8)):
                for j in range(max(0, col-1), min(col+2, 8)):
                    if (i != row or j != col) and board[i][j] != 0:
                        return True
        else:
            # Verificar si la pieza está rodeada por otras piezas en el mismo cuadrante
            quadrant_row = row // 4
            quadrant_col = col // 4
            for i in range(quadrant_row*4, (quadrant_row+1)*4):
                for j in range(quadrant_col*4, (quadrant_col+1)*4):
                    if (i != row or j != col) and board[i][j] != 0:
                        return True
        
        # Si la pieza no es estable, devolver False
        return False

    def is_stable_ap2(self, board, row, col, depth):
        if depth <= self.depth_stability:
            if (row == 0 and col == 0) or (row == 0 and col == 7) or (row == 7 and col == 0) or (row == 7 and col == 7):
                return True
            
            if row == 0 or col == 0 or row == 7 or col == 7:
                for i in range(max(0, row-1), min(row+2, 8)):
                    for j in range(max(0, col-1), min(col+2, 8)):
                        if (i != row or j != col) and board[i][j] != 0:
                            return True
            else:
                # Verificar si la pieza está rodeada por otras piezas en el mismo cuadrante
                quadrant_row = row // 4
                quadrant_col = col // 4
                up = self.is_stable_ap2(board, row - 1, col, depth + 1)
                down = self.is_stable_ap2(board, row + 1, col, depth + 1)
                right = self.is_stable_ap2(board, row, col + 1, depth + 1)
                left = self.is_stable_ap2(board, row, col - 1, depth + 1)

                return up and down and right and left
            
            # Si la pieza no es estable, devolver False
            return False
        
        return True
        


    def stability(self, board):
        board_array = board.board
        stable_pieces = 0
        for i in range(8):
            for j in range(8):
                if board_array[i][j] != 0 and self.is_stable(board, i, j):
                    stable_pieces += 1
    
    def stability2(self, board):
        eigenvalues, eigenvectors = np.linalg.eig(board.board)
        largest_eigenvalue_index = np.argmax(eigenvalues)
        largest_eigenvector = eigenvectors[:, largest_eigenvalue_index]
        acu =""
        for i in range(8):
            for j in range(8):
                acu +=str(eigenvectors[i][j]) + " | "
            acu += "\n"
        print(acu)

    def average_entropy(self, board):
        board_array = board.board
        change = 4
        entropy_window = []
        for i in range(0, 8, change):
            for j in range(0, 8, change):
                black = 0
                white = 0
                for k in range(i,change):
                    for m in range(j,change):
                        if board_array[k, m] == 1:
                            white += 1
                        elif board_array[k, m] == -1:
                            black += 1
                prob_black = black / 16
                prob_white = white / 16
                H = -(prob_black * math.log2(prob_black) + prob_white * math.log2(prob_white))
                entropy_window.append(H)
        
        entropy_window = np.array(entropy_window)
        # return np.mean(entropy_window)
        print(np.mean(entropy_window))

    def entropy(self, board, turn):
        pieces = board.black + board.white
        proportion = board.white / pieces if turn == 1 else board.black / pieces
        H = - proportion * math.log2(proportion) - (1 - proportion) * math.log2(1-proportion)

        return H
        
    def reward(self, board, turn, number_of_shifts, factor, move):
        
        total_reward = 0
        enemy_movements_size = len(board.getValidMoves(-turn))
        
        total_reward += self.reward_amount_movements(enemy_movements_size) * factor 
        total_reward += self.reward_corners(move,factor) * factor 
        # total_reward += 10 * self.entropy(board, turn)
        
        score = board.black if turn == -1 else board.white
        other_score = board.black if turn == 1 else board.white

        total_reward += (score - other_score) * factor 
    
        return total_reward 

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
                rewards_for_moves[index_move] += self.reward(board, turn, number_of_shifts,factor,move)
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