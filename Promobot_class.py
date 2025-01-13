import socket
import serial
from time import sleep
import os
import sys
import cv2
import threading

class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class Kawasaki_arm(object):
	def __init__(self, ip:str, port:int, Test_mode:bool=False):
		if not isinstance(ip, str):
			raise TypeError("ip must be a string")
		if not isinstance(port, int):
			raise TypeError("port must be an int")
		if not isinstance(Test_mode, bool):
			raise TypeError("Test_mode must be an bool")
		self.ip = ip
		self.port = port
		self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.Test_mode=Test_mode
		if self.Test_mode == False:
			self.__open_Connection()

	def printIP(self):
		print(self.ip)

	def HOME(self):
		self.__send_to_arm("HOME")

	def HOME2(self):
		self.__send_to_arm("HOME 2")

	def CP(self, value:bool):
		if not isinstance(value, bool):
			raise TypeError("value must be a bool")
		if value:
			self.__send_to_arm("CP ON")
		else:
			self.__send_to_arm("CP OFF")

	def SPEED(self, SPEED:float|int):
		if not isinstance(SPEED, float|int):
			raise TypeError("SPEED must be a float or an int")
		SPEED = round(SPEED)
		if SPEED <= 0:
			raise ValueError("SPEED value to LOW minimum value 1")
		if SPEED > 100:
			raise ValueError("SPEED value to HIGH maximum value 100")
		self.__send_to_arm("SPEED {0} ALWAYS".format(SPEED))

	def JMOVE(self, JT0:float|int, JT1:float|int, JT2:float|int, JT3:float|int, JT4:float|int, JT5:float|int):
		if not isinstance(JT0, float|int):
			raise TypeError("JT0 must be a float or an int")
		JT0 = round(JT0, 2)
		if not isinstance(JT1, float|int):
			raise TypeError("JT1 must be a float or an int")
		JT1 = round(JT1, 2)
		if not isinstance(JT2, float|int):
			raise TypeError("JT2 must be a float or an int")
		JT2 = round(JT2, 2)
		if not isinstance(JT3, float|int):
			raise TypeError("JT3 must be a float or an int")
		JT3 = round(JT3, 2)
		if not isinstance(JT4, float|int):
			raise TypeError("JT4 must be a float or an int")
		JT4 = round(JT4, 2)
		if not isinstance(JT5, float|int):
			raise TypeError("JT5 must be a float or an int")
		JT5 = round(JT5, 2)
		self.__send_to_arm("JMOVE ({0}, {1}, {2}, {3}, {4}, {5})".format(JT0, JT1, JT2, JT3, JT4, JT5))

	def JMOVE_TRANS(self, X:float|int, Y:float|int, Z:float|int, O:float|int, A:float|int, T:float|int):
		if not isinstance(X, float|int):
			raise TypeError("X must be a float or an int")
		X = round(X, 2)
		if not isinstance(Y, float|int):
			raise TypeError("Y must be a float or an int")
		Y = round(Y, 2)
		if not isinstance(Z, float|int):
			raise TypeError("Z must be a float or an int")
		Z = round(Z, 2)
		if not isinstance(O, float|int):
			raise TypeError("O must be a float or an int")
		O = round(O, 2)
		if not isinstance(A, float|int):
			raise TypeError("A must be a float or an int")
		A = round(A, 2)
		if not isinstance(T, float|int):
			raise TypeError("T must be a float or an int")
		T = round(T, 2)
		self.__send_to_arm("JMOVE TRANS ({0}, {1}, {2}, {3}, {4}, {5})".format(X, Y, Z, O, A, T))

	def LMOVE(self, JT0:float|int, JT1:float|int, JT2:float|int, JT3:float|int, JT4:float|int, JT5:float|int):
		if not isinstance(JT0, float|int):
			raise TypeError("JT0 must be a float or an int")
		JT0 = round(JT0, 2)
		if not isinstance(JT1, float|int):
			raise TypeError("JT1 must be a float or an int")
		JT1 = round(JT1, 2)
		if not isinstance(JT2, float|int):
			raise TypeError("JT2 must be a float or an int")
		JT2 = round(JT2, 2)
		if not isinstance(JT3, float|int):
			raise TypeError("JT3 must be a float or an int")
		JT3 = round(JT3, 2)
		if not isinstance(JT4, float|int):
			raise TypeError("JT4 must be a float or an int")
		JT4 = round(JT4, 2)
		if not isinstance(JT5, float|int):
			raise TypeError("JT5 must be a float or an int")
		JT5 = round(JT5, 2)
		self.__send_to_arm("LMOVE ({0}, {1}, {2}, {3}, {4}, {5})".format(JT0, JT1, JT2, JT3, JT4, JT5))

	def LMOVE_TRANS(self, X:float|int, Y:float|int, Z:float|int, O:float|int, A:float|int, T:float|int):
		if not isinstance(X, float|int):
			raise TypeError("X must be a float or an int")
		X = round(X, 2)
		if not isinstance(Y, float|int):
			raise TypeError("Y must be a float or an int")
		Y = round(Y, 2)
		if not isinstance(Z, float|int):
			raise TypeError("Z must be a float or an int")
		Z = round(Z, 2)
		if not isinstance(O, float|int):
			raise TypeError("O must be a float or an int")
		O = round(O, 2)
		if not isinstance(A, float|int):
			raise TypeError("A must be a float or an int")
		A = round(A, 2)
		if not isinstance(T, float|int):
			raise TypeError("T must be a float or an int")
		T = round(T, 2)
		self.__send_to_arm("LMOVE TRANS ({0}, {1}, {2}, {3}, {4}, {5})".format(X, Y, Z, O, A, T))

	def TOOL(self, X:float|int, Y:float|int, Z:float|int, O:float|int, A:float|int, T:float|int):
		if not isinstance(X, float|int):
			raise TypeError("X must be a float or an int")
		X = round(X, 2)
		if not isinstance(Y, float|int):
			raise TypeError("Y must be a float or an int")
		Y = round(Y, 2)
		if not isinstance(Z, float|int):
			raise TypeError("Z must be a float or an int")
		Z = round(Z, 2)
		if not isinstance(O, float|int):
			raise TypeError("O must be a float or an int")
		O = round(O, 2)
		if not isinstance(A, float|int):
			raise TypeError("A must be a float or an int")
		A = round(A, 2)
		if not isinstance(T, float|int):
			raise TypeError("T must be a float or an int")
		T = round(T, 2)
		self.__send_to_arm("TOOL TRANS ({0}, {1}, {2}, {3}, {4}, {5})".format(X, Y, Z, O, A, T))
		self.CP(True)

	def __open_Connection(self):
		if self.Test_mode == False:
			try:
				self.socket_connection.connect((self.ip, self.port))
			except:
				raise ConnectionError("Could not connect to kawasaki robot arm on IP: {0}, Port: {1}".format(self.ip, self.port))

	def __close_Connection(self):
		if self.Test_mode == False:
			self.socket_connection.close()

	def __send_to_arm(self, data:str):
		if not isinstance(data, str):
			raise TypeError("ip must be a string")
		if self.Test_mode == False:
			self.__receive_from_arm()
			self.socket_connection.send(data.encode('utf-8'))
		else:
			print("Test_mode: " + data)

	def __receive_from_arm(self):
		return self.socket_connection.recv(1024).decode()

	def __del__(self):
		if(hasattr(socket.socket, 'socket_connection')):
			self.__close_Connection()

