import numpy as np

# Encoding. X es blancas, 1. O es negras, -1. Vacio es 0.

class Reversi(object):
    
    def __init__(self):
        self.row_count = 8
        self.column_count = 8
        # if len(tablero) > 0:
        #     self.board = tablero
        # else:
        self.board = np.zeros((self.row_count, self.column_count))
        self.board_copy = self.board.copy()
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.board[4][4] = 1
        
        self.update_count()

    def set_board(self, board):
        self.board = board
        self.update_count()
        self.board_copy = self.board.copy()    

    def update_count(self):
        self.black = np.count_nonzero(self.board == -1)
        self.white = np.count_nonzero(self.board == 1)
        

    def print_board(self):
        print_board ="  0  1  2  3  4  5  6  7 \n"
        print_board +=" ╔══╦══╦══╦══╦══╦══╦══╦══╗"
        for i in range(self.row_count):
            print_board += "\n"+str(i)+"║"
            for j in range(self.column_count):
                if self.board[i][j] == 1:
                    print_board += "● ║"
                elif self.board[i][j] == -1:
                    print_board += "○ ║"
                else:
                    print_board += "  ║"
            if i != self.row_count - 1:
                print_board += "\n ╠══╬══╬══╬══╬══╬══╬══╬══╣"
            else:
                print_board += "\n ╚══╩══╩══╩══╩══╩══╩══╩══╝"
                
        print(print_board)
    
    def getValidMoves(self, tile):
        # Returns a list of [x,y] lists of valid moves for the given player on the given board.
        validMoves = []
        for x in range(8):
            for y in range(8):
                if self.is_valid_move(tile, x, y) != False:
                    validMoves.append([x, y])

        return validMoves

    def reset_last_move(self):
        self.board = self.board_copy.copy()
        self.update_count()

    def winner_exist(self):
        blancas = self.white
        negras = self.black
        espacios = 64 - blancas - negras
        
        if espacios > 0 and (self.getValidMoves(-1) or self.getValidMoves(1)):
            return 0
        
        if blancas > negras:
            return 1
        elif negras > blancas:
            return -1
        elif blancas == negras:
            return 2
                

    def is_on_board(self, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def is_valid_move(self, tile, x, y):
        if self.board[x][y] != 0:
            return False
        direcciones = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for direccion in direcciones:
            fichas_cambiadas = []
            i, j = x, y
            i += direccion[0]
            j += direccion[1]
            while i >= 0 and i < self.row_count and j >= 0 and j < self.column_count and self.board[i][j] != 0 and self.board[i][j] != tile:
                fichas_cambiadas.append((i, j))
                i += direccion[0]
                j += direccion[1]
            if i >= 0 and i < self.column_count and j >= 0 and j < self.column_count and self.board[i][j] == tile and len(fichas_cambiadas) > 0:
                return True
        return False

    def make_move(self, move, tile):
        if move:
            x = move[0]
            y = move[1]

            
            #print(x, y)
            if self.board[x][y] != 0:
                return
            direcciones = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
            for direccion in direcciones:
                fichas_cambiadas = []
                i, j = x, y
                i += direccion[0]
                j += direccion[1]
                while i >= 0 and i < self.row_count and j >= 0 and j < self.column_count and self.board[i][j] != 0 and self.board[i][j] != tile:
                    fichas_cambiadas.append((i, j))
                    i += direccion[0]
                    j += direccion[1]
                if i >= 0 and i < self.column_count and j >= 0 and j < self.column_count and self.board[i][j] == tile and len(fichas_cambiadas) > 0:
                    for ficha in fichas_cambiadas:
                        self.board[ficha[0]][ficha[1]] = tile
                    self.board[x][y] = tile
        
            self.update_count()