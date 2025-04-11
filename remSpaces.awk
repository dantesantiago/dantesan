#!/bin/awk -f

BEGIN { -v x; x = 1; }
{ 
  -v newLine; 
	if( x == 1 ) {
    print  $0;
    x = 2;
  } else {
  if( substr( $0, 262, 1 ) == " " ) {
    newLine = substr( $0, 1, 261 );
  } else {
    newLine = substr( $0, 1, 262 );
  }

  #newLine = sub(/[ \t]+$/, "", $0); # remove spaces at the end
  print  newLine;
  }
}
END { 
}

