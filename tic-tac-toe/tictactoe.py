from flask import request, jsonify, render_template
from game import TicTacToe, RandomComputerPlayer, SmartComputerPlayer, HumanPlayer, get_randomized_players, get_smart_players
import sys
import os
sys.path.append(os.path.abspath(r"../SMR-Demobot_V2/"))
from Promobot_class import Kawasaki_1, Robot_Hand
from time import sleep

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
# y- move back to the big television
# y+ move forward to the small television
# z+ move up, awai from the table
# z- move down to the table 
square_positions = {
	0: (484,    41, -98, -154, 180, -154),  # Top-left
	1: (374,    42, -98, -155, 180, -155),  # Top-center
	2: (264,    43, -98, -160, 180, -160),  # Top-right
	3: (485,   150, -98, -151, 180, -151),  # Middle-left
	4: (375,   151, -98, -165, 180, -165),  # Center
	5: (265,   153, -98, -166, 180, -166),  # Middle-right
	6: (486,   259, -98, -151, 180, -151),  # Bottom-left
	7: (376,   262, -98, -156, 180, -156),  # Bottom-center
	8: (268,   263, -98, -151, 180, -151),  # Bottom-right
	9: (380,   148,   0, -151, 180, -151),  # safe position
	10:(321,   -81, -55, -151, 180, -151),  # X storage box
	11:(424, -81.5, -51, -151, 180, -151),  # O storage box
}


def robot_moves(square, player):
	"""
	:param square: Integer (0-9) specifying the square on the Tic Tac Toe board.
	:param player: String ('X' or 'O') specifying the current player.
	"""
	global robot_is_moving, x_tile_count, o_tile_count
	while robot_is_moving == True:
		sleep(.01) 
	robot_is_moving = True
	
	magnetcontroller = Robot_Hand()
	magnetcontroller.magnet_OFF()

	k1 = Kawasaki_1()
	k1.SPEED(20)
	k1.TOOL(0, 0, 30, 0, 0, 0)               #X, Z, Y because Z is the same direction as the tool, so it changed from straight up position
	
	# Positions for placing tiles on the square (slightly lower than "above" positions)
	above_square_positions = {
		key: (x, y, z + 70, rx, ry, rz) for key, (x, y, z, rx, ry, rz) in square_positions.items()
	} #TODO give an appropiate value as an offset above the square

	# aside square position
	aside_square_positions = {
		key: (x - 10, y + 10, z , rx, ry, rz) for key, (x, y, z, rx, ry, rz) in square_positions.items()
	}

	print(f"Moving a {player} to the {square} position")

	# 1. Move to the safe position
	k1.JMOVE_TRANS(*square_positions[9])

	# 2. Move to the appropriate storage box (X or O)
	if player == 'X':
		if x_tile_count <= 0:
			print("no tiles left")
			robot_is_moving = False
			return
		z_offset = 7 * (5 - x_tile_count)
		x_box = square_positions[10]

		k1.JMOVE_TRANS(*above_square_positions[10])
		k1.SPEED(1)
		k1.LMOVE_TRANS(x_box[0], x_box[1], x_box[2] - z_offset, *x_box[3:])
		sleep(2)
		magnetcontroller.magnet_ON()
		sleep(4)
		k1.LMOVE_TRANS(*above_square_positions[10])
		x_tile_count -= 1 
	elif player == 'O':
		if o_tile_count <= 0:
			print("no tiles left")
			robot_is_moving = False
			return
		z_offset = 7 * (5 - o_tile_count)
		o_box = square_positions[11]
		
		k1.JMOVE_TRANS(*above_square_positions[11])
		k1.LMOVE_TRANS(o_box[0], o_box[1], o_box[2] - z_offset, *o_box[3:])
		sleep(2)
		magnetcontroller.magnet_ON()
		sleep(4)
		k1.LMOVE_TRANS(*above_square_positions[11])
		o_tile_count -= 1

	# 3. Move to the square's "above" position
	k1.SPEED(20)
	k1.JMOVE_TRANS(*above_square_positions[square])

	# 4. Move to the square's position to place the tile
	k1.SPEED(1)
	k1.LMOVE_TRANS(*square_positions[square])
	sleep(4)

	magnetcontroller.magnet_OFF()
	sleep(2)
	k1.LMOVE_TRANS(*aside_square_positions[square])

	k1.SPEED(20)
	k1.LMOVE_TRANS(*above_square_positions[square])

	# 5. Return to the safe position
	k1.JMOVE_TRANS(*square_positions[9])
	
	sleep(0.5)  # Adjust based on your robot's speed and movements #TODO
	
	robot_is_moving = False

