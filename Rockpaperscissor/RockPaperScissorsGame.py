from flask import Flask, render_template, jsonify, send_file, request
import threading
import sys
import cv2
import random
import time
import keyboard  # Install this package using `pip install keyboard`
from ultralytics import YOLO
sys.path.insert(0, '/Users/basti/Documents/GitHub/SMR-Demobot_V2')
from Promobot_class import Kawasaki_2, Robot_Hand

# Initialize robot and hand
k2 = Kawasaki_2()
Hand = Robot_Hand("COM9")
k2.SPEED(50)
k2.TOOL(0, 0, 40, 0, 0, 0)

# Initialize camera
camera = cv2.VideoCapture(1)  # Change the index if another camera is used
model = YOLO('Rockpaperscissor/best.pt', verbose=False)

# Global variable to indicate if the program should continue running
running = True

def live_feed():
    """Continuously display the live feed from the camera."""
    while running:
        ret, frame = camera.read()
        if ret:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            # cv2.imshow("Live Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit the live feed
                break
    camera.release()
    cv2.destroyAllWindows()
    
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

    # Check if robot wins
    if winning_conditions.get(robot_gesture) == detected_gesture:
        return "robot"
    return "user"

def capture_result_image():
    """Capture up to 5 frames and detect gestures using YOLO."""
    detected_gesture = None
    print("Starting gesture detection...")  # Debug statement
    if cv2.getWindowProperty("Detection Result", cv2.WND_PROP_VISIBLE) == 1:
        cv2.destroyWindow("Detection Result")  # Close the window after detection

    for attempt in range(5):  # Try for a maximum of 5 frames
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame.")  # Debug statement
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
                if conf > 0.5:  # Minimum confidence threshold
                    print(f"Detected gesture: {label} with confidence {conf:.2f}")
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    detected_gesture = label
                    # cv2.imwrite(f"detected_frame.jpg", frame)
                    cv2.imshow("Detection Result", frame)
                    cv2.waitKey(1)  # Update the detection result window
                 
        if detected_gesture:
            break
        time.sleep(0.5)  # Small delay before trying again

    if not detected_gesture:
        print("No gesture detected after multiple attempts.")  # Debug statement
    return detected_gesture


def start_move():
    """Perform the robot and hand movements and determine the game result."""
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
        print("No gesture detected from user.") 


if __name__ == "__main__":
    # Start the live feed in a separate thread
    feed_thread = threading.Thread(target=live_feed, daemon=True)
    feed_thread.start()
    print("Live feed started.")

    print("Press SPACEBAR to start the robot movements. Press 'q' to quit.")
    try:
        while True:
            # Wait for the spacebar press
            if keyboard.is_pressed("space"):
                print("Spacebar pressed. Starting move...")
                start_move()
                print("Press SPACEBAR again to start another move, or CTRL+C to exit.")
                time.sleep(1)  # Prevent immediate re-trigger
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        running = False  # Stop the live feed thread
        feed_thread.join()  # Wait for the thread to finish
        print("Program terminated.")
