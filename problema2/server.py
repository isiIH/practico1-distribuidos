from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
import logica

game = logica.Game()
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('load_join')
    emit('updatelist', {'teams':game.get_teams(), 'players':game.usernames, 'scores': game.get_scores()})

@socketio.on('disconnect')
def on_disconnect():
    print(f'user {request.sid} disconnected')
    if game.leave_player(request.sid):
        emit('updatelist', {'teams':game.get_teams(), 'players':game.usernames, 'scores': game.get_scores(), 'turn': game.game_rotations[game.team_turn]}, broadcast=True)
        if game.gamemode and len(game.get_teams().keys()) < 2:
            game.end_game()
            emit('game_over', {'message': "A team has disconnected! Game over."}, broadcast=True)

@socketio.on('join')
def on_join(data):
    name = data['name']
    team = data['team']
    data['sid'] = request.sid
    print(f"User {data['sid']} : {data['name']} want to join")
    if game.view_limit(team):
        if team in game.teams.keys():
            print(f"Ask to {game.teams[team][0]} : {game.usernames[game.teams[team][0]]}")
            emit('asktojoin', data, room=game.teams[team][0], callback=callJoin)
        else:
            game.join_player(request.sid, name, team)
            emit('updatelist', {'teams':game.get_teams(), 'players':game.usernames, 'scores': game.get_scores(), 'turn': game.game_rotations[game.team_turn]}, broadcast=True)
            if game.gamemode == 0:
                if len(game.teams.keys()) >= 2:
                    game.start_game()
                    emit("load_play", {'players': game.usernames}, broadcast=True)
            else:
                emit("load_play", {'players': game.usernames})

    else:
        emit('limit')

def callJoin(status, data):
    if status:
        print(f"{data['sid']} joined")
        game.join_player(data['sid'], data['name'], data['team'])
        emit('updatelist', {'teams':game.get_teams(), 'players':game.usernames, 'scores': game.get_scores(), 'turn': game.game_rotations[game.team_turn]}, broadcast=True)
        if game.gamemode == 1:
            emit("load_play", {'players': game.usernames})
    else:
        print(f"{data['sid']} rejected")
        emit('reject', {'msg': f"Team {data['team']} has rejected you"}, room=data['sid'])

@socketio.on('rolldice')
def on_roll():
    result, passTurn = game.roll_dice(request.sid)
    print(result)
    emit('diceresult', result)
    if passTurn:
        emit('updatelist', {'teams':game.get_teams(), 'players':game.usernames, 'scores': game.get_scores(), 'turn': game.game_rotations[game.team_turn]}, broadcast=True)

    if game.locked:
        msg = f"Team {game.game_rotations[game.team_turn]} has won! Game over."
        emit('game_over', {'message': msg}, broadcast=True)
        game.end_game()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
