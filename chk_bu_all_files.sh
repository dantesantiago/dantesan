#!/bin/bash
# DES--2013-12-02 - chk_bu_.sh
# dantesan--2016-09-26--SOS -- chk_bu_all_files.sh  - filesToBackup - list of files to back up
# dantesan--2018-01-24--VSP -- add .loadreport in the files to backup
# dantesan--2019-09-24--CTI -- Cigent Technology, Inc. - add Javascript files
#                 
# check if a file has changed/been updated
# - if updated, make a backup
# - to be executed in directory: 
# - to be executed in directory: "/cygdrive/C/Users/dantesax/DeskTop/FVE/ISG/FPT"
# - when adding files, the names should be in alphabetical order
# cannot add randomly! Error in FPT: backs up also the succeeding files after new files (in alphabetical/numerical order)
# if adding new file not the last one in alphabetical/numerical order: turn off chk_bu...sh
#                                                                      and copy to backup dir and run
#                                                                      chk_bu...sh again!
# sample calls:
# call: chk_bu_FPT.sh `pwd`/bu/r.tmp  >>  bu/2013-05-02.txt 
# call: chk_bu_Grantley.sh bu/r.tmp  >>  bu/2013-05-02.txt 
# r.tmp - has the messages from the sh
# 2013-05-02.txt - saves backup message

#set -x
# dantesan--2015-12-03 -
# NOTE: use $10 in the fileArr line when using in Cygwin. Retain $9 when using in Linux
# Oldest date: DES--2012-06-15 - CatalystRX -> Catamaran ... not used in UAL!

BU_OLD=

# check time and size - from chk_bu.sh
#dsantiago@chsi-mxl7010276[DwinDEV]$ ls -l DMR-502/DMRWeb/Claim.java | awk '{ print $6 }'
#9562
#dsantiago@chsi-mxl7010276[DwinDEV]$ ls -l DMR-502/DMRWeb/Claim.java | awk '{ print $9 }'
#14:31
#dsantiago@chsi-mxl7010276[DwinDEV]$

if [ "$1" == "" ]; then
  echo
  echo "Usage:"
  prg=$0
  #echo "${prg##*/} <output_file_name> <backup_log_file_name>"
  echo "${prg##*/} <output_file_name>"
  echo
  exit 1
fi

#dantesan--2021-02-08 - write PID to a file.
chk_bu_pid_fn=bu/chk_bu.pid
echo $$ > ${chk_bu_pid_fn}

No=N
Yes=Y

outfn=$1
#bulogfn=$2
outszmax=5000
outlnmax=1000
outlnmin=100

# dantesan--2018-01-03 - add cycle and backup counter
cycCtr=0
buCtr=0

#orig_dir="/cygdrive/C/Users/dantesax/Desktop/FVE/TASKS/RCRs/2013/CCG0100010571/DotCS"
# 2014-02-26
#orig_dir="/cygdrive/C/Users/dantesax/Desktop/FVE/TASKS/RCRs/2014/ME10.0/CCG0100010496/dotCS"
# 2014-04-04
#orig_dir="/cygdrive/C/Users/dantesax/Desktop/FVE/TASKS/RCRs/2014/ME10.0/CCG0100010832/dotCS"
# 2014-04-16
#orig_dir="/cygdrive/C/Users/dantesax/Desktop/FVE/TASKS/OTH/RPMC_Automation/dotCS"
# 2014-05-27
orig_dir=`pwd`
# 2015-09-17 - backup_directory - CTO - change this for the location of the backup sub-directory
# dantesan--2016-02-24 - all files can now be backed up
# dantesan--2016-05-18 - before running, need to copy all the files to backup in bu_dir, 
#                        checl filesToBackup variable, 
#                        change chkOrigFiles() if adding new file type
bu_dir=bu_dir 
bu=bu

if [ ! -d ${bu} ]; then
  mkdir ${bu}
fi

