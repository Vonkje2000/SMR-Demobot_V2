import cv2
from deepface import DeepFace
import numpy as np
import pyrealsense2 as rs

COLOR_CAMERA_RESOLUTION = (640, 480)

# Try initializing RealSense camera
try:
    # Connect to the camera
    pipe = rs.pipeline()

    # Configure streams
    config = rs.config()
    config.enable_stream(rs.stream.color, *COLOR_CAMERA_RESOLUTION, rs.format.bgr8, 60)

    # Start camera stream
    pipe.start(config)

    using_realSense = True

except Exception as e:
    print("RealSense camera not available. Using webcam instead.")
    using_realSense = False

    # Start capturing video from webcam
    cap = cv2.VideoCapture(0)

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    if using_realSense:
        # Wait for a frame from RealSense camera
        frames = pipe.wait_for_frames()
        frame = frames.get_color_frame()
        frame = np.asanyarray(frame.get_data())
    else:
        # Read frame from webcam
        ret, frame = cap.read()

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert grayscale frame to RGB format
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=10, minSize=(35, 35))

    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = rgb_frame[y:y + h, x:x + w]

        # Perform emotion analysis on the face ROI
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

        # Determine the dominant emotion
        emotion = result[0]['dominant_emotion']

        # Draw rectangle around face and label with predicted emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Real-time Emotion Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
if using_realSense:
    pipe.stop()
else:
    cap.release()

cv2.destroyAllWindows()

