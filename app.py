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

HOST_IP   = '192.168.0.10'
ROBOT1_IP = '192.168.0.1'  # Replace with your robot's IP address
ROBOT2_IP = '192.168.0.2'  # Replace with your robot's IP address

ROBOT_PORT = 10010  # Replace with the port your robot is listening on

def send_message(robot_ip: str, message):
    # This function implements basic UDP secure communication, with response and acknowledgment
    # Error/Confirmation codes to send to the robot
    CONFIRMED_RECOVERY = "1000"
    ERROR_RECOVERY = "4000"
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST_IP, ROBOT_PORT))
        message_confirmed = False
        while not message_confirmed:
            try:
                # Send message to the first robot
                try:  
                    server_socket.sendto(message.encode(), (robot_ip, ROBOT_PORT))
                    print(f"Message '{message}' sent to robot at {robot_ip}")
                except: 
                    print(f"Error sending message to robot: {robot_ip}") 

                # Wait for confirmation messages from both robots
                ready = select.select([server_socket], [], [], 5) # 5 second timeout
                if ready[0]:
                    data, addr = server_socket.recvfrom(1024)
                    if addr[0] == robot_ip:
                        print(f"Received confirmation from robot at {robot_ip}: {data.decode()}")
                        if (data.decode() == message):
                            try: 
                                time.sleep(3) 
                                server_socket.sendto(CONFIRMED_RECOVERY.encode(), (robot_ip, ROBOT_PORT))
                                print(f"Confirmation code '{CONFIRMED_RECOVERY}' sent to robot at {robot_ip}")
                                # This is the only way to end the loop
                                message_confirmed = True
                            except: 
                                print(f"Error sending confirmation code to robot: {robot_ip}")

                        else:
                            try:  
                                time.sleep(3)
                                server_socket.sendto(ERROR_RECOVERY.encode(), (robot_ip, ROBOT_PORT))
                                print(f"Error code '{ERROR_RECOVERY}' sent to robot at {robot_ip}")
                            except: 
                                print(f"Error sending error code to robot: {robot_ip}")
                    else:
                        print(f"Received message from unknown address {addr[0]}: {data.decode()}")
            except Exception as e:
                print(f"Error sending message to robot: {e}. Trying again")

        # Close the socket (never reached in this example)
        server_socket.close()
            


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
