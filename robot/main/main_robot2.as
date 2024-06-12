.PROGRAM main_robot2()
    ; *******************************************************************
    ;
    ; Program:      main_robot2
    ; Comment:      
    ; Author:       Shiyar Jamo | Coder Shiyar HHS Delft, Ixent Cornella
    ;
    ; Date:         5/27/2024
    ; *******************************************************************
    ;
    timeout = 120
    answer_timeout = 3
    ip[1] = 192
    ip[2] = 168
    ip[3] = 0
    ip[4] = 10  
    port = 10010
    numbytes = 1
    ret = 0

    WHILE TRUE DO
      TWAIT 1
      UDP_RECVFROM ret, port, $cnt[0], numbytes, timeout, ip[1]
      IF ret <> 0 THEN
        PRINT "No data received within timeout period or error code: ", ret
        ; Continue to the next iteration without halting
      ELSE
        
      PRINT "Message: ", $cnt[0]
      IF $cnt[0] == "0" THEN
        PRINT "IT IS 0, Hello Mode"
        SPEED 70 ALWAYS
        FOR .i = 1 TO 2
          JMOVE #[159.999,   -25.999,     0.407,   -12,    25.343,  90]
          JMOVE #[159.999,   -26.000,     0.408 ,    -12,   -35.013,  90]
        END
      END

      IF $cnt[0] == "1" THEN
          PRINT "IT IS 1, Dance Mode robot 2"
          SPEED 100 ALWAYS
          ACCURACY 5 ALWAYS
          ACCEL 50 ALWAYS
          DECEL 50 ALWAYS
        
          PRINT "IT IS 1, Dance Mode robot 2"
        
          SPEED 42.5 ALWAYS
          FOR .i = 1 TO 2
            JMOVE #[0,-35,0,0,45,90] ; Second move, it moves left on our look
            JMOVE #[0,-35,-70,0,-45,90] ; 3 move, it moves join 3 like saying hello  
          END
          SPEED 21.5 ALWAYS
          JMOVE #[0,-35,0,0,0,90] ; Second move, it moves left on our look
        
          SPEED 50 ALWAYS
          JMOVE #[43.311,65.532,0,0,0,90]  ; 5 move, it moves to back a little bit
          JMOVE #[125.484,63.402, 0,0,0,90] ; 6 move, it moves to back a little bit
          
          SPEED 100 ALWAYS
          ACCEL 75 ALWAYS
          JMOVE #[20.813, 27.551,0,0,0,90]
          ACCEL 50 ALWAYS
          SPEED 30 ALWAYS
          JMOVE #[66.735, 84.717, -2.286,  -0.365, -23.469, 90]
          JMOVE #[81.493, 44.063, -21.355, -0.365, -23.469, 90]
          JMOVE #[96.563, 99.333, -2.368,  -0.365, -23.469, 90]
          JMOVE #[104.075,53.074, -3.346,  33.003, -2.569,  90]
          JMOVE #[119.145,106.458, 9.610, -90, -2.569,  90]
          JMOVE #[129.028, 53.913, 0.000,   0.000, -36.670, 90]
          
          SPEED 10 ALWAYS
          JMOVE #[50.175,  53.913, 0.000,   0.000, -36.670, 90]
          JMOVE #[129.028, 53.913, 0.000,   0.000, -36.670, 90]
          JMOVE #[50.175,  53.913, 0.000,   0.000, -36.670, 90]
          ; 25 SECONDS INTO VIDEO
          SPEED 95 ALWAYS
          ACCEL 85 ALWAYS
          DECEL 85 ALWAYS
          JMOVE #[62.919,  53.913, 26.726,  0.000,  0.000, 90]
          JMOVE #[72.579,  76.125,-18.416,-90.000,  0.000,  90]
          JMOVE #[84.607,  53.913, 26.726,  0.000,  0.000,  90]
          JMOVE #[96.579,  76.125,-18.416,-90.000,  0.000, 90]
          JMOVE #[108.607, 53.913, 26.726,  0.000,  0.000,  90]
          JMOVE #[120.579, 76.125,-18.416,-90.000,  0.000,  90]
          JMOVE #[108.607, 53.913, 26.726,  0.000,  0.000,  90]
          JMOVE #[96.579,  76.125,-18.416,-90.000,  0.000,  90]
          JMOVE #[84.607,  53.913, 26.726,  0.000,  0.000, 90]
          JMOVE #[72.579,  76.125,-18.416,-90.000,  0.000,  90]
          JMOVE #[62.919,  53.913, 26.726,  0.000,  0.000, 90]
          ; 30 SECONDS IN 
        
          ACCEL 50 ALWAYS
          DECEL 50 ALWAYS
          SPEED 32.5 ALWAYS
          FOR .i = 1 TO 4
            JMOVE #[90,70,-45,0,0,90]
            JMOVE #[90,50, 35,0,0,90]
          END
          ; FINAL MOTION
          TWAIT 3
          ACCURACY 10 ALWAYS
          JMOVE #[50.175,  53.913, -5,  0.000, 0.000, 75]
          JMOVE #[50.175,  53.913, -10, 0.000, 0.000, 60]
          JMOVE #[50.175,  53.913, -15, 0.000, 0.000, 45]
          JMOVE #[50.175,  53.913, -20, 0.000, 0.000, 60]
          JMOVE #[50.175,  53.913, -25, 0.000, 0.000, 75]
          JMOVE #[50.175,  53.913, -30, 0.000, 0.000, 60]
          JMOVE #[50.175,  53.913, -35, 0.000, 0.000, 45]
          JMOVE #[50.175,  53.913, -40, 0.000, 0.000, 60]
          JMOVE #[50.175,  53.913, -45, 0.000, 0.000, 75]
          TWAIT 0.25
          JMOVE #[50.175,  53.913, -40, 0.000, 0.000, 60]
          JMOVE #[50.175,  53.913, -35, 0.000, 0.000, 45]
          JMOVE #[50.175,  53.913, -30, 0.000, 0.000, 60]
          JMOVE #[50.175,  53.913, -25, 0.000, 0.000, 75]
          JMOVE #[50.175,  53.913, -20, 0.000, 0.000, 90]
          
          SPEED 100 ALWAYS
          ACCURACY 5 ALWAYS
          ACCEL 80 ALWAYS
          DECEL 80 ALWAYS
      END
      
      IF $cnt[0] == "2" THEN
        PRINT "IT IS 2, game mode" 
        SPEED 100 ALWAYS 
        ;JMOVE #[0, 0, 0, 0, 0, 0]
        FOR .i = 1 TO 3
          JMOVE #[63.168, 64.145, 0.003, 0, -0.000, 90] 
          ;TWAIT 1
          JMOVE #[63.168, 90.260,0.003, 0, -0.001, 90]
        END
        PRINT " MOVING END"
      END

      IF $cnt[0] == "3" THEN
        PRINT "IT IS 3 tv mode"  
        SPEED 70 
        JMOVE #[ 159.999,  0.022,    -0.101,   0,     0.077, 180]
      END
      

      
      IF $cnt[0] == "7" THEN
        SPEED 70 ALWAYS
	; MOVE TO TV MODE FIRST TO PREVENT MOVEMENT ERRORS IN CONTROLLER
        JMOVE #[ 159.999,  0.022,    -0.101,   0,     0.077, 180]

        ACCEL 20 ALWAYS
        DECEL 20 ALWAYS
        SPEED 20 ALWAYS
        ;     X         Y       Z        O          A         T
        ;     0       458.2   370.6     90        46.25      77
        ;                      17
        PRINT "MOVING TO Y190 IN 1 SECOND(s)"
          LMOVE TRANS(0, 525,175, 90, 8, 90)
        
        SPEED 3 S
        PRINT "MOVING TO TOP IN 3 SECOND(s)"
        LMOVE TRANS(0, 525,370, 90, 8, 90)
        TWAIT 4.5
        SPEED 4 S
        PRINT "MOVING TO Y210 IN 4 SECOND(s)"
          LMOVE TRANS(0, 525,195, 90, 8, 90)
        TWAIT 1 
        ; 12 SECS 
        
        SPEED 2.8 S
        LMOVE TRANS(0, 525,10, 90, 8, 90)
        TWAIT 1.5
        
        SPEED 2.8 S
        PRINT "MOVING TO Y210 IN 3 SECOND(s)"
          LMOVE TRANS(0, 525,180, 90, 8, 90)
        TWAIT 1.4
        
        SPEED 2.5 S
        LMOVE TRANS(0, 525,30, 90, 8, 90)
        TWAIT 6
        ; 25 SECS BEFORE WAIT
        
        SPEED 2 S
        LMOVE TRANS(0, 525,280, 90, 8, 90)
        TWAIT 2
        
        SPEED 2 S
        LMOVE TRANS(0, 525,60, 90, 8, 90)

        SPEED 4 S
        LMOVE TRANS(0, 525,200, 90, 8, 90)
        ACCEL 70 ALWAYS
        DECEL 70 ALWAYS
      END

      ; Send confirmation message
      $cnt[0] = $ENCODE (/D, numbytes)
      UDP_SENDTO ret, ip[1], port, $cnt[0], 1, answer_timeout
      IF ret <> 0 THEN
        PRINT "Error with the UDP send, code: ", ret
        ; Optionally handle send error but do not halt
      END
      END
    END

.END