#!/bin/awk -f


# function to check if numeric 
function chkNumbr( num ) {
  len    = length( num );
  retNum = match( num, /[^.0-9-]/ );

  if( retNum != 0 ) # && RLENGTH != -1 )
    isNum = ERR_OC;
  else
    isNum = NO_ERR;    

  return isNum;
  
} # chkNum

# function to check if Alphabet 
function chkAlpha( alphaChars ) {
  len    = length( alphaChars );
  retNum = match( alphaChars, /[^ A-Z-]/ );
  
  if( retNum != 0 ) # && RLENGTH != -1 )
    isAlpha = ERR_OC;
  else
    isAlpha = NO_ERR;    

  return isAlpha;
  
} # chkAlpha 

# function to check if Spaces
function chkSpc( spcChar, numSpcs, errMsg ) {

  #retSpc = match( spcChar, /[ ]+/ );
  retSpc = match( spcChar, /[^ ]/ );

  if( retSpc != 0 )
    isSpc = ERR_OC;
  else
    isSpc = NO_ERR;    

  if( isSpc == ERR_OC ) {  
    allErrMsg = allErrMsg" | "errMsg;
    errRet = isSpc;
  }

  return isSpc;
}  

function chkVal( sepVal, substrVal, type, errMsg ) {


  chkValRV = NO_ERR;

  if( sepVal != substrVal ) {

    chkValRV = ERR_OC;

  } else {
    
    if( type == ALPHA ) {
      chkValRV = chkAlpha( substrVal );
    } else {    
      chkValRV = chkNumbr( substrVal );
    }  

  }
  
  if( chkValRV == ERR_OC ) {  
    #if( allErrMsg == "" )
       #allErrMsg = errMsg;
    #else
      allErrMsg = allErrMsg" | "errMsg;
  }

  if( chkValRV == ERR_OC )
    errRet = chkValRV;

  return chkValRV allErrs;
  
} # chkValue

function printErrorLine( LineNum, LineContents ) {
   printf( "%s: %s\n", LineNum, LineContents ) >> errFileOut;
   printf( "ERRORS: %s\n\n", allErrMsg ) >> errFileOut;
   if( errRet == NO_ERR )
     errRet = ERR_OC;
   return errRet;         
} # printErrorLine

function printGoodCCPOAdat( LineContents ) {
   printf( "%s\n", LineContents ) >> goodCCPOAdat;
   return;         
} # printGoodCCPOAdat
  
  

BEGIN { 

  FS=","; 

  # field variables
  -v memDepInd; 
  -v mdiErr;    mdiErr    = "memDepInd";
  
  -v ssn;       
  -v ssnErr;    ssnErr    = "SSN";
   
  -v fNmIni;    
  -v fNmErr;    fNmErr    = "fNmIni";
  
  -v sNmIni;    
  -v sNmErr;    sNmErr    = "sNmIni";
  
  -v lastNm;    
  -v lNmErr;    lNmErr    = "lastNm";
  
  -v num6;      
  -v num6Err;    num6Err  = "num6";
    
  -v num7;      
  -v num7Err;    num7Err  = "num7";
  
  -v premAmt;   
  -v premAmtErr;premAmtErr  = "premAmt";
    
  -v num9;      
  -v num9Err;    num9Err  = "num9";  
  
  -v mm;        
  -v mmErr;     mmErr     = "mm";
  
  -v ccYY;      
  -v ccYYErr; ccYYErr     = "ccYY";
    
  -v num12;     
  -v num12Err;  num12Err  = "num12";    
  
  -v popType;     
  -v popTypeErr;popTypeErr  = "popType";
    
  -v amt14;     
  -v amt14Err; amt14Err   = "amt14";
    
  -v id15;      
  -v id15Err;    id15Err  = "id15";
    
  -v num16;     
  -v num16Err;  num16Err  = "num16"; 
    
  -v spc17;     
  -v spc17Err;  spc17Err  = "spc17"; 
    
  -v num18;     
  -v num18Err;  num18Err  = "num18"; 
    
  -v spc19;     
  -v spc19Err;  spc19Err  = "spc19"; 
    
  -v premAmt20;       
  -v premAmt20Err;premAmt20Err  = "premAmt20";
   
  # additional variables
  
  -v NO_ERR;    NO_ERR    = 2;   # true in C Programming
  -v ERR_OC;    ERR_OC    = 0;   # false in C Programming
  -v errRet;    errRet    = NO_ERR;
  
  -v ALPHA;     ALPHA     = 2;
  -v NUM;       NUM       = 5;
  
  -v numLine;   numLine   = 0;
  
  -v allErrMsg Msg; allErrMsg = "";
  
  -v errFileOut; errFileOut   = "errFileOut.dat";
  -v goodCCPOAdat;   goodCCPOAdat = "goodCCPOA.dat";

  
  
}  # BEGIN

