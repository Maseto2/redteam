#!/usr/bin/env bash
# Uso: http-enum.sh masscan.json out-dir
MASSCAN_OUT="$1"
OUTDIR="$2"
mkdir -p "$OUTDIR"

jq -r '.[] | select(.ports[].port==80 or .ports[].port==443) | .ip' "$MASSCAN_OUT" | sort -u | while read ip; do
  echo "[*] Enumerando HTTP en $ip"
  gobuster dir -u "http://$ip" -w wordlists/common.txt -o "$OUTDIR/$ip-dir.txt"
  wappalyzer http://$ip > "$OUTDIR/$ip-tech.txt"
done
