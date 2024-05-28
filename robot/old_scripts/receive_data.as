.PROGRAM receive_data() ;

  WHILE TRUE DO
    numbytes = 10
    max_length = 10
    tout_rec = 60
    ret = 0
    TCP_RECV ret, sock_id1, $recv_buf[1], numbytes, tout_rec, max_length
    IF ret < 0 THEN
      PRINT "TCP_RECV error in RECV", ret
      $recv_buf[1] = "000"
     ELSE
      IF numbytes > 0 THEN
        ;PRINT "TCP_RECV OK in RECV", ret
        FOR i = 1 TO numbytes
        PRINT "RecBuff[", i, "]= ", $recv_buf[i]
        IF $recv_buf[1] == "1" THEN
          PRINT "IT IS 1"
          SPEED 80 ALWAYS
          JMOVE #[ -100.000,-59.995,9.834,13.745,8.050,50.603]
        END
        IF $recv_buf[1] == "2" THEN
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
      ELSE
        $recv_buf[1] = "000"
        ret = -1
      END
    END
  END
 
.END