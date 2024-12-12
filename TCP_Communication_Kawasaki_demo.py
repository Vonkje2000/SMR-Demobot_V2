from Kawasaki_class import Kawasaki_1
from Kawasaki_class import Kawasaki_2

k1 = Kawasaki_1()
k2 = Kawasaki_2()

k1.printIP()
k2.printIP()

k1.HOME()
k1.JMOVE_TRANS(-1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

k1.JMOVE(0, 5.0, -6.0, 7.0, 4.0, 2.0)

k1.SPEED(0)