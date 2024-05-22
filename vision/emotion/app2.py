import cv2
from fer import FER
import os
import logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # This hides informational and warning messages
logging.getLogger('tensorflow').setLevel(logging.FATAL)  # Set TensorFlow logging to only log fatal errors

# Using the webcam
cap = cv2.VideoCapture(0)
detector = FER(mtcnn=True)

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect emotions
    result = detector.detect_emotions(frame)
    
    for face in result:
        (x, y, w, h) = face["box"]
        emotion = max(face["emotions"], key=face["emotions"].get)
        
        # Adjust the center coordinates to move the circle a bit above
        center_coordinates = (x + w//2, y + h//2 - 10)  # Moves the circle 10 pixels above the center
        # Increase the radius to make the circle a bit larger
        radius = int(w * 1.1)  # 10% larger radius
        
        cv2.circle(frame, center_coordinates, radius, (0, 255, 0), 2)

        # Position the text a bit higher or adjust accordingly
        cv2.putText(frame, emotion, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Display the frame with results
    cv2.imshow('Emotion Detection', frame)
    
    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
