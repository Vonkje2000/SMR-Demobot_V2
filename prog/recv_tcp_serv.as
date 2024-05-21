.PROGRAM recv_tcp_serv() ;
  ;
  $recv_tcp_serv_s = "0, initiating"
  PRINT $recv_tcp_serv_s
  .recv_port = 11112
  .timeout_recv = 0.01
  .num = 0
  .ret_listen = -1
  ;.recv_sockid = -1
  $recv_tcp_serv_s = "Connecting on port " + $ENCODE (.recv_port)
  PRINT $recv_tcp_serv_s ;
  DO
    TCP_LISTEN .ret_listen, .recv_port
    IF .ret_listen < 0 THEN
      TWAIT 0.1
    END
  UNTIL .ret_listen >= 0
  ;
  DO
    TCP_ACCEPT .recv_sockid, .recv_port, 1
  UNTIL .recv_sockid > 0
  ;
  $recv_tcp_serv_s = "Connected and can start receiving poses through sockid: " + $ENCODE (.recv_sockid)
  PRINT $recv_tcp_serv_s;
  WHILE SIG (keep_active_sig) DO
    .num = 0
    TCP_RECV .ret, .recv_sockid, .$tcp_message[1], .num, .timeout_recv, 1
    ;$recv_tcp_serv_state = "Current state tcp comms: " + $ERROR(.ret)
    IF .ret >= 0 THEN ;If we received stuff, add message to internal tcp_buffer
      IF .num > 0 THEN
        FOR .i = 1 TO .num
          $tcp_buffer = $tcp_buffer + .$tcp_message[.i]
        END
      END
    ELSE
      TWAIT 0.01
    END
  END
  $recv_tcp_serv_s = "Closing connection"
  PRINT $recv_tcp_serv_s
  TCP_CLOSE .ret, .recv_sockid
  IF .ret < 0 THEN
    $recv_tcp_serv_s = "Closing connection error: " + $ERROR (.ret)
    PRINT $recv_tcp_serv_s
    TCP_CLOSE .ret, .recv_sockid
  END
  TCP_END_LISTEN .ret, .recv_port
  $recv_tcp_serv_s = "Closed succesfully"
  PRINT $recv_tcp_serv_s
.END