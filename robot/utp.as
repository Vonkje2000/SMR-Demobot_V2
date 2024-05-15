  timeout = 9
  ip[1] = 192
  ip[2] = 168
  ip[3] = 0
  ip[4] = 2  ; PC's IP address
  port = 10010
  numbytes = 1
  ret = 0
  
;  UDP_SENDTO ret,ip[1],10003, "a", 1, 5
;  IF ret<>0 THEN
;    TYPE “ERROR!”
;    HALT
;  END
  WHILE TRUE DO
    TWAIT 3
    UDP_RECVFROM ret,port,$cnt[0],numbytes,timeout,ip[1]
    IF ret<>0 THEN
      PRINT "Error with the UDP Recovery, code: ", ret
      HALT
    END
    PRINT "Message: ", $cnt[0]
  END