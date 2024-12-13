from flask import Flask, request, jsonify, render_template
import sys
sys.path.insert(0, '/Users/basti/Documents/GitHub/SMR-Demobot_V2')
from Promobot_class import Kawasaki_1

app = Flask(__name__)

k1 = Kawasaki_1()
k1.SPEED(100)
k1.TOOL(45, 145, 25, 0, 0, 0)
k1.JMOVE_TRANS(-200, 600, -60, 90, 90, 90)

@app.route('/')
def index():
    return render_template('joystick.html')

@app.route('/joystick', methods=['POST'])
def joystick():
    data = request.json
    x = data.get('x')
    y = data.get('y')
    
    degreesX = x * 10
    degreesY = y * 10   

    if degreesX == 0 and degreesY == 0:                                         #Horizontal print ("JMOVE:{0},{1},{2},{3},{4},{5}".format(-200, 600, -60, 90, 90, 90))
        k1.JMOVE_TRANS(-200, 600, -60, 90, 90, 90)
        print("Horizontal")
    elif degreesX == 0 and degreesY > 0:                                        #North
      k1.JMOVE_TRANS(-200, 600, -60, 90, 90, 90 + degreesY)
      print("North")
    elif degreesX > 0 and degreesY > 0:                                         #North-East
      k1.JMOVE_TRANS(-200, 600, -60, 90, 90 - degreesX, 90 + degreesY)
      print("North-East")
    elif degreesX > 0 and degreesY == 0:                                        #East
      k1.JMOVE_TRANS(-200, 600, -60, 90, 90 - degreesX, 90)
      print("East")
    elif degreesX > 0 and degreesY < 0:                                         #South-East
      k1.JMOVE_TRANS(-200, 600, -60, 90, 90 - degreesX, 90 + degreesY)
      print("South-East")
    elif degreesX == 0 and degreesY < 0:                                        #South
      k1.JMOVE_TRANS(-200, 600, -60, 90, 90, 90 + degreesY)
      print("South")
    elif degreesX < 0 and degreesY < 0:                                         #South-West
      k1.JMOVE_TRANS(-200, 600, -60, 90, 90 - degreesX, 90 + degreesY)
      print("South-West")
    elif degreesX < 0 and degreesY == 0:                                        #West
      k1.JMOVE_TRANS(-200, 600, -60, 90, 90 - degreesX, 90)
      print("West")
    elif degreesX < 0 and degreesY > 0:                                        #North-West                    
      k1.JMOVE_TRANS(-200, 600, -60, 90, 90 - degreesX, 90 + degreesY)
      print("North-West")
    print(f"Received joystick data: x={x}, y={y}")
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=False)
  

