#!/bin/bash
# dantsa--2018-02-16 - Interactive Automated Deployment Script
# dantesan--2018-02-22 - for CR

#set -x

ENVS="TEST PROD"
testServerNames="jetty1 jetty3"
prodServerNames="gis2con-jetty01 gis2con-jetty02 gis2con-jetty03 gis2con-jetty04 gis2con-jetty05 gis2con-jetty06 gis2con-jetty07" 
TEST=TEST
PROD=PROD

# valid machines where this script will run
tstSrvr=gis2con-jetty01-test
prdSrvr=gis2con-jetty01

srvrNmNA=gis2con

jettyMachNum=jetty

# server to Deploy
serverToDeploy=

# comment out when not developing ...
DEV=YES

SUCCESS=success

# common dir
#releaseAutomationDir=/gis2con/common/deployRelease
releaseAutomationDir=`pwd`	

# jetty PID
jettyPId=0
#startJetty?
stJy=YES
# chk Processing Count?
chkPC=YES

# Interactive mode is set!
interactiveMode=I
iMode=
typeset -u iMode

# exit or return values ---------------------------------------
exitOK=0
exitDRend=0
exitWU=1
exitNLI=2
exitProc=3
exitAbort=4
exitNG=5
retNF=6
exitDJE=7
exitSJE=8 
exitRLE=9
exitPLE=10
exitCSE=11
retDRends=0

# exit or return values ---------------------------------------

#messages --------------------------------------------
ERRR="ERROR:"
WARN="WARNING:"
serverNLI="Please log in to the server:"
serverProc="The server is currently processing. Please try again later."
deployCont="Server is not processing load. " # Deployment will continue ..."



chkServerExist="Checking server ..."
chkProcessing="Checking if server is processing ..."

deployInfo="This will do the actual deployment!"
doYouWantToCont="Do you want to continue? (press Y/y to confirm)"
contDeploy="Continue to deploy ..."
abortDeploy="Abort deployment ..."

#pauseListener
pauseListenerRun="This will now pause the listener ..."
pauseListenerExecdGD="Pause listener returned SUCCESS!"
pauseListenerExecdNG="Pause listener returned ERROR! NG!"
deploymentCantContnu="Deployment cannot continue."
pLRetNGButProcCntZero="Pause Listeners returned NG, but Processing Count is zero. Good to continue deployment."

#killJetty
jettyJarTBK="This will now kill the jetty jar file running ..."
jettyJarNF="The instance of the jetty jar file running is NOT found!"
jettyStopNG="The jetty jar was NOT killed!"
jettyStopOK="The jetty jar was killed!"

#deployJetty
deploymentSt="Deployment starts ..."
deploymentWB="Deployment will begin ..."
deployJettyOK="Deployment script returned SUCCESS ..."
deployJettyNG="Deployment script returned ERROR ..."
deployNGRestart="Do you want to restart jetty and resume listeners?" 
jenkinsBuildNoMsg="Please enter the jenkins build number:"


#startJetty
startJettyInfo="Jetty will now be started ..."
startJettyOK="Start jetty run is GOOD!"
startJettyNG="Start jetty has ERROR!"
stopJettyInfo="Jetty will now be stopped ..."
stopJettyNG="Stop jetty did NOT work!"
stopJettyOK="Stop jetty run is GOOD!"
startJettyDSDone="Jetty is already started by the deploy script ..."

#resumeListener
resumeListenerExecdGD="Resume listener returned SUCCESS!" 
#resumeListenerExecdNG="Resume listener returned ERROR! NG! Please run later!"
resumeListenerExecdNG="Resume listener returned ERROR! NG! Unverified deployment!"

dREnds="Run auccessfully and deployed the latest release in the server above above,"
dRDone=" - DEPLOYED!"

#Usage
invEnv="Invalid environment!"
invSrv="Invalid server name!"
useTstSrvr="You are deploying in GISTEST, please run this script in ${tstSrvr}!"
usePrdSrvr="You are deploying in GISPROD, please run this script in the PROD server!"

