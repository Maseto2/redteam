#!/usr/bin/env python3
import argparse
import csv
import json
import xml.etree.ElementTree as ET
from jinja2 import Template

def parse_args():
    parser = argparse.ArgumentParser(description="Agrega y normaliza datos de escaneo para generar un informe HTML.")
    parser.add_argument('--hosts',   required=True, help='CSV de hosts vivos')
    parser.add_argument('--masscan', required=True, help='JSON de resultados de Masscan')
    parser.add_argument('--nmap',    nargs='+', required=True, help='Archivos XML de resultados de Nmap')
    parser.add_argument('--output',  required=True, help='Ruta de salida para el HTML generado')
    return parser.parse_args()


def main():
    args = parse_args()
    data = []
    ip_device = {}

    # 1) Parsear Nmap primero para obtener dispositivos y también puertos (Medium)
    for xml_file in args.nmap:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for host in root.findall('host'):
                addr4 = host.find("address[@addrtype='ipv4']")
                if addr4 is None:
                    continue
                ip = addr4.get('addr')

                # Hostname PTR
                hn = host.find('hostnames/hostname')
                hostname = hn.get('name') if hn is not None else ''
                # Vendor MAC
                mac_el = host.find("address[@addrtype='mac']")
                vendor = mac_el.get('vendor') if mac_el is not None else ''
                device = hostname or vendor or ''
                ip_device[ip] = device

                for port in host.findall('ports/port'):
                    portid = port.get('portid')
                    svc = port.find('service')
                    service = svc.get('name') if svc is not None else ''
                    version = svc.get('version') if svc is not None else ''
                    data.append({
                        'ip': ip,
                        'device': device,
                        'port': portid,
                        'service': service,
                        'version': version,
                        'severity': 'Medium'
                    })
        except Exception:
            print(f"[WARN] No se pudo parsear Nmap XML {xml_file}.")

    # 2) Masscan JSON: añade puertos detectados (Low), asignando device si existe
    try:
        with open(args.masscan) as f:
            records = json.load(f)
            for rec in records:
                ip = rec.get('ip')
                device = ip_device.get(ip, '')
                for p in rec.get('ports', []):
                    service_info = p.get('service', {})
                    data.append({
                        'ip': ip,
                        'device': device,
                        'port': str(p.get('port')),
                        'service': service_info.get('name', ''),
                        'version': service_info.get('version', ''),
                        'severity': 'Low'
                    })
    except Exception:
        print("[WARN] No se pudo parsear Masscan JSON.")

    # 3) CSV de hosts vivos: sin puerto (Info)
    try:
        with open(args.hosts) as f:
            reader = csv.DictReader(f)
            for row in reader:
                ip = row.get('IP') or row.get('ip')
                device = ip_device.get(ip, '')
                data.append({
                    'ip': ip,
                    'device': device,
                    'port': '',
                    'service': 'Host activo',
                    'version': '',
                    'severity': 'Info'
                })
    except Exception:
        print("[WARN] No se pudo parsear CSV de hosts vivos.")

    # Ordenar data por IP y severidad
    severity_order = {'Critical':0, 'High':1, 'Medium':2, 'Low':3, 'Info':4}
    data.sort(key=lambda x: (x['ip'], severity_order.get(x['severity'], 5), x['port']))

    # Generar informe HTML
    tpl = Template(open('templates/report.html').read())
    html = tpl.render(data=data)
    with open(args.output, 'w') as f:
        f.write(html)
    print(f"Informe generado: {args.output}")

if __name__ == '__main__':
    main()
