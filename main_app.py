import sys
from flask import Flask, render_template
import logging
sys.path.insert(0, 'AI_voice_chat/')
import Main_AI_new_UI
sys.path.insert(0, 'Joystick/')
import joystick_server

app = Flask(__name__)
logging.getLogger('werkzeug').disabled = True
#logging.getLogger('werkzeug').disabled = False

@app.route('/')
@app.route('/index.html')
def index():
	return render_template('main.html')

app.add_url_rule('/AI_voice_chat', view_func=Main_AI_new_UI.AI_index, methods=['GET'])
app.add_url_rule('/API', view_func=Main_AI_new_UI.post_api, methods=['POST', 'GET'])

app.add_url_rule('/Maze_game', view_func=joystick_server.joystick_index, methods=['GET'])
app.add_url_rule('/joystick', view_func=joystick_server.joystick, methods=['POST'])

def main():
	app.run(debug=False, use_reloader=True)

if __name__ == "__main__":
	print(" * Running on http://127.0.0.1:5000")
	main()