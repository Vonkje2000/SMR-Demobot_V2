from flask import Flask, request, jsonify, render_template
import sys
import cv2
import threading
import random
import time
sys.path.insert(0, '/Users/basti/Documents/GitHub/SMR-Demobot_V2')
from Promobot_class import Kawasaki_2, Robot_Hand

k2 = Kawasaki_2()
Hand = Robot_Hand("COM9")
k2.SPEED(50)
k2.TOOL(0, 0, 0, 0, 0, 0)
robot_movement_conplete = threading.Event()

def move_robot():
    counter = 0
    while counter < 4:
        k2.LMOVE_TRANS(250, 300, 50, 20, 106, 180)  # X, Y, Z, Base, Shoulder, Elbow
        k2.LMOVE_TRANS(283, 309, 100, 20, 80, 180)   
        counter += 1

    robot_movement_conplete.set()
    # Move down to the lowest position
    k2.LMOVE_TRANS(250, 300, 50, 20, 106, 180)

def perform_hand_gesture():
    robot_movement_conplete.wait()

    time.sleep(0.7)  # Wait for the robot to finish its initial movements (3 movements, 2 seconds each)
    
    # Choose a random hand gesture
    if random.randint(1, 100) == 1:
        gesture = Hand.pistol
    else:
        gesture = random.choice([Hand.paper, Hand.scissors])                                                    #Hand.rock, 
        gesture()
    
    time.sleep(1)

def display_camera():
    # Open the camera
    cap = cv2.VideoCapture(2)  # 0 is the default camera
    
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return
    
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break
        
        # Rotate the frame by 90 degrees
        frame_rotated = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        
        # Display the rotated frame
        cv2.imshow("Rotated Camera View", frame_rotated)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

def main():
    # Create threads for robot movement, hand gestures, and camera display
    robot_thread = threading.Thread(target=move_robot)
    hand_thread = threading.Thread(target=perform_hand_gesture)
    camera_thread = threading.Thread(target=display_camera)
    
    # Start the threads
    robot_thread.start()
    hand_thread.start()
    camera_thread.start()
    
    # Wait for all threads to complete
    robot_thread.join()
    hand_thread.join()
    camera_thread.join()

if __name__ == "__main__":
    main()