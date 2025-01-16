.PROGRAM TCP_S_detec_clo(.socket_id,.output) ; a small function to detect if the connection got closed
	; *******************************************************************
	;
	; Program:      TCP_S_detec_clo
	; Comment:      a small function to detect if the connection got closed
	; Author:       User
	;
	; Date:         1/16/2025
	;
	; *******************************************************************
	;
	.error_id = 0
	.receive_amount = 0
	.timeout = 1
	.max_length = 255
	.$recv_buf[0] = ""
	TCP_RECV .error_id, .socket_id, .$recv_buf[0], .receive_amount, .timeout, .max_length
	IF .error_id <> -34024 AND .error_id < 0 THEN ;if a timeout occurs do not do anything but if the connection closses it stops the code
	  .output = TRUE
	END
	.output = FALSE
  .END