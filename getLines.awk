#!/bin/awk -f

BEGIN {
  
  mfFN = "mf.g4492678_no_hdr_sorted_spc_rem";
  #mfFN = "mf.g4492678_no_hdr_sorted_10";
  numLines = 522634;
  diffLinesFN = "diff_lines.dat";
  currLineFN = "currLine.dat";

}

{
  gisLine = $0;
  sub( /[\r\n]$+/, "", gisLine );
  lineNo = lineNo + 1;

  gisLine = system( "echo \""gisLine"\"" );

  #if ( lineNo == 2 ) 
  #  exit;

  mfLine = system( "head -"lineNo" "mfFN" | tail -1" );
  #mfLine = system( "grep -n\""gisLine"\"" mfFN);
  #mfLine = system( "grep \""gisLine"\"" mfFN);

  mfLine = system( "echo "mfLine );

  #sub( /[\r\n]$+/, "", mfLine );

  print lineNo >> currLineFN;
  if( gisLine != mfLine ) {
    print lineNo >> diffLinesFN;
  } else {
    printf "\nNO_DIFF!\n";
  } 

  
}

END {

}
