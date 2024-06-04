.PROGRAM main_robot1()
    ; *******************************************************************
    ;
    ; Program:      main_robot1
    ; Comment:      
    ; Author:       Shiyar Jamo | Coder Shiyar HHS Delft
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
        PRINT "IT IS 0"  
      END

      IF $cnt[0] == "1" THEN
        PRINT "IT IS 1, Dance Mode robot 1"
        SPEED 80 ALWAYS
        ACCURACY 20 ALWAYS
        ACCEL 100 ALWAYS
        DECEL 100 ALWAYS
        PRINT "IT IS 1, Dance Mode robot 1"
      
        SPEED 50 ALWAYS
        FOR .i = 1 TO 2
          JMOVE #[0,-35,0,0,45,-45] ; Second move, it moves left on our look
          JMOVE #[0,-35,-70,0,-45,45] ; 3 move, it moves join 3 like saying hello  
        END
      
        JMOVE #[0,-35,0,0,0,0] ; Second move, it moves left on our look
        SPEED 60 ALWAYS
        JMOVE #[-43.311,65.532,0,0,0,0]  ; 5 move, it moves to back a little bit
        JMOVE #[-125.484,63.402, 0,0,0,0] ; 6 move, it moves to back a little bit
      
        SPEED 100 ALWAYS
        JMOVE #[-20.813, 27.551,0,0,0,0]
        SPEED 57 ALWAYS
        JMOVE #[-66.735, 84.717, -2.286,  -0.365, -23.469, 0.002]
        JMOVE #[-81.493, 44.063, -21.355, -0.365, -23.469, 0.001]
        JMOVE #[-96.563, 99.333, -2.368,  -0.365, -23.469, 0.002]
        JMOVE #[-104.075,53.074, -3.346,  33.003, -2.569,  0.002]
        JMOVE #[-119.145,106.458, 9.610, -97.724, -2.569,  0.002]
        JMOVE #[-129.028, 53.913, 0.000,   0.000, -36.670, 0.000]
      
        SPEED 15 ALWAYS
        JMOVE #[-50.175,  53.913, 0.000,   0.000, -36.670, 0.000]
        JMOVE #[-129.028, 53.913, 0.000,   0.000, -36.670, 0.000]
        JMOVE #[-50.175,  53.913, 0.000,   0.000, -36.670, 0.000]
        ; 25 SECONDS INTO VIDEO
        SPEED 70 ALWAYS
        JMOVE #[-62.919,  53.913, 26.726,  0.000,  0.000,  0.000]
        JMOVE #[-72.579,  76.125,-18.416,-90.000,  0.000,  0.000]
        JMOVE #[-84.607,  53.913, 26.726,  0.000,  0.000,  0.000]
        JMOVE #[-96.579,  76.125,-18.416,-90.000,  0.000,  0.000]
        JMOVE #[-108.607, 53.913, 26.726,  0.000,  0.000,  0.000]
        JMOVE #[-120.579, 76.125,-18.416,-90.000,  0.000,  0.000]
        JMOVE #[-108.607, 53.913, 26.726,  0.000,  0.000,  0.000]
        JMOVE #[-96.579,  76.125,-18.416,-90.000,  0.000,  0.000]
        JMOVE #[-84.607,  53.913, 26.726,  0.000,  0.000,  0.000]
        JMOVE #[-72.579,  76.125,-18.416,-90.000,  0.000,  0.000]
        JMOVE #[-62.919,  53.913, 26.726,  0.000,  0.000,  0.000]
        ; 30 SECONDS IN 
      
        SPEED 53 ALWAYS
        FOR .i = 1 TO 4
          JMOVE #[-90,70,-45,0,0,0]
          JMOVE #[-90,50, 35,0,0,0]
        END
        ; FINAL MOTION
        TWAIT 3
        JMOVE #[-50.175,  53.913, -5,  0.000, 0.000, 15.000]
        JMOVE #[-50.175,  53.913, -10, 0.000, 0.000, 30.000]
        JMOVE #[-50.175,  53.913, -15, 0.000, 0.000, 45.000]
        JMOVE #[-50.175,  53.913, -20, 0.000, 0.000, 30.000]
        JMOVE #[-50.175,  53.913, -25, 0.000, 0.000, 15.000]
        JMOVE #[-50.175,  53.913, -30, 0.000, 0.000, 30.000]
        JMOVE #[-50.175,  53.913, -35, 0.000, 0.000, 45.000]
        JMOVE #[-50.175,  53.913, -40, 0.000, 0.000, 30.000]
        JMOVE #[-50.175,  53.913, -45, 0.000, 0.000, 15.000]
        TWAIT 0.25
        JMOVE #[-50.175,  53.913, -40, 0.000, 0.000, 30.000]
        JMOVE #[-50.175,  53.913, -35, 0.000, 0.000, 45.000]
        JMOVE #[-50.175,  53.913, -30, 0.000, 0.000, 30.000]
        JMOVE #[-50.175,  53.913, -25, 0.000, 0.000, 15.000]
        JMOVE #[-50.175,  53.913, -20, 0.000,0.000,0.000]
    END
      

      IF $cnt[0] == "3" THEN
        PRINT "IT IS 3 tv mode"  
        SPEED 100 ALWAYS
        JMOVE #[ -159.999, -2.405, -3.441, 100.636, 87.897, 184.071]
      END
      
      IF $cnt[0] == "4" THEN
        SPEED 50 ALWAYS
        PRINT "IT IS 4 detection people mode"  
        JMOVE #[-65.050, 6.617 ,-91.223, 90.552,   -2.919,92.648]
      END

      IF $cnt[0] == "5" THEN
        SPEED 60 ALWAYS
        PRINT "IT IS 5 detection emotion mode"  
        JMOVE #[-95.996,     7.024,   -11.651,    90.415,     1.545,   269.536]
        JMOVE #[ -77.661,    16.977,   -37.075,    93.348,    15.480,   262.938]
        JMOVE #[ -98.411,    28.083,   -50.928,    93.348,    -3.589,   167.597]
        JMOVE #[ -69.702,    33.844,   -55.492,    89.682,    -3.589,   114.793]
        JMOVE #[ -69.701,    60.146,   -25.016,    89.682,    -3.589,    94.990] ; end point
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