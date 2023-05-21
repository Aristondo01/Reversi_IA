from minmax2 import Minimax2
from Reversi import Reversi
import sys
import random
import numpy as np
from socketIO_client import SocketIO

if len(sys.argv) < 2:
    print("Usage: python jugador.py <username>")
    sys.exit()

# Cambia la URL y el puerto según tu servidor
URL = '127.0.0.1'
PORT = 4000

tournament_id = 123
user_name = sys.argv[1]
user_role = 'player'

minimax = Minimax2()
letras = 'abcdefgh'

def play_game(board, player_turn_id):

    move = minimax.minimax(board.board.copy(), player_turn_id, player_turn_id)
    if move:
        print(letras[move[1]], move[0] + 1, 'minimax')
    else:
        print('pass')
    board.make_move(move, player_turn_id)
    print(move)
    return move

def on_connect():
    print('Connected')
    socket.emit('signin', {
        'user_name': user_name,
        'tournament_id': tournament_id,
        'user_role': user_role
    })

def on_ok_signin():
    print("Successfully signed in!")

def on_ready(data):
    #print(data)
    game_id = data['game_id']
    player_turn_id = data['player_turn_id']
    boardito = data['board']
    print("------------------",player_turn_id,"------------------")
    if player_turn_id == 1:
        boardito = [-1 if x == 2 else x for x in boardito]
    elif player_turn_id == 2:
        boardito = [-1 if x == 1 else x for x in boardito]
        # boardito = [1 if x == 2 else x for x in boardito]
    
    board_array = np.array(boardito).reshape(8, 8)
    
    # Mostrar el board
    print(board_array)

    board = Reversi()
    board.set_board(board_array)
    # turn = player_turn_id

    move = play_game(board, player_turn_id)
    index = move[0] * 8 + move[1]
    print("COSAS", index)
    socket.emit('play', {
        'tournament_id': tournament_id,
        'player_turn_id': player_turn_id,
        'game_id': game_id,
        'movement': index
    })

def on_finish(data):
    print(data)
    game_id = data['game_id']
    player_turn_id = data['player_turn_id']
    winner_turn_id = data['winner_turn_id']
    board_array = np.array(data['board'])

    board = Reversi()
    board.set_board(board_array)

    if winner_turn_id == player_turn_id:
        print("You won!")
    elif winner_turn_id == 3 - player_turn_id:
        print("You lost!")
    else:
        print("It's a draw!")

    socket.emit('player_ready', {
        'tournament_id': tournament_id,
        'player_turn_id': player_turn_id,
        'game_id': game_id
    })

socket = SocketIO(URL, PORT)
socket.on('connect', on_connect)
socket.on('ok_signin', on_ok_signin)
socket.on('ready', on_ready)
socket.on('finish', on_finish)
socket.wait()
