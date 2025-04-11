#!/bin/bash
# dantesan--2020-10-09--sada - Copied from vigzip.sh and modified.
# dantesan--2015-12-28 -- Vi the Gzipped (even if not) Version/Backup
# This should be called only in the directory of the file to replace
# followed shell script convention - 0 - true, not 0 - false
# Linux version

# dantesan--2016-04-11 - use standard bu_dir directory
#                        instead of $[ext}_dir directory.

#set -x 

LASTBACKUP=1000

prg=$0

uDir=_dir
buDir=bu
tmpDir=tmp
yes=0 #YES
no=1 #NO 

fileDNE=3 # File Does Not Exist

# flag to check if decompressed
decompd=${no}
# gzip extension
gZipExt=.gz

asterisk=*

# dantesan--2016-10-11 -- check if Linux or Cygwin
OStype=`uname`
echo ${OStype} | grep "CYGWIN"
if [ $? -eq 0 ]; then
	cygwinOS=${yes}
else
	cygwinOS=${no}
fi

# tmpFileCopy - temp file copy

# dantesan--2016-04-11 - standard bu_dir
#if [ "$3" == "" ]; then
if [ "$2" == "" ]; then
  echo
  echo "Usage:"
  #prg=$0
	# dantesan--2016-04-11 - standard bu_dir
  #echo "${prg##*/} <file_name> <file_type or ext> <version_num>"
  echo "${prg##*/} <file_name> <version_num> <string_to_search>"
  echo " use: ${LASTBACKUP} for version/backup number to get last backup"
  echo
  exit 1
fi

# check tmp dir
if [ ! -d ${tmpDir} ]; then
  mkdir ${tmpDir}
fi

# get the file name, remove ext
#[dt209853@edhlsmakd002]$ fn=TmoltrsUnloader.java
#[dt209853@edhlsmakd002]$ echo ${fn%%.*}
#TmoltrsUnloader
#[dt209853@edhlsmakd002]$ fn=TmoltrsUnloader
#[dt209853@edhlsmakd002]$ echo ${fn%%.*}
#TmoltrsUnloader
#[dt209853@edhlsmakd002]$ 

# dantesan--2016-04-11 - standard bu_dir
#fileNm=$1
#fileName=${fileNm%%.*}
fileName=$1
#fileExt=$2
#fileNamePlusExt=${fileName}.${fileExt}
fileNamePlusExt=${fileName}
#extDir=$2${uDir}
#subDir=${extDir}/bu
subDir=bu_dir/bu

# decompressed file name
gUnzipd=${subDir}/${fileNamePlusExt} # will have buNum later

# ext_dir/filename + .extension
fpFileName=${extDir}/${fileNamePlusExt}  # changes to this file will create backups when chk_bu is running!
# tmp file
tmpFileName=${tmpDir}/${fileNamePlusExt}
# ext_dir/bu_dir/filename + .extension
fpBuFileName=${subDir}/${fileNamePlusExt}  

# dantesan--2016-04-11 - standard bu_dir
if [ "$2" = "" ]; then
  buNum=${LASTBACKUP}
else
# dantesan--2016-04-11 - standard bu_dir
  #buNum=$3
  buNum=$2
fi

# unzipped bu file name
uzBUFileName=${subDir}/${fileNamePlusExt} #_${buNum}
gzipdBuFN=

# file size-date-time
fileSzDT=
tempSzDT=

# ---------------------------------------------------------------------------
# SUBROUTINE/S
function gZipFile() {

  uzBUFileName=$1
  gzipdBuFN=${uzBUFileName}${gZipExt}

  # chec if file exists ...
  if [ -f ${uzBUFileName} ]; then
    gzip -9 -S ${gZipExt} ${uzBUFileName}
  else
    echo
    echo "${uzBUFileName} does not eexists! Nothing to gzip!"
    echo
  fi 

  # CTO - check if gzipped

} # function gZipFile()

function decompGZ() {

  gzipdBuFN=$1                  # gzipdBuFN=java_dir/bu/TmoltrsUnloader.java_8.gz
  uzBUFileName=${gzipdBuFN%.*}  # uzBUFileName=${gzipdBuFN%.*} = java_dir/bu/TmoltrsUnloader.java_8

  if [ -f ${gzipdBuFN} ]; then
    gzip -d ${gzipdBuFN}
    decompd=${yes}
  else
    echo
    echo "${gzipdBuFN} does not eexists! Nothing to decompress!"
    echo
  fi 


  # CTO - check if decompressed

} # function decompGZ()

