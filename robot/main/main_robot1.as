.PROGRAM main_robot1()
    ; *******************************************************************
    ; Program:      main_robot1
    ; Comment:      
    ; Author:       Shiyar Jamo | Coder Shiyar HHS Delft | Ixent Cornell
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
        
      IF $cnt[0] == "1" THEN
        PRINT "IT IS 1, Dance Mode robot 1"
        SPEED 55 ALWAYS
        ACCURACY 32 ALWAYS
        ACCEL 100 ALWAYS
        DECEL 100 ALWAYS      
  
        FOR .i = 1 TO 2
          JMOVE #[0,-35,0,180,45,0] ; Second move, it moves left on our look
          JMOVE #[0,-35,-70,180,-45,0] ; 3 move, it moves join 3 like saying hello  
        END
      
        SPEED 50 ALWAYS
        JMOVE #[0,-35,0,180,0,0] ; Second move, it moves left on our look

        JMOVE #[-43.311,65.532,0,180,0,0]  ; 5 move, it moves to back a little bit
        JMOVE #[-125.484,63.402, 0,180,0,0] ; 6 move, it moves to back a little bit
      
        SPEED 100 ALWAYS
        JMOVE #[-20.813, 27.551,0,180,0,0]
        SPEED 57 ALWAYS
        JMOVE #[-66.735, 84.717, -2.286,  -0.365, -23.469, 180]
        JMOVE #[-81.493, 44.063, -21.355, -0.365, -23.469, 180]
        JMOVE #[-96.563, 99.333, -2.368,  -0.365, -23.469, 180]
        JMOVE #[-104.075,53.074, -3.346,  33.003, -2.569,  180]
        JMOVE #[-119.145,106.458, 9.610, -97.724, -2.569,  180]
        JMOVE #[-129.028, 53.913, 0.000,   0.000, -36.670, 180]
      
        SPEED 15 ALWAYS
        JMOVE #[-50.175,  53.913, 0.000,   0.000, -36.670, 180]
        JMOVE #[-129.028, 53.913, 0.000,   0.000, -36.670, 180]
        JMOVE #[-50.175,  53.913, 0.000,   0.000, -36.670, 180]
        ; 25 SECONDS INTO VIDEO
        SPEED 70 ALWAYS
        JMOVE #[-62.919,  53.913, 26.726,  0.000,  0.000,  180]
        JMOVE #[-72.579,  76.125,-18.416,-90.000,  0.000,  180]
        JMOVE #[-84.607,  53.913, 26.726,  0.000,  0.000,  180]
        JMOVE #[-96.579,  76.125,-18.416,-90.000,  0.000,  180]
        JMOVE #[-108.607, 53.913, 26.726,  0.000,  0.000,  180]
        JMOVE #[-120.579, 76.125,-18.416,-90.000,  0.000,  180]
        JMOVE #[-108.607, 53.913, 26.726,  0.000,  0.000,  180]
        JMOVE #[-96.579,  76.125,-18.416,-90.000,  0.000,  180]
        JMOVE #[-84.607,  53.913, 26.726,  0.000,  0.000,  180]
        JMOVE #[-72.579,  76.125,-18.416,-90.000,  0.000,  180]
        JMOVE #[-62.919,  53.913, 26.726,  0.000,  0.000,  180]
        ; 30 SECONDS IN 
      

        ACCEL 80 ALWAYS
        DECEL 80 ALWAYS
        SPEED 50 ALWAYS
        FOR .i = 1 TO 4
          JMOVE #[-90,70,-45,0,0,180]
          JMOVE #[-90,50, 35,0,0,180]
        END
        ; FINAL MOTION
        TWAIT 3
        JMOVE #[-50.175,  53.913, -5,  0.000, 0.000, 165]
        JMOVE #[-50.175,  53.913, -10, 0.000, 0.000, 150]
        JMOVE #[-50.175,  53.913, -15, 0.000, 0.000, 135]
        JMOVE #[-50.175,  53.913, -20, 0.000, 0.000, 150]
        JMOVE #[-50.175,  53.913, -25, 0.000, 0.000, 165]
        JMOVE #[-50.175,  53.913, -30, 0.000, 0.000, 150]
        JMOVE #[-50.175,  53.913, -35, 0.000, 0.000, 135]
        JMOVE #[-50.175,  53.913, -40, 0.000, 0.000, 150]
        JMOVE #[-50.175,  53.913, -45, 0.000, 0.000, 165]
        TWAIT 0.25
        JMOVE #[-50.175,  53.913, -40, 0.000, 0.000, 150]
        JMOVE #[-50.175,  53.913, -35, 0.000, 0.000, 135]
        JMOVE #[-50.175,  53.913, -30, 0.000, 0.000, 150]
        JMOVE #[-50.175,  53.913, -25, 0.000, 0.000, 165]
        JMOVE #[-50.175,  53.913, -20, 0.000,0.000,180]
    END
    
    IF $cnt[0] == "7" THEN
      PRINT "IT IS 7 pong game" 
      SPEED 70 ALWAYS
      JMOVE #[ -159.999, -2.405, -3.441, 0, 0, 0]
      PRINT "Moving to bottom point" 
      JMOVE TRANS(-2.3, 386.626, 150, 91.7, 92, 95.7)
      TWAIT 0.35
      ACCEL 10 ALWAYS
      DECEL 10 ALWAYS
      SPEED 5 ALWAYS
      ;     X         Y       Z        O          A         T
      ;  -2.308    386.626   -50    91.702     92.001    95.700
      
      PRINT "Moving to top point" 
      SPEED 3 S
      LMOVE TRANS(-2.3, 386.626, 440, 91.7, 92, 95.7)
      ;     X         Y       Z        O          A         T
      ;  -2.308    386.626   300    91.702     92.001    95.700
      PRINT "WAIT 5s"
      TWAIT 4
    
      PRINT "Moving to bottom point" 
      SPEED 9.2 S
      LMOVE TRANS(-2.3, 386.626, 90, 91.7, 92, 95.7)
      
      
      PRINT "Moving to z 175" 
      SPEED 2.9 S 
      LMOVE TRANS(-2.3, 386.626, 240, 91.7, 92, 95.7)
      
      PRINT "Moving to bottom point" 
      SPEED 2.5 S 
      LMOVE TRANS(-2.3, 386.626, 125, 91.7, 92, 95.7)
      LMOVE TRANS(-2.3, 386.626, 90, 91.7, 92, 95.7)
      PRINT "WAIT 3.9s"
      TWAIT 3
      PRINT "Moving to top point"
      ACCEL 20 ALWAYS 
      SPEED 2.5 S
      JMOVE TRANS(-2.3, 386.626, 440, 91.7, 92, 95.7)
      ACCEL 10 ALWAYS
      TWAIT 0.5
      
      PRINT "Moving to bottom point" 
      LMOVE TRANS(-2.3, 386.626, 90, 91.7, 92, 95.7)
      
      PRINT "Moving to stop point" 
      SPEED 2 S
      LMOVE TRANS(-2.3, 386.626, 160, 91.7, 92, 95.7)

      ACCEL 80 ALWAYS
      DECEL 80 ALWAYS
      SPEED 100 ALWAYS
