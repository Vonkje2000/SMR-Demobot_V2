from flask import Flask, request, jsonify, render_template
import sys
sys.path.insert(0, '/Users/basti/Documents/GitHub/SMR-Demobot_V2')
from Promobot_class import Kawasaki_1

app = Flask(__name__)

k1 = Kawasaki_1()
k1.SPEED(100)
k1.TOOL(0, 0, 180, 0, 0, 0)                                                 #X, Z, Y because Z is the same direction as the tool, so it changed from straight up position
k1.JMOVE_TRANS(-143, 750, -170, 90.238, 91.971, 94.861)                     #X, Y, Z, Base, Shoulder, Elbow

@app.route('/')
def index():
    return render_template('joystick.html')

@app.route('/joystick', methods=['POST'])
def joystick():
    import math

    data = request.json
    x = data.get('x')
    y = data.get('y')

    degreesX = x * 10
    degreesY = y * 10

    if degreesX == 0 and degreesY == 0:
        # Horizontal
        k1.LMOVE_TRANS(-143, 750, -170, 90.238, 91.971, 94.861)
        print("Horizontal")
    else:
        # General formula for movement
        base_rotation = 91.971 - degreesX
        shoulder_rotation = 94.861 + degreesY

        k1.LMOVE_TRANS(-143, 750, -170, 90.238, base_rotation, shoulder_rotation)

        # Determine direction using atan2
        angle_rad = math.atan2(degreesY, degreesX)  # Returns angle in radians
        angle_deg = math.degrees(angle_rad)        # Convert to degrees
        angle_deg = (angle_deg + 360) % 360        # Normalize to [0, 360)

        # Map angle to one of 8 cardinal directions
        directions = [
            "East", "North-East", "North", "North-West",
            "West", "South-West", "South", "South-East"
        ]
        index = int((angle_deg + 22.5) // 45) % 8  # 22.5 ensures correct rounding to nearest direction
        print(directions[index])
    print(f"Received joystick data: x={x}, y={y}")
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=False)
  

