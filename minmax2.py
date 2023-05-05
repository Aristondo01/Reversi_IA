import numpy as np
from Reversi import Reversi
import math
import hashlib
import time
import random

class Minimax2(object):
    
    def __init__(self):
        self.search_depth = 4
        self.corners = [[0,0], [0,7], [7,0], [7,7]]
        self.depth_stability = 2
        self.history = {}
        pass
    
    def reward_amount_movements(self,amount):
        if amount == 0:
            return 5
        elif amount == 1:
            return 7
        elif amount > 2 and amount < 3:
            return 10
        elif amount > 3 and amount < 5:
            return 12
        else:
            return 15
        
    def reward_corners(self, board, turn, factor, move):
        if not move:
            board_array = board.board
            reward_corner = 0
            for corner in self.corners:
                i, j = corner
                if board_array[i][j] == 1 and factor == 1:
                    reward_corner += 25
                elif board_array[i][j] == -1 and factor == -1:
                    reward_corner += 50
            return reward_corner

        reward_corner = 0
        if move in self.corners:
            if factor == 1:
                reward_corner += 100
            else:
                reward_corner += 200
            
            
        return reward_corner

    def is_stable_ap1(self, board, row, col):
        board_array = board.board
        # Verificar si la pieza está en una esquina
        if (row == 0 and col == 0) or (row == 0 and col == 7) or (row == 7 and col == 0) or (row == 7 and col == 7):
            return True
        
        # Verificar si la pieza está en un borde
        if row == 0 or col == 0 or row == 7 or col == 7:
            # Verificar si la pieza está rodeada por otras piezas en el mismo borde
            for i in range(max(0, row-1), min(row+2, 8)):
                for j in range(max(0, col-1), min(col+2, 8)):
                    if (i != row or j != col) and board_array[i][j] != 0:
                        return True
        else:
            # Verificar si la pieza está rodeada por otras piezas en el mismo cuadrante
            quadrant_row = row // 4
            quadrant_col = col // 4
            for i in range(quadrant_row*4, (quadrant_row+1)*4):
                for j in range(quadrant_col*4, (quadrant_col+1)*4):
                    if (i != row or j != col) and board_array[i][j] != 0:
                        return True
        
        # Si la pieza no es estable, devolver False
        return False

    def is_stable_ap2(self, board, row, col, depth):
        board_array = board.board
        if depth <= self.depth_stability:
            if (row == 0 and col == 0) or (row == 0 and col == 7) or (row == 7 and col == 0) or (row == 7 and col == 7):
                return True
            
            if row == 0 or col == 0 or row == 7 or col == 7:
                for i in range(max(0, row-1), min(row+2, 8)):
                    for j in range(max(0, col-1), min(col+2, 8)):
                        if (i != row or j != col) and board_array[i][j] != 0:
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
        


    def stability(self, board, turn):
        board_array = board.board
        stable_pieces = 0
        for i in range(8):
            for j in range(8):
                if board_array[i][j] != 0 and board_array[i][j] == turn and self.is_stable_ap2(board, i, j, 0):
                    stable_pieces += 1
        return stable_pieces

    def entropy(self, board, turn):
        pieces = board.black + board.white
        # proportion = board.white / pieces if turn == 1 else board.black / pieces
        proportion = board.white / 64 if turn == 1 else board.black / 64
        H = - proportion * math.log2(proportion) - (1 - proportion) * math.log2(1-proportion)

        return H
    
    def reward_borders(self, move):
        if move:
            x, y = move
            reward = 0
            if x == 0 or x == 7 or y == 0 or y == 7:
                reward = 50
            return reward
        return 0
    
    def reward_borders_2(self, board, tile):
        reward = 0
        board_array = board.board
        for i in range(8):
            if board_array[i][0] == tile:
                reward += 10
            if board_array[i][7] == tile:
                reward += 10
        for i in range(8):
            if board_array[0][i] == tile:
                reward += 10
            if board_array[0][i] == tile:
                reward += 10
        return reward

        
    def reward_center(self, board, turn):
        board_array = board.board
        reward = 0
        if board_array[4][4] == turn:
            reward += 20
        if board_array[4][5] == turn:
            reward += 20
        if board_array[5][4] == turn:
            reward += 20
        if board_array[5][5] == turn:
            reward += 20
        return reward

        
    def reward(self, board, turn, number_of_shifts, factor, move = None):
        
        total_reward = 0
        enemy_movements_size = len(board.getValidMoves(-turn))
        self_movements_size = len(board.getValidMoves(turn))

        corner_factor = 1

        if 0 <= board.black + board.white <= 30:
            corner_factor = 2
        elif 31 <= board.black + board.white <= 40:
            corner_factor = 1.3 
        
        border_factor = 0.1
        if 5 <= board.black + board.white <= 15:
            border_factor = 2
        if 16 <= board.black + board.white <= 30:
            border_factor = 0.5
        if 31 <= board.black + board.white <= 45:
            border_factor = 0.3

        # print(self.reward_borders(move))

        total_reward += 50 * self.reward_corners(board, turn, factor, move) * corner_factor * factor
        # total_reward += 10 * self.stability(board, turn) * factor 
        total_reward += 10 * self.reward_amount_movements(enemy_movements_size) * -factor
        total_reward += 10 * self.reward_borders(move) * factor * border_factor
        # total_reward += 10 * self.reward_borders_2(board, turn) * factor * border_factor
        total_reward += 10 *self.reward_center(board, turn) * factor

        tiles = 1
        if board.black + board.white < 25:
            tiles = -2
        if board.black + board.white < 15:
            tiles = -5
        if board.black + board.white < 5:
            tiles = -10

        score = board.black if turn == -1 else board.white
        other_score = board.black if turn == 1 else board.white

        total_reward += (score - other_score) * tiles * factor


        # print(total_reward * factor)
    
        return total_reward
    
    def add_board_history(self, hex, reward):
        if hex not in self.history:
            self.history[hex] = reward

    def get_hex_board(self, board):
        arr_bytes = board.board.copy().tobytes()
        hash_obj = hashlib.sha256(arr_bytes)
        hash_hex = hash_obj.hexdigest()
        return hash_hex
    
    def is_in_history(self, board):
        return self.get_hex_board(board) in self.history

    def get_history_value(self, board):
        hex_value = self.get_hex_board(board)
        return self.history[hex_value]


    def minimax_func(self, board_array, turn, maximize, depth):
        board = Reversi()
        board.set_board(board_array.copy())
        hash_hex = self.get_hex_board(board)
        factor = 1 if maximize == turn else -1

        # print(factor)

        if (time.time() - self.start_time) > self.limit - 5:
            reward = self.reward(board, turn, 0, factor) 
            if depth == 0:
                possible_moves = board.getValidMoves(turn)
                if possible_moves:
                    return random.choice(possible_moves), reward
                else:
                    return (), reward
            
            return reward
        
        if depth <= self.search_depth:
            winner = board.winner_exist()
            # Aca vamos a poner la funcion de recompensa en lugar de los valores dummy hay que incluir depth = 0.
            if winner == turn:
                return 1000 * factor
            if winner == -turn:
                return 1000 * factor
            if winner == 2:
                return 0
            

            number_of_shifts = np.count_nonzero(board != 0)-4
            
            possible_moves = board.getValidMoves(turn)
            rewards_for_moves = np.zeros(len(possible_moves))

            if not possible_moves:
                if depth == 0:
                    reward = self.reward(board, -turn, number_of_shifts,factor)
                    self.add_board_history(hash_hex, reward)
                    return (), reward
                reward = self.minimax_func(board_array.copy(), -turn, maximize, depth+1)
                self.add_board_history(hash_hex, reward)
                return 0
            
            for index_move in range(len(possible_moves)):
                move = possible_moves[index_move]
                board.make_move(move, turn)
                if False:
                    rewards_for_moves[index_move] += self.get_history_value(board)
                else:
                    rewards_for_moves[index_move] += self.reward(board, turn, number_of_shifts,factor,move)
                    rewards_for_moves[index_move] += self.minimax_func(board.board.copy(), -turn, maximize, depth+1)
                    self.add_board_history(board, rewards_for_moves[index_move])
                # rewards_for_moves[index_move] += self.reward(board, turn, number_of_shifts,factor,move)
                board.reset_last_move()
                
            
            if depth == 0:
                reward = rewards_for_moves[np.argmax(rewards_for_moves)]
                self.add_board_history(hash_hex, reward)
                return possible_moves[np.argmax(rewards_for_moves)], reward
            
            if maximize == turn:
                reward = np.max(rewards_for_moves)
                self.add_board_history(hash_hex, reward)
                return reward
            else:
                reward = np.min(rewards_for_moves)
                self.add_board_history(hash_hex, reward)
                return reward
            
        else:
            return 0
        
    def minimax(self, board_array, turn, maximize):
        rewards_per_epoch = []
        moves = []
        self.start_time = time.time()
        self.limit = 40
        max_depth = 7
        i = 0

        move, reward = self.minimax_func(board_array, turn, maximize, 0)

        return move

        while i < max_depth and time.time() - self.start_time < self.limit:
            print(i)
            self.search_depth = i
            move, reward = self.minimax_func(board_array, turn, maximize, 0)
            moves.append(move)
            rewards_per_epoch.append(reward)
            i += 1

        if maximize == turn:
            reward_index = np.argmax(rewards_per_epoch)
            return moves[reward_index]
        else:
            reward_index = np.argmin(rewards_per_epoch)
            return moves[reward_index]
