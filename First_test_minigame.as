.PROGRAM promo_v2_test()
    ; *******************************************************************
    ;
    ; Program:      promo_v2_test
    ; Comment:
    ; Author:       Bastiaan
    ;
    ; Date:         12/6/2024
    ;
    ; *******************************************************************
    ;
    IFPDISP 1
    SPEED 70 ALWAYS
    TOOL TRANS(40, 30, 60, 0, 0, 0)
    .X = 0
    .Y = 0
    .GradenX = .X * 10
    .GradenY = .Y * 10
    
    WHILE SIG (button_start) == FALSE DO
  label:
      IF (.GradenX == 0 AND .GradenY == 0) THEN         ;North
        LMOVE TRANS (-200, 600, -60, 90, 90, 90)
        PRINT "TESTHorizontaal" 
        GOTO label
      END
      IF (.GradenX == 0 AND .GradenY > 0) THEN         ;North
        LMOVE TRANS (-200, 600, -60, 90, 90, 90 + .GradenY)
        PRINT "TESTN" 
        GOTO label
      END
      IF (.GradenX > 0 AND .GradenY > 0) THEN     ;North-East
        LMOVE TRANS (-200, 600, -60, 90, 90 - .GradenX, 90 + .GradenY)
        PRINT "TESTNE"
        GOTO label
      END
      IF (.GradenX > 0 AND  .GradenY == 0) THEN    ;East
        LMOVE TRANS (-200, 600, -60, 90, 90 - .GradenX, 90)
        PRINT "TESTE"
        GOTO label
      END
      IF (.GradenX > 0 AND  .GradenY < 0) THEN    ;South-East
        LMOVE TRANS (-200, 600, -60, 90, 90 - .GradenX, 90 + .GradenY)
        PRINT "TESTSE"
        GOTO label
      END
      IF (.GradenX == 0 AND  .GradenY < 0) THEN    ;South
        LMOVE TRANS (-200, 600, -60, 90, 90, 90 + .GradenY)
        PRINT "TESTS"
        GOTO label
      END
      IF (.GradenX < 0 AND  .GradenY < 0) THEN    ;South-West
        LMOVE TRANS (-200, 600, -60, 90, 90 - .GradenX, 90 + .GradenY)
        PRINT "TESTSW"
        GOTO label
      END
      IF (.GradenX < 0 AND  .GradenY == 0) THEN    ;West
        LMOVE TRANS (-200, 600, -60, 90, 90 - .GradenX, 90)
        PRINT "TESTW"
        GOTO label
      END
      IF (.GradenX < 0 AND  .GradenY > 0) THEN      ;North-West
        LMOVE TRANS (-200, 600, -60, 90, 90 - .GradenX, 90 + .GradenY)
        PRINT "TESTNW"
        GOTO label
      END
     
      
      ;LMOVE TRANS (-70, 407, 331, 180, 0, 0)
      ;LMOVE TRANS (-70, 407, 331, 180, 45, 0)
      ;LMOVE TRANS (-70, 407, 331, 180, 0, 0)
      ;LMOVE TRANS (-70, 407, 331, 135, 45, 45)
      ;LMOVE TRANS (-70, 407, 331, 180, 0, 0)
      ;LMOVE TRANS (-70, 407, 331, 90, 45, 90)
      ;LMOVE TRANS (-70, 407, 331, 180, 0, 0)
      ;LMOVE TRANS (-70, 407, 331, 225, -45, -45)
      ;LMOVE TRANS (-70, 407, 331, 180, 0, 0)
      ;LMOVE TRANS (-70, 407, 331, 0, 45, 180)
      ;LMOVE TRANS (-70, 407, 331, 180, 0, 0)
      ;LMOVE TRANS (-70, 407, 331, -45, 45, 225)
      ;LMOVE TRANS (-70, 407, 331, 180, 0, 0)
      ;LMOVE TRANS (-70, 407, 331, -90, 30, -90)
      ;LMOVE TRANS (-70, 407, 331, 180, 0, 0)
      ;LMOVE TRANS (-70, 407, 331, 225, 45, -45)
    END
    PRINT "TEST"
    PRINT "HALLO"
    ;HOME
  .END