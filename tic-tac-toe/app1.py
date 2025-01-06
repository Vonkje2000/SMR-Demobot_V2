from flask import Flask, request, jsonify, render_template, redirect, url_for
from game import TicTacToe, RandomComputerPlayer, HumanPlayer, get_randomized_players
import sys
sys.path.insert(0, 'D:/Berkas/SMR/Block 2/SMR-Demobot_V2')
from Promobot_class import Kawasaki_1
import time

app1 = Flask(__name__)
k1 = Kawasaki_1()
k1.SPEED(20)
k1.TOOL(0, 0, 30, 0, 0, 0)                                                 #X, Z, Y because Z is the same direction as the tool, so it changed from straight up position

# Store the game state globally for simplicity
current_game = None
x_player = None
o_player = None
current_letter = 'X'
x_player_moves = []
o_player_moves = []


def robot_moves(square, player):
    """
    :param square: Integer (0-9) specifying the square on the Tic Tac Toe board.
    :param player: String ('X' or 'O') specifying the current player.
    """
    try:
        # Define safe position (adjust based on your workspace setup)
        safe_position = (-162, 439, -21, -99, 179, -99)  # Example position

        # Define storage positions for X and O tiles
        x_box = (-162, 439, -21, -99, 179, -99)  # Adjust coordinates for X storage box
        o_box = (-162, 439, -21, -99, 179, -99)  # Adjust coordinates for O storage box

        # Define positions for above each square (in meters), adjust for your board's physical setup
        above_square_positions = {
            0: (-23, 565, -190, -99, 180, -99),  # Above Top-left
            1: (-23, 437, -190, -123, 180, -123),  # Above Top-center
            2: (-23, 313, -190, 137, 180, 137),  # Above Top-right
            3: (-145, 565, -190, 96, 180, 96),  # Above Middle-left
            4: (-145, 437, -190, 96, 180, 96),  # Above Center
            5: (-145, 313, -190, 96, 180, 96),  # Above Middle-right
            6: (-132, 439, -21, -99, 179, -99) ,  # Above Bottom-left
            7: (-278, 437, -190, 97, 180, 97),  # Above Bottom-center
            8: (-278, 313, -190, 97, 180, 97),  # Above Bottom-right
        }

        # Positions for placing tiles on the squares (slightly lower than "above" positions)
        square_positions = {
            key: (x, y, z - 0.1, rx, ry, rz)  # Lower z by 0.1 meters to "place" tile
            for key, (x, y, z, rx, ry, rz) in above_square_positions.items()
        }

        # 1. Move to the safe position
        print(f"Moving to safe position: {safe_position}")
        k1.JMOVE_TRANS(*safe_position)

        # 2. Move to the appropriate storage box (X or O)
        if player == 'X':
            print(f"Moving to X box: {x_box}")
            k1.JMOVE_TRANS(*x_box)
            print("Picking up an X tile.")
        elif player == 'O':
            print(f"Moving to O box: {o_box}")
            k1.JMOVE_TRANS(*o_box)
            print("Picking up an O tile.")

        # Simulate a short pause to "pick up" the tile (e.g., close gripper)
        # Add actual gripper control commands here
        #robot.set_digital_out(0, True)  # Example: close the gripper
        print("Gripper closed.")

        # 3. Move to the square's "above" position
        above_position = above_square_positions[square]
        print(f"Moving above square {square}: {above_position}")
        k1.JMOVE_TRANS(*above_position)

        # 4. Move to the square's position to place the tile
        place_position = square_positions[square]
        print(f"Placing tile on square {square}: {place_position}")
        k1.JMOVE_TRANS(*place_position)

        # Simulate a short pause to "release" the tile (e.g., open gripper)
        # Add actual gripper control commands here
        #robot.set_digital_out(0, False)  # Example: open the gripper
        print("Gripper opened. Tile placed.")

        # 5. Return to the safe position
        print(f"Returning to safe position: {safe_position}")
        k1.JMOVE_TRANS(*safe_position)
        time.sleep(4)# Wait 5 seconds (adjust this based on the robot's speed))

    except Exception as e:
        print(f"Error during robot movement: {e}")

