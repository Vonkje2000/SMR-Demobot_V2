from flask import request, jsonify, render_template
import sys
import os
sys.path.append(os.path.abspath(r"C:/Users/.../SMR-Demobot_V2"))
from Promobot_class import Kawasaki_1
import threading
from time import sleep

position_0_trans = [620, 20, 100, 0, 90, 0]

base_rotation = position_0_trans[4]
shoulder_rotation = position_0_trans[5]

stop_thread = True

def thread_writer():
	global stop_thread
	k1 = Kawasaki_1()
	while True:
		k1.JMOVE_TRANS(position_0_trans[0], position_0_trans[1], position_0_trans[2], position_0_trans[3], base_rotation, shoulder_rotation)
		#print("base_rotation : {0}, shoulder_rotation : {1}".format(base_rotation, shoulder_rotation))
		if(stop_thread):
			break

t = threading.Thread(target=thread_writer)

def joystick_index():
	global stop_thread
	k1 = Kawasaki_1()
	k1.SPEED(100)
	k1.TOOL(0, 0, 180, 0, 0, 0)                                                 #X, Z, Y because Z is the same direction as the tool, so it changed from straight up position
	k1.JMOVE_TRANS(position_0_trans[0], position_0_trans[1], position_0_trans[2], position_0_trans[3], position_0_trans[4], position_0_trans[5])                     #X, Y, Z, Base, Shoulder, Elbow
	if (stop_thread == True):
		stop_thread = False
		t.start()
	return render_template('joystick.html')

def joystick():
	global base_rotation, shoulder_rotation
	data = request.json

	# General formula for movement
	base_rotation = position_0_trans[4] - (data.get('x') * 10)
	shoulder_rotation = position_0_trans[5] + (data.get('y') * 10)

	#print(f"Received joystick data: x={data.get('x')}, y={data.get('y')}")
	return jsonify({"status": "success"})
			
def maze_cleanup():
	global stop_thread
	if (stop_thread == False):
		stop_thread = True
		t.join()
	k1 = Kawasaki_1()
	print("maze cleanup")
	return jsonify({"status": "success"})
	  
def maze_reset():
	global stop_thread
	if (stop_thread == True):
		stop_thread = False
		t.join()
	k1 = Kawasaki_1()
	k1.JMOVE_TRANS(position_0_trans[0], position_0_trans[1], position_0_trans[2], position_0_trans[3], position_0_trans[4], position_0_trans[5])
	k1.JMOVE_TRANS(position_0_trans[0], position_0_trans[1], position_0_trans[2], position_0_trans[3], position_0_trans[4], position_0_trans[5] + 90)
	k1.JMOVE_TRANS(position_0_trans[0], position_0_trans[1], position_0_trans[2], position_0_trans[3], position_0_trans[4], position_0_trans[5])
	if (stop_thread == False):
		stop_thread = True
		t.start()
	return jsonify({"status": "success"})