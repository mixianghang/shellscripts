#!/bin/bash

awkCmd='BEGIN{
  FS=": "
  result=""
  inetnum=0
}
{
  if ($1 == "inetnum" || inetnum>0){
	i = 0
	if ($1 == "inetnum") {
	  inetnum++;
	  result=$2;
	} else {
	  result=result "\t" $2;
	  i++;
	}
	while (1) {
	  status = getline;
	  if (status == 0){
		print result;
		break;
	  }
	  if ($1 == "changed") {
		result=result "\t" $2;
		i++;
		continue;
	  } else if ($1 == "inetnum") {
		inetnum++;
		if (i>=2) {
		 #print "wohao",i,$1,$2
		 #print result,i $1
		}
		print result;
		result=$2;
		break;
	  } else {
		print "some thing wrong";
	  }
	}
  }
}
END{
}'

if [ $# -lt 4 ];then
  echo "Usage: sourceDir date1 date2 resultDir"
  exit 1
fi
sourceDir=$1
date1=$2
date2=$3
resultDir=$4
if [ $# -gt 4 ];then
  curDir=$5
else
  curDir=$(pwd)
fi
tempDir=$curDir/temp/genChangedKeysForLacnic
rm -rf $tempDir
mkdir -p $tempDir
mkdir -p $resultDir/$date2
mkdir -p $resultDir/latest

#generate uniqekeylist  for person and inetnum objects
objects=("inetnum")
keys=("inetnum")
object="inetnum"
index=0
for object in ${objects[@]}
do
    kw=${keys[$index]}
    ((index++))
#retrieve kw list
    grep -E -i  "^$kw:" $sourceDir/$date1/lacnic.dp | sed -E "s/$kw:[ ]+(.*)/\1/g" | sort | uniq > $tempDir/${date1}_${object}_kwlist
    grep -E -i  "^$kw:" $sourceDir/$date2/lacnic.dp | sed -E "s/$kw:[ ]+(.*)/\1/g" | sort | uniq > $resultDir/${date2}/${object}_kwlist
#retrieve kwlist with changed date
	grep -E -i "^(changed:|$kw:)[ ]+" $sourceDir/$date1/lacnic.dp | awk "$awkCmd" | sort | uniq > $tempDir/${date1}_${object}
	grep -E -i "^(changed:|$kw:)[ ]+" $sourceDir/$date2/lacnic.dp | awk "$awkCmd" | sort | uniq > $tempDir/${date2}_${object}
#diff kwlist
	diff -iEBb $tempDir/${date1}_${object} $tempDir/${date2}_${object} > $tempDir/${date2}_${object}_diff
#retrieve appended(include changed and appended) and deleted
	grep -i -E "^>.*" $tempDir/${date2}_${object}_diff | sed -E 's/>[ ]+(.*)/\1/g' | awk 'BEGIN{FS="\t"}{print $1}' > $resultDir/${date2}/${object}_kwlist_appended
	grep -i -E "^<.*" $tempDir/${date2}_${object}_diff | sed -E 's/>[ ]+(.*)/\1/g' | awk 'BEGIN{FS="\t"}{print $1}' > $resultDir/${date2}/${object}_kwlist_deleted

done

#generate person kwlist 
grep -E -i "^(owner-c|tech-c|abuse-c):" $sourceDir/$date1/lacnic.dp | awk '{if (NF >= 2) {print $2}}' | sort | uniq > $tempDir/${date1}_person_kwlist
grep -E -i "^(owner-c|tech-c|abuse-c):" $sourceDir/$date2/lacnic.dp | awk '{if (NF >= 2) {print $2}}' | sort | uniq > $resultDir/${date2}/person_kwlist
diff -iEBb  $tempDir/${date1}_person_kwlist $resultDir/${date2}/person_kwlist > $tempDir/${date2}_person_kwlist_diff
grep -i -E "^>.*" $tempDir/${date2}_person_kwlist_diff | sed -E 's/>[ ]+(.*)/\1/g' > $resultDir/${date2}/person_kwlist_appended
grep -i -E "^<.*" $tempDir/${date2}_person_kwlist_diff | sed -E 's/<[ ]+(.*)/\1/g' > $resultDir/${date2}/person_kwlist_deleted

rm -rf $tempDir	
cp -rf $resultDir/$date2/* $resultDir/latest/


