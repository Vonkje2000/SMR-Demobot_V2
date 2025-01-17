.PROGRAM TCP_server_send (.socket_ID,.$data,.transmission_complete)
	; *******************************************************************
	;
	; Program:      TCP_server_send
	; Comment:      
	; Author:       Anton Vonk
	;
	; Date:         12/9/2024
	;
	; *******************************************************************
	;
	.$send_buf[0] = .$data
	.error_ID = 0
	.timeout = 1
	TCP_SEND .error_ID,.socket_ID,.$send_buf[0],1,.timeout
	IF .error_ID < 0 THEN
		.transmission_complete = FALSE
		PRINT "TCP_SEND error in SEND",.error_ID
	ELSE
		;PRINT "TCP_SEND OK in SEND",.error_ID
		.transmission_complete = TRUE
	END 
  .END