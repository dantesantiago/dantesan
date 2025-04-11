#!/bin/awk -f

BEGIN { FS=","; }

{ 
  -v ssn; ssn=$1;
  -v f; f=$2;
  -v l; l=$3; 
  -v dob; dob=$4;#print f","l","dob;
  -v newdob; 
  newdob = substr( dob, 1, 4 )substr( dob, 6, 2 )substr( dob, 9, 4 );
  print ssn","f","l","newdob;
}
END { 
}

