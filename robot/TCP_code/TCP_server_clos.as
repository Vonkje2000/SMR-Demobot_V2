.PROGRAM TCP_server_clos (.socket_ID,.port)
	; *******************************************************************
	;
	; Program:      TCP_server_close
	; Comment:      Closses a socket connection and stops the listening of the server
	; Author:       Anton Vonk
	;
	; Date:         12/9/2024
	;
	; *******************************************************************
	;
	.error_ID = 0
	TCP_CLOSE .error_ID,.socket_ID
	IF .error_ID < 0 THEN
	  PRINT "TCP_CLOSE error ERROE=(”,.ret,” ) ",$ERROR(.error_ID)
	  .error_ID = 0
	  TCP_CLOSE .error_ID,.socket_ID
	  IF .error_ID < 0 THEN
		PRINT "TCP_CLOSE error id=",.socket_ID
	  END
	END
	.error_ID = 0
	TCP_END_LISTEN .error_ID,.port
	IF .error_ID < 0 THEN
	  PRINT "TCP_END_LISTEN error id=",.socket_ID
	ELSE
	  ;PRINT "TCP_END_LISTEN OK id=",.socket_ID
	  .socket_ID = -1
	END
  .END