# dantesan-2021-03-10--sada - Create $BUXTMP if it does not exist!
BUXTMP=bu/x.tmp
if [ ! -f ${BUXTMP} ]; then
  echo "" > ${BUXTMP}
fi


if [ ! -d ${bu_dir}/${bu} ]; then
  mkdir -p ${bu_dir}/${bu}

  # dantesan--2017-08-29 - copy the files to bu_dir
  cp -p *.* bu_dir/.
fi

# dantesan--2020-05-15 (sada) - fix #LS-L_RESULTS_10_POS and #LS-L_RESULTS_9_POS
#                      - set DOMAIN_USER variable "Y" when #LS-L_RESULTS_9_POS
LSLR09P=9
LSLR10P=10
len_lsl=`ls -l | grep bu_dir | awk '{print NF}'`
#len_lsl=0 #Error test
if [ ${len_lsl} -eq ${LSLR09P} ]; then
  DOMAIN_USER=${No}
fi
if [ ${len_lsl} -eq ${LSLR10P} ]; then
  DOMAIN_USER=${Yes}
fi
if [ -z ${DOMAIN_USER} ]; then
  echo >&2
  echo >&2
  echo "DOMAIN_USER is not defined." >&2
  echo "Please check length of 'ls -l' results." >&2
  echo "Result should be either "${LSLR09P}" or "${LSLR10P}"." >&2
  echo >&2
  exit 1
fi
# dantesan--2020-05-15 (sada) - fix #LS-L_RESULTS_10_POS and #LS-L_RESULTS_9_POS

# sada -- dantesan-2020-04-14 - create $1 if not existing yet ...
if [ ! -f $1 ]; then
  echo "" > $1
fi

# dantesan--2016-02-24 - put the list of files to back up in this variable
# dantesan--2016-03-15 - HWA! - backup multiple make files (Makefile --> Makefile*)
# dantesan--2016-03-30 - Add Perl programs
# dantesan--2016-05-18 - this will be overriden by chkOrigFiles                # c for ,pc file - dantesan--2016-09-26--SOS
# dantsa--2016-12-07 - Add story files
# dantsa--2016-12-08 - Add CFF files
# dantsa--2017-02-02 - Add dat files
# dantsa--2017-03-15 - Add awk files - Happy 14th Anniversary!
#filesToBackup="${bu_dir}/Makefile* ${bu_dir}/*.c ${bu_dir}/*.h ${bu_dir}/*.p[lmc] ${bu_dir}/*.java ${bu_dir}/*.story ${bu_dir}/*.cff ${bu_dir}/*.sh ${bu_dir}/*.dat ${bu_dir}/*.awk"
# dantesan--2017-03-16 - remove .dat for now
#filesToBackup="${bu_dir}/Makefile* ${bu_dir}/*.c ${bu_dir}/*.h ${bu_dir}/*.p[lmc] ${bu_dir}/*.java ${bu_dir}/*.story ${bu_dir}/*.cff ${bu_dir}/*.sh ${bu_dir}/*.awk"

# sample run: chk_bu_all_files.sh bu/x.tmp > bu/2016-02-24.txt & (fg to return)
#             tail -f bu/x.tmp

# dantesan--2016-09-26 - SOS - check if Linux/Unix or Cygwin
#						 SOS - Secretary of State CA - Natoma Technology - EFS project
uName=`uname`
# check if Cygwin
echo ${uName} | grep "CYGWIN"
if [ $? -eq 0 ]; then
  	cygwinBU=${Yes}    # bu in Cygwin
else
  	cygwinBU=${No}	   # bu in Linux or Unix
fi
# dantesan--2016-09-26 - SOS - check if Linux/Unix or Cygwin


cd "$orig_dir"
pwd

# ------------------ Subroutine ----------------------------------
num_files_orig=0


