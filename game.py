# Rock, Paper, Scissors
# pip install pyserial

import serial
import random
import time

arduino = None
try:
    arduino = serial.Serial('COM8', 9600)  # Change 'COMx' to the appropriate port on your system
    time.sleep(3)
except:
    # arduino.close()    
    print('issues with connecting to the arduino, check port number')

options = ["Rock", "Paper", "Scissors"]
def get_rock_paper_scissors_choice():
    robot_choice = random.choice(options)
    return robot_choice

def send_command_to_arduino(robot_choice):
    try:
        command_mapping = {
                "Rock": b'0',
                "Paper": b'1',
                "Scissors": b'2'
        }
        arduino.write(command_mapping[robot_choice])
    except:
        print('issues with connecting to the arduino')

