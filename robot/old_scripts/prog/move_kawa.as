.PROGRAM move_kawa()
  $movement_state = "Initiating"
  .current_speed = 10 ;percentage of monitor speed
  .current_accurac = 2 ;Milimeters
  .current_deceler = 100 ;Percentage of max decel
  .current_acceler = 100 ;Percentage of max accel
  ;
  WHILE SIG (keep_active_sig) DO
    $movement_state = "Waiting for trajectory point in queue"
    IF queue_front > 0 THEN
      ;
      $movement_state = "Setting motion parameters"
      IF NOT queue[queue_front, 1] == .current_speed THEN
        .current_speed = queue[queue_front, 1]
        SPEED .current_speed ALWAYS
      END
      IF NOT queue[queue_front, 2] == .current_accurac THEN
        .current_accurac = queue[queue_front, 2]
        ACCURACY .current_accurac ALWAYS
      END
      IF NOT queue[queue_front, 3] == .current_deceler THEN
        .current_deceler = queue[queue_front, 3]
        DECEL .current_deceler ALWAYS
      END
      IF NOT queue[queue_front, 4] == .current_acceler THEN
        .current_acceler = queue[queue_front, 4]
        ACCEL .current_acceler ALWAYS
      END
      ;
      IF queue[queue_front, 0] == 11 THEN
        POINT .#next_joint_posi = #PPOINT (queue[queue_front, 6], queue[queue_front, 7], queue[queue_front, 8], queue[queue_front, 9], queue[queue_front, 10], queue[queue_front, 11])
        JMOVE .#next_joint_posi
      END
      IF queue[queue_front, 0] == 12 THEN
        POINT .next_cartesian_ = TRANS (queue[queue_front, 6], queue[queue_front, 7], queue[queue_front, 8], queue[queue_front, 9], queue[queue_front, 10], queue[queue_front, 11])
        LMOVE .next_cartesian_
      END
      ;
      IF queue[queue_front, 5] == 1 THEN
        BREAK
      END
      ;
      $movement_state = "Deleting trajectory point from queue"
      CALL del_front_queue
    ELSE
      TWAIT 0.1
    END
  END
.END