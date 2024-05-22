from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO, emit
import threading
import socket
import vision.main as vision
import voice_manager
import json
from fer import FER
import os
import logging

app = Flask(__name__)
socketio = SocketIO(app)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'  # This hides informational and warning messages
logging.getLogger('tensorflow').setLevel(logging.FATAL)  # Set TensorFlow logging to only log fatal errors

ROBOT_IP = '192.168.0.1'  # Replace with your robot's IP address
ROBOT_PORT = 10010  # Replace with the port your robot is listening on

def send_message(message):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            # Send message to the robot
            sock.sendto(message.encode(), (ROBOT_IP, ROBOT_PORT))
            print(f"Message '{message}' sent to robot")
        except Exception as e:
            print(f"Error sending message to robot: {e}")

def getAudioPath(fileName):
    return 'static/audio/' + fileName + '.wav'

def responseSocket(message):
    socketio.emit('response', message)

@socketio.on('message')
def handle_message(data):
    data = json.loads(data)
    print(['received message: ', data])
    if data['type'] == 'voice':
        voice_manager.play_sound(getAudioPath(data['message']))
    elif data['type'] == 'robot':
        if data['message'] == 'dancing_started':
            send_message('1')
            voice_manager.play_sound(getAudioPath(data['message']))
        elif data['message'] == 'game_started':
            send_message('2')
    responseSocket(data)

@app.route('/')
def index():
    return render_template('index.html')

models = {}

def load_models_async():
    global models
    models['objects_detection'] = vision.YOLO('vision/model-detect.pt')
    models['pose_detection'] = vision.YOLO('vision/model-pose.pt')
    models['emotion_detection'] = FER(mtcnn=True)
    print("All models loaded")

# Start model loading in a separate thread after the server starts
threading.Thread(target=load_models_async).start()

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
    app.run(debug=True)