# dantesan--2016-05-18 - need to check if files exist to avoid error messages:
# ls: cannot access bu_dir/*c: No such file or directory
# ls: cannot access bu_dir/*h: No such file or directory
# ls: cannot access bu_dir/Makefile*: No such file or directory
# ls: cannot access bu_dir/*c: No such file or directory
# ls: cannot access bu_dir/*h: No such file or directory
# ls: cannot access bu_dir/Makefile*: No such file or directory

chkOrigFiles() {
  # this is ran once before the while loop
  filesToBackup=

  # Makefile
  ls -l Makefile* 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${bu_dir}/Makefile*"
  else
    filesToBackup=
  fi
  
  # C files
  ls -l *.c 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.c"
  fi
  
  # H files
  ls -l *.h 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.h"
  fi
  
  # perl files ... dsantiago--2018-08-22 - ... and python ...
  ls -l *.p[lmy] 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.p[lmy]"
  fi
  
  # java files
  ls -l *.java 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.java"
  fi
  
  # dantsa--2016-12-07 - Add story files
  ls -l *.story 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.story"
  fi

  # dantsa--2016-12-08 - Add CFF files
  ls -l *.cff 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.cff"
  fi

  # dantesan--2017-01-03 - Add SH files
  ls -l *.sh 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.sh"
  fi

  # sada - dantesan--2020-04-13 - Add XML files
  ls -l *.xml 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.xml"
  fi

  # dantesan--2017-02-02 - Add dat files
  # dantesan--2017-03-16 - remove .dat for now
#  ls -l *.dat 2> /dev/null
#  if [ $? -eq 0 ]; then
#    filesToBackup="${filesToBackup} ${bu_dir}/*.dat"
#  fi

  # dantesan--2017-03-15 - Add awk files
  ls -l *.awk 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.awk"
  fi

  # dantesan--2017-12-26 - Add json files
  ls -l *.json 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.json"
  fi

  # dantesan--2018-01-24--VSP
  ls -l *.loadreport 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.loadreport"
  fi

  # dantesan--2018-08-27--Cigent
  ls -l *.xls* 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.xls*"
  fi

  # dantesan--2018-09-24--Cigent
  ls -l *.js 2> /dev/null
  if [ $? -eq 0 ]; then
    filesToBackup="${filesToBackup} ${bu_dir}/*.js"
  fi

  #dsantiago--2018-08-22 - python first time backed-up
  #echo "<${filesToBackup}>---------------------------------"
  

} # chkOrigFiles()


