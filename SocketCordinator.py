import time
from socketIO_client import SocketIO

# Cambia la URL y el puerto según tu servidor
URL = '127.0.0.1'
PORT = 3000
tournament_id = 1234
user_name = 'coordinator'
user_role = 'coordinator'  # Cambiar el user_role a 'player'


def connect():
    print('Conectado al servidor')
    socket.emit('signin', {
        'user_name': user_name,
        'tournament_id': tournament_id,
        'user_role': user_role
    })


def ok_signin():
    print('Inicio de sesión exitoso')

    # Emitir señal de "ready" a todos los jugadores después de un tiempo
    #time.sleep(5)
    socket.emit('start_tournament', {
        'tournament_id': tournament_id
    })
    print('Torneo iniciado')

# Conexión al servidor
socket = SocketIO(URL, PORT)
socket.on('connect', connect)
socket.on('ok_signin', ok_signin)
socket.wait()