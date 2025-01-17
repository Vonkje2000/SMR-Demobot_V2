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
	;
	IF INSTR (0 , .$message , "WAIT_UNTIL_DONE") > 0 THEN
		RETURN
	END
	;
	IF INSTR (0 , .$message , "Overwrite_mode") > 0 THEN
		IF INSTR (0 , .$message , "ENABLE") > 0 THEN
			Overwrite_mode = 1
			RETURN
		END
		Overwrite_mode = 0
		RETURN
	END
	;
	IF INSTR (0 , .$message , "HERE JT") > 0 THEN
		HERE .#local_pos
		DECOMPOSE .value[0] = .#local_pos
		.$string = ""
		.$string = .$string + $ENCODE(/F8.2,.value[0]) + ", "
		.$string = .$string + $ENCODE(/F8.2,.value[1]) + ", "
		.$string = .$string + $ENCODE(/F8.2,.value[2]) + ", "
		.$string = .$string + $ENCODE(/F8.2,.value[3]) + ", "
		.$string = .$string + $ENCODE(/F8.2,.value[4]) + ", "
		.$string = .$string + $ENCODE(/F8.2,.value[5])
		$return_message = .$string
		ret_data_avail = TRUE
		RETURN
	END
	;
	IF INSTR (0 , .$message , "HERE POS") > 0 THEN
		HERE .local_pos
		DECOMPOSE .value[0] = .local_pos
		.$string = ""
		.$string = .$string + $ENCODE(/F8.2,.value[0]) + ", "
		.$string = .$string + $ENCODE(/F8.2,.value[1]) + ", "
		.$string = .$string + $ENCODE(/F8.2,.value[2]) + ", "
		.$string = .$string + $ENCODE(/F8.2,.value[3]) + ", "
		.$string = .$string + $ENCODE(/F8.2,.value[4]) + ", "
		.$string = .$string + $ENCODE(/F8.2,.value[5])
		$return_message = .$string
		ret_data_avail = TRUE
		RETURN
	END
	;
	IF INSTR(0, .$message, "HOME 2") > 0 THEN
		HOME 2
		RETURN
	END
	;
	IF INSTR(0, .$message, "HOME") > 0 THEN
		HOME
		RETURN
	END
	;
	IF INSTR(0, .$message, "CP ON") > 0 THEN
		CP ON
		RETURN
	END
	;
	IF INSTR(0, .$message, "CP OFF") > 0 THEN
		CP OFF
		RETURN
	END
	;
	IF INSTR(0, .$message, "SPEED") > 0 THEN
		.$value_string = $MID(.$message, LEN("SPEED ") + 1, LEN(.$message) - LEN("SPEED "))
		.value[0] = VAL(.$value_string,0)
		SPEED .value[0] ALWAYS
		RETURN
	END
	;
	IF INSTR(0, .$message, "JMOVE") > 0 THEN
		IF INSTR(0, .$message, "TRANS") > 0 THEN
			.$value_string = $MID(.$message, LEN("JMOVE TRANS (") + 1, LEN(.$message) - LEN("JMOVE TRANS ()"))
			.value[0] = VAL(.$value_string,0)
			;
			.i = 1
			WHILE .i < 6 DO
				.value[9] = INSTR(0,.$value_string, " ")
				.$value_string = $MID(.$value_string, .value[9] + 1, LEN(.$value_string) - .value[9])
				.$temp = $DECODE(.$value_string, ",", 1)
				.value[.i] = VAL(.$value_string,0)
				.i = .i + 1
			END
			;
			JMOVE TRANS(.value[0],.value[1],.value[2],.value[3],.value[4],.value[5])
		ELSE
			.$value_string = $MID(.$message, LEN("JMOVE (") + 1, LEN(.$message) - LEN("JMOVE ()"))
			.value[0] = VAL(.$value_string,0)
			;
			.i = 1
			WHILE .i < 6 DO
				.value[9] = INSTR(0,.$value_string, " ")
				.$value_string = $MID(.$value_string, .value[9] + 1, LEN(.$value_string) - .value[9])
				.$temp = $DECODE(.$value_string, ",", 1)
				.value[.i] = VAL(.$value_string,0)
				.i = .i + 1
			END
			;
			POINT .#next_joint_position = #PPOINT(.value[0],.value[1],.value[2],.value[3],.value[4],.value[5])
			JMOVE .#next_joint_position
	  	END
		RETURN
	END
	;
	IF INSTR(0, .$message, "LMOVE") > 0 THEN
		IF INSTR(0, .$message, "TRANS") > 0 THEN
			.$value_string = $MID(.$message, LEN("LMOVE TRANS (") + 1, LEN(.$message) - LEN("LMOVE TRANS ()"))
			.value[0] = VAL(.$value_string,0)
			;
			.i = 1
			WHILE .i < 6 DO
				.value[9] = INSTR(0,.$value_string, " ")
		  		.$value_string = $MID(.$value_string, .value[9] + 1, LEN(.$value_string) - .value[9])
				.$temp = $DECODE(.$value_string, ",", 1)
				.value[.i] = VAL(.$value_string,0)
				.i = .i + 1
			END
			;
			LMOVE TRANS(.value[0],.value[1],.value[2],.value[3],.value[4],.value[5])
		ELSE
			.$value_string = $MID(.$message, LEN("LMOVE (") + 1, LEN(.$message) - LEN("LMOVE ()"))
			.value[0] = VAL(.$value_string,0)
			;
			.i = 1
			WHILE .i < 6 DO
				.value[9] = INSTR(0,.$value_string, " ")
				.$value_string = $MID(.$value_string, .value[9] + 1, LEN(.$value_string) - .value[9])
				.$temp = $DECODE(.$value_string, ",", 1)
				.value[.i] = VAL(.$value_string,0)
				.i = .i + 1
			END
			;
			POINT .#next_joint_position = #PPOINT(.value[0],.value[1],.value[2],.value[3],.value[4],.value[5])
			LMOVE .#next_joint_position
		END
		RETURN
	END
	;
	IF INSTR(0, .$message, "TOOL") > 0 THEN
		IF INSTR(0, .$message, "TRANS") > 0 THEN
			.$value_string = $MID(.$message, LEN("TOOL TRANS (") + 1, LEN(.$message) - LEN("TOOL TRANS ()"))
			.value[0] = VAL(.$value_string,0)
		  
			.i = 1
			WHILE .i < 6 DO
				.value[9] = INSTR(0,.$value_string, " ")
				.$value_string = $MID(.$value_string, .value[9] + 1, LEN(.$value_string) - .value[9])
				.$temp = $DECODE(.$value_string, ",", 1)
				.value[.i] = VAL(.$value_string,0)
				.i = .i + 1
			END

			TOOL TRANS(.value[0],.value[1],.value[2],.value[3],.value[4],.value[5])
			RETURN
		END
	END
	;
	PRINT "UNKNOWN COMMAND"
  .END