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
type="inetnum"
kw="inetnum"
grep -E -i -m 10 "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/${kw}:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist
type="inet6num"
kw="inet6num"
grep -E -i -m 10 "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/${kw}:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist
type="role"
kw="nic-hdl"
grep -E -i -m 10 "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/${kw}:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="orgnisation"
kw="orgnisation"
grep -E -i -m 10 "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/${kw}:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="irt"
kw="irt"
grep -E -i -m 10 "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/${kw}:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="mntner"
kw="mntner"
grep -E -i -m 10 "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/${kw}:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="aut-num"
kw="aut-num"
grep -E -i -m 10 "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/${kw}:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist


type="as-set"
kw="as-set"
grep -E -i -m 10 "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/${kw}:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="as-block"
kw="as-block"
grep -E -i -m 10 "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/${kw}:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist


type="route-set"
kw="route-set"
grep -E -i -m 10 "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/${kw}:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist

type="domain"
kw="domain"
grep -E -i -m 10 "^$kw:" $sourceDir/$date/ripe.db.$type | sed -r 's/${kw}:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist
