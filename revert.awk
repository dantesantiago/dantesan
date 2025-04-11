#!/bin/awk -f
# reverts to original format the mediaId.EIDC.modified file
# GISCONSMR-5078

BEGIN { 

  FS=":";

  # put the old and new values and update the num* vars
  clientIdOld[1] = "12290367";
  clientIdNew[1] = "22222222";
  numClienIds = 1;

  divIdOld[1]= "0004";
  divIdOld[2] = "0010";
  divIdNew[1]= "4444";
  divIdNew[2] = "1111";
  numDivIds = 2;

  revertedFN = "EIDC.mod.sort.rev";
  sortRevFN = "EIDC.mod.sort.rev.sort";

  revLn;

  system("cp /dev/null "revertedFN);

}
{ 
  revLn = $0; 

  # '}: ' -> '};'
  if( match( $0, "}, " ) > 0 ) {
    sub("}, ", "},", revLn);
  }

  if( match( $0, ": " ) > 0 ) {
    sub(": ", " : ", revLn);
  }

  # rev clientId
  for( i = 1; i <= numClienIds; i++ ) {
    #printf "clientIdNew[i] = <%s>", clientIdNew[i];
    if( match( $0, clientIdNew[$i] ) > 0 ) {
      sub(clientIdNew[i], clientIdOld[i], revLn);
      #printf "\nclientId chgd: %s", revLn;    
    }
  }

  # rev divId's
  for( i = 1; i <= numDivIds; i++ ) {

    if( match( $0, divIdNew[i] ) > 0 ) {
      sub(divIdNew[i], divIdOld[i], revLn);
      #printf "\ndivId chgd: %s", revLn;    
    }

  }

  print revLn >> revertedFN;


}
END { 
  system("sort "revertedFN"  > "sortRevFN);
  system("rm -f "revertedFN);

  # then do: diff sortRevFN sorted_original_EIDC_file
  # there should be no differences!
}