# get the file size-date-time
function getFSzDT() {

  local fileName=$1  # the file name
  local bufn=$2      # if 0 or ${yes}, the bu file name
                     # if 1 or ${no}, the tmp file name
	

  

  if [ -f ${fileName} ]; then

		# dantesan--2016-10-11 -- check OStype
		if [ ${cygwinOS} -eq ${yes} ]; then
    	local filesdt=`ls -l ${fileName} | awk '{ printf"%s-%s-%s-%s\n", $6, $7, $8, $9 }'`
		else
    	local filesdt=`ls -l ${fileName} | awk '{ printf"%s-%s-%s-%s\n", $5, $6, $7, $8 }'`
		fi

  else
    local filesdt=
  fi

  if [ ${bufn} -eq 0 ]; then # bu file
    fileSzDT=${filesdt}
  else  		    # temp file
    tempSzDT=${filesdt}
  fi

} # function getFSzDT()



# SUBROUTINE/S
# ---------------------------------------------------------------------------

# file name + .extension + bu number

# check if viewing LASTBACKUP
if [ ${buNum} -eq ${LASTBACKUP} ]; then

  # get last backup ...
  # Last backup is in $2${extDir}, but 
  #cp -p ${fpFileName} ${tmpFileName}

	# dantesan--2016-10-11 -- check OStype
	if [ ${cygwinOS} -eq ${yes} ]; then
  	tmpBUFileName=`ls -ltr ${fpBuFileName}* | tail -1 | awk '{ printf "%s\n", $10 }'`
	else
  	tmpBUFileName=`ls -ltr ${fpBuFileName}* | tail -1 | awk '{ printf "%s\n", $9 }'`
	fi

else
  #tmpBUFileName=`ls -ltr ${uzBUFileName}_${buNum}* | tail -1 | awk '{ printf "%s\n", $9 }'`
  # check if file does not exist!
  ls -ltr ${uzBUFileName}_${buNum}${asterisk} >/dev/null 2>&1
  if [ $? -eq 0  ]; then 

		# dantesan--2016-10-11 -- check OStype
		if [ ${cygwinOS} -eq ${yes} ]; then
    	tmpBUFileName=`ls -ltr ${uzBUFileName}_${buNum}${asterisk} | tail -1 | awk '{ printf "%s\n", $10 }'`
		else
    	tmpBUFileName=`ls -ltr ${uzBUFileName}_${buNum}${asterisk} | tail -1 | awk '{ printf "%s\n", $9 }'`
		fi

  else
    echo
    echo "File or backup: ${uzBUFileName}_${buNum}${asterisk} does not exist!"
    echo
    echo "Nothing to view!"
    echo
    echo "Done ..."
    echo
    exit ${fileDNE}
  fi
fi


# check if gzipped
echo ${tmpBUFileName} | grep ${gZipExt} > /dev/null
# check if gzipped
if [ $? -eq 0 ]; then
  decompGZ ${tmpBUFileName} # uzBUFileName is set in decompGZ.
else
  uzBUFileName=${tmpBUFileName}
fi
# make a backup
#cp -p ${fpFileName} ${tmpFileName}
cp -p ${uzBUFileName} ${tmpFileName}
if [ $? -eq 0 ]; then
  cpMade=${yes}        # CTO - use this!
else
  cpMade=${no}
fi

grep -n $3 ${uzBUFileName}

# does not work if saved, but no changes were done
#diff ${uzBUFileName} ${tmpFileName} > /dev/null
getFSzDT ${uzBUFileName} ${yes}
getFSzDT ${tmpFileName} ${no}

if [ "${fileSzDT}" != "${tempSzDT}" ]; then
  echo
  echo "File was changed ... It will be restored ..."
  echo
  cp -f -p  ${tmpFileName} ${uzBUFileName} 
fi
# check if decompd
if [ ${decompd} -eq 0 ]; then
  gZipFile ${uzBUFileName}
fi
echo
echo "Done ..."
echo