class Kawasaki_1(Kawasaki_arm, metaclass=Singleton):
	def __init__(self, ip:str = "192.168.0.1", port:int = 42069, Test_mode:bool=False):
		super().__init__(ip, port, Test_mode)

class Kawasaki_2(Kawasaki_arm, metaclass=Singleton):
	def __init__(self, ip:str = "192.168.0.3", port:int = 42069, Test_mode:bool=False):
		super().__init__(ip, port, Test_mode)

class Robot_Hand(metaclass=Singleton):
	def __init__(self, port:str = "COM8", Test_mode:bool=False) -> None:
		if not isinstance(port, str):
			raise TypeError("port must be a string")
		if not isinstance(Test_mode, bool):
			raise TypeError("Test_mode must be a bool")
		self.Test_mode = Test_mode
		self.Serial = serial.Serial()
		self.Serial.port = port
		self.Serial.baudrate = 9600
		self.Serial.bytesize = 8
		self.Serial.parity = "N"
		self.Serial.stopbits = 1
		self.Serial.timeout = None
		if self.Test_mode == False:
			try:
				self.Serial.open()
			except:
				if sys.platform == "win32":
					print ("You are using windows and your port is wrong so I opened device manager for you :)")
					os.system('devmgmt.msc')
				raise ConnectionError("Could not open the connection on Serial {0}".format(self.Serial.port))
			sleep(0.1)
		self.__send("00000")

	def fingers(self, thumb:int, index:int, middle:int, ring:int, pinkie:int):
		if not isinstance(thumb, int):
			raise TypeError("thumb must be an int")
		if thumb < 0 or thumb > 9:
			raise ValueError("thumb value must be 0-9")
		if not isinstance(index, int):
			raise TypeError("index must be an int")
		if index < 0 or index > 9:
			raise ValueError("index value must be 0-9")
		if not isinstance(middle, int):
			raise TypeError("middle must be an int")
		if middle < 0 or middle > 9:
			raise ValueError("middle value must be 0-9")
		if not isinstance(ring, int):
			raise TypeError("ring must be an int")
		if ring < 0 or ring > 9:
			raise ValueError("ring value must be 0-9")
		if not isinstance(pinkie, int):
			raise TypeError("pinkie must be an int")
		if pinkie < 0 or pinkie > 9:
			raise ValueError("pinkie value must be 0-9")
		self.__send("{0}{1}{2}{3}{4}".format(thumb, index, middle, ring, pinkie))

	def rock(self):
		self.__send("00000")

	def paper(self):
		self.__send("99999")

	def scissors(self):
		self.__send("09900")

	def thumb(self):
		self.__send("90000")

	def rock_and_roll(self):
		self.__send("99009")
	
	def pistol(self):
		self.__send("99000")

	def __send(self, data:str):
		data = data + "\n"
		if self.Test_mode == False:
			try:
				self.Serial.write(data.encode('utf-8'))
			except:
				raise ConnectionError ("Serial device disconnected")
			sleep(0.1)
			received = self.Serial.read_all().decode()
			if (received != ""):
				print(received)
		else:
			print("Test_mode: " + data)

	def __del__(self):
		if(self.Serial.is_open):
			self.Serial.close()
			#print("close serial {0}".format(self.Serial.port))

