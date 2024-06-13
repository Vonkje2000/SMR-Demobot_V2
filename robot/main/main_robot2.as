.PROGRAM main_robot2()
    ; *******************************************************************
    ;
    ; Program:      main_robot2
    ; Comment:      
    ; Author:       Shiyar Jamo | Coder Shiyar HHS Delft, Ixent Cornella
    ;
    ; Date:         13/06/2024
    ; *******************************************************************
    ;
    ; VARIABLE DECLARATION
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
      ; This program will always recover UDP data for the robot to know what it is supposed to do.
      TWAIT 1
      UDP_RECVFROM ret, port, $cnt[0], numbytes, timeout, ip[1]
      IF ret <> 0 THEN
        PRINT "No data received within timeout period or error code: ", ret
        ; Continue to the next iteration without halting
      ELSE
        PRINT "Message: ", $cnt[0]
        ; First case: Hello mode. The robot waves to the users.
        IF $cnt[0] == "0" THEN
          PRINT "IT IS 0, Hello Mode"
          SPEED 70 ALWAYS
          FOR .i = 1 TO 2
            JMOVE #[160, -25.999, 0.407, -12, 25.343, 90]
            JMOVE #[160, -26, 0.408, -12, -35.013, 90]
          END
        END
        ; Second case: Dance mode.
        IF $cnt[0] == "1" THEN
          ; Set parameters for the dance.
          SPEED 100 ALWAYS
          ACCURACY 5 ALWAYS
          ACCEL 50 ALWAYS
          DECEL 50 ALWAYS
          PRINT "Dance Mode robot 2"
          ; All the following moves are for the robot to perform the dance
          SPEED 42.5 ALWAYS
          FOR .i = 1 TO 2
            JMOVE #[0, -35, 0, 0, 45, 90]; Second move, it moves left on our look
            JMOVE #[0, -35, -70, 0, -45, 90]; 3 move, it moves join 3 like saying hello
          END
          SPEED 21.5 ALWAYS
          JMOVE #[0, -35, 0, 0, 0, 90]; Second move, it moves left on our look
          SPEED 50 ALWAYS
          JMOVE #[43.311, 65.532, 0, 0, 0, 90]; 5 move, it moves to back a little bit
          JMOVE #[125.48, 63.402, 0, 0, 0, 90]; 6 move, it moves to back a little bit
          SPEED 100 ALWAYS
          ACCEL 75 ALWAYS
          JMOVE #[20.813, 27.551, 0, 0, 0, 90]
          ACCEL 50 ALWAYS
          SPEED 30 ALWAYS
          JMOVE #[66.735, 84.717, -2.286, -0.365, -23.469, 90]
          JMOVE #[81.493, 44.063, -21.355, -0.365, -23.469, 90]
          JMOVE #[96.563, 99.333, -2.368, -0.365, -23.469, 90]
          JMOVE #[104.07, 53.074, -3.346, 33.003, -2.569, 90]
          JMOVE #[119.15, 106.46, 9.61, -90, -2.569, 90]
          JMOVE #[129.03, 53.913, 0, 0, -36.67, 90]
          SPEED 10 ALWAYS
          JMOVE #[50.175, 53.913, 0, 0, -36.67, 90]
          JMOVE #[129.03, 53.913, 0, 0, -36.67, 90]
          JMOVE #[50.175, 53.913, 0, 0, -36.67, 90]
          ; 25 SECONDS INTO VIDEO
          SPEED 95 ALWAYS
          ACCEL 85 ALWAYS
          DECEL 85 ALWAYS
          JMOVE #[62.919, 53.913, 26.726, 0, 0, 90]
          JMOVE #[72.579, 76.125, -18.416, -90, 0, 90]
          JMOVE #[84.607, 53.913, 26.726, 0, 0, 90]
          JMOVE #[96.579, 76.125, -18.416, -90, 0, 90]
          JMOVE #[108.61, 53.913, 26.726, 0, 0, 90]
          JMOVE #[120.58, 76.125, -18.416, -90, 0, 90]
          JMOVE #[108.61, 53.913, 26.726, 0, 0, 90]
          JMOVE #[96.579, 76.125, -18.416, -90, 0, 90]
          JMOVE #[84.607, 53.913, 26.726, 0, 0, 90]
          JMOVE #[72.579, 76.125, -18.416, -90, 0, 90]
          JMOVE #[62.919, 53.913, 26.726, 0, 0, 90]
          ; 30 SECONDS IN
          ACCEL 50 ALWAYS
          DECEL 50 ALWAYS
          SPEED 32.5 ALWAYS
          FOR .i = 1 TO 4
            JMOVE #[90, 70, -45, 0, 0, 90]
            JMOVE #[90, 50, 35, 0, 0, 90]
          END
          ; FINAL MOTION
          TWAIT 3
          ACCURACY 10 ALWAYS
          JMOVE #[50.175, 53.913, -5, 0, 0, 75]
          JMOVE #[50.175, 53.913, -10, 0, 0, 60]
          JMOVE #[50.175, 53.913, -15, 0, 0, 45]
          JMOVE #[50.175, 53.913, -20, 0, 0, 60]
          JMOVE #[50.175, 53.913, -25, 0, 0, 75]
          JMOVE #[50.175, 53.913, -30, 0, 0, 60]
          JMOVE #[50.175, 53.913, -35, 0, 0, 45]
          JMOVE #[50.175, 53.913, -40, 0, 0, 60]
          JMOVE #[50.175, 53.913, -45, 0, 0, 75]
          TWAIT 0.25
          JMOVE #[50.175, 53.913, -40, 0, 0, 60]
          JMOVE #[50.175, 53.913, -35, 0, 0, 45]
          JMOVE #[50.175, 53.913, -30, 0, 0, 60]
          JMOVE #[50.175, 53.913, -25, 0, 0, 75]
          JMOVE #[50.175, 53.913, -20, 0, 0, 90]
          SPEED 100 ALWAYS
          ACCURACY 5 ALWAYS
          ACCEL 80 ALWAYS
          DECEL 80 ALWAYS
        END
        ; Rock Paper Scissors game
        IF $cnt[0] == "2" THEN
          PRINT "IT IS 2, game mode"
          SPEED 100 ALWAYS
          FOR .i = 1 TO 3
            JMOVE #[63.168, 64.145, 0.003, 0, 0, 90]
            ;TWAIT 1
            JMOVE #[63.168, 90.26, 0.003, 0, -0.001, 90]
          END
          PRINT " MOVING END"
        END
        ; TV Mode: the robots are placed in a way that the TV is more visible.
        IF $cnt[0] == "3" THEN
          PRINT "IT IS 3 tv mode"
          SPEED 70
          JMOVE #[160, 0.022, -0.101, 0, 0.077, 180]
        END
        ; Pong Game: Robots play pong against each other. 
        IF $cnt[0] == "7" THEN
          SPEED 70 ALWAYS
          ; MOVE TO TV MODE first TO PREVENT MOVEMENT ERRORS IN CONTROLLER
          JMOVE #[160, 0.022, -0.101, 0, 0.077, 180]
          ACCEL 40 ALWAYS
          DECEL 40 ALWAYS
          SPEED 40 ALWAYS
          ;     X         Y       Z        O          A         T
          ;     0       458.2   370.6     90        46.25      77
          ;                      17
          PRINT "MOVING TO Y190 IN 1 SECOND(s)"
          LMOVE TRANS (0, 525, 175, 90, 8, 90)
          SPEED 3 S
          PRINT "MOVING TO TOP IN 3 SECOND(s)"
          LMOVE TRANS (0, 525, 380, 90, 8, 90)
          TWAIT 5.2
          SPEED 3.5 S
          JMOVE TRANS (0, 450, 195, 90, 8, 90)
          PRINT "MOVING TO Y210 IN 4 SECOND(s)"
          SPEED 1 S
          LMOVE TRANS (0, 525, 195, 90, 8, 90)
          TWAIT 0.6
          ; 12 SECS
          SPEED 2.8 S
          LMOVE TRANS (0, 525, 10, 90, 8, 90)
          TWAIT 1.4
          SPEED 2.8 S
          PRINT "MOVING TO Y210 IN 3 SECOND(s)"
          LMOVE TRANS (0, 525, 180, 90, 8, 90)
          TWAIT 1.4
          SPEED 2.5 S
          LMOVE TRANS (0, 525, 48, 90, 8, 90)
          TWAIT 6
          ; 25 SECS BEFORE WAIT
          SPEED 2 S
          LMOVE TRANS (0, 525, 280, 90, 8, 90)
          TWAIT 2
          SPEED 1 S
          JMOVE TRANS (0, 475, 60, 90, 8, 90)
          SPEED 1 S
          LMOVE TRANS (0, 525, 60, 90, 8, 90)
          SPEED 3 S
          JMOVE TRANS (-100, 475, 200, 90, 8, 90)
          SPEED 1 S
          LMOVE TRANS (0, 525, 200, 90, 8, 90)
          TWAIT 0.5

          ; Defeat Dance for the robot when it loses.
          FOR .i = 1 TO 3
            SPEED 0.8 S
            JMOVE #[70, 40, -40, 90, 0, 90]
            SPEED 0.8 S
            JMOVE #[110, 40, -40, 90, 0, 90]
          END
          ; slowly goes to tv mode
          SPEED 3 S
          JMOVE #[160, 0.022, -0.101, 0, 0.077, 180]
          ; Reset to default program ACCEL and DECEL.
          ACCEL 70 ALWAYS
          DECEL 70 ALWAYS
        END

        ; Send confirmation message to server
        $cnt[0] = $ENCODE (/D, numbytes)
        UDP_SENDTO ret, ip[1], port, $cnt[0], 1, answer_timeout
        IF ret <> 0 THEN
          PRINT "Error with the UDP send, code: ", ret
        END
      END
    END

.END