#!/usr/bin/env python3
import argparse, csv
from scapy.all import sr1, IP, ICMP, ARP, Ether, srp

def icmp_ping(ip):
    pkt = IP(dst=ip)/ICMP()
    resp = sr1(pkt, timeout=1, verbose=0)
    return resp is not None

def arp_ping(ip, iface=None):
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip)
    ans, _ = srp(pkt, timeout=1, iface=iface, verbose=0)
    return len(ans) > 0

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-t","--target", required=True, help="Red en formato CIDR")
    p.add_argument("-o","--output", required=True, help="CSV de salida")
    args = p.parse_args()

    import ipaddress
    net = ipaddress.ip_network(args.target, strict=False)
    results = []

    for ip in net.hosts():
        alive = icmp_ping(str(ip)) or arp_ping(str(ip))
        if alive:
            results.append((str(ip),))

    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IP"])
        writer.writerows(results)

if __name__=="__main__":
    main()
