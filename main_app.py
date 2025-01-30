import sys
from flask import Flask, render_template, jsonify
import logging
import webbrowser
import os
from time import sleep

from Promobot_class import Kawasaki_1, Kawasaki_2, Robot_Hand, Intel_Camera, Internet_detector

k1 = Kawasaki_1(Test_mode=True)
k2 = Kawasaki_2(Test_mode=True)
RH = Robot_Hand(Test_mode=True)		# remove delay for testing in __send
Realsense = Intel_Camera(Test_Mode=True, Demo_Mode=False)
id = Internet_detector()

if(RH.Test_mode == False):
	RH.magnet_OFF()
	RH.rock()
	RH.stop_state()
	sleep(2)

if(k1.Test_mode == False or k2.Test_mode == False):
	k1.SPEED(10)
	k1.LMOVE(60, -32, -121, 180, 66, 90)
	k2.SPEED(20)
	k2.LMOVE(-52, -54, -113, -12, -40, -73)
	sleep(4)

sys.path.insert(0, 'AI_voice_chat/')
import Main_AI_new_UI
sys.path.insert(0, 'Joystick/')
import joystick_server
sys.path.insert(0, 'tic-tac-toe/')
import tictactoe
sys.path.insert(0, 'Rockpaperscissor/')
import RockPaperScissorsflask
sys.path.insert(0, 'vision/')
import vision_filtered

import util_class

app = Flask(__name__)
#logging.getLogger('werkzeug').disabled = True
logging.getLogger('werkzeug').disabled = False


@app.route('/internet_status', methods=['GET'])
def internet_status():
    """API endpoint to check internet status."""
    is_connected = id.status()
    return jsonify({"connected": is_connected})


@app.route('/')
@app.route('/index.html')
@app.route('/index')
def index():
	return render_template('main.html')

@app.errorhandler(404)
def page_not_found(e):
	print("probably you forgot to add the video from video/promobot/ to the static/videos/")
	return "<h1>404 Page not found</h1>", 404

app.add_url_rule('/AI_voice_chat', view_func=Main_AI_new_UI.AI_index, methods=['GET'])
app.add_url_rule('/API', view_func=Main_AI_new_UI.post_api, methods=['POST', 'GET'])

app.add_url_rule('/Maze_game', view_func=joystick_server.joystick_index, methods=['GET'])
app.add_url_rule('/joystick', view_func=joystick_server.joystick, methods=['POST'])
app.add_url_rule('/Maze_game/cleanup', view_func=joystick_server.maze_cleanup, methods=['POST'])
app.add_url_rule('/Maze_game/reset', view_func=joystick_server.maze_reset, methods=['POST'])

app.add_url_rule('/tictactoe', view_func=tictactoe.tictactoe_index, methods=['GET'])
app.add_url_rule('/tictactoe/move/<type>', view_func=tictactoe.make_move, methods=['POST'])
app.add_url_rule('/tictactoe/restart/<mode>', view_func=tictactoe.restart, methods=['POST'])
app.add_url_rule('/tictactoe/cleanup', view_func=tictactoe.cleanup, methods=['GET'])

app.add_url_rule('/rockpaperscissors', view_func=RockPaperScissorsflask.RPS_index, methods=['GET'])
app.add_url_rule('/rockpaperscissors/start_robot', view_func=RockPaperScissorsflask.start_signal, methods=['POST'])
app.add_url_rule('/rockpaperscissors/get_captured_image', view_func=RockPaperScissorsflask.get_captured_image, methods=['GET'])
app.add_url_rule('/rockpaperscissors/game_result', view_func=RockPaperScissorsflask.get_game_result, methods=['GET'])
app.add_url_rule('/rockpaperscissors/state', view_func=RockPaperScissorsflask.GET_RPS_state, methods=['GET'])

app.add_url_rule('/Machine_vision', view_func=vision_filtered.vision_index, methods=['GET'])
app.add_url_rule('/Machine_vision/video_feed/<filter_id>', view_func=vision_filtered.video_feed, methods=['GET'])

app.add_url_rule('/util/webpage', view_func=util_class.util_page, methods=['GET'])
app.add_url_rule('/util/webcam', view_func=util_class.util_video_feed, methods=['GET'])

def main():
	app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
	#print(" * Running on http://127.0.0.1:5000")
	webbrowser.WindowsDefault().open(url="http://127.0.0.1:5000")		# easier to use
	#os.popen("\"C:/Program Files/Mozilla Firefox/firefox.exe\" --kiosk --private-window \"http://127.0.0.1:5000\"")		#looks better
	#os.popen("\"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe\" --app=\"http://127.0.0.1:5000\"")		#looks better after pressing F11
	main()