from flask import Flask, render_template, request, url_for
from flask_socketio import SocketIO, emit, join_room
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
    return render_template('index.html', teams=game.get_teams(), players=game.usernames)

@app.route('/play')
def play():
    return render_template('play.html', teams=game.get_teams(), players=game.usernames, scores=game.scores)

@socketio.on('connection')
def on_connect(socket):
    print('user connected')

@socketio.on('disconnect')
def on_admin_disconnect():
    print('user disconnected')

# only emitted by players

@socketio.on('join')
def on_join(data):
    name = data['name']
    team = data['team']
    success = game.join_player(request.sid, name, team)
    join_room(team)
    if success:
        emit('updatelist', {'teams':game.get_teams(), 'players':game.usernames}, broadcast=True)
        if len(game.teams.keys()) >= 2:
            emit("play", broadcast=True)
    else:
        emit('limit', {'success': success, 'limit': game.limit_players_per_room})

@socketio.on('rolldice')
def on_roll():
    print(request.sid)
    emit('diceresult', game.roll_dice(request.sid))

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')