createCffSkltnInfo="Create CFF Skeleton is executed to verify deployment ..."
createCffSkltnGD="Create CFF Skeleton returned GOOD! Deployment GOOD!"
createCffSkltnNG="Create CFF Skeleton returns ERROR! Deployment ERROR!"
#mediaId=7771717
cCSChkStr="mediaId"
cCSChkErr="Error"
getJettyPIdGD=" ... is running!"
getJettyPIdNG=" ... NOT running!"



#messages --------------------------------------------

# shell scripts called -------------------------------
getServerStatusSh=getServerStatus.sh
pauseListenersSh=pause-listeners.sh
resumeListenersSh=resume-listeners.sh
deployJettySh=deploy-jetty.sh
startJettySh=start-jetty.sh
createCffSkltnSh=createCffSkeleton.sh
stopJettySh=stop-jetty.sh
# shell scripts called -------------------------------


# Subroutines --------------------------

showMsg() {


  if [ -z ${DEV} ]; then
    dashChar="--------------------------------------------------------------------------------"
    equalChar="================================================================================"
  else
    dashChar="--------------------------------------------------------------------DEV-TST-----"
    equalChar="====================================================================DEV=TST====="
  fi

  case "${2}" in

  "1")
    sep1=
    sep2=${dashChar}
    ;;

  "2")
    sep1=${equalChar}
    sep2=${sep1}
    ;;

  "3")
    sep1=${dashChar}
    sep2=
    ;;

  "4")
    sep1=${dashChar}
    sep2=${sep1}
    ;;

  "5")
    echo
    echo "START-START-START-START-START-START-START-START-START-START-START-START-START-ST"
    echo
    return 0
    ;;

  "6")
    echo
    echo "END-END-END-END-END-END-END-END-END-END-END-END-END-END-END-END-END-END-END-END-"
    echo
    return 0
    ;;

  "7")
    echo
    echo "ABORT-ABORT-ABORT-ABORT-ABORT-ABORT-ABORT-ABORT-ABORT-ABORT-ABORT-ABORT-ABORT-AB"
    echo
    return 0
    ;;

  "8")
    echo
    echo "ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ER"
    echo
    return 0
    ;;

  "9")
    echo
    echo "WARNING-WARNING-WARNING-WARNING-WARNING-WARNING-WARNING-WARNING-WARNING-WARNING-"
    echo
    return 0
    ;;

  *)
    sep1=
    sep2=
    ;;

  esac

  echo ${sep1}
  echo "$1"
  echo ${sep2}

}

# retunn 0 when Y/y
getReply() { 
  
  if [ "${iMode}" != "${interactiveMode}" ]; then
    return ${exitOK}
  fi

  showMsg "${1}" ${2}
  typeset -l answer
  read answer
  if [ "${answer}" == "y" ]; then
    return ${exitOK}
  else
    return ${exitAbort}
  fi
}


vrfyCntnuDplymnt() {

  getReply "${doYouWantToCont}" 1
  if [ $? -eq 0 ]; then
    showMsg "${contDeploy}" 
  else
    showMsg "${abortDeploy}"
    exit ${exitAbort}
  fi 

}

chkProcessingCnt() {

  showMsg "${chkProcessing}" 1

  # check if the server is currently processing a data
  #ssh ${serverToDeploy} "serverStatus=`${shellScriptDir}/${getServerStatusSh}`" > /dev/null

  serverStatus=`./${getServerStatusSh}`

  procLoad=`echo "${serverStatus}" | grep processedCount 2>/dev/null`
  procCnt=`echo ${procLoad} | awk -F: '{ print $2 }' |  awk -F, '{ print $1 }'`

  if [ ${procCnt} -gt 0 ]; then
    showMsg "${WARN} ${procLoad}"  # |  ${serverProc}" #EXTRA_MSG 
    showMsg "${serverProc}" 1
    echo
    echo
    return ${exitProc}
  else
    showMsg "${procLoad}"  #  |  
    showMsg "${deployCont}" 1
    return ${exitOK}
  fi
} 

