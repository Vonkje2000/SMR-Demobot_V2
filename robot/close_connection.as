.PROGRAM closeconnection() ;
  ret = 0
  IF sock_id1 >= 0 THEN
    TCP_CLOSE ret, sock_id1
  END
  IF ret < 0 THEN
    PRINT "TCP_CLOSE error id = ", sock_id1
  ELSE
    PRINT "TCP_CLOSE OK id = ", sock_id1
  END
.END