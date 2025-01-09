from flask import Flask, request, jsonify, render_template
import sys
import cv2
import random
import time
import keyboard  # Install this package using `pip install keyboard`
sys.path.insert(0, '/Users/basti/Documents/GitHub/SMR-Demobot_V2')
from Promobot_class import Kawasaki_2, Robot_Hand

# Initialize robot and hand
k2 = Kawasaki_2()
Hand = Robot_Hand("COM9")
k2.SPEED(50)
k2.TOOL(0, 0, 40, 0, 0, 0)

# Initialize camera
camera = cv2.VideoCapture(1)  # Change the index if another camera is used

def show_video_feed():
    """Display a live video feed from the camera."""
    while True:
        ret, frame = camera.read()  # Capture a single frame
        if ret:
            cv2.imshow("Live Video Feed", frame)  # Show the captured frame in a window
        else:
            print("Failed to capture video.")
            break
        
        # Exit when the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting video feed.")
            break

    cv2.destroyAllWindows()  # Close the OpenCV window

def start_move():
    """Perform the robot and hand movements."""
    Hand.rock()  # Start with a rock gesture
    counter = 0
    while counter < 4:
        k2.LMOVE_TRANS(250, 300, 50, 20, 106, 180)  # X, Y, Z, Base, Shoulder, Elbow
        k2.LMOVE_TRANS(283, 309, 100, 20, 80, 180)
        counter += 1
    time.sleep(0.7)

    # Choose a random hand gesture
    if random.randint(1, 100) == 1:
        robot_gesture = 'pistol'
        gesture = Hand.pistol
    else:
        robot_gesture = random.choice(['paper', 'scissors'])  # Add 'rock' if needed
        gesture = getattr(Hand, robot_gesture)

    print(f"Performing gesture: {robot_gesture}")
    gesture()

    # Move back to the lowest position
    k2.LMOVE_TRANS(250, 300, 50, 20, 106, 180)

    # Display live video feed after movement
    show_video_feed()

if __name__ == "__main__":
    print("Press SPACEBAR to start the robot movements.")
    try:
        while True:
            # Wait for the spacebar press
            if keyboard.is_pressed("space"):
                print("Spacebar pressed. Starting move...")
                start_move()
                print("Press SPACEBAR again to start another move, or CTRL+C to exit.")
                # Prevent immediate re-trigger
                time.sleep(1)  # Adjust delay as needed
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        camera.release()  # Release the camera when the program exits
        print("Camera released.")
