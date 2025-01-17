from Promobot_class import Kawasaki_1

ismoving = False

# def dance_1():
#     global ismoving
#     ismoving = True
#     print("Danse 1")
#     k1 = Kawasaki_1()
#     k1.SPEED(80)
#     k1.TOOL(0, 0, 0, 0, 0, 0)
#     k1.ACCEL_ALWAYS(100)
#     k1.DECEL_ALWAYS(100)
#     k1.HOME()
    
#     # Taunt
#     k1.DECEL_ALWAYS(45)
#     k1.ACCEL_ALWAYS(35)
#     k1.JMOVE(0, -20, -130, -10, 45, 0)
#     k1.JMOVE(0, -20, -115, 10, -5, 0)
#     k1.ACCEL(50)
#     k1.JMOVE(0, -20, -130, -10, 45, 0)
#     k1.JMOVE(0, -20, -115, 10, -5, 0)
#     k1.ACCEL(50)
#     k1.JMOVE(0, -20, -130, -10, 45, 0)

#     #Head Bobbing and Early Bow
#     k1.JMOVE(0, -20, -80, 0, -60, 0)
#     k1.JMOVE(0, -20, -120, 0, -90, 0)
#     k1.JMOVE(0, -20, -80, 0, -60, 0) 

#     #18 Tilt and Rotate 
#     k1.SPEED(70) 
#     k1.DECEL_ALWAYS(50)
#     k1.ACCEL_ALWAYS(70)
#     k1.JMOVE(0, -60, -90, -180, 60, 0)
#     k1.JMOVE(-20, 30, -90, 90, -45, 0)
#     k1.JMOVE(-50, -30, -70, -180, 45, 0)
#     k1.JMOVE(-10, -20, -20, 0, -90, 0)
#     k1.JMOVE(-60, -20, -50, 180, 90, 0)
#     k1.JMOVE(-30, 45, -80, 90, -60, 0)
#     k1.DECEL(20)
#     k1.JMOVE(-60, -60, -90, -180, 60, 0)
#     k1.JMOVE(-20, -20, -20, 0, -90, 0)
#     k1.JMOVE(-40, 50, -70, 0, 90, 0)
#     k1.DECEL(15)
#     k1.JMOVE(-70, 0, -50, 180, 45, 0)

#     # # Initial turns with subtle tilts
#     k1.SPEED(70)
#     k1.ACCEL_ALWAYS(80)
#     k1.DECEL_ALWAYS(60)
#     k1.JMOVE(-5, -20, -130, -45, -15, 0)
#     k1.JMOVE(-10, -20, -110, 0, 25, 0)
#     k1.JMOVE(-15, -20, -130, 45, -15, 0)
#     k1.JMOVE(-20, -20, -110, 0, 25, 0)  
#     k1.JMOVE(-25, -20, -130, -45, -15, 0)
#     k1.JMOVE(-30, -20, -110, 0, 25, 0)
#     k1.JMOVE(-30, -20, -130, 0, -15, 0)
#     k1.JMOVE(-30, -20, -110, 0, 25, 0)
#     k1.JMOVE(-35, -20, -130, 45, -15, 0)

#     # Repeating dynamic moves for emphasis
#     k1.SPEED(80)
#     k1.JMOVE(-40, -20, -110, 0, 25, 0)
#     k1.JMOVE(-45, -20, -130, 0, -15, 0)
#     k1.JMOVE(-45, -20, -110, 0, 25, 0)

#     # Initial turns with subtle tilts
#     k1.SPEED(70)
#     k1.JMOVE(-50, -20, -130, 45, -15, 0)
#     k1.JMOVE(-55, -20, -110, 0, 25, 0) 
#     k1.JMOVE(-60, -20, -130, -45, -15, 0)
#     k1.JMOVE(-65, -20, -110, 0, 25, 0)
#     k1.JMOVE(-70, -20, -130, 45, -15, 0)
#     k1.JMOVE(-75, -20, -110, 0, 25, 0)
#     k1.JMOVE(-80, -20, -130, 0, -15, 0)
#     k1.JMOVE(-80, -20, -110, 0, 25, 0)
#     k1.JMOVE(-80, -20, -130, -45, -15, 0)
#     k1.JMOVE(-85, -20, -110, 0, 25, 0)
#     k1.JMOVE(-90, -20, -130, 45, -15, 0)
    
#     # Repeating dynamic moves for emphasis
#     k1.SPEED(80)
#     k1.JMOVE(-90, -20, -110, 0, 25, 0)
#     k1.JMOVE(-90, -20, -130, 0, -15, 0)
#     k1.JMOVE(-90, -20, -110, 0, 25, 0)
#     k1.JMOVE(-90, -20, -130, 0, -15, 0)
#     k1.JMOVE(-90, -20, -110, 180, 25, 0)

