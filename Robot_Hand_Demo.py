from Promobot_class import Robot_Hand
from time import sleep

Hand = Robot_Hand("COM8")

sleep(1)
Hand.rock()

sleep(1)
Hand.paper()

sleep(1)
Hand.scissors()

sleep(1)
Hand.thumb()

sleep(1)
Hand.rock_and_roll()

sleep(1)
Hand.fingers(0,2,4,6,8)

sleep(1)
Hand.fingers(0,0,0,0,0)
sleep(0.1)
Hand.fingers(9,0,0,0,0)
sleep(0.1)
Hand.fingers(9,9,0,0,0)
sleep(0.1)
Hand.fingers(9,9,9,0,0)
sleep(0.1)
Hand.fingers(9,9,9,9,0)
sleep(0.1)
Hand.fingers(9,9,9,9,9)