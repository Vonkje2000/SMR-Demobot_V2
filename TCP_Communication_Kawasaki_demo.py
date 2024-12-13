from Kawasaki_class import Kawasaki_1
from Kawasaki_class import Kawasaki_2

k1 = Kawasaki_1()
k2 = Kawasaki_2()

k1.printIP()
k2.printIP()

k1.SPEED(100)
k2.SPEED(45)

k1.TOOL(0, 0, 0, 0, 0, 0)
k2.TOOL(0, 0, 0, 0, 0, 0)

k1.HOME()
k2.HOME()

k1.JMOVE(4, -15, -125, 9, 22, 170)
k2.JMOVE(4, -15, -125, 9, 22, 170)

k1.JMOVE_TRANS(20, 370, 150, 90, 90, 90)
k2.JMOVE_TRANS(20, 370, 150, 90, 90, 90)

k1.JMOVE_TRANS(20, 550, 150, 90, 90, 90)
k2.JMOVE_TRANS(20, 550, 150, 90, 90, 90)

k1.LMOVE_TRANS(20, 370, 150, 90, 90, 90)
k2.LMOVE_TRANS(20, 370, 150, 90, 90, 90)

k1.TOOL(40, 30, 60, 0, 0, 0)
k2.TOOL(40, 30, 60, 0, 0, 0)