#     # Diagonal Sway
#     k1.SPEED(70)
#     k1.ACCEL(35)
#     k1.DECEL(45)
#     k1.JMOVE(0, -30, -60, -25, 60, 0)
#     k1.ACCEL(60)
#     k1.DECEL(45)
#     k1.JMOVE(0, 15, -50, 180, -60, 0)
#     k1.ACCEL(60)
#     k1.DECEL(45)
#     k1.JMOVE(-10, -35, -120, -90, 60, 0)
#     k1.ACCEL(60)
#     k1.DECEL(45)
#     k1.JMOVE(-35, 15, -90, 90, -60, 0)
#     k1.ACCEL(60)
#     k1.DECEL(45)
#     k1.JMOVE(-70, -35, -120, -90, 60, 0)

#     k1.ACCEL_ALWAYS(70)
#     k1.DECEL_ALWAYS(60)
#     k1.SPEED(70)
#     k1.JMOVE(-30, 20, -110, 90, -60, 0)
#     k1.JMOVE(-10, -20, -110, -90, 60, 0)
#     k1.JMOVE(-70, 20, -110, 180, -60, 0)
#     k1.JMOVE(-20, -20, -110, -180, 60, 0)

#     k1.ACCEL_ALWAYS(100)
#     k1.DECEL_ALWAYS(100)
#     k1.JMOVE(-30, -30, -90, 180, 60, 0)
#     k1.JMOVE(0, -20, -90, -180, -30, 0)
#     k1.JMOVE(-20, -20, -90, 90, -50, 0)
#     k1.JMOVE(-10, -40, -90, 90, 50, 0)
#     k1.JMOVE(-20, -30, -90, 0, -50, 0)
#     k1.ACCEL_ALWAYS(70)
#     k1.DECEL_ALWAYS(60)
#     k1.JMOVE(0, 35, -50, -180, 30, 0)
#     k1.JMOVE(-90, 0, -50, 180, 60, 0)
#     k1.JMOVE(0, 45, -80, -180, -60, 0)
#     k1.JMOVE(-30, -60, -80, 180, 30, 0)
    
#     # #23 Faces sideways and waves
#     k1.SPEED(50)
#     k1.ACCEL_ALWAYS(70)
#     k1.DECEL_ALWAYS(40)
#     k1.JMOVE(0, 0, 0, 90, 0, 0)
#     k1.JMOVE(0, -20, 40, 90, 0, 0)
#     k1.JMOVE(0, 40, 0, 90, 0, 0)
#     k1.JMOVE(0, -20, 40, 90, 0, 0)
#     k1.JMOVE(0, 40, 0, 90, 0, 0)
#     k1.JMOVE(0, 0, 0, 90, 0, 0)
    
#     # #24 Faces sideways and bow's
#     k1.JMOVE(-90, 0, 0, 0, 0, 0)
#     k1.JMOVE(-90, 0, -110, 0, -90, 0)
#     k1.JMOVE(-90, 0, 0, 0, 0, 0)
#     k1.JMOVE(0, 0, -90, 0, 0, 0)

#     k1.ACCEL_ALWAYS(100)
#     k1.DECEL_ALWAYS(100)
#     ismoving = False

