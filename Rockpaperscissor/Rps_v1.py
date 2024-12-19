from flask import Flask, request, jsonify, render_template
import sys
import cv2
import threading
sys.path.insert(0, '/Users/basti/Documents/GitHub/SMR-Demobot_V2')
from Promobot_class import Kawasaki_2

k2 = Kawasaki_2()
k2.SPEED(50)
k2.TOOL(0, 0, 0, 0, 0, 0)

def move_robot():
    counter = 0
    while counter < 20:
        k2.LMOVE_TRANS(283, 309, 100, 20, 80, 180)   
        k2.LMOVE_TRANS(250, 300, 50, 20, 106, 180)  # X, Y, Z, Base, Shoulder, Elbow
        counter += 1

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
    # Create threads for robot movement and camera display
    robot_thread = threading.Thread(target=move_robot)
    camera_thread = threading.Thread(target=display_camera)
    
    # Start the threads
    robot_thread.start()
    camera_thread.start()
    
    # Wait for both threads to complete
    robot_thread.join()
    camera_thread.join()

if __name__ == "__main__":
    main()
