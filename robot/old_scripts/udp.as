.PROGRAM connect_to_pc_by_udp()
  timeout = 120
  answer_timeout = 3
  ip[1] = 192
  ip[2] = 168
  ip[3] = 0
  ip[4] = 10  
  port = 10010
  numbytes = 1
  ret = 0
  WHILE TRUE DO
    TWAIT 1
    UDP_RECVFROM ret, port, $cnt[0], numbytes, timeout, ip[1]
    IF ret <> 0 THEN
      PRINT "No data received within timeout period or error code: ", ret
      ; Continue to the next iteration without halting
    ELSE
        PRINT "Message: ", $cnt[0]
      ; Send confirmation message
      $cnt[0] = $ENCODE (/D, numbytes)
      UDP_SENDTO ret, ip[1], port, $cnt[0], 1, answer_timeout
      IF ret <> 0 THEN
        PRINT "Error with the UDP send, code: ", ret
        ; Optionally handle send error but do not halt
      END
    END
  END
.END