runPauseListeners() {

  plRetVal=`./${pauseListenersSh}`	

   #cd ${OLPWD}
  
  if [ "${plRetVal}" == "${SUCCESS}" ]; then
     showMsg "${pauseListenerExecdGD}" 1
     return ${exitOK}
  else
     showMsg "${WARN} ${pauseListenerExecdNG}" 1
     return ${exitNG}
  fi
}

runResumeListeners() {

  resumeLstnr=`./${resumeListenersSh}`

  if [ ${resumeLstnr} == "${SUCCESS}" ]; then
     showMsg "${resumeListenerExecdGD}" 3
     return ${exitOK}
  else
     showMsg "${WARN} ${resumeListenerExecdNG}" 3
     return ${exitNG}
  fi
}

# get jetty PID
getJettyPId() {
  # added is the check for the war file running
  jettyProcPId=`ps -eaf | grep ${jettyStr} | grep -v grep | grep ${jettyMachNum} | grep war`
  jettyProcPId=`echo "${jettyProcPId}" | awk '{ print $2 }' | awk '{ print $1 }'`       # This gets the first row value.
  jettyPId=${jettyProcPId}

  if [ ! -z ${jettyPId} ]; then
    if [ ${jettyPId} -gt 0 ]; then
      stJy=NO
      chkPC=YES
      showMsg "${jettyMachNum} ${getJettyPIdGD}" 
    else
      stJy=YES
      chkPC=NO
      showMsg "${jettyMachNum} ${getJettyPIdNG}" 
    fi
  else
    stJy=YES
    chkPC=NO
    showMsg "${jettyMachNum} ${getJettyPIdNG}" 
  fi
 
  return ${jettyProcPId}
}


# stop-jetty.sh to be called
stopJetty() {

  showMsg "${stopJettyInfo}" 3

  ./${stopJettySh}
 
  return $?

}


# stop-jetty.sh is sometimes not working.
killJetty() {
  
  showMsg "${jettyJarTBK}" 2

  pidVal=${1}
  if [ ${pidVal} -le 0 ]; then
    showMsg "${WARN} ${jettyJarNF}"
    killRetVal=${retNF}
  else
    if [ -z ${DEV} ]; then
      killRetVal=`kill -9 ${pidVal}`
    else
      killRetVal=0
    fi
  fi

  return ${killRetVal}

}

# deployment 
deployJetty() {

  showMsg "${deploymentWB}" 2
  jenkinsBuildNo=0

  if [ "${iMode}" != "${interactiveMode}" ]; then
    jenkinsBuildNo=${3}
    if [ -z ${jenkinsBuildNo} ]; then  # make sure! 
      jenkinsBuildNo=${iMode}
    fi
    showMsg "jenkins build number: ${jenkinsBuildNo}"
  fi

  if ! [[ "${jenkinsBuildNo}" =~ ^[0-9]+$ ]] ||
       [ ${jenkinsBuildNo} -eq 0 ] ; then

    jenkinsBuildNo=0

    while [ ${jenkinsBuildNo} -le 0 ]
    do
      showMsg "${jenkinsBuildNoMsg}" 1
      read jenkinsBuildNo

      if ! [[ "${jenkinsBuildNo}" =~ ^[0-9]+$ ]] ; then
        jenkinsBuildNo=0
        continue
      fi

    done
  fi


  showMsg "${deploymentSt}" 2

  ./${deployJettySh} ${jenkinsBuildNo}

  djRet=$?

  if [ ${djRet} -eq 0 ]; then
    showMsg "${deployOK}" 
  else
    showMsg "${ERRR} ${deployNG}" 
  fi

  return ${djRet}

}

# start Jetty
startJetty() {

  showMsg "${startJettyInfo}" 2

  ./${startJettySh}
 
  return $?

}

