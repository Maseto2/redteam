#!/usr/bin/env bash
set -e

# 1) DETECCIÓN AUTOMÁTICA DE SUBRED (igual que antes) …
if [ -z "$1" ]; then
  IFACE=$(ip route | awk '/^default/ {print $5; exit}')
  TARGET=$(ip -o -f inet addr show dev "$IFACE" \
           | awk '{print $4}' | head -n1)
  echo "[*] Objetivo detectado automáticamente: $TARGET (interfaz $IFACE)"
else
  TARGET="$1"
fi

# 2) DIRECTORIO DE SALIDA
OUTDIR="reports/initial-recon/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTDIR"

# 3) PING SWEEP
echo "[*] Lanzando ping_sweep..."
python3 ping_sweep.py -t "$TARGET" -o "$OUTDIR/hosts_alive.csv" &

# 4) MASSCAN (usando siempre la copia local)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "[*] Lanzando masscan-fast..."
bash "$SCRIPT_DIR/masscan-fast.sh" "$TARGET" "$OUTDIR/masscan.json" &

wait

# 5) NMAP
echo "[*] Hosts vivos detectados, iniciando Nmap..."
bash "$SCRIPT_DIR/nmap-nse.sh" "$OUTDIR/hosts_alive.csv" "$OUTDIR/nmap"

echo "[*] Recon completo en $OUTDIR"
