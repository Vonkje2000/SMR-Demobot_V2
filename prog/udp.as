.PROGRAM udp()
  ; *******************************************************************
  ;
  ; Program:      udp
  ; Comment:
  ; Author:       User
  ;
  ; Date:         5/15/2024
  ;
  ; *******************************************************************
  ;
  timeout = 9
  ip[1] = 192
  ip[2] = 168
  ip[3] = 0
  ip[4] = 2  ; PC's IP address
  port = 10010
  numbytes = 1
  ret = 0
  WHILE TRUE DO
    TWAIT 3
    UDP_RECVFROM ret, port, $cnt[0], numbytes, timeout, ip[1]
    IF ret <> 0 THEN
      PRINT "Error with the UDP Recovery, code: ", ret
      HALT
    END
    PRINT "Message: ", $cnt[0]
    ; Send confirmation message
    $message = $ENCODE (/D, numbytes)
    UDP_SENDTO ret, ip[1], 10003, $message, 20, timeout
    IF ret <> 0 THEN
      PRINT "Error with the UDP send, code: ", ret
      HALT
    END
  END
.END