chk_files() {

  #if [ ! -d bu ]; then
  #  mkdir bu
  #fi

  # dantesax--2014-11-05 - check if new file is not backed-up yet!
  #new_file=`ls -ltr src/*.java | tail -1 | awk '{ print $10 }'`  - src directory does not exist for java files - dantesan--2015-09-16
  #new_file=${new_file##*/}                                      - use java_dir in place of src
  ## check if in bu already                                      - if there is no intermediate directory, the java will always be backedup as Exstream saves it!
  #ls -l src/bu/${new_file}* > /dev/null                         - without an intermediate directory (mdb_dir), one db was save 15 times in 15 minutes!
  #


  # dantsa--2017-02-10 - always update bu_dir - just copy new files to run directory!
  #cp -p *.* bu_dir/.
  # Makefile is the only file with no '.'!
  #if [ -f Makefile ]; then
  #  cp -p Makefile bu_dir/.
  #fi
  
  #if [ $? -ne 0 ]; then

    # dantesax--2014-12-01 - This fixed the problem of adding new files! Just -ls -ltr!
    # dantesax--2015-01-25 - define 'BU_OLD=' if files to be backed up are old!
    # dantesan--2015-12-03 - java files are not being saved into fileArr because it should be $9, not $10 (cygwin)

    #WRONG_POS_ERROR - 2020-05-08 - See notes in PANDUIT/NOTES/2020/05/W2/iNotes--2020-05-08--Automation.txt by searching #WRONG_POS_ERROR_ANALYSIS.
    #                             - Due to windows update???!!

    if [ -z "$BU_OLD" ]; then
		if [ "${cygwinBU}" == "${Yes}" ]; then
                #WRONG_POS_ERROR - 2020-05-08 - Fix is to set the number of info returned by ls -l
                  if [ ${DOMAIN_USER} == ${Yes} ]; then
      		    fileArr=(`ls -l ${filesToBackup} | awk '{print $1" "$2" "$3" "$5" "$6" "$7" "$8" "$9" "$10}' | awk '{ print $9 }' 2>/dev/null | xargs`) # -ltr - new files at the end of the list!
                  else 
      		    fileArr=(`ls -l ${filesToBackup} | awk '{ print $9 }' 2>/dev/null | xargs`) # -ltr - new files at the end of the list!
                  fi
		else
      		fileArr=(`ls -l ${filesToBackup} | awk '{ print $10 }' 2>/dev/null | xargs`) # -ltr - new files at the end of the list!
		fi
      #set -A fileArr `ls -l ${bu_dir}/*.java | awk '{ print $10 }' | xargs 2>/dev/null` # cygwin
    else
		if [ "${cygwinBU}" == "${Yes}" ]; then
                #WRONG_POS_ERROR - 2020-05-08 - Fix is to set the number of info returned by ls -l
                  if [ ${DOMAIN_USER} == ${Yes} ]; then
      		    fileArr=(`ls -l ${filesToBackup} | awk '{print $1" "$2" "$3" "$5" "$6" "$7" "$8" "$9" "$10}' | awk '{ print $9 }' 2>/dev/null | xargs`) # -ltr - new files at the end of the list!
                  else 
      		    fileArr=(`ls -l ${filesToBackup} | awk '{ print $9 }' 2>/dev/null | xargs`) # -ltr - new files at the end of the list!
                  fi
		else
      		fileArr=(`ls -ltr ${filesToBackup} | awk '{ print $10 }' 2>/dev/null | xargs`) # -ltr - new files at the end of the list!
		fi
      #set -A fileArr `ltr -l ${bu_dir}/*.java | awk '{ print $10 }' 2>/dev/null | xargs` # cygwin
    fi

  #else
  #  fileArr=(`ls -l ${bu_dir}/*.java | awk '{ print $10 }' | xargs`) 
  #fi


  # dantesan--2017-03-30 -- BUG(?) found or maybe limitation!-------------------------------------------------------
  # [Thu Mar 30 16:32:17] $  ls -l bu_dir/GISCONSMR-4394--Determination_of_when_to_make_records_ineligible_when_in_Premier_Group_is_incorrect.story bu_dir/GISCONSMR-4394--current.cff bu_dir/GISCONSMR-4394--previous.cff | awk '{ print $10 }' | xargs

  #[Thu Mar 30 16:32:45] $ 

  #verify:

  #[Thu Mar 30 16:37:31] $ fileArr=(`ls -l bu_dir/GISCONSMR-4394--Determination_of_when_to_make_records_ineligible_when_in_Premier_Group_is_incorrect.story bu_dir/GISCONSMR-4394--current.cff bu_dir/GISCONSMR-4394--previous.cff | awk '{ print $10 }' | xargs`)
  #[Thu Mar 30 16:37:36] $ 
  #[Thu Mar 30 16:37:38] $ echo ${fileArr[0]}
  #
  #[Thu Mar 30 16:38:01] $ fileArr=(`ls -li bu_dir/GISCONSMR-4394--current.cff bu_dir/GISCONSMR-4394--previous.cff | awk '{ print $10 }' | xargs`)
  #[Thu Mar 30 16:38:11] $ 
  #[Thu Mar 30 16:38:11] $ echo ${fileArr[0]}
  #bu_dir/GISCONSMR-4394--current.cff
  #[Thu Mar 30 16:38:13] $ 
  #
  #  
  # When the long file name is removed, the array is updated!!!
  # dantesan--2017-03-30 -- BUG(?) found or maybe limitation!-------------------------------------------------------



  filelist=${fileArr[@]}

  num_files=${#fileArr[*]}
  i=${num_files}
  while [ ${i} -ge 0 ]
  do
    ctr[$i]=${i}
    i=`expr ${i} - 1`
    # dantesax--2014-10-03 - initialize vars
    #currfs[$i]=0
    #currtm[$i]= 
  done
  
  file_count=${ctr[@]}

  i=${num_files}
  #if [ ${num_files_orig} -eq 0 ]; then
    while [ ${i} -ge 0 ]
    do
      if [ "${currfs[$i]}" == "" ]; then
        currfs[$i]=0
        currtm[$i]= 
      fi
      i=`expr ${i} - 1`
    done

  #else
  #  currfs[${num_files}]=0
  #  currtm[${num_files}]=
  #fi
  num_files_orig=${num_files}

} # chk_files()


# DES--2013-07-24 
# workaround to remove same backup file
#
#
rmDupFile() { 

  buedFile=$1

  # dantesax--2014-11-05 -- allows new files but backs up almost all previous file
  #                         if one previous file is backed!
  #files=`ls -ltr bu/${buedFile}* | tail -2 | awk '{ print $10 }' | xargs`
  files=`ls -l bu/${buedFile}* | tail -2 | awk '{ print $10 }' | xargs`
  

  file1=`echo ${files} | awk '{ print $1 }'`
  file2=`echo ${files} | awk '{ print $2 }'`

  # only one backup file - return
  if [ "${file2}" == "" ]; then
    return
  fi

  diff ${file1} ${file2} > /dev/null

  # files are same
  if [ $? -eq 0 ]; then  

    echo "Duplicate backup to be deleted ..." > $outfn

    num1=${file1##*_}
    num2=${file2##*_}

    if [ ${num1} -gt ${num2} ]; then
      rm -f ${file1}
    else
      rm -f ${file2}
    fi

  fi
  
} # rmDupFile()
# ------------------ Subroutine ----------------------------------

# dantesan--2016-05-18 - check the files to backup
chkOrigFiles

while [ 1 == 1 ]
do

  chk_files  

  ctr=0
  dir0=

  # check output file
  if [ -f $outfn ]; then
    #outsz=`ls -l $outfn | awk '{ print $6 }'`
    #if [ $outsz -gt $outszmax ]; then
    #  echo "" > $outfn
    #fi
    outln=`wc -l ${outfn} | awk '{ print $1 }'`

    # dantesax--2013-06-14 - BOINK!!! /home/dantesax/awk was created! dunno ...
    #                      - export PATH=/usr/bin:${PATH}
    if [ "${outln}" == "" ]; then
      numlns=`wc -l ${outfn}`
      outln=`echo "${numlns}" | awk '{ printf "%s\n", substr( $0, 1, 4 }'`
    fi
    if [ ${outln} -ge ${outszmax} ]; then
      echo " " >> ${outfn}
      echo " " >> ${outfn}
      echo "LOG file will be curtailed ..." >> ${outfn}
      echo " " >> ${outfn}
      echo " " >> ${outfn}
      tail -${outlnmin} ${outfn} > ${outfn}
    fi

  fi

  # dantesan--2018-01-03 - add cycle counter
  cycCtr=`expr ${cycCtr} + 1`
  echo >> $outfn
  echo >> $outfn
  echo "---------------------------------------------------------------------------------------" >> $outfn
  echo >> $outfn
  echo "Cycle Number: ${cycCtr}" >> $outfn
      

  for file in ${filelist}
  do

     dir=${file%/*}
     fn=${file##*/}
     if [ "$dir0" != "$dir" ]; then
       echo >> $outfn
       echo "Directory: $dir ----------------------------------------------------------------" >> $outfn
       echo >> $outfn
     fi
     fileno=`expr $ctr + 1`
     echo >> $outfn
     # dantesan--2015-11-23 - put the date
     date >> $outfn
     echo >> $outfn
     #dantesan-sada-2024-11-05 - Cycle number ...
     echo "Cycle no.: $cycCtr   File number: $fileno" >> $outfn
     echo >> $outfn
     echo Checking:$file >> $outfn
     echo "fn = $fn" >> $outfn
     echo "dir = $dir" >> $outfn
     echo >> $outfn

     # dantesax--2013-08-07 - check if a file has been deleted!
     #                      - If a file is deleted or missing, the ${currfs[@]} and ${currtm[@]} arrays
     #                      -   will be not in sync with the contents of the src directory.
     #                      - The arrays need to be reconstructed.
     #if [ ! -f $fn ]; then
     #  break 
     #fi
     
     if [ ${currfs[$ctr]} -eq 0 ] && [ "${currtm[$ctr]}" == ""  ]; then 
       echo >> $outfn
       echo Initializing ... >> $outfn

       # DES--2012-06-15 - make _0 file if not yet backed up
       #dsantiago@chsi-mxl7010276[src]$ ls -l bu/dts_server.cfg_0
       #ls: cannot access bu/dts_server.cfg_0: No such file or directory
       #dsantiago@chsi-mxl7010276[src]$  

       init_file=`ls -l ${bu_dir}/bu/${fn}_0` > /dev/null 2>&1 # > /dev/null solves the problem above!
       if [ $? -ne 0 ]; then
         cp -p ${fn} ${bu_dir}/bu/${fn}_0 >> $outfn
         #WRONG_POS_ERROR - 2020-05-08
         if [ ${DOMAIN_USER} == ${Yes} ]; then
           ls -l ${fn} ${bu_dir}/bu/${fn}_0 | awk '{print $1" "$2" "$3" "$5" "$6" "$7" "$8" "$9" "$10}' >> $outfn
         else
           ls -l ${fn} ${bu_dir}/bu/${fn}_0 >> $outfn
         fi
       fi
       echo >> $outfn

       #sleep 1
       # dantesax--2013-08-07 - When a new file is added, all the succeeding files are backedup!
       #                      - The reason is, the file names/file times in the src directory are not 
       #                      -   in syc with the contents of the ${currfs[@]} and ${currtm[@]} arrays!
       #                      -   got to redo the arrays!
       #                      -   for now, just get out of the loop!
       #break

     fi


     if [ -f $file ]; then
# DES--2012-07-30 - ls -l is different now!
#dsantiago[src]$ ls -l bu/pbs_auto_list_loads.sh_28 pbs_auto_list_loads.sh
#-rwx------+ 1 Administrators mkgroup 10688 Jul 26 15:56 bu/pbs_auto_list_loads.sh_28
#-rwx------+ 1 Administrators mkgroup 10703 Jul 30 09:35 pbs_auto_list_loads.sh
#dsantiago[src]$

		# dantesan--2016-09-26 -- SOS
		if [ "${cygwinBU}" == "${Yes}" ]; then
                  #WRONG_POS_ERROR - 2020-05-08
                  if [ ${DOMAIN_USER} == ${Yes} ]; then
       		    filesize=`ls -l $file | awk '{print $1" "$2" "$3" "$5" "$6" "$7" "$8" "$9" "$10}' | awk '{ print $5 }'` # $5 b4  # Cygwin
       		    filetime=`ls -l $file | awk '{print $1" "$2" "$3" "$5" "$6" "$7" "$8" "$9" "$10}' | awk '{ print $8 }'` # #8 b4  # Cygwin
                  else
       		    filesize=`ls -l $file | awk '{ print $5 }'` # $5 b4  # Cygwin
       		    filetime=`ls -l $file | awk '{ print $8 }'` # #8 b4  # Cygwin
                  fi
		else
       		  filesize=`ls -l $file | awk '{ print $5 }'` # $5 b4   # Linux
       		  filetime=`ls -l $file | awk '{ print $8 }'` # #8 b4   # Linux
		fi

       if [ ${currfs[$ctr]} -ne 0 ] || [ "${currtm[$ctr]}" != ""  ]; then 

         if [ ${currfs[$ctr]} -ne $filesize ] || [ "${currtm[$ctr]}" != "$filetime" ]; then 

           # dantesan--2018-01-03 - add backup counter
           buCtr=`expr ${buCtr} + 1`
           echo >> $outfn
           echo "Backup Ctr: ${buCtr}" >> $outfn
           
           echo >> $outfn
           echo $file has changed ... >> $outfn
           echo >> $outfn
           echo "$fn is to be backed-up. Please see backup log file to get/see name ..." >> $outfn
           echo >> $outfn
           cd $dir
           # sada-dantesan--2020-04-17 - gzip the n-2 version, not the previous one ...
           #                           - so that previous file can be compared ...
           # sada-dantesan--2021-05-27 - add cycle counter
           bufa2 $fn ${cycCtr}
           
           # DES--2015-03-06 - check if backup is done
#           notbued=-2
#           bufarv=`bufa2 $fn` # sada-dantesan--2020-04-17 - bufa to bufa2
#           if [ ${bufarv} -eq ${notbued} ]; then
#             echo "${fn} backup already exists!"
#             echo "No backup is done!"
#           fi
#
           # DES--2013-07-24
           sleep 1
           #rmDupFile ${fn}  # file is the full path name, fn - is the file name only

           # DES--2015-03-06
           # need to really remove the back up if it is the same as previous one!
           #[src]$ remdupbu.sh
           #
           #Please run in bu dir!
           #
           #[src]$ cd bu
           #[bu]$ remdupbu.sh
           #
           #Usage:
           #  remdupbu.sh <file_name> <max_file_no>
           #
           #[bu]$ 

   
           cd "$orig_dir"
           echo >> $outfn
         else
           echo >> $outfn
           echo $file is same ... >> $outfn
           echo >> $outfn
         fi
         #sleep 1
       fi
     else
      
       echo >> $outfn
       echo "WARNING-WARNING-WARNING: $dir/$file does not exist!" >> $outfn
       echo >> $outfn

       filesize=0
       filetime=
     fi

     # 2013-07-24 - Remove duplicate backup file
     #cd $dir
     #rmDupFile ${fn}  # file is the full path name, fn - is the file name only
     #cd "$orig_dir"

     currfs[${ctr}]=$filesize
     currtm[${ctr}]=$filetime
     ctr=`expr $ctr + 1`
  
     dir0="$dir"
  
  done # for

  sleepDuration=3;
  echo >> $outfn
  echo >> $outfn
  
  echo >> $outfn
  # DES--2015-03-06 - New files can now be copied due to the changes in bufa.
  #echo " DO NOT COPY NEW FILES ..." >> $outfn
  echo >> $outfn
  echo >> $outfn
  echo "Zzzzzzzzzz ... zzzzzz ... zzzzzzz ... zzzzzz ... zzzzzzz ..." >> $outfn
  #echo "Zzzzzzzzzz ... zzzzzz ... zzzzzzz ... zzzzzz ... zzzzzzz ... WHEN COPYING NEW FILES, TURN OFF THEN RUN AGAIN AFTER COPYING!" >> $outfn

  echo >> $outfn
  sleep ${sleepDuration} # take a break!
  echo "Zzzzzzzzzz ... zzzzzz ... zzzzzzz ... zzzzzz ... zzzzzzz ..." >> $outfn
  sleep ${sleepDuration} # take a break!
  echo "Zzzzzzzzzz ... zzzzzz ... zzzzzzz ... zzzzzz ... zzzzzzz ..." >> $outfn
  sleep ${sleepDuration} # take a break!
  echo "Zzzzzzzzzz ... zzzzzz ... zzzzzzz ... zzzzzz ... zzzzzzz ..." >> $outfn
  sleep ${sleepDuration} # take a break!
  echo "Zzzzzzzzzz ... zzzzzz ... zzzzzzz ... zzzzzz ... zzzzzzz ... " >> $outfn
  sleep ${sleepDuration} # take a break!

done # while




