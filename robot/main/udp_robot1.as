.PROGRAM utp_robot1()
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
    timeout = 60
    ip[1] = 192
    ip[2] = 168
    ip[3] = 0
    ip[4] = 10  
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
        END
      IF $cnt[0] == "2" THEN
      PRINT "IT IS 2"  
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