END

      IF $cnt[0] == "3" THEN
        PRINT "IT IS 3 tv mode"  
        SPEED 70 ALWAYS
        JMOVE #[ -159.999, -2.405, -3.441, 0, 0, 180]
      END
      
      IF $cnt[0] == "4" THEN
        SPEED 50 ALWAYS
        PRINT "IT IS 4 detection people mode"  
        JMOVE #[-65.050, 6.617 ,-91.223, 0,   0,183]
      END

      IF $cnt[0] == "5"   THEN
        SPEED 60 ALWAYS
        PRINT "IT IS 5 detection emotion mode"  
        JMOVE #[-95.996,     7.024,   -11.651,    0,     1.545,   180]
        JMOVE #[ -77.661,    16.977,   -37.075,   0,    15.480,   150]
        JMOVE #[ -98.411,    28.083,   -50.928,   0,    -3.589,   140]
        JMOVE #[ -69.702,    33.844,   -55.492,   0,    -3.589,    160]
        JMOVE #[ -69.701,    60.146,   -35.016,    0.682,    -3.589,    180]
      END
      
      IF $cnt[0] == "6"   THEN
        SPEED 60 ALWAYS
        PRINT "IT IS 5 detection emotion mode"  
        JMOVE #[-105.996,     7.024,   -11.651,    0,     1.545,   170]
        JMOVE #[ -67.661,    16.977,   -37.075,   0,    15.480,   130]
        JMOVE #[ -108.411,    28.083,   -50.928,   0,    -3.589,   150]
        JMOVE #[ -69.702,    33.844,   -55.492,   0,    -3.589,    165]
        JMOVE #[ -69.701,    60.146,   -35.016,    0.682,    -3.589,    180]
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