def return_tile_to_box(square, tile):
    """
    Moves the robot to a specific square, picks up the tile, and returns it to its storage box.
    :param square: Integer (0-8), the square number.
    :param tile: String ('X' or 'O'), the type of tile to return.
    """
    try:
        # Define safe position (example values, adjust as necessary)
        safe_position = (-162, 439, -21, -99, 179, -99)

        # Define storage positions for X and O tiles
        x_box = (-102, 439, -21, -99, 179, -99)
        o_box = (-102, 385, -21, -99, 179, -99)

        # Define positions for above each square
        above_square_positions = {
            0: (-23, 565, -190, -99, 180, -99),  # Above Top-left
            1: (-23, 437, -190, -123, 180, -123),  # Above Top-center
            2: (-23, 313, -190, 137, 180, 137),  # Above Top-right
            3: (-145, 565, -190, 96, 180, 96),  # Above Middle-left
            4: (-145, 437, -190, 96, 180, 96),  # Above Center
            5: (-145, 313, -190, 96, 180, 96),  # Above Middle-right
            6: (-132, 439, -21, -99, 179, -99) ,  # Above Bottom-left
            7: (-278, 437, -190, 97, 180, 97),  # Above Bottom-center
            8: (-278, 313, -190, 97, 180, 97),  # Above Bottom-right
        }

        # Positions for the square itself
        square_positions = {
            key: (x, y, z - 0.1, o, a, t) for key, (x, y, z, o, a, t) in above_square_positions.items()
        }

        # Move to the safe position
        print(f"Moving to safe position: {safe_position}")
        k1.JMOVE_TRANS(*safe_position)

        # Move above the square
        above_position = above_square_positions[square]
        print(f"Moving above square {square}: {above_position}")
        k1.JMOVE_TRANS(*above_position)

        # Move to the square to pick up the tile
        place_position = square_positions[square]
        print(f"Picking up tile '{tile}' from square {square}: {place_position}")
        k1.JMOVE_TRANS(*place_position)

        # Close the gripper to pick up the tile
        #k1.CLOSE_GRIPPER()
        print("Gripper closed. Tile picked up.")

        # Return to the safe position
        k1.JMOVE_TRANS(*safe_position)

        # Move to the appropriate storage box
        if tile == 'X':
            print(f"Returning tile '{tile}' to X box: {x_box}")
            k1.JMOVE_TRANS(*x_box)
        elif tile == 'O':
            print(f"Returning tile '{tile}' to O box: {o_box}")
            k1.JMOVE_TRANS(*o_box)

        # Open the gripper to release the tile
        #kawasaki_arm.OPEN_GRIPPER()
        print(f"Tile '{tile}' returned to its box.")

        # Return to the safe position
        k1.JMOVE_TRANS(*safe_position)

    except Exception as e:
        print(f"Error while returning tile to box: {e}")


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
        square = move
        current_game.make_move(move, current_letter)
        robot_moves(square, current_letter)
        print("waiting for the robot to finish the movement")
        time.sleep(6) # Adjust based on the robot's speed and movement time
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
    
    
    # Trigger the robot to pick up and place the tile
    robot_moves(square, current_letter)
    print("waiting for the robot to finish the movement")
    time.sleep(6) # Adjust based on the robot's speed and movement time
    

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
        square = move
    else:
        move = o_player.get_move(current_game)
        o_player_moves.append(move)
        print(f"Player 'O' (computer) makes a move to square {move}. Moves so far: {o_player_moves}")
        square = move
    
    
    # Trigger the robot to pick up and place the tile
    robot_moves(square, current_letter)
    print("waiting for the robot to finish the movement")
    time.sleep(6) # Adjust based on the robot's speed and movement time

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
    global x_player_moves, o_player_moves

     # Save the current board state before resetting
    previous_board = current_game.board.copy()

    # Reset the game state
    current_game = TicTacToe()
    x_player, o_player = get_randomized_players()
    current_letter = 'X'

    x_player_moves.clear()
    o_player_moves.clear()

    print ("The game has been restarted, the robot will clear the board") 

    # Robot puts tiles back to storage boxes
    for square,tile in enumerate (previous_board):
        if tile != ' ':  # Check if there's a tile in the square
            print(f"Robot is moving to square {square} to pick up tile '{tile}' and return it to the box.")
            return_tile_to_box(square, tile)  # Return tile to its corresponding box
            # Wait for the robot to finish before moving to the next square
            time.sleep(10)  # Adjust based on your robot's speed and movements

    # If the computer is the first player, make its move immediately
    if isinstance(x_player, RandomComputerPlayer):
        move = x_player.get_move(current_game)
        square = move
        current_game.make_move(move, current_letter)
        x_player_moves.append(move)
        robot_moves(square, current_letter)
        print("waiting for the robot to finish the movement")
        time.sleep(6) # Adjust based on the robot's speed and movement time
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