# create CFF Skeleton
createCffSkltn() {

  showMsg "${createCffSkltnInfo}" 2

  tmpFN=`mktemp /tmp/cCSout.logXXXXXX`

  ./${createCffSkltnSh} > ${tmpFN} 2>&1 # ${mediaId}`

  numCFF=`cat ${tmpFN} | grep ${cCSChkStr} | wc -l`
  #rm -f ${tmpFN} 

  # numCFF = 1 if CFF is created!
  if [ ! -z ${numCFF} ]; then
    if [ ${numCFF} -eq 0 ]; then
      return ${exitCSE}
    fi
  else
    return ${exitCSE}
  fi

  # 2018-05-04 - last day! 
  # check if there is Error!
  numERR=`cat ${tmpFN} | grep -i ${cCSChkErr} | wc -l`
  rm -f ${tmpFN} 
  # numERR = null if CFF has NO error!
  if [ ! -z ${numERR} ]; then
    if [ ${numERR} -eq 1 ]; then
      return ${exitCSE}
    else
      return ${exitOK}
    fi
  else
    return ${exitOK}
  fi

}

Usage() {
  echo
  echo "Usage:"
  echo

  if [ "${iMode}" == "${interactiveMode}" ]; then
    echo "${prg##*/} <ENV> <server_name> " # [I|i]"
    #echo "  ... I or i for Interactive mode"
  else
    echo "${prg##*/} <ENV> <server_name> <Jenkins_Build_Number>"
  fi
  echo
  echo "ENV = TEST or PROD"
  echo " for TEST, server_name = jetty1 | jetty3"
  echo " for PROD, server_name = the machine name"
  echo
  echo
  exit ${exitWU}
}


remSpc() {
  noSpc=`echo "${1}" | tr -d " "`
  echo ${noSpc}
}

# Subroutines --------------------------

prg=$0
iMode=${3}

if [ "$2" == "" ]; then

  # RAI.sh ran!
  if [ "${1}" == "${interactiveMode}" ]; then
    iMode=${1}
  fi
  Usage
fi

ENVR=${1}

ENVR=`remSpc "${ENVR}"`
echo "${ENVS}" | grep -w ${ENVR} > /dev/null
if [ $? -ne 0 ]; then
  showMsg "${invEnv}" 2

  Usage
fi

# check this machine 
hostNm=`hostname`
runSrvr=`echo ${hostNm} | grep ${tstSrvr}`
if [ "${ENVR}" == "${TEST}" ]; then
  if [ "${runSrvr}" == "" ]; then
    showMsg "${useTstSrvr}" 2
    exit ${exitWU}
  fi
else
  if [ "${runSrvr}" != "" ]; then
    showMsg "${usePrdSrvr}" 2
    exit ${exitWU}
  fi
fi


serverName=${2}


