#!/usr/bin/env bash
# Uso: nmap-nse.sh hosts.csv out-prefix
HOSTFILE="$1"
PREFIX="$2"
mkdir -p "$PREFIX"

mapfile -t HOSTS < <(tail -n +2 "$HOSTFILE")
for host in "${HOSTS[@]}"; do
  ip="$host"
  echo "[*] Escaneando $ip"
  nmap -Pn -sV -O --script "default,safe,vuln,auth,exploit" \
       -iL <(echo "$ip") \
       -oA "$PREFIX/$ip"
done
