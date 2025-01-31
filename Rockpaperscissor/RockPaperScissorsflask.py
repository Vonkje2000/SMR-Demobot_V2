from flask import render_template, jsonify, send_file, request
import threading
import sys
import cv2
import random
from time import sleep
from ultralytics import YOLO
sys.path.insert(0, '/Users/basti/Documents/GitHub/SMR-Demobot_V2')
from Promobot_class import Kawasaki_2, Robot_Hand, Intel_Camera

# Variabelen en initiële setup (camera, model, robot, etc.)
model = YOLO('Rockpaperscissor/best.pt', verbose=False)

# Resultaten en foto variabelen
captured_image_path = None
winner = "none"

RPS_state = "none"

def capture_result_image():
	"""Capture up to 5 frames and detect gestures using YOLO."""
	global captured_image_path
	detected_gesture = None
	#print("Starting gesture detection...")
	if cv2.getWindowProperty("Detection Result", cv2.WND_PROP_VISIBLE) == 1:
		cv2.destroyWindow("Detection Result")

	camera = Intel_Camera()
	for attempt in range(5):
		print("picture taken: " + str(attempt))
		frame = camera.read()
		
		#frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

		# Perform YOLO detection
		results = model.predict(frame, conf=0.4, save=False, show=False, verbose=False)

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
					#cv2.imshow("Detection Result", frame)
					#cv2.waitKey(1)
		
		if detected_gesture:
			break

	if not detected_gesture:
		print("No gesture detected after multiple attempts.")
	return detected_gesture

def determine_winner(robot_gesture:str, detected_gesture:str) -> str:
	"""Determine the winner based on robot's and user's gestures."""
	robot_gesture = robot_gesture.lower()
	detected_gesture = detected_gesture.lower()
	if robot_gesture == "pistol":
		return "robot"
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
	global RPS_state
	while (RPS_state != "none"):
		sleep(0.1)
	RPS_state = "busy"
	# Initialize robot and hand
	Hand = Robot_Hand()
	Hand.rock()  # Start with a rock gesture
	k2 = Kawasaki_2()
	counter = 0
	while counter < 4:
		k2.LMOVE(-52, -54, -113, -12, -40, -73) # low
		k2.LMOVE(-49, -45, -96, -6.5, -47, -78) # up
		counter += 1

	# Choose a random hand gesture for the robot
	Hand = Robot_Hand()
	if random.randint(1, 100) == 1:
		robot_gesture = 'pistol'  # Special case
		gesture = Hand.pistol
	else:
		robot_gesture = random.choice(['rock', 'paper', 'scissors'])
		gesture = getattr(Hand, robot_gesture)

	#print(f"Robot performed gesture: {robot_gesture}")
	gesture()

	# Move back to the lowest position
	k2.LMOVE(-52, -54, -113, -12, -40, -73)

	sleep(1)  # Wait for the robot to finish its movements

	# Capture and present the result along with YOLO detection
	detected_gesture = capture_result_image()
	global winner

	if detected_gesture:
		# Determine and print the winner
		winner = determine_winner(robot_gesture, detected_gesture)
	else:
		winner = "none"
	
	RPS_state = "none"

def start_signal():
	"""Start the robot movements when the button is pressed."""
	start_move()	#thread gave an issue with the last test
	#threading.Thread(target=start_move).start()  # Start de robotbeweging in een aparte thread
	return jsonify({"status": "move_started"})

def get_captured_image():
	"""Retourneer de afbeelding van de gedetecteerde handeling."""
	image_path = 'Rockpaperscissor/image.jpg'
	return send_file(image_path, mimetype='image/jpg')
	
def get_game_result():
	global winner
	return jsonify({"result": str(winner)})

def RPS_index():
	threading.Thread(target=RPS_robot_setup).start()
	return render_template('RPS.html')

def GET_RPS_state():
	global RPS_state
	return jsonify({"status": RPS_state})

def RPS_robot_setup():
	global RPS_state
	RPS_state = "busy"
	k2 = Kawasaki_2()
	k2.SPEED(70)	#test with max speed
	k2.TOOL(0, 0, 40, 0, 0, 0)
	k2.LMOVE(-52, -54, -113, -12, -40, -73)
	Hand = Robot_Hand()
	Hand.rock()
	RPS_state = "none"