from flask import Flask, jsonify, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
boggle_game = Boggle()

@app.route('/', methods=["GET", "POST"])
def home_page():
    if request.method == 'POST':
        if 'board' not in session:
            board = boggle_game.make_board()
            session['board'] = board
        
        return redirect('/board')
    return render_template('home.html')
@app.route('/board')
def board():
    board = session.get('board', [])
    
    return render_template('board.html', board=board)

@app.route('/checkword')
def check_word():
    try:
        word = request.args.get('word')
        board = session.get('board', [])  # Corrected line
        if not board:  # If there's no board in the session
            return jsonify({'result': 'error', 'message': 'Board not found'}), 400

        result = boggle_game.check_valid_word(board, word)
        return jsonify({'result': result})
    except Exception as e:
        # Log the error for debugging
        print(f"Error checking word: {e}")
        # Return a generic error message to the client
        return jsonify({'result': 'error', 'message': 'An error occurred'}), 500

@app.route('/post-score', methods=["POST"])
def post_score():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    num_plays = session.get('num_plays', 0)

    session['num_plays'] = num_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)

@app.route('/get-stats', methods=["GET"])
def get_stats():
    return jsonify({
        'num_plays': session.get('num_plays', 0),
        'highscore': session.get('highscore', 0)
    })