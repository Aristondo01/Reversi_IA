from socketIO_client import SocketIO

# Cambia la URL y el puerto según tu servidor
URL = '127.0.0.1'
PORT = 4000

tournament_id = 123
user_name = 'gallanghof2'
user_role = 'player'

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
    game_id = data['game_id']
    player_turn_id = data['player_turn_id']
    board = data['board']
    # Aquí va tu lógica para jugar el juego
    movement = None  # Reemplaza esto con tu movimiento
    socket.emit('play', {
        'tournament_id': tournament_id,
        'player_turn_id': player_turn_id,
        'game_id': game_id,
        'movement': movement
    })

def on_finish(data):
    game_id = data['game_id']
    player_turn_id = data['player_turn_id']
    winner_turn_id = data['winner_turn_id']
    board = data['board']
    # Aquí va tu lógica para limpiar el tablero
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
