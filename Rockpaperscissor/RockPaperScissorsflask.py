from flask import Flask, render_template, jsonify, send_file
import threading
import time
import random
import cv2
from ultralytics import YOLO
import os

app = Flask(__name__)

# Variabelen en initiële setup (camera, model, robot, etc.)
camera = cv2.VideoCapture(1)  # Camera instellen
model = YOLO('Rockpaperscissor/best.pt', verbose=False)
running = True

# Resultaten en foto variabelen
game_result = None
captured_image_path = None

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
                    captured_image_path = "/path/to/save/image.jpg"  # Pas dit pad aan
                    cv2.imwrite(captured_image_path, frame)  # Bewaar de afbeelding
                    cv2.imshow("Detection Result", frame)
                    cv2.waitKey(1)
        
        if detected_gesture:
            break
        time.sleep(0.5)

    if not detected_gesture:
        print("No gesture detected after multiple attempts.")
    return detected_gesture

def determine_winner(robot_gesture, detected_gesture):
    """Determine the winner based on robot's and user's gestures."""
    winning_conditions = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock",
    }
    
    if robot_gesture == detected_gesture:
        return "draw"
    if winning_conditions.get(robot_gesture) == detected_gesture:
        return "robot"
    return "user"

def start_move():
    """Start robot movement and game."""
    global game_result
    robot_gesture = random.choice(['rock', 'paper', 'scissors'])
    print(f"Robot performed gesture: {robot_gesture}")
    
    # Simuleer robotbeweging en stel het resultaat in na de timer
    time.sleep(3)  # Simuleer vertraging voor robotbeweging
    detected_gesture = capture_result_image()
    winner = determine_winner(robot_gesture, detected_gesture)
    
    if winner == "draw":
        game_result = f"Result: It's a draw! Both chose {robot_gesture}."
    elif winner == "robot":
        game_result = f"Result: Robot wins! Robot: {robot_gesture}, User: {detected_gesture}."
    else:
        game_result = f"Result: You win! Robot: {robot_gesture}, User: {detected_gesture}."

@app.route('/start_move', methods=['POST'])
def start_move_route():
    """Start the robot movements when the button is pressed."""
    print("Start button pressed, starting move...")
    threading.Thread(target=start_move).start()  # Start de robotbeweging in een aparte thread
    return jsonify({"status": "move_started"})

@app.route('/captured_image', methods=['GET'])
def get_captured_image():
    """Retourneer de afbeelding van de gedetecteerde handeling."""
    if captured_image_path and os.path.exists(captured_image_path):
        return send_file(captured_image_path, mimetype='image/jpeg')
    return jsonify({"error": "No image captured yet."})

@app.route('/game_result', methods=['GET'])
def get_game_result():
    """Retourneer het resultaat van het spel."""
    if game_result:
        return jsonify({"result": game_result})
    return jsonify({"result": "Game not finished yet."})

@app.route('/')
def index():
    """Webpagina met de Start-knop."""
    return render_template('index.html')

def live_feed():
    """Live feed van de camera."""
    while running:
        ret, frame = camera.read()
        if ret:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            # cv2.imshow("Live Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    feed_thread = threading.Thread(target=live_feed, daemon=True)
    feed_thread.start()
    print("Live feed gestart.")
    app.run(debug=True, use_reloader=False)
