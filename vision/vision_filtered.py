from flask import Flask, render_template, Response
import cv2
from flask_socketio import SocketIO
from ultralytics import YOLO
import sys
import os
sys.path.append(os.path.abspath(r"../SMR-Demobot_V2/"))
from Promobot_class import Intel_Camera
Realsense = Intel_Camera()

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

#load the models
model = YOLO('yolov8n.pt', verbose=False)

# Load the Haar cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_people(frame):
   # Run YOLO inference
    results = model.predict(frame, conf=0.4, save=False, show=False, verbose=False)

    # Draw bounding boxes for detected people
    for result in results[0].boxes:
        if result.cls == 0:  # Class 0 = 'person'
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame

# not in use function
def detect_non_people_objects(frame):
    # Run YOLO inference
    results = model.predict(frame, conf=0.4, save=False, show=False, verbose=False)

    # Draw bounding boxes for non-person objects
    for result in results[0].boxes:
        if result.cls != 0:  # Skip 'person' class (ID 0)
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    
    return frame

# def blur_faces(frame):
#     # Convert the frame to grayscale for Haar Cascade
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
#     for (x, y, w, h) in faces:
#         # Extract the face region
#         face_region = frame[y:y+h, x:x+w]
#         # Apply Gaussian blur to the face region
#         blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
#         # Replace the original face region with the blurred one
#         frame[y:y+h, x:x+w] = blurred_face

#     return frame

def apply_cartoon(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(frame, 9, 300, 300)
    return cv2.bitwise_and(color, color, mask=edges)

def apply_edges(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 100, 200)

def apply_solarize(frame, threshold=128):
    frame[frame > threshold] = 255 - frame[frame > threshold]
    return frame

#TODO Replace the 1-5 for the names of the filters so that every body can understand what each filter does
def apply_filter(filter_id, frame):
    # Apply the selected filter
    if filter_id == 1:  # People detection
        return detect_people(frame)
    # elif filter_id == 2:  # Face blur
    #     return blur_faces(frame)
    elif filter_id == 3:  # grayscale
         return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_id == 4:  # non people detection
        return apply_solarize(frame)
    elif filter_id == 5:  # cartoonized
        return apply_cartoon(frame)
    else:  # outline
        return apply_edges(frame)

#TODO THIS IS A MEMORY LEAK IT NEVER STOPS TAKING PICTURES
#IT ALSO STARTS MY FANS INSTANTLY
def generate_frames(filter_id):
    while True:
        frame = Realsense.read()
        frame = apply_filter(filter_id, frame)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def vision_index():
    return render_template('vision_index.html')

def video_feed(filter_id):
    return Response(generate_frames(filter_id), mimetype='multipart/x-mixed-replace; boundary=frame')
