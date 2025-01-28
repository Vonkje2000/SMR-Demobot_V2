from flask import request, jsonify, render_template
from game import TicTacToe, RandomComputerPlayer, SmartComputerPlayer, HumanPlayer, get_randomized_players, get_smart_players
import sys
import os
sys.path.append(os.path.abspath(r"../SMR-Demobot_V2/"))
from Promobot_class import Kawasaki_1, Robot_Hand
import time

# Store the game state globally for simplicity
current_game = None
x_player = None
o_player = None
x_tile_count = 5
o_tile_count = 5
current_letter = 'X'
robot_is_moving = False

# Define positions for above each square (in mm), adjust for your board's physical setup
# x+ move to the left
# x- move to the right
# y+ move back to the big television
# y- move forward to the small television
# z+ move up, awai from the table
# z- move down to the table 
square_positions = {
	0: (490,  39, -70, -151, 180, -151),  # Top-left
	1: (490, 148, -70, -151, 180, -151),  # Top-center
	2: (490, 261, -70, -151, 180, -151),  # Top-right
	3: (380,  39, -70, -151, 180, -151),  # Middle-left
	4: (380, 148, -70, -151, 180, -151),  # Center
	5: (380, 261, -70, -151, 180, -151),  # Middle-right
	6: (270,  39, -70, -151, 180, -151),  # Bottom-left
	7: (270, 148, -70, -151, 180, -151),  # Bottom-center
	8: (270, 261, -70, -151, 180, -151),  # Bottom-right
	9: (380, 148,   0, -151, 180, -151),  # safe position
	10:(326, -81, -22, -151, 180, -151),  # X storage box
	11:(431, -81, -22, -151, 180, -151),  # O storage box
}


def robot_moves(square, player):
	"""
	:param square: Integer (0-9) specifying the square on the Tic Tac Toe board.
	:param player: String ('X' or 'O') specifying the current player.
	"""
	global robot_is_moving, x_tile_count, o_tile_count
	while robot_is_moving == True:
		time.sleep(.01) 
	robot_is_moving = True
	
	magnetcontroller = Robot_Hand()

	k1 = Kawasaki_1()
	k1.SPEED(20)
	k1.TOOL(0, 0, 30, 0, 0, 0)               #X, Z, Y because Z is the same direction as the tool, so it changed from straight up position
	
	# Positions for placing tiles on the square (slightly lower than "above" positions)
		key: (x, y, z + 70, rx, ry, rz) for key, (x, y, z, rx, ry, rz) in square_positions.items()
	}

	print(f"Moving a {player} to the {square} position")

	# 1. Move to the safe position
	#print(f"Moving to safe position: {square_positions[9]}")
	k1.JMOVE_TRANS(*square_positions[9])

	# 2. Move to the appropriate storage box (X or O)
	if player == 'X':
		if x_tile_count <= 0:
			print("no tiles left")
			robot_is_moving = False
			return
		z_offset = 30 * (10 - x_tile_count) #TODO change the 70 into appropiate value
		x_box = square_positions[10]
		#print(f"Moving to X box: {square_positions [10]}")
		k1.JMOVE_TRANS(*above_square_positions[10])
    
		k1.JMOVE_TRANS(x_box[0], x_box[1], x_box[2] - z_offset, *x_box[3:])
		# turn on the magnet #TODO
    
		k1.JMOVE_TRANS(*above_square_positions[10])
		#print("Picking up an X tile.")
		x_tile_count -= 1 
	elif player == 'O':
		if o_tile_count <= 0:
			print("no tiles left")
			robot_is_moving = False
			return
		z_offset = 30 * (10 - o_tile_count) #TODO change the 70 into appropiate value
		o_box = square_positions[11]
		#print(f"Moving to O box: {square_positions [11]}")
		k1.JMOVE_TRANS(*above_square_positions[11])
    
		k1.JMOVE_TRANS(o_box[0], o_box[1], o_box[2] - z_offset, *o_box[3:])
		# turn on the magnet #TODO

		magnetcontroller.magnet_ON()

		k1.JMOVE_TRANS(*above_square_positions[11])
		#print("Picking up an O tile.")
		o_tile_count -= 1

	# 3. Move to the square's "above" position
	#print(f"Moving above square {square}: {above_square_positions[square]}")
	k1.JMOVE_TRANS(*above_square_positions[square])

	# 4. Move to the square's position to place the tile
	#print(f"Placing tile on square {square}: {square_positions[square]}")
	k1.JMOVE_TRANS(*square_positions[square])

	# magnet off
	magnetcontroller.magnet_OFF()

	# 5. Return to the safe position
	#print(f"Returning to safe position: {square_positions[9]}")
	k1.JMOVE_TRANS(*square_positions[9])
	
	time.sleep(1.5)  # Adjust based on your robot's speed and movements #TODO
	
	robot_is_moving = False

