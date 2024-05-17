.PROGRAM read_tcp_buffer()
  ;
  $read_tcp_buffer = "Initiating"
  ;
  .$start_of_msg0 = $CHR (2)
  .$start_of_msg1 = $CHR (1)
  .$end_of_msg = $CHR (3)
  .$temp = "init"
  ;
start:
  WHILE SIG (keep_active_sig) DO
    WAIT LEN ($tcp_buffer) > 0
    ;PRINT "Message: ", $msg
    .$temp = $DECODE ($tcp_buffer, .$start_of_msg0, 0) ;Delete everything up to first start_of_message
    IF LEN ($tcp_buffer) > 0 THEN ;Check if TCP buffer is not empty, can be empty of no start_of_message available.
      .$temp = $DECODE ($tcp_buffer, "|", 0) ;Store characters upto seperator as variable
      .$seperator = $DECODE ($tcp_buffer, "|", 1) ;Remove pipe seperator
      IF .$temp == .$start_of_msg0 THEN ;Check if start_of_message was indeed found
        WAIT LEN ($tcp_buffer) > 2
        ;PRINT "yes1!"
        .$temp = $DECODE ($tcp_buffer, "|", 0) ;Store characters upto seperator as variable
        .$seperator = $DECODE ($tcp_buffer, "|", 1) ;Remove pipe seperator
        IF .$temp == .$start_of_msg1 THEN ;Check if start_of_heading was found
          WAIT LEN ($tcp_buffer) > 3
          ;PRINT "yes2!"
          .$temp = $DECODE ($tcp_buffer, "|", 0) ;Store characters upto seperator as variable
          .msg_length = VAL (.$temp)
          WAIT LEN ($tcp_buffer) >= .msg_length
          ;print "Message length: ", .msg_length
          .$full_message = $DECODE ($tcp_buffer, .$end_of_msg, 0) ;store everything up to end_of_message
          ;print .$full_message
          IF LEN (.$full_message) == (.msg_length - 1) THEN
            ; print "YES!!!!!", .$full_message
            CALL decode_traj_pt (.$full_message, .msg_id, .prog_speed, .prog_acc, .prog_accel, .prog_decel, .prog_break, .joint0, .joint1, .joint2, .joint3, .joint4, .joint5)
            CALL ins_rear_queue (.msg_id, .prog_speed, .prog_acc, .prog_accel, .prog_decel, .prog_break, .joint0, .joint1, .joint2, .joint3, .joint4, .joint5)
          ELSE
            $read_tcp_buffer = "error"
            PRINT "oh no :( 3"
            ;call shutdown error!
          END
        ELSE
          $read_tcp_buffer = "error"
          PRINT "oh no :( 2"
          ;call shutdown error!
        END
      ELSE
        $read_tcp_buffer = "error"
        PRINT "oh no :( 1"
        ;call shutdown error!
      END
    ELSE
      $read_tcp_buffer = "error"
      ;print "TCP buffer empty!"
      TWAIT 0.5
    END
  END
.END