def dance_1():
    global ismoving
    ismoving = True
    print("Danse 1")
    k1 = Kawasaki_1()
    k1.SPEED(70)
    k1.TOOL(0, 0, 25, 0, 0, 0)
    # k1.ACCEL_ALWAYS(100)
    # k1.DECEL_ALWAYS(100)
    # k1.HOME()
    
    # Dance routine using JMOVE_TRANS

    # Test 1
    # k1.JMOVE_TRANS(-128, 559, 30, 140, 142, 117)  # Starting position
    # k1.JMOVE_TRANS(-98, 589, 30, 145, 152, 122)   # Move forward-right with orientation change
    # k1.JMOVE_TRANS(-98, 559, 35, 145, 142, 125)   # Move right with slight elevation
    # k1.JMOVE_TRANS(-128, 529, 30, 130, 132, 117)  # Move directly backward
    # k1.JMOVE_TRANS(-158, 529, 35, 125, 142, 115)  # Move backward-left with slight elevation
    # k1.JMOVE_TRANS(-158, 559, 30, 125, 152, 112)  # Move left with orientation change
    # k1.JMOVE_TRANS(-158, 589, 30, 135, 152, 115)  # Move forward-left with slight descent

    # test 2
    # k1.JMOVE_TRANS(-128, 559, 30, 140, 142, 117)  # Starting position
    # k1.JMOVE_TRANS(-128, 599, 50, 150, 150, 120)  # Move far forward
    # k1.JMOVE_TRANS(-78, 534, 60, 160, 155, 130)   # Move diagonal-right
    # k1.JMOVE_TRANS(-178, 509, 40, 130, 145, 110)  # Move far backward-left
    # k1.JMOVE_TRANS(-78, 584, 45, 140, 150, 125)   # Move diagonal-up-right
    # k1.JMOVE_TRANS(-178, 599, 50, 125, 160, 120)  # Move far forward-left
    # k1.JMOVE_TRANS(-128, 559, 40, 145, 140, 120)  # Return to center with elevation
    # k1.JMOVE_TRANS(-128, 509, 50, 135, 140, 115)  # Move directly backward with descent
    # k1.JMOVE_TRANS(-178, 534, 55, 125, 145, 110)  # Diagonal backward-left
    # k1.JMOVE_TRANS(-78, 599, 50, 145, 155, 125)   # Forward-right with slight tilt
    # k1.JMOVE_TRANS(-198, 584, 45, 120, 150, 115)  # Far backward-left with twist
    # k1.JMOVE_TRANS(-78, 484, 40, 140, 135, 120)   # Deep diagonal backward-right
    # k1.JMOVE_TRANS(-198, 534, 60, 125, 145, 110)  # Leftward arc
    # k1.JMOVE_TRANS(-58, 584, 55, 150, 155, 125)   # Forward arc to the right
    # k1.JMOVE_TRANS(-128, 599, 60, 145, 150, 120)  # Full extension forward
    # k1.JMOVE_TRANS(-128, 559, 30, 140, 142, 117)  # Return to starting position



    # # k1.JMOVE_TRANS(-128, 559, 30, 140, 142, 117)  # Starting position

    # # # Spiral motion expanding outward
    # # k1.JMOVE_TRANS(-128, 579, 35, 145, 145, 120)  # Small forward move
    # # k1.JMOVE_TRANS(-108, 569, 40, 150, 150, 125)  # Shift right and forward
    # # k1.JMOVE_TRANS(-108, 549, 45, 155, 145, 130)  # Shift backward and right
    # # k1.JMOVE_TRANS(-128, 539, 50, 150, 140, 125)  # Shift directly backward
    # # k1.JMOVE_TRANS(-148, 549, 55, 145, 135, 120)  # Shift backward-left
    # # k1.JMOVE_TRANS(-148, 569, 60, 140, 140, 115)  # Shift forward-left
    # # k1.JMOVE_TRANS(-128, 589, 65, 135, 145, 120)  # Expand forward
    # # k1.JMOVE_TRANS(-98, 559, 70, 140, 150, 125)   # Move right and outward
    # # k1.JMOVE_TRANS(-128, 529, 75, 145, 140, 130)  # Move backward and outward
    # # k1.JMOVE_TRANS(-158, 559, 80, 140, 135, 125)  # Complete the spiral with a leftward arc
    # # k1.JMOVE_TRANS(-128, 559, 30, 140, 142, 117)  # Return to starting position


    # # Generic dancing
    # k1.JMOVE(0,60,60,140,50,0)
    # k1.JMOVE(-80,-40,-60,-180,70,0)
    # k1.JMOVE(-20,60,60,200,90,0)
    # k1.JMOVE(-70,-40,-60,-180,70,0)
    # k1.JMOVE(-50,90,100,200,90,0)
    # k1.JMOVE(-90,-40,-60,-180,70,0)
    
    # # Spiral Rise
    # k1.SPEED(70)  
    # k1.JMOVE(0, -10, -90, -360, 0, 0)  # Arm rises top right with a twist
    # k1.JMOVE(-90, -10, -100, 360, 0, 0)  # Repositions rightside
    # k1.JMOVE(-60, 45, -80, -210, 0, 0)  # spins down rightside
    # k1.JMOVE(0, 45, -80, 360, 0, 0)  # spins bottomside
    # k1.JMOVE(0, -10, -90, -360, 0, 0)  # Spins around Z-axis while slightly rising leftside

    # # Finish
    # # Wave
    # k1.SPEED(50)
    # k1.JMOVE(0, 0, 0, 90, 0, 0) #Rises straight and turns head
    # k1.JMOVE(0, -20, 40, 90, 0, 0) #Moves to side
    # k1.JMOVE(0, 40, 0, 90, 0, 0) #Moves to side
    # k1.JMOVE(0, -20, 40, 90, 0, 0) #Moves to side
    # k1.JMOVE(0, 40, 0, 90, 0, 0) #Moves to side
    # k1.JMOVE(0, 0, 0, 90, 0, 0) #Stops upright
    # #Bow
    # k1.JMOVE(-90, 0, 0, 0, 0, 0) #Looks up straight
    # k1.JMOVE(-90, 0, -110, 0, -90, 0) #bow's and lower's the end of arm tool (head)
    # k1.JMOVE(-90, 0, 0, 0, 0, 0) #Looks up straight
    # k1.JMOVE(0, 0, -90, 0, 0, 0) #Looks forward
    
    k1.ACCEL_ALWAYS(100)
    k1.DECEL_ALWAYS(100)
    ismoving = False

def Get_moving():
    return ismoving

if __name__ == "__main__":
    dance_1()