def clean_up_board(previous_board):
	global robot_is_moving, x_tile_count, o_tile_count
	while robot_is_moving == True:
		time.sleep(.01)
	robot_is_moving = True

	magnetcontroller = Robot_Hand()

	k1 = Kawasaki_1()
	k1.SPEED(20)
	k1.TOOL(0, 0, 30, 0, 0, 0)                                                 #X, Z, Y because Z is the same direction as the tool, so it changed from straight up position

	for square,tile in enumerate (previous_board):
		if tile != ' ':  # Check if there's a tile in the square
			print(f"Robot is moving to square {square} to pick up tile '{tile}' and return it to the box.")
			
			# Positions for the square itself
			above_square_positions = {
				key: (x, y, z + 70, o, a, t) for key, (x, y, z, o, a, t) in square_positions.items()
			}

			# Move to the safe position
			#print(f"Moving to safe position: {square_positions[9]}")
			k1.JMOVE_TRANS(*square_positions[9])

			# Move above the square
			#print(f"Moving above square {square}: {above_square_positions[square]}")
			k1.JMOVE_TRANS(*above_square_positions[square])

			# Move to the square to pick up the tile
			#print(f"Picking up tile '{tile}' from square {square}: {square_positions[square]}")
			k1.JMOVE_TRANS(*square_positions[square])

			# Close the gripper to pick up the tile
			magnetcontroller.magnet_ON()

			# Return to the safe position
			k1.JMOVE_TRANS(*square_positions[9])

			# Move to the appropriate storage box
			if tile == 'X':
				print(f"returning to X box: {square_positions [10]}")
				z_offset = 30 * (5 - x_tile_count) #TODO adjust the height
				x_box = square_positions[10]
				k1.JMOVE_TRANS(*above_square_positions[10])
				k1.JMOVE_TRANS(x_box[0],x_box[1],x_box[2] - z_offset, *x_box[3:])
				magnetcontroller.magnet_OFF()

				k1.JMOVE_TRANS(*above_square_positions[10])
				x_tile_count += 1
			elif tile == 'O':
				print(f"returning to O box: {square_positions [11]}")
				z_offset = 30 * (5 - o_tile_count) #TODO adjust the height
				o_box = square_positions[11]
				k1.JMOVE_TRANS(*above_square_positions[11])
				k1.JMOVE_TRANS(o_box[0],o_box[1],o_box[2] - z_offset, *o_box[3:])
				magnetcontroller.magnet_OFF()
				k1.JMOVE_TRANS(*above_square_positions[11])

			# Return to the safe position
			k1.JMOVE_TRANS(*square_positions[9])

	time.sleep(1.5)  # Adjust based on your robot's speed and movements #TODO
	robot_is_moving = False

def reset_game(level=0):
	print("Game restarted")
	global current_game, x_player, o_player, current_letter
	# Start a new game
	current_game = TicTacToe()
	match level:
		case 0:
			x_player, o_player = get_randomized_players()
		case _:
			x_player, o_player = get_smart_players()
	current_letter = 'X'

def start_game():
	print("start Game")
	global current_game, x_player, o_player, current_letter
	# If the computer is the first player, make its move immediately
	if isinstance(x_player, RandomComputerPlayer) or isinstance(x_player, SmartComputerPlayer):
		move = x_player.get_move(current_game)
		current_game.make_move(move, current_letter)
		robot_moves(move, current_letter)
		time.sleep(2) # for testing without a robot arm
		current_letter = 'O'  # Switch to human's turn

def tictactoe_index():
	return render_template('Tic_tac_toe_index1.html')  # Render the frontend

def make_move(type):
	global current_game, x_player, o_player, current_letter
	
	# Get the move based on the current player
	if current_letter == 'X':
		if type == "make":
			move = request.json.get('square')
			#print(f"Player 'X' makes a move to square {move}.")
		elif type == "get":
			move = x_player.get_move(current_game)
			#print(f"Player 'X' (computer) makes a move to square {move}.")
	else:
		if type == "make":
			move = request.json.get('square')
			#print(f"Player 'O' makes a move to square {move}.")
		elif type == "get":
			move = o_player.get_move(current_game)
			#print(f"Player 'O' (computer) makes a move to square {move}.")
	
	# # Trigger the robot to pick up and place the tile
	robot_moves(move, current_letter)
	#time.sleep(2) # for testing without a robot arm

	# Make the move and check for winner
	
	current_game.make_move(move, current_letter)
	winner = current_game.current_winner

	# Prepare the response
	response = {
		'move': move,
		'board': current_game.board,
		'winner': winner,
		'is_tie': not current_game.empty_squares() and not winner,
		'current_letter' : current_letter
	}

	# Switch the turn
	current_letter = 'O' if current_letter == 'X' else 'X'

	return jsonify(response)

def restart(mode):
	global current_game, x_player, o_player, current_letter
	
	# Save the current board state before resetting
	previous_board = current_game.board.copy()

	if mode == "EASY":
		reset_game(0)
	else:
		reset_game(69)

	clean_up_board(previous_board)
	
	start_game()

	return jsonify({
		'board': current_game.board, 
		'current_letter': current_letter,
		'x_player' : 'Computer' if not isinstance(x_player, HumanPlayer) else 'Human',
		'o_player' : 'Computer' if not isinstance(o_player, HumanPlayer) else 'Human'
		})

def cleanup():
	global current_game
	
	# Save the current board state before resetting
	previous_board = current_game.board.copy()

	clean_up_board(previous_board)
	reset_game(0)

	return jsonify({
		'board':'cleanup'
		})
	

reset_game(0)