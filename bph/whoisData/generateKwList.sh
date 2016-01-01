#!/bin/bash
if [ $# -lt 2 ]
then
    echo "Usage sourceDir resultDir"
    exit 1
fi
sourceDir=$1
resultDir=$2
date=$(date +%Y%m%d)
mkdir -p $resultDir/$date
gzip -d $sourceDir/$date/*.gz

type="inet6num"
kw="inet6num"
echo $type $kw
grep -E -i  "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist


type="role"
kw="nic-hdl"
echo $type $kw
grep -E -i  "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="organisation"
kw="organisation"
echo $type $kw
grep -E -i  "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="irt"
kw="irt"
echo $type $kw
grep -E -i  "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="mntner"
kw="mntner"
echo $type $kw
grep -E -i  "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="aut-num"
kw="aut-num"
echo $type $kw
grep -E -i  "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist


type="as-set"
kw="as-set"
echo $type $kw
grep -E -i  "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="as-block"
kw="as-block"
echo $type $kw
grep -E -i  "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist


type="route-set"
kw="route-set"
echo $type $kw
grep -E -i  "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="domain"
kw="domain"
echo $type $kw
grep -E -i  "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="inetnum"
kw="inetnum"
echo $type $kw
grep -E -i  "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist
