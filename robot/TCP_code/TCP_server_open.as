.PROGRAM TCP_server_open (.port,.socket_ID)
	; *******************************************************************
	;
	; Program:      TCP_server_open
	; Comment:      
	; Author:       Anton Vonk
	;
	; Date:         12/9/2024
	;
	; *******************************************************************
	;
	.connect_count = 0
	.error_ID = 0
	.timeout = 1
	.ip[0] = 0
	.ip[1] = 0
	.ip[2] = 0
	.ip[3] = 0
  listen:
	TCP_LISTEN .error_ID,.port
	IF .error_ID < 0 THEN
	  IF .connect_count >= 5 THEN
		PRINT "Connection with PC is failed (LISTEN). Program is stopped."
		.socket_ID = -1
		goto exit
	  ELSE
		.connect_count = .connect_count+1
		PRINT "TCP_LISTEN error=",.error_ID," error count=",.connect_count
		GOTO listen
	  END
	ELSE
	  ;PRINT "TCP_LISTEN OK ",.error_ID
	END
	.connect_count = 0
  accept:
	TCP_ACCEPT .socket_ID,.port,.timeout,.ip[0]
	PRINT "Waiting on a computer to connect"
	WHILE .socket_ID < 0 DO
	  TCP_ACCEPT .socket_ID,.port,.timeout,.ip[0]
	END
	PRINT "TCP_ACCEPT OK id=",.socket_ID,", IP: ",.ip[0],".",.ip[1],".",.ip[2],".",.ip[3]
	
  exit: 
  .END