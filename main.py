from Reversi import Reversi
from Agent import Agent
REVERSI = Reversi()


Blanco = Agent(1)
Negro = Agent(-1)


# REVERSI.print_board()
# movimiento = Negro.my_turn(REVERSI.board, REVERSI.getValidMoves(-1)) 
# REVERSI.make_move(movimiento, Negro.color)
# REVERSI.print_board()
# movimiento = Blanco.my_turn(REVERSI.board, REVERSI.getValidMoves(1)) 
# REVERSI.make_move(movimiento, Blanco.color)
# REVERSI.print_board()


done = False
turno = -1
while not done:
    
    if REVERSI.winner_exist() != 0:
        done = True
    else:
        if turno == -1:
            movimiento = Negro.my_turn(REVERSI.board, REVERSI.getValidMoves(-1)) 
            if movimiento != None:
                REVERSI.make_move(movimiento, Negro.color)
        elif turno == 1:
            movimiento = Blanco.my_turn(REVERSI.board, REVERSI.getValidMoves(1)) 
            if movimiento != None:
                REVERSI.make_move(movimiento, Blanco.color)
            
        turno*=-1
        
victoria="Empate"
if REVERSI.winner_exist() == 1:
    victoria = "Blanco"
elif REVERSI.winner_exist() == -1:
    victoria = "Negro"

print("Gano:", victoria)
REVERSI.print_board()



# print(REVERSI.getValidMoves(1))


