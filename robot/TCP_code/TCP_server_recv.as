.PROGRAM TCP_server_recv (.socket_ID,.$recv_buf[],.receive_amount)
	; *******************************************************************
	;
	; Program:      TCP_server_recv
	; Comment:      Read received messages from the socket
	; Author:       Anton Vonk
	;
	; Date:         12/9/2024
	;
	; *******************************************************************
	;
	.error_ID = 0
	.receive_amount = 0
	.timeout = 60
	.max_length = 255
	TCP_RECV .error_ID,.socket_ID,.$recv_buf[0],.receive_amount,.timeout,.max_length
	IF .error_ID < 0 THEN
	  PRINT "TCP_RECV error in RECV",.error_ID
	  .$recv_buf[0]="000"
	  .receive_amount = .error_ID
	ELSE
	  IF .receive_amount > 0 THEN
		;PRINT "TCP_RECV OK in RECV",.error_ID
	  ELSE
		.$recv_buf[0]="0"
	  END
	END
  .END