def clean_up_board(previous_board):
	global robot_is_moving, x_tile_count, o_tile_count
	#board is empty do not start the connection with robot and arduino to save time
	if(previous_board == [' ',' ',' ',' ',' ',' ',' ',' ',' ']):
		#print("board clear")
		return

	while robot_is_moving == True:
		sleep(.01)
	robot_is_moving = True

	magnetcontroller = Robot_Hand()
	magnetcontroller.magnet_OFF()

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
			# aside square position
			aside_square_positions = {
				key: (x - 10, y - 10, z , rx, ry, rz) for key, (x, y, z, rx, ry, rz) in square_positions.items()
			}

			# Move to the safe position
			k1.SPEED(20)
			k1.JMOVE_TRANS(*square_positions[9])

			# Move above the square
			k1.JMOVE_TRANS(*above_square_positions[square])

			# Move to the square to pick up the tile
			k1.SPEED(1)
			k1.LMOVE_TRANS(*square_positions[square])
			sleep(4)
			magnetcontroller.magnet_ON()
			sleep(2)

			# Return to the safe position
			k1.LMOVE_TRANS(*square_positions[9])
			k1.SPEED(20)

			# Move to the appropriate storage box
			if tile == 'X':
				z_offset = 7 * (4 - x_tile_count)
				x_box = square_positions[10]
				x_box_down = x_box[0],x_box[1],x_box[2] - z_offset, *x_box[3:]

				k1.JMOVE_TRANS(*above_square_positions[10])
				k1.SPEED(1)
				k1.LMOVE_TRANS(*x_box_down)
				sleep(4)
				magnetcontroller.magnet_OFF()
				sleep(2)
				k1.LMOVE_TRANS(x_box_down[0] - 10,x_box_down[1] - 10,*x_box[2:])
				k1.LMOVE_TRANS(*above_square_positions[10])
				x_tile_count += 1
			elif tile == 'O':
				z_offset = 7 * (4 - o_tile_count)
				o_box = square_positions[11]
				o_box_down = o_box[0],o_box[1],o_box[2] - z_offset, *o_box[3:]
				
				k1.JMOVE_TRANS(*above_square_positions[11])
				k1.SPEED(1)
				k1.LMOVE_TRANS(*o_box_down)
				sleep(4)
				magnetcontroller.magnet_OFF()
				sleep(2)
				k1.LMOVE_TRANS(o_box_down[0] - 10,o_box_down[1] - 10,*o_box[2:])
				k1.LMOVE_TRANS(*above_square_positions[11])
			
			k1.SPEED(20)

			# Return to the safe position
			k1.JMOVE_TRANS(*square_positions[9])

	sleep(1.5)
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
		sleep(2) # for testing without a robot arm
		current_letter = 'O'  # Switch to human's turn

One_time_flag = False	# TODO TEST THIS
def tictactoe_index():
	global One_time_flag
	if (One_time_flag == False):
		One_time_flag = True
		reset_game(0)
		
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
	#sleep(2) # for testing without a robot arm

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

	return jsonify({'board':'cleanup'})
	

#reset_game(0)	#TODO IF TEST THIS WORKS REMOVE