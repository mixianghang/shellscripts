#!/bin/bash
if [[ $# -eq 1 && $1 == "clean" ]]
then
  tc qdisc del dev eth0 root
  echo "cleaned"
  exit
fi

if [[ $# -eq 3 && $1 =~ ^[0-9]{1,3}mbit$ && $2 =~ ^[0-9]{1,5}$ && $3 =~ ^[0-9]{1,3}ms$  ]]
then
  echo $1 $2 $3
  tc qdisc del dev eth0 root
  tc qdisc add dev eth0 root handle 1: cbq avpkt 1500 bandwidth 100mbit
  tc class add dev eth0 parent 1: classid 1:1 cbq rate $1 allot 1500 prio 1 bounded isolated
  tc filter add dev eth0 parent 1: protocol ip prio 16 u32 match ip sport $2 0xffff flowid 1:1
  tc qdisc add dev eth0 parent 1:1 handle 10: netem delay $3 limit 2000
  echo "set to $1 and $3 on tcp port $2"
else
  echo "Usage: clean or (bandwidth, port, delayinms)"
  exit 1
fi
