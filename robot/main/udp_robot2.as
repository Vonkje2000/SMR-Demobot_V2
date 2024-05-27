.PROGRAM utp_robot2()
    ; *******************************************************************
    ;
    ; Program:      utp_2
    ; Comment:      
    ; Author:       Shiyar Jamo | Coder Shiyar HHS Delft
    ;
    ; Date:         5/27/2024
    ;
    ; *******************************************************************
    ;
    timeout = 9
    ip[1] = 192
    ip[2] = 168
    ip[3] = 0
    ip[4] = 2  
    port = 10010
    numbytes = 1
    ret = 0
    WHILE TRUE DO
      TWAIT 3
      UDP_RECVFROM ret, port, $cnt[0], numbytes, timeout, ip[1]
      IF ret <> 0 THEN
        PRINT "No data received within timeout period or error code: ", ret
        ; Continue to the next iteration without halting
      ELSE
        
        PRINT "Message: ", $cnt[0]
        IF $cnt[0] == "1" THEN
          PRINT "IT IS 1"
          ;JMOVE #[-1.763, -5.005, 0.493,3.324, 0.621,-0.964]
          ;TWAIT 1
          ;JMOVE #[-1.762,-36.763,  9.152,3.324, 0.621,-0.964]
        END
      IF $cnt[0] == "2" THEN
      PRINT "IT IS 2"  
      JMOVE #[54.917, 61.902, 2.811, -0.643, -0.050, 0.069]
      FOR .i = 1 TO 3
        PRINT "Moving inside loop", .i, " from 5"
        JMOVE #[54.917,81.172,2.046, -2.362,  -0.050,  0.069]
        TWAIT 1
        JMOVE #[54.917,66.111, 2.047,  -2.362 , -0.050, 0.069]
      END
                            

      END
      IF $cnt[0] == "0" THEN
        PRINT "IT IS 0"  
        END

        ; Send confirmation message
        $cnt[0] = $ENCODE (/D, numbytes)
        UDP_SENDTO ret, ip[1], port, $cnt[0], 1, 9
        IF ret <> 0 THEN
          PRINT "Error with the UDP send, code: ", ret
          ; Optionally handle send error but do not halt
        END
      END
    END
  .END