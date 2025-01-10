import cv2

def capture_rotated_frame():
    # Initialize the camera (0 for the default camera)
    cap = cv2.VideoCapture(2)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    print("Press 's' to save a picture, or 'q' to quit.")
    
    picture_number = 0

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Rotate the frame 90 degrees clockwise
        rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        # Display the rotated frame
        cv2.imshow("Rotated Frame", rotated_frame)

        # Handle key press events
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            # Save the rotated frame as an image file
            save_path = "picture{0}.jpg".format(picture_number)
            picture_number += 1
            cv2.imwrite(save_path, rotated_frame)
            print(f"Image saved as '{save_path}'.")
        elif key == ord('q'):
            # Exit the loop
            print("Exiting...")
            break

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_rotated_frame()