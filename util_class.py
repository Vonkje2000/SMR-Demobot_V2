from Promobot_class import Intel_Camera
import cv2
from flask import Response

def video_feed():
	Realsense = Intel_Camera()
	while True:
		frame = Realsense.read()
		frame = cv2.resize(frame, (320, 240))
		frame = cv2.imencode('.jpg', frame)[1].tobytes()
		yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def util_video_feed():
	return Response(video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

def util_page():
	#page = "<!DOCTYPE html> <html lang=\"en\"> <head> <meta charset=\"UTF-8\"> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"> <title>Live Camera Stream</title> <style> video \{ width: 100%; max-width: 600px; border: 1px solid #ccc; \} </style> </head> <body> <h1>Live Camera Stream</h1> <img class=\"video-box\" src=\"/Machine_vision/video_feed/detection\" alt=\"Main Filter\"> </body> </html>"
	page = "<!DOCTYPE html> <html lang=\"en\"> <head> <meta charset=\"UTF-8\"> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"> <title>Live Camera Stream</title> <style> video \{ width: 100%; max-width: 600px; border: 1px solid #ccc; \} </style> </head> <body> <h1>Live Camera Stream</h1> <img class=\"video-box\" src=\"/util/webcam\" alt=\"Main Filter\"> </body> </html>"
	return page