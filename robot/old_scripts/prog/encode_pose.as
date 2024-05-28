.PROGRAM encode_pose(.$pose) ;
  HERE .#cp
  DECOMPOSE .cp[0] = .#cp
  .$s = "|"
  .$pose = $CHR (2) + $ENCODE (/L, .$s, .cp[0], .$s, .cp[1], .$s, .cp[2], .$s, .cp[3], .$s, .cp[4], .$s, .cp[5], .$s) + $CHR (3) + $CHR (10)
.END