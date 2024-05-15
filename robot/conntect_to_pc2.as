.PROGRAM connect_to_pc()
  tout_open = 9
  ip[1] = 192
  ip[2] = 168
  ip[3] = 0
  ip[4] = 2  ; PC's IP address
  port = 10001
  er_count = 0
  sock_id1 = 0
connect:
  WHILE TRUE DO  ; Forever loop
    TIMER (2) = 0
    TCP_CONNECT sock_id1, port, ip[1], tout_open
    IF sock_id1 < 0 THEN
      er_count = er_count + 1
      IF er_count >= 5 THEN
        PRINT "Client Communication with PC has failed. Closing socket."
      ELSE
        PRINT "TCP_CONNECT error id = ", sock_id1, ", error count = ", er_count
        GOTO connect
      END
    ELSE
      PRINT "TCP_CONNECT OK id = ", sock_id1, ", with time elapsed = ", TIMER (2)
      ; Call the "rps" function if connection is successful
      ; GOTO rpss
    END
  END
rpss:
  ; Define the actions to perform when the connection is successful
  ; This function will be called whenever the connection is established successfully
.END