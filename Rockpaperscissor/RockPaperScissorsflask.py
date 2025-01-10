from flask import render_template, jsonify, send_file, request
import threading
import sys
import cv2
import random
import time
from ultralytics import YOLO
sys.path.insert(0, '/Users/basti/Documents/GitHub/SMR-Demobot_V2')
from Promobot_class import Kawasaki_2, Robot_Hand

# Variabelen en initiële setup (camera, model, robot, etc.)
camera = cv2.VideoCapture(2)  # Camera instellen
model = YOLO('Rockpaperscissor/best.pt', verbose=False)
running = True

# Resultaten en foto variabelen
captured_image_path = None
winner = "none"

def capture_result_image():
    """Capture up to 5 frames and detect gestures using YOLO."""
    global captured_image_path
    detected_gesture = None
    print("Starting gesture detection...")
    if cv2.getWindowProperty("Detection Result", cv2.WND_PROP_VISIBLE) == 1:
        cv2.destroyWindow("Detection Result")

    for attempt in range(5):
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame.")
            continue
        
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        # Perform YOLO detection
        results = model.predict(frame, conf=0.4, save=False, show=False)

        # Process results
        for result in results:
            for box in result.boxes:
                conf = box.conf[0]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = model.names[int(box.cls[0])]
                if conf > 0.5:
                    detected_gesture = label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    captured_image_path = "Rockpaperscissor/image.jpg"  # Pas dit pad aan
                    cv2.imwrite(captured_image_path, frame)  # Bewaar de afbeelding
                    cv2.imshow("Detection Result", frame)
                    cv2.waitKey(1)
        
        if detected_gesture:
            break
        time.sleep(0.5)

    if not detected_gesture:
        print("No gesture detected after multiple attempts.")
    return detected_gesture

def determine_winner(robot_gesture:str, detected_gesture:str) -> str:
    """Determine the winner based on robot's and user's gestures."""
    robot_gesture = robot_gesture.lower()
    detected_gesture = detected_gesture.lower()
    if robot_gesture == detected_gesture:
        return "draw"
    
    winning_conditions = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock",
    }
    
    if winning_conditions.get(robot_gesture) == detected_gesture:
        return "robot"
    return "user"

def start_move():
    """Perform the robot and hand movements and determine the game result."""
    # Initialize robot and hand
    k2 = Kawasaki_2()
    Hand = Robot_Hand("COM9")
    k2.SPEED(50)
    k2.TOOL(0, 0, 40, 0, 0, 0)
    Hand.rock()  # Start with a rock gesture
    counter = 0
    while counter < 4:
        k2.LMOVE_TRANS(250, 300, 50, 20, 106, 180)  # X, Y, Z, Base, Shoulder, Elbow
        k2.LMOVE_TRANS(283, 309, 100, 20, 80, 180)
        counter += 1
    time.sleep(0.7)

    # Choose a random hand gesture for the robot
    if random.randint(1, 100) == 1:
        robot_gesture = 'pistol'  # Special case
        gesture = Hand.pistol
    else:
        robot_gesture = random.choice(['rock', 'paper', 'scissors'])
        gesture = getattr(Hand, robot_gesture)

    print(f"Robot performed gesture: {robot_gesture}")
    gesture()

    # Move back to the lowest position
    k2.LMOVE_TRANS(250, 300, 50, 20, 106, 180)

    time.sleep(1)  # Wait for the robot to finish its movements

    # Capture and present the result along with YOLO detection
    detected_gesture = capture_result_image()
    global winner

    if detected_gesture:
        # Determine and print the winner
        winner = determine_winner(robot_gesture, detected_gesture)
        if winner == "draw":
            print(f"Result: It's a draw! Both chose {robot_gesture}.")
        elif winner == "robot":
            print(f"Result: Robot wins! Robot: {robot_gesture}, User: {detected_gesture}.")
        else:
            print(f"Result: You win! Robot: {robot_gesture}, User: {detected_gesture}.")
    else:
        winner = "none"
        print("No gesture detected from user.") 

def start_signal():
    """Start the robot movements when the button is pressed."""
    data = request.get_json()
    print('Start signal received:', data)
    threading.Thread(target=start_move).start()  # Start de robotbeweging in een aparte thread
    return jsonify({"status": "move_started"})

def get_captured_image():
    """Retourneer de afbeelding van de gedetecteerde handeling."""
    image_path = 'Rockpaperscissor\image.jpg'
    return send_file(image_path, mimetype='image/jpg')
    
def get_game_result():
    global winner
    return jsonify({"result": str(winner)})

def RPS_index():
    return render_template('RPS.html')

def live_feed():
    """Live feed van de camera."""
    while running:
        ret, frame = camera.read()
        if ret:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            #cv2.imshow("Live Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    camera.release()
    cv2.destroyAllWindows()

feed_thread = threading.Thread(target=live_feed, daemon=True)
feed_thread.start()
