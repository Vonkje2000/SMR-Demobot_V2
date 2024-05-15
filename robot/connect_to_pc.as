.PROGRAM connect_to_pc() 
  tout_open = 60
  ip[1] = 192
  ip[2] = 168
  ip[3] = 0
  ip[4] = 2  ; PC's IP address
  port = 10001
  er_count = 0

connect:
  TIMER (2) = 0
  TCP_CONNECT sock_id1, port, ip[1], tout_open
  IF sock_id1 < 0 THEN
    er_count = er_count + 1
    IF er_count >= 5 THEN
      PRINT "Client Communication with PC has failed"
    ELSE
      PRINT "TCP_CONNECT error id = ", sock_id1, ", error count = ", er_count
      GOTO connect
    END
  ELSE
    PRINT "TCP_CONNECT OK id = ", sock_id1, ", with time elapsed = ", TIMER (2)
  END
  
.END