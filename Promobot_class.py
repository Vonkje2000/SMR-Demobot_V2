import socket

class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class Kawasaki_arm(object):
	def __init__(self, ip:str, port:int):
		if not isinstance(ip, str):
			raise TypeError("ip must be a string")
		if not isinstance(port, int):
			raise TypeError("port must be an int")
		self.ip = ip
		self.port = port
		self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__open_Connection()

	def printIP(self):
		print(self.ip)

	def HOME(self):
		self.__send_to_arm("HOME")

	def HOME2(self):
		self.__send_to_arm("HOME 2")

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

	def __open_Connection(self):
		try:
			self.socket_connection.connect((self.ip, self.port))
		except:
			raise ConnectionError("Could not connect to kawasaki robot arm on IP: {0}, Port: {1}".format(self.ip, self.port))

	def __close_Connection(self):
		self.socket_connection.close()

	def __send_to_arm(self, data:str):
		if not isinstance(data, str):
			raise TypeError("ip must be a string")
		self.__receive_from_arm()
		self.socket_connection.send(data.encode('utf-8'))

	def __receive_from_arm(self):
		return self.socket_connection.recv(1024).decode()

	def __del__(self):
		if(hasattr(socket.socket, 'socket_connection')):
			self.__close_Connection()

class Kawasaki_1(Kawasaki_arm, metaclass=Singleton):
	def __init__(self, ip = "192.168.0.1", port = 42069):
		super().__init__(ip, port)

class Kawasaki_2(Kawasaki_arm, metaclass=Singleton):
	def __init__(self, ip = "192.168.0.3", port = 42069):
		super().__init__(ip, port)