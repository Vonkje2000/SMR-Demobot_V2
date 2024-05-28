.PROGRAM udp_robot1()
    ; This is the main program of robot1, for the DEMOBOT project, SMR2.
    ; It implements UDP communication to server with acknowledgments.
    ; github.com/icorn1
    ;
    ; Confirmation / Error code:
    error_code = 4000
    confirm_code = 1000

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
        $cnt[0] = $ENCODE (/D, numbytes)
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
.PROGRAM udp_robot2()
  ; This is the main program of robot2, for the DEMOBOT project, SMR2.
  ; It implements UDP communication to server with acknowledgments.
  ; github.com/icorn1
  ;
  ; Confirmation / Error code:
  error_code = 4000
  confirm_code = 1000

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

      END
      IF $cnt[0] == "2" THEN

      END
      IF $cnt[0] == "0" THEN

      END

      ; Send confirmation message
      $cnt[0] = $ENCODE (/D, $cnt[0])
      UDP_SENDTO ret, ip[1], port, $cnt[0], 1, timeout
      IF ret <> 0 THEN
        PRINT "Error with the UDP send, code: ", ret
      ELSE
        PRINT "Message sent to host"
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
.PROGRAM dance1 () ; 
  ; *******************************************************************
  ;
  ; Program:      dance1
  ; Comment:      
  ; Author:       icorn1
  ;
  ; Date:         5/28/2024
  ;
  ; *******************************************************************
  ;
  SPEED 100 ALWAYS 
  JMOVE #[0,0,0,0,0,0]
  TWAIT(3)
    
  JMOVE #[0,26,0,0,0,0]
  JMOVE #[0,-33,0,0,0,45]
  JMOVE #[-55,71,0,0,0,-45]
  JMOVE #[-93,28,0,0,0,45]
  JMOVE #[0,26,0,0,0,-45]
  JMOVE #[0,-33,0,0,0,45]
  JMOVE #[-55,71,0,0,0,0]
  
.END
.PROGRAM dance2()
  ; *******************************************************************
  ;
  ; Program:      dance2
  ; Comment:      
  ; Author:       icorn1
  ;
  ; Date:         5/28/2024
  ;
  ; *******************************************************************
  ;
  
  JMOVE #[0,0,0,0,0,0]
  TWAIT(3)

  JMOVE #[0,-26,0,0,0,0]
  JMOVE #[0,33,0,0,0,-45]
  JMOVE #[55,71,0,0,0,45]
  JMOVE #[93,28,0,0,0,-45]
  JMOVE #[55,71,0,0,0,45]
  JMOVE #[0,33,0,0,0,-45]
  JMOVE #[0,-26,0,0,0,0]
.END
.PROGRAM Comment___ () ; Comments for IDE. Do not use.
	; @@@ PROJECT @@@
	; @@@ PROJECTNAME @@@
	; udp_robot1
	; @@@ HISTORY @@@
	; 28.05.2024 11:30:20
	; 
	; @@@ INSPECTION @@@
	; @@@ CONNECTION @@@
	; Left Kawa (1)
	; 192.168.0.1
	; 23
	; @@@ PROGRAM @@@
	; 0:udp_robot1:F
	; 0:udp_robot2:F
	; 0:dance1:F
	; 0:dance2:F
	; @@@ TRANS @@@
	; @@@ JOINTS @@@
	; @@@ REALS @@@
	; @@@ STRINGS @@@
	; @@@ INTEGER @@@
	; @@@ SIGNALS @@@
	; @@@ TOOLS @@@
	; @@@ BASE @@@
	; @@@ FRAME @@@
	; @@@ BOOL @@@
.END
