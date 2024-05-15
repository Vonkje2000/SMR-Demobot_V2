from flask import Flask, render_template, request, jsonify, Response
import threading
import socket
import vision.main as vision
import voice_manager
app = Flask(__name__)

server_socket = None
client_socket = None
server_active = threading.Event()
def start_server(host, port):
    global server_socket, client_socket, server_active
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}")
    server_active.set()
    print(f"Server is listening on {host}:{port}")

    while server_active.is_set():
        try:
            client_socket, addr = server_socket.accept()
            print(f"Connected by {addr}")
        except socket.error as e:
            if server_active.is_set():
                raise  # If the server is supposed to be running, re-raise the error
            else:
                break  # If the server is shutting down, exit the loop


def send_message(message):
    global client_socket
    if client_socket:
        client_socket.sendall(message.encode())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_server', methods=['POST'])
def handle_start_server():
    threading.Thread(target=start_server, args=('192.168.0.2', 10001)).start()
    return jsonify(status="Server started")


@app.route('/stop_server', methods=['POST'])
def handle_stop_server():
    global server_socket, client_socket,server_active
    server_active.clear()
    if client_socket:
        client_socket.close()
        client_socket = None
    if server_socket:
        server_socket.close()
        server_socket = None
    return jsonify(status="Server stopped")


@app.route('/send', methods=['POST'])
def handle_send():
    message = request.json.get('message')
    send_message(message)
    return jsonify(status="Message sent")

@app.route('/voice', methods=['POST'])
def handle_voice():
    message = request.json.get('message')
    # voice_manager.say(message)
    voice_manager.play_sound('static/audio/'+message+'.wav')
    print(message)
    return jsonify(status="Message sent")

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
