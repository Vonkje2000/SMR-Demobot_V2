.PROGRAM shutdown_kawa() ;
  ;$shutdown_reason = "Something went wrong :( ERROR"
  ;PRINT $shutdown_reason
  ;PRINT $recv_tcp_serv_state
  ;PRINT $movement_state
  PRINT "Shutting down!"
  SIGNAL -keep_active_sig
.END