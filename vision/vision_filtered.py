from flask import Flask, render_template, Response
import cv2
from flask_socketio import SocketIO
from ultralytics import YOLO

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Initialize webcam
camera = cv2.VideoCapture(0)

#load the models
model = YOLO('yolov8n.pt')

def detect_people(frame):
   # Run YOLO inference
    results = model(frame)

    # Draw bounding boxes for detected people
    for result in results[0].boxes:
        if result.cls == 0:  # Class 0 = 'person'
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            
            # Extract the class index and confidence score
            class_id = int(result.cls)
            confidence = float(result.conf)  # Confidence score
            
            # Get the class label from the model's class names
            label = model.names[class_id]
            text = f"{label} {confidence:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def apply_cartoon(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7,5)
    color = cv2.bilateralFilter(frame, 7, 150, 150)
    return cv2.bitwise_and(color, color, mask=edges)

def apply_edges(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 25, 150)

def apply_thermal(frame):
    # Convert the frame to grayscale to simulate heat intensities
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Normalize the grayscale image to enhance contrast
    normalized_gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    # Invert the grayscale image to reverse the intensity mapping
    inverted_gray = cv2.bitwise_not(normalized_gray)
    # Apply the thermal color map
    thermal_frame = cv2.applyColorMap(inverted_gray, cv2.COLORMAP_JET)
    return thermal_frame

def apply_filter(filter_id, frame):
    # Apply the selected filter
    if filter_id == 1:  # People detection
        return detect_people(frame)
    elif filter_id == 2:  # Face blur
        return apply_edges(frame)
    elif filter_id == 3:  # grayscale
         return apply_thermal(frame)
    elif filter_id == 4:  # non people detection
        return apply_cartoon(frame)
    # elif filter_id == 5:  # cartoonized
    #     return apply_cartoon(frame)
    # else:  # outline
    #     return apply_edges(frame)

def generate_frames(filter_id):
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = apply_filter(filter_id, frame)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('vision_index.html')

@app.route('/video_feed/<int:filter_id>')
def video_feed(filter_id):
    return Response(generate_frames(filter_id), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    socketio.run(app,debug=False, use_reloader=False)
