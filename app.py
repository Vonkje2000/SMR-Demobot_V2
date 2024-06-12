from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import threading
import socket
import vision.main as vision
import json
from fer import FER
import os
import logging
import time
import game
app = Flask(__name__)
socketio = SocketIO(app)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'  # This hides informational and warning messages
logging.getLogger('tensorflow').setLevel(logging.FATAL)  # Set TensorFlow logging to only log fatal errors

ROBOT1_IP = '192.168.0.1'  # Replace with your robot's IP address
ROBOT2_IP = '192.168.0.2'  # Replace with your robot's IP address
ROBOT_PORT_EMERGENCY = 10020
def send_message(message, ROBOT_PORT = 10010):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        try:
            try:  
                server_socket.sendto(message.encode(), (ROBOT1_IP, ROBOT_PORT))
                server_socket.sendto(message.encode(), (ROBOT2_IP, ROBOT_PORT))
                print(f"Message '{message}' sent to robot at {ROBOT1_IP}")
            except: 
                print(f"Error sending message to robots") 
        except Exception as e:
            print(f"Error sending message to robot: {e}")


def get_audio_path(fileName):
    return 'static/audio/' + fileName + '.wav'

def responseSocket(message):
    socketio.emit('response', message)

@socketio.on('message')
def handle_message(data):
    data = json.loads(data)

    def handle_game_mode():
        game.send_command_to_arduino('Rock')
        robotChoice = game.get_rock_paper_scissors_choice()
        time.sleep(0.5)
        send_message('2')
        time.sleep(2.7)
        game.send_command_to_arduino(robotChoice)
        data['robotChoice'] = robotChoice
         
    # print(['received message: ', data])
    if data['message'] == 'heyMode':
            game.send_command_to_arduino('Paper')
            send_message('0')
    if data['message'] == 'danceMode':
            game.send_command_to_arduino('Paper')
            send_message('1')
    elif data['message'] == 'gameMode':
            handle_game_mode()        
    elif data['message'] == 'tvMode':
            game.send_command_to_arduino('Paper')
            send_message('3') 
    elif data['message'] == 'objects_detection':
            send_message('4')     
    elif data['message'] == 'emotion_detection':
            send_message('5')                 
    elif data['message'] == 'pose_detection':
            send_message('6')
    elif data['message'] == 'playPongGame':
            game.send_command_to_arduino('Paper')
            send_message('7')                     
    elif data['message'] == 'startEmergency':
            send_message('hold',ROBOT_PORT_EMERGENCY) 
    elif data['message'] == 'stopEmergency':
            send_message('continue',ROBOT_PORT_EMERGENCY)                   
    responseSocket(data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tv')
def tv():
    return render_template('tv_screen.html')

models = {}

def load_models_async():
    global models
    models['objects_detection'] = vision.YOLO('vision/model-detect.pt')
    models['pose_detection'] = vision.YOLO('vision/model-pose.pt')
    models['emotion_detection'] = FER(mtcnn=True)
    print("All models loaded")

def generate_feed(model_type):
    model = models.get(model_type, None)
    if model is None:
        return "Model not loaded yet", 503
    return Response(vision.gen_frames(model if model_type != 'emotion_detection' else None, model if model_type == 'emotion_detection' else None),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/<model_type>')
def detection_feed(model_type):
    if model_type in ['objects_detection', 'pose_detection', 'emotion_detection']:
        return generate_feed(model_type)
    else:
        return "Invalid model type", 404

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        # Start model loading in a separate thread after the server starts
        threading.Thread(target=load_models_async, daemon=True).start()
    app.run(debug=True) 
 