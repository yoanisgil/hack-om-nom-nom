from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
from web_game import WebGameEngine

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'iGZhnHD+s6a}5q%y7w3q6$89JNFa25'
socketio = SocketIO(app)

game_engine = WebGameEngine()


@app.route('/')
def index():
    game_tiles = [['Cat', 'Rat', 'Cheese'], ['Hedgehog', 'Frog', 'Fly'], ['Wolf', 'Rabbit', 'Carrot']]
    transposed = map(list, zip(*game_tiles))
    return render_template('game.html', game_tiles=transposed)


@app.route('/init_session', methods=['POST'])
def hello_world():
    json_request = request.json

    if 'num_players' not in json_request:
        return jsonify({'error': 'num_players is required'}), 400

    num_players = int(json_request['num_players'])

    session = game_engine.new_session(num_players)

    return jsonify(session.to_json())


@app.route('/next_move', methods=['POST'])
def next_move():
    json_request = request.json

    if 'card_index' not in json_request:
        return jsonify({'error': 'card_index is required'}), 400

    if 'session_id' not in json_request:
        return jsonify({'error': 'session_id is required'}), 400

    session_id = json_request['session_id']

    if not game_engine.has_next_move(session_id):
        return jsonify({'error': 'Game has ended'}), 400

    session = game_engine.next_move(session_id, int(json_request['card_index']))

    return jsonify(session.to_json())


if __name__ == "__main__":
    app.debug = True
    socketio.run(app, host='0.0.0.0')
