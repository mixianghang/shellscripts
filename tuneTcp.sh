#!/bin/bash
minSize=16777216
defaultSize=16777216
maxSize=33554432
if [ $# -ge 3 ];then
  minSize=$1
  defaultSize=$2
  maxSize=$3
fi
cp /etc/sysctl.conf.bak /etc/sysctl.conf
echo "net.core.wmem_max=$maxSize" >> /etc/sysctl.conf
echo "net.core.rmem_max=$maxSize" >> /etc/sysctl.conf
#min default max buffer size, will be constrained by net.core.rmem_max
echo "net.ipv4.tcp_wmem= $minSize $defaultSize $maxSize" >> /etc/sysctl.conf
echo "net.ipv4.tcp_rmem= $minSize $defaultSize $maxSize" >> /etc/sysctl.conf
# if this set, the rece windown size can be larger than 64kb
echo 'net.ipv4.tcp_window_scaling = 1' >> /etc/sysctl.conf
#enbale tcp timestamp before enabling tcp_sack
echo 'net.ipv4.tcp_timestamps = 1' >> /etc/sysctl.conf
#enable selective acknowledge, 
echo 'net.ipv4.tcp_sack = 1' >> /etc/sysctl.conf
#By default, TCP saves various connection metrics in the route cache when the connection closes, so that connections established in the near future can use these to set initial conditions. Usually, this increases overall performance, but may sometimes cause performance degradation. If set, TCP will not cache metrics on closing connections.
echo 'net.ipv4.tcp_no_metrics_save = 1' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_slow_start_after_idle = 1' >> /etc/sysctl.conf
#set the congestion control algorithm
#check current algorithm /proc/sys/net/ipv4/tcp_congestion_control
#check available algorithms from file /proc/sys/net/ipv4/tcp_available_congestion_control
#check allowed from file /proc/sys/net/ipv4/tcp_allowed_congestion_control
echo 'net.ipv4.tcp_congestion_control = cubic' >> /etc/sysctl.conf
