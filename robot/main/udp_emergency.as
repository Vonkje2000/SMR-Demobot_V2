.PROGRAM udp_emergency (.ret,.$receive) ; 
    ; *******************************************************************
    ;
    ; Program:      udp_emergency
    ; Comment:      In this program, control parameters are recieved for
    ;               the main background process, main.pc. It allows to stop
    ;               program execution in case of emergency through the touchscreen.
    ; Author:       Ixent Cornell | github.com/icorn1 | Shiyar Jamo HHS Delft | github.com/codershiyar
    ; Date:         6/4/2024
    ; *******************************************************************
    
    ip[1] = 192
    ip[2] = 168
    ip[3] = 0
    ip[4] = 10
    .$recv_buf[1] = .$receive
    .ret = 0
     timeout = 60
     max_length = 255
    .port = 10020
    .$receive = ""
    .num = 0
    
    ; We use UDP to recover message from server with the following parameters. 
    ; Check the Kawasaki AS Manual to get more information on the function.
    UDP_RECVFROM .eret, .port, .$recv_buf[1], .num, timeout, ip[1], max_length
    IF .eret < 0 THEN
      PRINT "UDP_RECV error in Control Program ", .eret
      PRINT ".num = ", .num
      .ret = -1
    ELSE
      IF .num > 0 THEN
        IF .num * max_length <= 255 THEN
          FOR .j = 1 TO .num
            .$receive = .$receive + .$recv_buf[.j]
          END
        ELSE
          .ret = -1
          PRINT "String too long"
          PRINT .$recv_buf[1]
        END
      ELSE
        PRINT "Invalid response"
        .ret = -1
      END
    END

  .END