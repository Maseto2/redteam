#!/usr/bin/env bash
# Uso: ssl-check.sh hosts.csv out-file
HOSTFILE="$1"
OUTFILE="$2"
> "$OUTFILE"

while read ip; do
  cert=$(echo | openssl s_client -connect "$ip:443" 2>/dev/null | openssl x509 -noout -dates)
  echo -e "$ip\t$cert" >> "$OUTFILE"
done < <(tail -n +2 "$HOSTFILE") 
