from flask import request, jsonify, render_template
import sys
import os
sys.path.append(os.path.abspath(r"C:/Users/.../SMR-Demobot_V2"))
from Promobot_class import Kawasaki_1, Robot_Hand
import threading
from time import sleep

position_0_trans = [529, 58, 145, 0, 90, 180]

base_rotation = position_0_trans[4]
shoulder_rotation = position_0_trans[5]

stop_thread = True
robot_state = "none"

def thread_writer():
	global stop_thread, base_rotation, shoulder_rotation
	k1 = Kawasaki_1()
	while True:
		k1.JMOVE_TRANS(position_0_trans[0], position_0_trans[1], position_0_trans[2], position_0_trans[3], base_rotation, shoulder_rotation)
		#print("base_rotation : {0}, shoulder_rotation : {1}".format(base_rotation, shoulder_rotation))
		sleep(0.5)
		if(stop_thread):
			break

t = None

def joystick_index():
	global robot_state
	if (robot_state == "none"):
		robot_state = "starting"
		threading.Thread(target=joystick_robot_setup).start()
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
	global stop_thread, robot_state, t
	if(robot_state != "done" and robot_state != "none"):
		while(robot_state != "setup"):
			sleep(0.1)

		if (stop_thread == False):
			stop_thread = True
			while (t.is_alive()):
				t.join()

		robot_state = "cleaning"
		threading.Thread(target=joystick_robot_cleanup).start()
	
		while(not(robot_state == "done" or robot_state == "none")):
			sleep(0.1)
	
	if(robot_state == "done" or robot_state == "none"):
		robot_state == "none"
		return jsonify({"status": "success"})
	
	return jsonify({"status": "busy"})
	  
def maze_reset():
	global stop_thread, t
	if (stop_thread == False):
		stop_thread = True
		while (t.is_alive()):
			t.join()
	k1 = Kawasaki_1()
	k1.JMOVE_TRANS(position_0_trans[0], position_0_trans[1], position_0_trans[2], position_0_trans[3], position_0_trans[4], position_0_trans[5])
	k1.JMOVE_TRANS(position_0_trans[0], position_0_trans[1], position_0_trans[2], position_0_trans[3], position_0_trans[4], position_0_trans[5] + 120)
	sleep(3)
	k1.JMOVE_TRANS(position_0_trans[0], position_0_trans[1], position_0_trans[2], position_0_trans[3], position_0_trans[4], position_0_trans[5])
	sleep(2)
	if (stop_thread == True):
		stop_thread = False
		t = threading.Thread(target=thread_writer)
		t.start()
	return jsonify({"status": "success"})

def joystick_robot_setup():
	global stop_thread, robot_state, t
	k1 = Kawasaki_1()
	magnetcontroller = Robot_Hand()
	magnetcontroller.magnet_OFF()
	k1.SPEED(40)
	k1.TOOL(0, 0, 30, 0, 0, 0)
	# add all code for pickup
	k1.LMOVE(60, -32, -121, 164, 66, 53)
	k1.LMOVE_TRANS(203, 147, 141, -91, 180, -91)
	k1.LMOVE_TRANS(-230, 103, 141, 86, 180, -33)
	k1.LMOVE_TRANS(-274, 41, -73, -42, 180, -133)
	# above maze holder
	k1.SPEED(1)
	k1.LMOVE_TRANS(-274.660, 41.242, -114.699, 29.057, 179.998, -61.943)
	k1.SPEED(2)
	# Rotate
	k1.JMOVE(-81.459, 20.104, -143.202, 179.996, 16.693, 75.399)
	magnetcontroller.magnet_ON()
	k1.TOOL(0, 0, 180, 0, 0, 0)
	# Slowly pulling out
	k1.SPEED(2)
	k1.LMOVE_TRANS(-276.102, 41.159, -239.034, 7.794, 179.993, 1.723)
	k1.LMOVE_TRANS(-279.096, 40.890, -239.039, 21.514, 179.996, 15.448)
	k1.LMOVE_TRANS(-279.106, 40.865, -194.347, 37.452, 179.997, 31.383)
	k1.SPEED(3)
	k1.LMOVE_TRANS(-275.919, 41.216, -194.351, 18.869, 179.996, 12.800)
	k1.LMOVE_TRANS(-276.114, 44.940, 56.567, 7.294, 179.993, 1.225)
	# Above mazeholder
	k1.JMOVE(0.123, -18, -90, 180, 108, 74)
	k1.JMOVE(   65, -18, -90, 180, 108, 74)
	k1.JMOVE(   65, -18, -90, 180,  72, 74)
	# Maze pos
	k1.JMOVE(77.601, -16.888, -130.994, 207.067, -28.680, 62.854)
	k1.JMOVE_TRANS(position_0_trans[0], position_0_trans[1], position_0_trans[2], position_0_trans[3], position_0_trans[4], position_0_trans[5])
	
	if (stop_thread == True):
		stop_thread = False
		t = threading.Thread(target=thread_writer)
		t.start()
	robot_state = "setup"

def joystick_robot_cleanup():
	global robot_state
	k1 = Kawasaki_1()
	magnetcontroller = Robot_Hand()
	magnetcontroller.magnet_OFF()

	k1.TOOL(0, 0, 180, 0, 0, 0)
	magnetcontroller.magnet_ON()
	k1.SPEED(10)

	k1.JMOVE(89, -20, -120, 179, -9.3, 87.87)
	k1.JMOVE( 90.244, -20.482, -82.901, 179.802, 103.231, 87.882)
	k1.JMOVE(  3.742, -20.482, -82.901, 179.802, 103.231, 87.882)
	k1.JMOVE(-89.187, -20.482, -82.901, 179.802, 103.231, 87.882)
	k1.SPEED(10)
	#boven houder
	k1.LMOVE_TRANS(-277.729, 40.344, 99.820, 126.687, 178.880, 125.689)
	sleep(1)
	k1.SPEED(1)
	k1.ACCEL(1)
	# little bit in holder
	k1.LMOVE_TRANS(-279.522, 45.289, -50.949, 126.654, 178.882, 125.655)
	#against holder
	k1.ACCEL(1)
	k1.LMOVE_TRANS(-275.591, 45.061, -50.992, 126.745, 178.880, 125.724)
	k1.ACCEL(1)
	# Little bit down
	k1.LMOVE_TRANS(-277.415, 47.533, -207.379, 126.735, 178.879, 125.740)
	k1.ACCEL(1)
	k1.LMOVE_TRANS(-277.330, 43.071, -207.581, 126.675, 178.880, 125.674)
	k1.ACCEL(1)
	# Last bit down and rotate
	k1.LMOVE_TRANS(-277.996, 43.983, -264.391, 126.548, 178.876, 125.532)
	k1.SPEED(3)
	k1.ACCEL(1)
	k1.JMOVE(-81.750, 20.021, -143.181, 177.132, 16.025, -8.809)
	magnetcontroller.magnet_OFF()
	# Back up without maze
	k1.LMOVE(-81.813, 11.245, -142.974, 178.130, 24.996, -7.446)
	k1.SPEED(10)
	# Back to start position
	k1.JMOVE(0, 11.245, -142.974, 178.130, 24.996, -7.446)
	k1.JMOVE(67, 11, -90, 178, 74, -7)
	k1.JMOVE(84, 0, -90, 180, 90, -98)
	k1.TOOL(0, 0, 30, 0, 0, 0)
	
	robot_state = "done"