serverName=`remSpc "${serverName}"`
if [ "${ENVR}" == "${TEST}" ]; then    # PROD

  echo "${testServerNames}" | grep -w ${serverName} > /dev/null
  if [ $? -ne 0 ]; then
    showMsg "${invSrv}" 2
    Usage
  fi

  jettyStr=GISTEST
  serverToDeploy=gis2con-jetty01-test

  hostNum=${serverName##*y}
  jettyMachNum=${jettyMachNum}${hostNum}       # only in gis2con-jetty01-test
  deployedInSrvr=${jettyMachNum}
    
  if [ -z ${DEV} ]; then 
    shellScriptDir=/opt/gis2consumer-jetty${hostNum}/
  else
    shellScriptDir=${releaseAutomationDir}/rA_test
  fi

else

  # check where running ... which PROD server ...
  echo "${prodServerNames}" | grep -w ${serverName} > /dev/null
  if [ $? -ne 0 ] || [ ${serverName} == ${srvrNmNA} ]; then
    showMsg "${invSrv}" 2
    Usage
  fi

  serverToDeploy=${serverName}
  if [ -z ${DEV} ]; then 
    shellScriptDir=/opt/gis2consumer-jetty/
    jettyStr=PROD
  else
    shellScriptDir=${releaseAutomationDir}/rA_test
    jettyStr=GISPROD
  fi
  deployedInSrvr=${serverToDeploy}

  # PROD - this lines to make sure that logged in to
  #        the server to deploy, when deployRelease.sh is called directly.
  if [ "${ENVR}" == "${PROD}" ]; then 
    # logged in so no need!
    #nslookup ${serverName} > /dev/null 
    
    # Before, design was to deploy from gis2con-jetty01 to all servers.
    # Current design is the RC ssh's to the server to deploy.
    if [ ${serverName} != `hostname` ]; then
      showMsg " ${serverNLI} ${serverName}"
      exit ${exitNLI}
    fi
  fi



fi

# go to the shell script execute directory
cd ${shellScriptDir}



echo
showMsg " " 5
echo
showMsg "${prg} ${ENVR} ${serverName}" 2
echo
echo

showMsg "${deployInfo}" 2
vrfyCntnuDplymnt

# cd to shell script directory
#cd ${shellScriptDir}

# sudo gisadmin
#sudo su - gisadmin

# Check Processing Count ... but check if jetty is running!
getJettyPId

if [ "${chkPC}" == "YES" ]; then
  chkProcessingCnt
  cpcRet=$?
  if [ ${cpcRet} -eq 0 ]; then
    showMsg "${pauseListenerRun}" 0
    vrfyCntnuDplymnt

  # 2018-04-26 - release Automation ss is not stopped even if procCnt > 0
  else
    exit ${exitProc}
  fi
  
  # Turn off LoadListener
  runPauseListeners
  rplRet=$?  # returns "success"! Check in the function!
  if [ ${rplRet} -ne 0 ]; then
    showMsg "${pauseListenersSh} returned error! ${abortDeploy}" 2
    showMsg " " 7
    exit ${exitPLE}
  fi
  # dantesan--2018-04-26 
  # - stop-jetty.sh should work after GISCONSMR-3597 is Resolved!
  stopJetty
  getJettyPId 

  # check jettyPId if not null - means it is running!
  if [ ! -z ${jettyPId} ]; then
  
    showMsg "${stopJettyNG}" 1

    # jettyPId - global var
    # Kill jetty jar run - stop-jetty.sh had a problem ...
    killJetty ${jettyPId}
    kjRet=$?
    if [ ${kjRet} -eq 0 ]; then
      showMsg "${jettyStopOK}" 
    elif [ ${kjRet} -eq ${retNF} ]; then
      exit ${retNF}
    else
      showMsg "${ERRR} ${jettyStopNG}" 
      exit $?
    fi

  else
    showMsg "${stopJettyGD}" 3
  fi # check jettyPId if not null - means it is running!
fi
# deployment
deployJetty
if [ $? -ne 0 ]; then
  showMsg "${deployJettyNG}" 3
  retDRend=${retDJE}
  getReply "${deployNGRestart}" 3
  if [ $? -ne 0 ]; then
    exit ${retDJE}
  fi
else
  showMsg "${deployJettyOK}" 3
fi

# check if jetty is already running:
getJettyPId

if [ "${stJy}" == "YES" ]; then
  #startJetty
  startJetty
  if [ $? -ne 0 ]; then
    showMsg "${startJettyNG}" 3
    showMsg " " 8
    exit ${retSJE}
  else
    showMsg "${startJettyOK}" 3
  fi
else
  showMsg "${startJettyDSDone}" 2
fi

#resumeListener
runResumeListeners
if [ $? -ne 0 ]; then
  showMsg "" 9
  exit ${exitRLE}
fi

# dantesan--2018-03-05 - Verify if deployment is good!
#createCffSkeleton
createCffSkltn
if [ $? -ne 0 ]; then
  showMsg "${createCffSkltnNG}" 2
  showMsg "" 8
  exit ${exitCSE}
else
  showMsg "${createCffSkltnGD}" 2
fi

showMsg " ${prg} ${deployedInSrvr} ${dRDone}" 2
showMsg "${drDone}" 0

showMsg " " 6

exit ${retDRend}

#--- END ---








