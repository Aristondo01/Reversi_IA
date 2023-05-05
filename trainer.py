import numpy as np
def read_tablero():
    with open("tablero.txt", "r",encoding="utf-8") as file:
            text = file.read()

    tablero_temp = text.split("\n")
    
    tablero=[]
    for i in range(len(tablero_temp)):
        tablero.append(np.array(tablero_temp[i].split(",")))
    
    
    return np.array(tablero)