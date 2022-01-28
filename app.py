from itsdangerous import json
from boggle import Boggle
from flask import Flask, jsonify, request,  render_template, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Winnie'
debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def make_html_board():
    """Show board"""

    board = boggle_game.make_board()
    session['board'] = board
    high_score = session.get('high_score', 0)
    game_num = session.get('game_num', 1)

    return render_template('board.html', board=board, game_num=game_num, high_score=high_score)

@app.route('/check-word')
def check_word():
    """Check if word is in dictionary and on board"""

    word = request.args['guess']
    board = session['board']
    return jsonify(result=boggle_game.check_valid_word(board, word))


@app.route('/post-score', methods=['POST'])
def post_score():
    """Receive and save score if highest score, add to number of game plays"""

    score = request.json['score']
    high_score = session.get('high_score', 0)
    game_num = session.get('game_num', 0)

    session['game_num'] = game_num + 1
    session['high_score'] = score if score > high_score else session['high_score']
    return jsonify(highScore=score > high_score)
