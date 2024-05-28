.PROGRAM main_robot1()
    ; This is the main program of robot1, for the DEMOBOT project, SMR2.
    ; github.com/icorn1
    ;
    timeout = 30
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
          PRINT " 1"
        END
        IF $cnt[0] == "2" THEN
        PRINT "IT IS 2"  
        END
        IF $cnt[0] == "0" THEN
          PRINT "IT IS 0"  
        END
  
        ; Send confirmation message
        $cnt[0] = $ENCODE (/D, $cnt[0])
        UDP_SENDTO ret, ip[1], port, $cnt[0], 1, timeout
        IF ret <> 0 THEN
          PRINT "Error with the UDP send, code: ", ret
        ELSE
          ; Recieve confirmation code or error code
          UDP_RECVFROM ret, port, $cnt[0], numbytes, timeout, ip[1]
          IF ret <> 0 THEN
            PRINT "No data received within timeout period or error code: ", ret
            ; Continue to the next iteration without halting
          ELSE
            IF $cnt[0] == "1000" THEN
              PRINT "Communication successfull with server. Confirmation code: ", $cnt[0]
            ELSE
              PRINT "Communication error with server. Error code: ", $cnt[0]
            END
          END
        END
      END
    END
  .END