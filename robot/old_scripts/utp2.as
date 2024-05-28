.PROGRAM receive_data()
  timeout = 60
  ip[1] = 192
  ip[2] = 168
  ip[3] = 0
  ip[4] = 2  ; PC's IP address
  port = 10010
  numbytes = 1
  ret = 0
  max_retries = 5   ; Maximum number of retries before waiting
  retry_delay = 5   ; Delay (in seconds) after reaching max retries
  
  WHILE TRUE DO
    retries = 0
    connected = FALSE
    
    ; Attempt to connect and receive data
    WHILE NOT connected DO
      TWAIT 3  ; Wait before trying to receive data
      UDP_RECVFROM ret, port, $cnt[0], numbytes, timeout, ip[1]
      
      ; Check if data was received successfully
      IF ret==0 THEN
        connected = TRUE  ; Successfully connected and received data
      ELSE
        PRINT "Error with the UDP Recovery, code: ", ret, ", Retrying..."
        retries = retries + 1  ; Increment retry counter
        
        ; Check if maximum retries reached
        IF retries >= max_retries THEN
          PRINT "Max retries reached. Waiting before retrying..."
          TWAIT retry_delay  ; Wait before retrying
          retries = 0  ; Reset retry counter
        END
      END
    END
    
    ; Process the received message
    PRINT "Message: ", $cnt[0]
    IF $cnt[0] == "1" THEN
      PRINT "IT IS 1"
      JMOVE #[-1.763, -5.005, 0.493, 3.324, 0.621, -0.964]
      TWAIT 1
      JMOVE #[-1.762, -36.763, 9.152, 3.324, 0.621, -0.964]
    END
    IF $cnt[0] == "2" THEN
      PRINT "IT IS 2"
      SPEED 100 ALWAYS
      JMOVE #[0, 0, 0, 0, 0, 0]
      FOR .i = 1 TO 3
        PRINT "Moving inside loop", .i, " from 5"
        JMOVE #[25.704, -50, 18.275, -18.404, -1.851, 9.318]
        ;TWAIT 1
        JMOVE #[36.603, -60, 18.275, -18.404, 36.537, 151.41]
      END
    END
  END
.END
