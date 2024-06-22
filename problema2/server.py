from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
import logica
import logging

game = logica.Game()
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

# Identifica qué archivo de texto modificar
def configure_logger(client_id):
    logger = logging.getLogger(client_id)
    if not logger.hasHandlers():
        handler = logging.FileHandler(f'rmi/logs/{client_id}_log.txt')
        formatter = logging.Formatter('%(asctime)s, %(message)s', datefmt='%H:%M:%S %d-%m-%Y')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('load_join')
    emit('updatelist', {'teams':game.get_teams(), 'players':game.usernames, 'scores': game.get_scores()})

    # Inicio del juego
    logger = configure_logger(request.sid)
    logger.info(f"ini, juego{game.num_juego}, inicio-juego")

@socketio.on('disconnect')
def on_disconnect():
    print(f'user {request.sid} disconnected')
    if game.leave_player(request.sid):
        emit('updatelist', {'teams':game.get_teams(), 'players':game.usernames, 'scores': game.get_scores(), 'turn': game.game_rotations[game.team_turn]}, broadcast=True)
        if game.gamemode and len(game.get_teams().keys()) < 2:

            # fin del juego, elimina a todos los jugadores
            for team_name, team_list in game.teams.items():
                for cid in team_list:
                    logger = configure_logger(cid)
                    logger.info(f"fin, juego{game.num_juego}, fin-juego")
                    os.popen(f"java -cp rmi/client Client rmi/logs/{cid}_log.txt").read()

            game.end_game()
            emit('game_over', {'message': "A team has disconnected! Game over."}, broadcast=True)

@socketio.on('join')
def on_join(data):
    name = data['name']
    team = data['team']
    data['sid'] = request.sid
    print(f"User {data['sid']} : {data['name']} want to join")

    #Crear un jugador
    logger = configure_logger(request.sid)
    logger.info(f"ini, juego{game.num_juego}, crea-jugador, {team}, {name}")

    if game.view_limit(team):
        if team in game.teams.keys():
            print(f"Ask to {game.teams[team][0]} : {game.usernames[game.teams[team][0]]}")
            emit('asktojoin', data, room=game.teams[team][0], callback=callJoin)

            # Operación para aceptar a un jugador en el equipo
            logger = configure_logger(game.teams[team][0])
            logger.info(f"ini, juego{game.num_juego}, aceptar-jugador, {data['team']}, {data['name']}")
        else:
            game.join_player(request.sid, name, team)
            if game.gamemode == 0:
                if len(game.teams.keys()) >= 2:
                    game.start_game()
                    emit("load_play", {'players': game.usernames}, broadcast=True)
            else:
                emit("load_play", {'players': game.usernames})
            data = {'teams':game.get_teams(), 'players':game.usernames, 'scores': game.get_scores(), 'turn': game.game_rotations[game.team_turn]}
            print(data)
            emit('updatelist', data, broadcast=True)

            # Se ingresa exitósamente a un jugador en el equipo
            logger.info(f"fin, juego{game.num_juego}, crea-jugador, {team}, {name}, True")

    else:
        emit('limit')

        # Se alcanzó el límite, no se ingresa al jugador
        logger.info(f"fin, juego{game.num_juego}, crea-jugador, {team}, {name}, False")

def callJoin(status, data):
    logger = configure_logger(game.teams[data['team']][0])
    if status:

        print(f"{data['sid']} joined")
        game.join_player(data['sid'], data['name'], data['team'])
        emit('updatelist', {'teams':game.get_teams(), 'players':game.usernames, 'scores': game.get_scores(), 'turn': game.game_rotations[game.team_turn]}, broadcast=True)
        if game.gamemode == 1:
            emit("load_play", {'players': game.usernames})
        
    else:
        print(f"{data['sid']} rejected")
        emit('reject', {'msg': f"Team {data['team']} has rejected you"}, room=data['sid'])

    # Se acepta o rechaza a un jugador en un equipo
    logger.info(f"fin, juego{game.num_juego}, aceptar-jugador, {data['team']}, {data['name']}, {status}")

    #No se ingresa al nuevo jugador
    logger = configure_logger(request.sid)
    logger.info(f"fin, juego{game.num_juego}, crea-jugador, {data['team']}, {data['name']}, {status}")

@socketio.on('rolldice')
def on_roll(data):
    team = data['team']
    name = data['name']

    result, passTurn = game.roll_dice(request.sid)

    if result > 0:
        #Operación de lanzar lado con un resultado válido
        logger = configure_logger(request.sid)
        logger.info(f"ini, juego{game.num_juego}, lanza-dado, {team}, {name}, {result}")
    
    emit('diceresult', result)
    if passTurn:
        emit('updatelist', {'teams':game.get_teams(), 'players':game.usernames, 'scores': game.get_scores(), 'turn': game.game_rotations[game.team_turn]}, broadcast=True)
    
    if result > 0: logger.info(f"fin, juego{game.num_juego}, lanza-dado, {team}, {name}, {result}")

    if game.locked:
        #Fin del juego, se ingresa el log en todos los jugadores
        for team_name, team_list in game.teams.items():
            for cid in team_list:
                logger = configure_logger(cid)
                logger.info(f"fin, juego{game.num_juego}, fin-juego")
                os.popen(f"java -cp rmi/client Client rmi/logs/{cid}_log.txt").read()

        msg = f"Team {game.game_rotations[game.team_turn]} has won! Game over."
        game.end_game()
        emit('game_over', {'message': msg}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
