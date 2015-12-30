grep -E -i  "apnic\|\w+\|ipv4" ./delegated-apnic-20151209 | sed -E '
s/[^\|]+\|[^\|]+\|[^\|]+\|([0-9\.]+)\|.*/\1/g' 
