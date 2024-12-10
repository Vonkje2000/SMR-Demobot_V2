from flask import Flask, request, jsonify, render_template, redirect, url_for
from game import TicTacToe, RandomComputerPlayer, HumanPlayer, get_randomized_players

app1 = Flask(__name__)

# Store the game state globally for simplicity
current_game = None
x_player = None
o_player = None
current_letter = 'X'
x_player_moves = []
o_player_moves = []


@app1.route('/')
def index():
    global current_game, x_player, o_player, current_letter
    # Start a new game
    current_game = TicTacToe()
    x_player, o_player = get_randomized_players()
    current_letter = 'X'
    
    # If the computer is the first player, make its move immediately
    if isinstance(x_player, RandomComputerPlayer):
        move = x_player.get_move(current_game)
        current_game.make_move(move, current_letter)
        current_letter = 'O'  # Switch to human's turn

    return render_template('index1.html')  # Render the frontend


@app1.route('/make_move', methods=['POST'])
def make_move():
    global current_game, x_player, o_player, current_letter

    # Retrieve data from the frontend
    square = request.json.get('square')

    # Ensure the move is valid
    if not current_game or square not in current_game.available_moves():
        return jsonify({'error': 'Invalid move'}), 400

    # Make the move and check for winner
    current_game.make_move(square, current_letter)
    
    if current_letter == 'X':
        x_player_moves.append(square)
        print(f"Player 'X' makes a move to square {square}. Moves so far: {x_player_moves}")
    else:
        o_player_moves.append(square)
        print(f"Player 'O' makes a move to square {square}. Moves so far: {o_player_moves}")
    
    winner = current_game.current_winner
    board = current_game.board

    # Prepare the response
    response = {
        'board': board,
        'winner': winner,
        'is_tie': not current_game.empty_squares() and not winner
    }

    # Switch the turn
    current_letter = 'O' if current_letter == 'X' else 'X'

    return jsonify(response)

@app1.route('/back')
def redirect_to_main():
    return redirect('http://127.0.0.1:5000')  # Redirects to Welcome page (running on port 5000)

@app1.route('/get_move', methods=['POST'])
def get_computer_move():
    global current_game, x_player, o_player, current_letter

    # Get the move based on the current player
    if current_letter == 'X':
        move = x_player.get_move(current_game)
        x_player_moves.append(move)
        print(f"Player 'X' (computer) makes a move to square {move}. Moves so far: {x_player_moves}")
    else:
        move = o_player.get_move(current_game)
        o_player_moves.append(move)
        print(f"Player 'O' (computer) makes a move to square {move}. Moves so far: {o_player_moves}")
    
    # Make the move and check for winner
    current_game.make_move(move, current_letter)
    winner = current_game.current_winner
    board = current_game.board

    # Prepare the response
    response = {
        'move': move,
        'board': board,
        'winner': winner,
        'is_tie': not current_game.empty_squares() and not winner
    }

    # Switch the turn
    current_letter = 'O' if current_letter == 'X' else 'X'

    return jsonify(response)

@app1.route('/restart', methods=['POST'])
def restart():
    global current_game, x_player, o_player, current_letter
    # Reset the game state
    current_game = TicTacToe()
    x_player, o_player = get_randomized_players()
    current_letter = 'X'

    x_player_moves.clear()
    o_player_moves.clear()

    print ("The game has been restarted") 

    # If the computer is the first player, make its move immediately
    if isinstance(x_player, RandomComputerPlayer):
        move = x_player.get_move(current_game)
        current_game.make_move(move, current_letter)
        x_player_moves.append(move)
        current_letter = 'O'  # Switch to human's turn
        

    return jsonify({
        'board': current_game.board, 
        'current_letter': current_letter,
        'x_player' : 'Computer' if isinstance(x_player, RandomComputerPlayer) else 'Human',
        'o_player' : 'Computer' if isinstance(o_player, RandomComputerPlayer) else 'Human'
        })

if __name__ == '__main__':
    #app1.run(debug=True)
    app1.run(port=5001)
