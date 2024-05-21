from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO, emit
import threading
import socket
import time
import vision.main as vision
import voice_manager
import json
app = Flask(__name__)
socketio = SocketIO(app)


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
    return 'static/audio/'+fileName+'.wav'

@socketio.on('message')
def handle_message(data):
    data = json.loads(data)
    print('received message: ')
    print(data)
    if data['type'] == 'voice':
        voice_manager.play_sound(getAudioPath(data['message']))
        # if data['message'] == 'active_system':
        #     threading.Thread(target=start_server, args=('192.168.0.2', 10001)).start()
        # elif data['message'] == 'deactivate_system':
        #     handle_stop_server()

    elif data['type'] == 'robot':
        if data['message'] == 'dancing_started':
            send_message('1')
            voice_manager.play_sound(getAudioPath(data['message']))
        elif data['message'] == 'game_started':    
            send_message('2')
    socketio.emit('response', {"status": "success", "action": "voice", "message": "sound played"})
   
@app.route('/')
def index():
    return render_template('index.html')


objects_detection_model = vision.YOLO('vision/model-detect.pt')
@app.route('/objects_detection')
def objects_detection_feed():
    return Response(vision.gen_frames(objects_detection_model), mimetype='multipart/x-mixed-replace; boundary=frame')

pose_detection_model = vision.YOLO('vision/model-pose.pt')
@app.route('/pose_detection')
def pose_detection_feed():
    return Response(vision.gen_frames(pose_detection_model), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
