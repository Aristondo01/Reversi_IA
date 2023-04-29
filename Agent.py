class Agent(object):
    def __init__(self,color):
        self.color = color
        self.board = []
        self.posible_movements = []
        
    def my_turn(self, board,posible_movements):
        self.board = board
        self.posible_movements = posible_movements
        return self.select_movment()  

    def select_movment(self):
        
        if len(self.posible_movements):
            return self.posible_movements[0]
        else:
            return None
    
    
    