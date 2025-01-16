.PROGRAM promo_v2_front()
	; *******************************************************************
	;
	; Program:      promo_v2_front
	; Comment:
	; Author:       Anton Vonk
	;
	; Date:         1/13/2025
	;
	; *******************************************************************
	;
	WHILE TRUE DO
		IF new_message == 1 THEN
			CALL Run_message ($message)
			new_message = 0
		END
	END
  .END