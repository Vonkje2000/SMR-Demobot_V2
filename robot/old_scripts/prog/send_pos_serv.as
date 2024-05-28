.PROGRAM send_pos_serv()
  ;
  $send_server_sta = "Initiating"
  .send_port = 11111
  .send_msgs_per_s = 10
  .timeout_recv = 0.1
  .num = 0
  .ret_listen = -1
  .ret_sockid = -1
  ;
  $send_server_sta = "Listening on port " + $ENCODE (.send_port)
  ;
  DO
    TCP_LISTEN .ret_listen, .send_port
    IF .ret_listen < 0 THEN
      TWAIT 0.1
    END
  UNTIL .ret_listen >= 0
  ;
  DO
    TCP_ACCEPT .send_sockid, .send_port, 1
  UNTIL .send_sockid > 0
  ;
  $send_server_sta = "Connected and can start sending current poses through sockid" + $ENCODE (.send_sockid)
  ;
  WHILE SIG (keep_active_sig) DO
    CALL encode_pose (.$pose)
    .$send_buf[1] = .$pose
    TCP_SEND .ret, .send_sockid, .$send_buf[1], 1, .timeout_recv
    TWAIT (1 / .send_msgs_per_s)
  END
  ;
  $send_server_sta = "Closing connection"
  ;
  TCP_CLOSE .ret, .send_sockid
  IF .ret < 0 THEN
    $recv_tcp_serv_s = "Closing connection error: " + $ERROR (.ret)
    TCP_CLOSE .ret, .send_sockid
  END
  TCP_END_LISTEN .ret, .send_port
  ;
.END