class Intel_Camera(object, metaclass=Singleton):
	def __init__(self, cameranumbr:int = 1, Demo_Mode:bool=False,Test_Mode:bool=False):
		if not isinstance(cameranumbr, int):
			raise TypeError("Camera number must be an int")
		if not isinstance(Demo_Mode, bool):
			raise TypeError("Demo Mode must be a bool")
		if not isinstance(Test_Mode, bool):
			raise TypeError("Test Mode must be a bool")
		self.Test_Mode = Test_Mode
		if Test_Mode == False:	
			self.camera = cv2.VideoCapture(cameranumbr)
			self.lock = threading.Lock()
			self.t = threading.Thread(target=self.__reader)
			self.t.daemon = True
			self.t.start()
			self.Demo_Mode = Demo_Mode
		else:
			print("Test Mode: Camera initialized")

	def __reader(self):
		while True:
			with self.lock:
				ret = self.camera.grab()
			if not ret:
				break
			if self.Demo_Mode == True:
				ret = cv2.rotate(ret, cv2.ROTATE_90_CLOCKWISE)
				cv2.imshow("Live Feed", ret)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
		self.camera.release()
		cv2.destroyAllWindows()
	
	def read(self):
		if self.Test_Mode == False:
			with self.lock:
				_, frame = self.camera.retrieve()
			return frame
		else:
			return cv2.imread("test_image.jpg")