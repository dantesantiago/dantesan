#!/bin/awk -f

BEGIN {
 pos1 = 261;
 pos2 = 262;
}

{
  if( substr( $0, pos2, 1 ) != " " ) {
    print substr( $0, 1, pos1 );
  } else {
    print substr( $0, 1, pos2 );
  }

}

