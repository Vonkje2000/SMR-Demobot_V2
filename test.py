import cv2
import mediapipe as mp

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5)

# Utility for drawing hand landmarks.
mp_drawing = mp.solutions.drawing_utils

# Function to classify the hand gesture.

def classify_gesture(landmarks, width, height):
    # Simplifying and focusing on essential fingers
    thumb_tip = (landmarks.landmark[4].x * width, landmarks.landmark[4].y * height)
    index_tip = (landmarks.landmark[8].x * width, landmarks.landmark[8].y * height)
    middle_tip = (landmarks.landmark[12].x * width, landmarks.landmark[12].y * height)
    ring_tip = (landmarks.landmark[16].x * width, landmarks.landmark[16].y * height)
    pinky_tip = (landmarks.landmark[20].x * width, landmarks.landmark[20].y * height)
    wrist = (landmarks.landmark[0].x * width, landmarks.landmark[0].y * height)

    # Check finger extension relative to wrist
    extended = [tip[1] < wrist[1] - 0.05 * height for tip in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]]

    # Count extended fingers
    num_extended = sum(extended)

    # Define gestures based on extended fingers
    if num_extended == 0:
        return 'Rock'  # All fingers are curled into a fist
    elif num_extended == 5:
        return 'Paper'  # All fingers are extended
    elif num_extended == 2 and extended[1] and extended[2]:
        return 'Scissors'  # Only index and middle are extended
    else:
        return 'Unknown'  # If gesture does not match any expected configuration

# The rest of your existing code can remain the same.


# Start capturing video from the webcam.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = classify_gesture(hand_landmarks, image_width, image_height)
            cv2.putText(image, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('Rock Paper Scissors Detector', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
