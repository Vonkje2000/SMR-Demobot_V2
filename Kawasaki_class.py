class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class Kawasaki_arm(object):
	def __init__(self, ip):
		self.ip = ip

	def printIP(self):
		print(self.ip)

	def HOME(self):
		print("HOME")

	def HOME2(self):
		print("HOME 2")

	def SPEED(self, SPEED:float|int):
		if not isinstance(SPEED, float|int):
			raise TypeError("SPEED must be a float or an int")
		SPEED = round(SPEED)
		if SPEED <= 0:
			raise ValueError("SPEED value to LOW minimum value 1")
		if SPEED > 100:
			raise ValueError("SPEED value to HIGH maximum value 100")
		print("SPEED {0} ALWAYS".format(SPEED))

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
		print("JMOVE({0}, {1}, {2}, {3}, {4}, {5})".format(JT0, JT1, JT2, JT3, JT4, JT5))

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
		print("JMOVE({0}, {1}, {2}, {3}, {4}, {5})".format(X, Y, Z, O, A, T))

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
		print("LMOVE({0}, {1}, {2}, {3}, {4}, {5})".format(JT0, JT1, JT2, JT3, JT4, JT5))

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
		print("LMOVE({0}, {1}, {2}, {3}, {4}, {5})".format(X, Y, Z, O, A, T))

class Kawasaki_1(Kawasaki_arm, metaclass=Singleton):
	def __init__(self):
		super().__init__("192.168.0.3")

class Kawasaki_2(Kawasaki_arm, metaclass=Singleton):
	def __init__(self):
		super().__init__("192.168.0.1")