{ 

  
  numLine++; 

  allErrMsg = "";

  errRet = NO_ERR;

  
  # Check Member Indicator
  memDepInd = $1;
  memIndChk = substr( $0, 1, 1);
  if( memIndChk != memDepInd || ( memIndChk != "M" && memIndChk != "D" ) ) {
      errRet = ERR_OC;
      #sprintf( allErrMsg, " %s ", mdiErr );
      allErrMsg = mdiErr;
  }
  
  
  # Check SSN
  ssn       = $2;
  ssnChk = substr( $0, 3, 9);
  chkVal( ssn, ssnChk, NUM, ssnErr ); 

  # Check first name initial
  fNmIni    = $3;
  fNmIniChk = substr( $0, 13, 1 );
  chkVal( fNmIni, fNmIniChk, ALPHA, fNmErr );
  
  # Check second name initial
  sNmIni    = $4;
  sNmIniChk = substr( $0, 15, 1 );
  chkVal( sNmIni, sNmIniChk, ALPHA, sNmErr );

  # Check last name
  lastNm    = $5;
  lastNameChk = substr( $0, 17, 13 );
  chkVal( lastNm, lastNameChk, ALPHA, lNmErr );
  
  # Check num6 - CTO
  num6      = $6;
  num6Chk = substr( $0, 31, 3 );
  chkVal( num6, num6Chk, NUM, num6Err );
  
  # Check num7 - CTO
  num7      = $7;
  num7Chk = substr( $0, 35, 3 );
  chkVal( num7, num7Chk, NUM, num7Err );  
  
  # Check premAmt
  premAmt   = $8; sub(/^[ ]+/, "", premAmt ); 
  premAmtChk = substr( $0, 39, 9 );
  sub(/^[ ]+/, "", premAmtChk );
  chkVal( premAmt, premAmtChk, NUM, premAmtErr );

  # Check num9 - CTO
  num9      = $9;
  num9Chk = substr( $0, 49, 1 );
  chkVal( num9, num9Chk, NUM, num9Err );
 
  # Check mm
  mm        = $10;
  mmChk = substr( $0, 51, 2 );
  chkVal( mm, mmChk, NUM, mmErr );

  # Check ccYY
  ccYY      = $11;
  ccYYChk = substr( $0, 54, 4 );
  chkVal( ccYY, ccYYChk, NUM, ccYYErr );
  
  # Check num12 - CTO
  num12     = $12;
  num12Chk = substr( $0, 59, 3 );
  chkVal( num12, num12Chk, NUM, num12Err );  

  # Check popType - CTO 
  popType   = $13;
  popTypeChk = substr( $0, 63, 3 );
  chkVal( popType, popTypeChk, NUM, popTypeErr );
  
  # Check amt14 - CTO
  amt14     = $14; sub(/^[ \t]+/, "", amt14 );
  amt14Chk = substr( $0, 67, 9 );
  sub(/^[ \t]+/, "", amt14Chk );
  chkVal( amt14, amt14Chk, NUM, amt14Err );     
  
  # Check id15 - CTO
  id15      = $15;
  id15Chk = substr( $0, 77, 8 );
  chkVal( id15, id15Chk, NUM, id15Err );  
  
  # Check num16 - CTO
  num16     = $16;
  num16Chk = substr( $0, 86, 1 );
  chkVal( num16, num16Chk, NUM, num16Err );  

  # Check spc17 - CTO
  spc17     = $17; # single space
  #spc17Chk = substr( $0, 88, 1 );
  chkSpc( spc17, 1, spc17Err );  
  
  # Check num18 - CTO
  num18     = $18;
  num18Chk = substr( $0, 90, 3 );
  chkVal( num18, num18Chk, NUM, num18Err );  
  
  # Check spc19 - CTO
  spc19     = $19; # 3 spaces
  #spc19Chk = substr( $0, 94, 3 );
  chkSpc( spc19, 3, spc19Err );  
    
  # Check premAmt20
  premAmt20 = $20; sub(/^[ \t]+/, "", premAmt20 );
  sub( /[\n]$/, "", premAmt20 );
  # remove line feed! This causes error if not removed!
  sub( /[\r]$/, "", premAmt20 ); 
  premAmt20Chk = substr( $0, 98, 9 );
  sub(/^[ \t]+/, "", premAmt20Chk );
  chkVal( premAmt20, premAmt20Chk, NUM, premAmt20Err );    
  
    
  if( errRet == ERR_OC )
    printErrorLine( numLine, $0 );
  else  # Line is good!
    printf( "%s\n", $0 ) >> goodCCPOAdat;  
    
  allErrMsg = "";  

}
END { 
}

