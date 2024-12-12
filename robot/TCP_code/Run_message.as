.PROGRAM Run_message (.$message)
	; *******************************************************************
	;
	; Program:      Run_message
	; Comment:      
	; Author:       Anton Vonk
	;
	; Date:         12/11/2024
	;
	; *******************************************************************
	;
	.$temp = ""
	.$value_string = ""
	.value[0] = 0
	.value[1] = 0
	.value[2] = 0
	.value[3] = 0
	.value[4] = 0
	.value[5] = 0
	.value[6] = 0
	.value[7] = 0
	.value[8] = 0
	.value[9] = 0
	
	IF INSTR(0, .$message, "HOME 2") > 0 THEN
	  HOME 2
	  RETURN
	END
	
	IF INSTR(0, .$message, "HOME") > 0 THEN
	  HOME
	  RETURN
	END
	
	IF INSTR(0, .$message, "SPEED") > 0 THEN
	  .$value_string = $MID(.$message, LEN("SPEED ") + 1, LEN(.$message) - LEN("SPEED "))
	  .value[0] = VAL(.$value_string,0)
	  SPEED .value[0] ALWAYS
	  RETURN
	END
	
	IF INSTR(0, .$message, "JMOVE") > 0 THEN
	  IF INSTR(0, .$message, "TRANS") > 0 THEN
		.$value_string = $MID(.$message, LEN("JMOVE TRANS (") + 1, LEN(.$message) - LEN("JMOVE TRANS ()"))
		.value[0] = VAL(.$value_string,0)
		
		.i = 1
		WHILE .i < 6 DO
		  .value[9] = INSTR(0,.$value_string, " ")
		  .$value_string = $MID(.$value_string, .value[9] + 1, LEN(.$value_string) - .value[9])
		  .$temp = $DECODE(.$value_string, ",", 1)
		  .value[.i] = VAL(.$value_string,0)
		  .i = .i + 1
		END
		
		JMOVE TRANS(.value[0],.value[1],.value[2],.value[3],.value[4],.value[5])
		
	  ELSE
		.$value_string = $MID(.$message, LEN("JMOVE (") + 1, LEN(.$message) - LEN("JMOVE ()"))
		.value[0] = VAL(.$value_string,0)
		
		.i = 1
		WHILE .i < 6 DO
		  .value[9] = INSTR(0,.$value_string, " ")
		  .$value_string = $MID(.$value_string, .value[9] + 1, LEN(.$value_string) - .value[9])
		  .$temp = $DECODE(.$value_string, ",", 1)
		  .value[.i] = VAL(.$value_string,0)
		  .i = .i + 1
		END
		
		POINT .#next_joint_position = #PPOINT(.value[0],.value[1],.value[2],.value[3],.value[4],.value[5])
		JMOVE .#next_joint_position
		
	  END
	  RETURN
	END
	
	IF INSTR(0, .$message, "LMOVE") > 0 THEN
	  IF INSTR(0, .$message, "TRANS") > 0 THEN
		.$value_string = $MID(.$message, LEN("LMOVE TRANS (") + 1, LEN(.$message) - LEN("LMOVE TRANS ()"))
		.value[0] = VAL(.$value_string,0)
		
		.i = 1
		WHILE .i < 6 DO
		  .value[9] = INSTR(0,.$value_string, " ")
		  .$value_string = $MID(.$value_string, .value[9] + 1, LEN(.$value_string) - .value[9])
		  .$temp = $DECODE(.$value_string, ",", 1)
		  .value[.i] = VAL(.$value_string,0)
		  .i = .i + 1
		END
		
		LMOVE TRANS(.value[0],.value[1],.value[2],.value[3],.value[4],.value[5])
		
	  ELSE
		.$value_string = $MID(.$message, LEN("LMOVE (") + 1, LEN(.$message) - LEN("LMOVE ()"))
		.value[0] = VAL(.$value_string,0)
		
		.i = 1
		WHILE .i < 6 DO
		  .value[9] = INSTR(0,.$value_string, " ")
		  .$value_string = $MID(.$value_string, .value[9] + 1, LEN(.$value_string) - .value[9])
		  .$temp = $DECODE(.$value_string, ",", 1)
		  .value[.i] = VAL(.$value_string,0)
		  .i = .i + 1
		END
		
		POINT .#next_joint_position = #PPOINT(.value[0],.value[1],.value[2],.value[3],.value[4],.value[5])
		LMOVE .#next_joint_position
	  END
	  RETURN
	END
	
	PRINT "UNKNOWN COMMAND"
	
  .END