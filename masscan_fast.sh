#!/usr/bin/env bash
# Uso: masscan-fast.sh <target/CIDR> <output.json> [rate_pps]

if [ "$#" -lt 2 ]; then
  echo "Uso: $0 <target/CIDR> <output.json> [rate_pps]" >&2
  exit 1
fi

TARGET="$1"
OUTPUT="$2"
RATE="${3:-10000}"
PORTS="0-65535"                # <-- por defecto todos los puertos

exec masscan "$TARGET" \
  --ports "$PORTS" \
  --rate "$RATE" \
  -oJ "$OUTPUT
