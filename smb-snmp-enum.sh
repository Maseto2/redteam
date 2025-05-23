#!/usr/bin/env bash
# Uso: smb-snmp-enum.sh masscan.json out-dir
MASSCAN_OUT="$1"
OUTDIR="$2"
mkdir -p "$OUTDIR"

# Enumera SMB
jq -r '.[] | select(.ports[].port==139 or .ports[].port==445) | .ip' "$MASSCAN_OUT" | sort -u | while read ip; do
  echo "[*] Ejecutando enum4linux en $ip"
  enum4linux -a "$ip" > "$OUTDIR/$ip-smb.txt"
done

# Enumera SNMP
jq -r '.[] | select(.ports[].port==161) | .ip' "$MASSCAN_OUT" | sort -u | while read ip; do
  for community in public private; do
    echo "[*] SNMPwalk $community@$ip"
    snmpwalk -v2c -c "$community" "$ip" >> "$OUTDIR/$ip-snmp-$community.txt"
  done
done
