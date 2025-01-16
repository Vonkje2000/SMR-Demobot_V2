.PROGRAM TCP_server_test ()
	; *******************************************************************
	;
	; Program:      TCP_server_test
	; Comment:      
	; Author:       Anton Vonk
	;
	; Date:         12/9/2024
	;
	; *******************************************************************
	;
	.port = 42069
	.$recv_buf[0] = ""
	.receive_amount = 0
	.transmission_complete = FALSE
	.Message_number = 0
	IF socket_ID > -1 THEN
		CALL TCP_server_clos(socket_ID, .port)
		socket_ID = -1
		TCP_listen_act = FALSE
	END
	;
	IF TCP_listen_act == TRUE THEN
		.error_ID = 0
		TCP_END_LISTEN .error_ID,.port
		TCP_listen_act = FALSE
	END
	;
	WHILE TRUE DO
		TCP_listen_act = TRUE
		CALL TCP_server_open(.port,socket_ID)
		IF socket_ID < 0 THEN
		GOTO exit_end
		END
		;
		WHILE TRUE DO
			.Message_number = .Message_number + 1
			.$data = "Message: " + $ENCODE(.Message_number)
			CALL TCP_server_send(socket_ID,.$data,.transmission_complete) ;Instructing processing 1
			IF .transmission_complete <> TRUE THEN
				PRINT "CODE 001 SEND ERROR"
				GOTO exit
			END
			;
			CALL TCP_server_recv(socket_ID,.$recv_buf[],.receive_amount) ;Receiving the result of processing 1
			IF .receive_amount < 0 THEN
				IF .receive_amount == -34025 THEN
					PRINT "CONNECTION HAS BEEN CLOSED FROM THE OTHER SIDE"
					GOTO exit
				ELSE
					PRINT "CODE 003 RECV ERROR"
					GOTO exit
				END
			END
			PRINT .$recv_buf[0]
			CALL Run_message(.$recv_buf[0])
		END
		;
exit:
		CALL TCP_server_clos(socket_ID, .port) ;Closing communication
		TCP_listen_act = FALSE
	END
exit_end:
.END