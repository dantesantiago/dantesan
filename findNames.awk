#!/bin/awk -f

BEGIN {
  namesFN = "Names.txt";
}

{
  #print lnfs
#print $0;
  while (( getline lnf < namesFN ) > 0 ) {
    if( index( $0, lnf ) != 0 ) print $0 > "out.txt";
  }
}


END {

}
