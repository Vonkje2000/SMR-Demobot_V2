import sys
from flask import Flask, render_template
import logging

from Promobot_class import Kawasaki_1, Kawasaki_2, Robot_Hand

k1 = Kawasaki_1(Test_mode=True)
k2 = Kawasaki_2()
RH = Robot_Hand()

sys.path.insert(0, 'AI_voice_chat/')
import Main_AI_new_UI
sys.path.insert(0, 'Joystick/')
import joystick_server
sys.path.insert(0, 'tic-tac-toe/')
import tictactoe
sys.path.insert(0, 'Rockpaperscissor/')
import RockPaperScissorsflask

app = Flask(__name__)
#logging.getLogger('werkzeug').disabled = True
logging.getLogger('werkzeug').disabled = False

@app.route('/')
@app.route('/index.html')
def index():
	return render_template('main.html')

app.add_url_rule('/AI_voice_chat', view_func=Main_AI_new_UI.AI_index, methods=['GET'])
app.add_url_rule('/API', view_func=Main_AI_new_UI.post_api, methods=['POST', 'GET'])

app.add_url_rule('/Maze_game', view_func=joystick_server.joystick_index, methods=['GET'])
app.add_url_rule('/joystick', view_func=joystick_server.joystick, methods=['POST'])

app.add_url_rule('/tictactoe', view_func=tictactoe.tictactoe_index, methods=['GET'])
app.add_url_rule('/tictactoe/move/<type>', view_func=tictactoe.make_move, methods=['POST'])
app.add_url_rule('/tictactoe/restart/<mode>', view_func=tictactoe.restart, methods=['POST'])

app.add_url_rule('/rockpaperscissors', view_func=RockPaperScissorsflask.RPS_index, methods=['GET'])
app.add_url_rule('/rockpaperscissors/start_robot', view_func=RockPaperScissorsflask.start_signal, methods=['POST'])
app.add_url_rule('/rockpaperscissors/get_captured_image', view_func=RockPaperScissorsflask.get_captured_image, methods=['GET'])
app.add_url_rule('/rockpaperscissors/game_result', view_func=RockPaperScissorsflask.get_game_result, methods=['GET'])

def main():
	app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
	#print(" * Running on http://127.0.0.1:5000")
	main()