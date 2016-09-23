#!/bin/bash
startDate=$(date +"%Y%m%d")
endDate=$startDate
if [ $# -ge 2 ];then
  startDate=$1
  endDate=$2
fi
uniformBaseDir=/data/seclab/BPH/Uniform/
errorReportDir=$uniformBaseDir/ErrorDetection
errorReportFile=$errorReportDir/tempReport_brief
errorReportAttachment=$errorReportDir/tempReport_attachment
registryList=(afrinic apnic arin lacnic ripe)
recipientList="xmi@iu.edu,mixianghang@outlook.com"
timeLimit=$(( 12 * 3600 ))
if [ $# -ge 3 ];then
  timeLimit=$3
fi
ccList=""
bccList=""
#detect validation error
#detect api query error
detectApiQueryError() {
  if [ $# -lt 3 ];then
	echo "Usage for ${FUNCNAME[0]}: date errorReportFile errorReportAttachment"
	exit 1
  fi
  local today=$1
  local errorReportFile=$2
  local errorReportAttachment=$3
  local logBaseDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/log
  local appendRipeLog=$logBaseDir/logErrorForAppendRipe_$today
  local appendRipePersonLog=$logBaseDir/logErrorForAppendRipePerson_$today
  local retrieveAfrinicLog=$logBaseDir/logErrorForRetrieveAfrinic_$today
  local retrieveLacnicLog=$logBaseDir/logErrorForRetrieveLacnic_$today
  local logFiles=($appendRipeLog $appendRipePersonLog $retrieveAfrinicLog $retrieveLacnicLog)
  local logFile=${logFiles[0]}
  local len=${#logFiles[@]}
  local index=0
  while [ $index -lt $len ];
  do
	logFile=${logFiles[$index]}
	if [ ! -e $logFile ];then
	  local currTimeInSec=$(date +"%s")
	  local timeCost=$(($currTimeInSec - $startTimeInSec))
	  if [[ $timeCost -ge $timeLimit ]];then
		echo "send missing logfile msg"
		echo "$logFile cannot be found when detecting errors" | mail -s "log file not found when detecting errors"  -b $bccList -c $ccList $recipientList
		checkError "sending log_not_found emails"
		return
	  fi
	  sleep 60
	  continue
	fi
	errorNum=$(wc -l <$logFile)
	if [ $errorNum -gt 0 ];then
	  echo "get $errorNum errors from $logFile" >>$errorReportFile
	  echo "get the following $errorNum errors from $logFile" >>$errorReportAttachment
	  while read -r line || [[ -n "$line" ]]
	  do
		echo ">>$line" >>$errorReportAttachment
	  done < $logFile
	fi
	((index++))
  done
}
#detect uniform check errors
detectUniformError() {
  if [ $# -lt 3 ];then
	echo "Usage for ${FUNCNAME[0]}: date errorReportFile errorReportAttachment"
	exit 1
  fi
  local today=$1
  local errorReportFile=$2
  local errorReportAttachment=$3
  local logBaseDir=$uniformBaseDir/$today/missing/
  for registry in ${registryList[@]}
  do
	local checkBaseDir=$logBaseDir/$registry/validate/check
	local logFiles=(asn_log inetnum_log person_log org_log)
	local len=${#logFiles[@]}
	local index=0
	while [ $index -lt $len ];
	do
	  local logName=${logFiles[$index]}
	  local logFile=$checkBaseDir/${logFiles[$index]}
	  if [ ! -e $logFile ];then
		local currTimeInSec=$(date +"%s")
		local timeCost=$(($currTimeInSec - $startTimeInSec))
		if [[ $timeCost -ge $timeLimit ]];then
		  echo "$logFile cannot be found when detecting errors" | mail -s "log file not found when detecting errors"  -b $bccList -c $ccList $recipientList
		  return
		fi
		sleep 60
		continue
	  fi
	  errorNum=$(wc -l <$logFile)
	  if [ $errorNum -gt 0 ];then
		echo "get $errorNum errors from $logName for $registry on $today" >>$errorReportFile
		echo "get the following $errorNum errors from $logName for $registry on $today" >>$errorReportAttachment
		while read -r line || [[ -n "$line" ]]
		do
		  echo ">>$line" >>$errorReportAttachment
		done < $logFile
	  fi
	  ((index++))
	done
  done
}

checkError() {
  if [ $? -ne 0 ];then
	echo "error when $1"
	exit 1
  fi
}


today=$startDate
startTimeInSec=$(date +"%s")
while [ $today -le $endDate ];
do
  echo $today
  startSec=$(date +"%s")
  errorReportFile=$errorReportDir/${today}_errorReport_brief
  errorReportAttachment=$errorReportDir/${today}_errorReport_attachment
  [[ -e $errorReportFile ]] && rm $errorReportFile && touch $errorReportFile
  [[ -e $errorReportAttachment ]] && rm $errorReportAttachment && touch $errorReportAttachment
  detectApiQueryError $today $errorReportFile $errorReportAttachment
  checkError "detecting api query errors"
  detectUniformError $today $errorReportFile $errorReportAttachment
  checkError "detecting uniform check errors"
  numOfError=0
  [[ -e $errorReportFile ]] && numOfError=$(wc -l <$errorReportFile)
  if [ $numOfError -gt 0 ];then
	echo "send error notification emails"
	cat $errorReportFile | mail -s "whois error report for $today" -a $errorReportAttachment -b $bccList -c $ccList  $recipientList
	checkError "send email"
  fi
  endSec=$(date +"%s")
  echo "time cost for $today is $(($endSec - $startSec))"
  today=$(date -d "$today +1day" +"%Y%m%d")
done
