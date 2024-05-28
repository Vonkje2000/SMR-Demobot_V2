.PROGRAM init_kawa()
  ;Initiate driver
  ONE shutdown_kawa ;Calls program when error occurs
  keep_active_sig = 2010 ; Define signal number
  SIGNAL keep_active_sig ;Set signal to TRUE
  ;Initiate movement pose queue
  queue_size = 50
  queue_front = 0
  queue_rear = 0
  ;Initiate tcp string buffer
  $tcp_buffer = ""
  seq_num_old = 0
.END