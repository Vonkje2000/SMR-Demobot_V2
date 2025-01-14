from Promobot_class import Kawasaki_1

ismoving = False

def dance_1():
    global ismoving
    ismoving = True
    print("Danse 1")
    k1 = Kawasaki_1()
    k1.SPEED(70)
    k1.TOOL(0, 0, 0, 0, 0, 0)

    k1.HOME()
    

    #Dance Routine

    #1 Taunt
    k1.JMOVE(0, -20, -130, -10, 45, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(0, -20, -115, 10, -5, 0)  # Tilt downward with slight rotation
    k1.JMOVE(0, -20, -130, -10, 45, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(0, -20, -115, 10, -5, 0)  # Tilt downward with slight rotation
    # #2 start Bow
    k1.JMOVE(0, -20, -80, 0, -60, 0)  # Head bob up
    k1.JMOVE(0, -20, -120, 0, -90, 0)  # Head bob down
    k1.JMOVE(0, -20, -80, 0, -60, 0)  # Head bob up
    
    #5 Turning and dancing
    k1.SPEED(60)
    k1.JMOVE(-5, -20, -115, 180, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-10, -20, -130, 160, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-15, -20, -100, 210, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-20, -20, -130, 220, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-25, -20, -100, 180, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-30, -20, -130, 160, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-35, -20, -100, 180, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-40, -20, -130, 220, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-40, -20, -100, 180, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-40, -20, -130, 180, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-40, -20, -100, 180, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-40, -20, -130, 180, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-45, -20, -105, 180, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-50, -20, -130, 160, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-55, -20, -100, 180, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-60, -20, -130, 220, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-65, -20, -105, 180, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-70, -20, -130, 160, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-75, -20, -100, 180, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-80, -20, -130, 220, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-90, -20, -100, 180, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-90, -20, -130, 180, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-90, -20, -100, 180, -15, 0)  # Tilt downward with slight rotation
    k1.JMOVE(-90, -20, -130, 180, 25, 0)  # Tilt upward with slight counter rotation
    k1.JMOVE(-90, -20, -105, 180, 0, 0)  # Tilt downward with slight rotation

    #4 Spiraling Up and Down
    k1.SPEED(60)
    k1.JMOVE(0, 15, -50, 90, -60, 0)  # Spiral upward with rotation
    k1.JMOVE(-10, -35, -120, -90, 60, 0)  # Spiral downward with rotation
    k1.JMOVE(-20, 15, -90, 90, -60, 0)  # Spiral upward with rotation
    k1.JMOVE(-30, -35, -120, -90, 60, 0)  # Spiral downward with rotation 
    k1.JMOVE(-40, 15, -90, 90, -60, 0)  # Spiral upward with rotation
    k1.JMOVE(-40, -35, -120, -90, 60, 0)  # Spiral downward with rotation 
    #3 Twisting Dips with Added Rotations
    k1.SPEED(70)
    k1.JMOVE(-30, 20, -110, 90, -60, 0)  # Twist and dip left
    k1.JMOVE(0, -20, -110, -90, 60, 0)  # Twist and dip right
    k1.JMOVE(-30, 20, -110, 180, -60, 0)  # Twist and dip left with rotation
    k1.JMOVE(0, -20, -110, -180, 60, 0)  # Twist and dip right with rotation

    #6 Diagonal Sway
    k1.JMOVE(0, -30, -60, -90, 45, 0)  # Sway diagonally up-left
    k1.JMOVE(0, 0, -120, 210, 45, 0)  # Sway diagonally down-left
    k1.JMOVE(-45, 30, -100, 45, -45, 0)  # Sway diagonally down-right
    k1.JMOVE(0, -30, -60, -25, 60, 0)  # Sway diagonally up-left
    
    #7 Rotate and Dip
    k1.JMOVE(-45, 30, -60, 45, -90, 0)  # Sway diagonally up-right
    k1.JMOVE(-25, -40, -120, 0, -45, 0)  # Sway diagonally up-right

    #8 Circular Sweep
    k1.JMOVE(-30, 20, -90, 180, -60, 0)  # Sweep to the left
    k1.JMOVE(0, -20, -90, -180, 60, 0)  # Sweep to the right
    
    #15 Mirrored diagonal sway
    k1.JMOVE(0, -30, -120, -45, 45, 0)  # Arm 1 sways diagonally down-left
    k1.JMOVE(0, 15, -90, 90, -90, 0)  # Arm 1 moves toward center

    #16 Rotate around a shared point
    k1.JMOVE(-30, 20, -90, 180, -60, 0)  # Arm 1 rotates clockwise
    k1.JMOVE(0, -20, -90, 90, -45, 0)  # Arm 1 moves in a circular path


    #18 Tilt and Rotate 
    k1.JMOVE(0, 45, -80, 180, -60, 0)  # Tilt backward and rotate
    k1.JMOVE(0, -60, -90, -180, 60, 0)  # Tilt forward and rotate back
    k1.JMOVE(-30, 30, -60, 90, -45, 0)  # Move in a semi-circle left
    k1.JMOVE(0, -30, -70, -90, 45, 0)  # Complete the semi-circle to the right
    k1.JMOVE(-30, 45, -80, 180, -60, 0)  # Tilt backward and rotate
    k1.JMOVE(-60, -60, -90, -180, 60, 0)  # Tilt forward and rotate back
 

    #21 Dramatic pose
    #k1.JMOVE(0, 45, 45, 90, -30, 0)  # Arm rises top right with a twist
    k1.JMOVE(0, 50, -70, -180, 90, 0)       # Arm flicks to the right
    k1.JMOVE(-90, 0, -50, 180, 90, 0)  # Ends with a dramatic full rotation
    k1.JMOVE(0, 50, -60, -180, 90, 0)       # Arm flicks to the right
    k1.JMOVE(0, -20, -20, 0, -90, 0)     # Arm flicks to the left
    k1.JMOVE(-90, 0, -50, 180, 90, 0)  # Ends with a dramatic full rotation
    k1.JMOVE(0, -20, -20, 0, -90, 0)     # Arm flicks to the left

    #22 Spiral Rise
    k1.SPEED(70)  
    k1.JMOVE(0, -10, -90, -360, 0, 0)  # Arm rises top right with a twist
    k1.JMOVE(-90, -10, -100, 360, 0, 0)  # Repositions rightside
    k1.JMOVE(-60, 45, -80, -210, 0, 0)  # spins down rightside
    k1.JMOVE(0, 45, -80, 360, 0, 0)  # spins bottomside
    k1.JMOVE(0, -10, -90, -360, 0, 0)  # Spins around Z-axis while slightly rising leftside

    k1.JMOVE(0, 0, -120, -180, 90, 0)  # Spins back around Z-axis while lowering
    k1.JMOVE(-20, 40, -30, 90, -30, 0)  # Arm rises top right with a twist
    k1.JMOVE(0, 0, -60, 0, -60, 0)  # Nod forward
    k1.JMOVE(0, 0, -120, 0, -90, 0)  # Nod downward
    k1.JMOVE(0, 0, -90, 0, -90, 0)  # Return to home position

    #23 Faces sideways and waves
    k1.SPEED(50)
    k1.JMOVE(0, 0, 0, 90, -90, 0) #Rises straight and turns head
    k1.JMOVE(0, 30, 0, 90, -90, 0) #Moves to side
    k1.JMOVE(0, -20, 0, 90, -90, 0) #Moves to side
    k1.JMOVE(0, 30, 0, 90, -90, 0) #Moves to side
    k1.JMOVE(0, -20, 0, 90, -90, 0) #Moves to side
    k1.JMOVE(0, 0, 0, 90, -90, 0) #Stops upright
    
    #24 Faces sideways and bow's
    k1.JMOVE(-90, 0, 0, 0, 0, 0) #Looks up straight
    k1.JMOVE(-90, 0, -110, 0, -90, 0) #bow's and lower's the end of arm tool (head)
    k1.JMOVE(-90, 0, 0, 0, 0, 0) #Looks up straight
    k1.JMOVE(0, 0, -90, 0, 0, 0) #Looks forward
    
   
  
    ismoving = False

def Get_moving():
    return ismoving

if __name__ == "__main__":
    dance_1()