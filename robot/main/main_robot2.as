.PROGRAM main_robot2()
    ; *******************************************************************
    ;
    ; Program:      main_robot2
    ; Comment:      
    ; Author:       Shiyar Jamo | Coder Shiyar HHS Delft, Ixent Cornella
    ;
    ; Date:         5/27/2024
    ;
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
          JMOVE #[0, 26,0, 0 , -90, 0, 0]
          JMOVE #[0, -26,0, 0 , -90, 0, 0]
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
            JMOVE #[0,-35,0,0,45,-45] ; Second move, it moves left on our look
            JMOVE #[0,-35,-70,0,-45,45] ; 3 move, it moves join 3 like saying hello  
          END
          SPEED 21.5 ALWAYS
          JMOVE #[0,-35,0,0,0,0] ; Second move, it moves left on our look
        
          SPEED 50 ALWAYS
          JMOVE #[43.311,65.532,0,0,0,0]  ; 5 move, it moves to back a little bit
          JMOVE #[125.484,63.402, 0,0,0,0] ; 6 move, it moves to back a little bit
          
          SPEED 100 ALWAYS
          ACCEL 75 ALWAYS
          JMOVE #[20.813, 27.551,0,0,0,0]
          ACCEL 50 ALWAYS
          SPEED 30 ALWAYS
          JMOVE #[66.735, 84.717, -2.286,  -0.365, -23.469, 0.002]
          JMOVE #[81.493, 44.063, -21.355, -0.365, -23.469, 0.001]
          JMOVE #[96.563, 99.333, -2.368,  -0.365, -23.469, 0.002]
          JMOVE #[104.075,53.074, -3.346,  33.003, -2.569,  0.002]
          JMOVE #[119.145,106.458, 9.610, -97.724, -2.569,  0.002]
          JMOVE #[129.028, 53.913, 0.000,   0.000, -36.670, 0.000]
          
          SPEED 10 ALWAYS
          JMOVE #[50.175,  53.913, 0.000,   0.000, -36.670, 0.000]
          JMOVE #[129.028, 53.913, 0.000,   0.000, -36.670, 0.000]
          JMOVE #[50.175,  53.913, 0.000,   0.000, -36.670, 0.000]
          ; 25 SECONDS INTO VIDEO
          SPEED 95 ALWAYS
          ACCEL 85 ALWAYS
          DECEL 85 ALWAYS
          JMOVE #[62.919,  53.913, 26.726,  0.000,  0.000,  0.000]
          JMOVE #[72.579,  76.125,-18.416,-90.000,  0.000,  0.000]
          JMOVE #[84.607,  53.913, 26.726,  0.000,  0.000,  0.000]
          JMOVE #[96.579,  76.125,-18.416,-90.000,  0.000,  0.000]
          JMOVE #[108.607, 53.913, 26.726,  0.000,  0.000,  0.000]
          JMOVE #[120.579, 76.125,-18.416,-90.000,  0.000,  0.000]
          JMOVE #[108.607, 53.913, 26.726,  0.000,  0.000,  0.000]
          JMOVE #[96.579,  76.125,-18.416,-90.000,  0.000,  0.000]
          JMOVE #[84.607,  53.913, 26.726,  0.000,  0.000,  0.000]
          JMOVE #[72.579,  76.125,-18.416,-90.000,  0.000,  0.000]
          JMOVE #[62.919,  53.913, 26.726,  0.000,  0.000,  0.000]
          ; 30 SECONDS IN 
        
          ACCEL 50 ALWAYS
          DECEL 50 ALWAYS
          SPEED 32.5 ALWAYS
          FOR .i = 1 TO 4
            JMOVE #[90,70,-45,0,0,0]
            JMOVE #[90,50, 35,0,0,0]
          END
          ; FINAL MOTION
          TWAIT 3
          ACCURACY 10 ALWAYS
          JMOVE #[50.175,  53.913, -5,  0.000, 0.000, 15.000]
          JMOVE #[50.175,  53.913, -10, 0.000, 0.000, 30.000]
          JMOVE #[50.175,  53.913, -15, 0.000, 0.000, 45.000]
          JMOVE #[50.175,  53.913, -20, 0.000, 0.000, 30.000]
          JMOVE #[50.175,  53.913, -25, 0.000, 0.000, 15.000]
          JMOVE #[50.175,  53.913, -30, 0.000, 0.000, 30.000]
          JMOVE #[50.175,  53.913, -35, 0.000, 0.000, 45.000]
          JMOVE #[50.175,  53.913, -40, 0.000, 0.000, 30.000]
          JMOVE #[50.175,  53.913, -45, 0.000, 0.000, 15.000]
          TWAIT 0.25
          JMOVE #[50.175,  53.913, -40, 0.000, 0.000, 30.000]
          JMOVE #[50.175,  53.913, -35, 0.000, 0.000, 45.000]
          JMOVE #[50.175,  53.913, -30, 0.000, 0.000, 30.000]
          JMOVE #[50.175,  53.913, -25, 0.000, 0.000, 15.000]
          JMOVE #[50.175,  53.913, -20, 0.000, 0.000, 0.000]
          
          SPEED 100 ALWAYS
          ACCURACY 5 ALWAYS
          ACCEL 80 ALWAYS
          DECEL 80 ALWAYS
      END
        
      IF $cnt[0] == "3" THEN
        PRINT "IT IS 3 tv mode"  
        SPEED 100 ALWAYS
        JMOVE #[ 159.999,    -2.405,    -3.441,   100.636,    87.897,   184.071]
      END
      
      IF $cnt[0] == "2" THEN
        PRINT "IT IS 2, game mode" 
        SPEED 100 ALWAYS 
        ;JMOVE #[0, 0, 0, 0, 0, 0]
        FOR .i = 1 TO 3
          JMOVE #[63.168, 64.145, 0.003, 0.001, -0.000, -0.002] 
          ;TWAIT 1
          JMOVE #[63.168, 90.260,0.003,  0.001, -0.001,  -0.002]
        END
        PRINT " MOVING END"
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