from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO, emit
import threading
import socket
import select
import vision.main as vision
import voice_manager
import json
from fer import FER
import os
import logging
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'  # This hides informational and warning messages
logging.getLogger('tensorflow').setLevel(logging.FATAL)  # Set TensorFlow logging to only log fatal errors

ROBOT1_IP = '192.168.0.1'  # Replace with your robot's IP address
ROBOT2_IP = '192.168.0.2'  # Replace with your robot's IP address

ROBOT_PORT = 10010  # Replace with the port your robot is listening on

def send_message(message):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        try:
            # Send message to the first robot
            try:  
                server_socket.sendto(message.encode(), (ROBOT1_IP, ROBOT_PORT))
                print(f"Message '{message}' sent to robot at {ROBOT1_IP}")
            except: 
                print(f"Error sending message to robot: 1") 
            
            try:  
                server_socket.sendto(message.encode(), (ROBOT2_IP, ROBOT_PORT))
                print(f"Message '{message}' sent to robot at {ROBOT2_IP}")
            except: 
                print(f"Error sending message to robot: 2") 

            # Wait for confirmation messages from both robots
            ready = select.select([server_socket], [], [], 5)
            if ready[0]:
                while True:
                    data, addr = server_socket.recvfrom(1024)
                    if addr[0] == ROBOT1_IP:
                        print(f"Received confirmation from robot at {ROBOT1_IP}: {data.decode()}")
                    elif addr[0] == ROBOT2_IP:
                        print(f"Received confirmation from robot at {ROBOT2_IP}: {data.decode()}")
                    else:
                        print(f"Received message from unknown address {addr[0]}: {data.decode()}")
        except Exception as e:
            print(f"Error sending message to robot: {e}")

def play_rock_paper_scissors():
    options = ["Rock", "Paper", "Scissors"]
    computer_choice = random.choice(options)
    return computer_choice

def getAudioPath(fileName):
    return 'static/audio/' + fileName + '.wav'

def responseSocket(message):
    socketio.emit('response', message)

@socketio.on('message')
def handle_message(data):
    data = json.loads(data)
    print(['received message: ', data])
    if data['type'] == 'game':
        send_message('2')
        data['robotchoise'] = play_rock_paper_scissors()
    elif data['type'] == 'robot':
        if data['message'] == 'tvMode':
            send_message('0')   
        elif data['message'] == 'dancingMode':
            send_message('1')
            voice_manager.play_sound(getAudioPath(data['message']))
  
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
threading.Thread(target=load_models_async, daemon=True).start()

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
