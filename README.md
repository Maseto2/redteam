# 🛡️ Red Team Reconnaissance Scripts

A curated collection of scripts to automate the initial reconnaissance phase during penetration tests. This toolkit includes scanning, enumeration, parsing, and reporting utilities to streamline red team workflows.

## 📦 Repository Structure

When cloning this repo, everything will be placed inside a `redteam/` directory automatically:

```bash
git clone https://github.com/Maseto2/redteam.git
cd redteam
⚙️ Requirements
Before running the scripts, make sure the following tools and libraries are installed:

System tools
python3, pip, masscan, nmap, jq, enum4linux, gobuster, snmpwalk, openssl

Recommended OS: Kali Linux or any Debian-based distro

Python dependencies
pip3 install pandas jinja2 scapy

On Kali, you can install system tools with:
sudo apt update
sudo apt install python3-pip masscan nmap jq enum4linux gobuster snmp snmp-mibs-downloader openssl


🧰 Script Overview
Script	Description	Usage
recon-orchestrator.sh	Automates initial recon: ping sweep, masscan, nmap	sudo ./recon-orchestrator.sh [CIDR]
ping_sweep.py	Identifies live hosts via ICMP and ARP	Called by orchestrator
masscan-fast.sh	Launches a fast masscan on all ports	Called by orchestrator
nmap-nse.sh	Runs nmap with default/safe/exploit NSE scripts	Called by orchestrator
http-enum.sh	Uses Gobuster and Wappalyzer to enum HTTP dirs and tech	./http-enum.sh masscan.json out-dir
smb-snmp-enum.sh	Uses enum4linux and snmpwalk for SMB/SNMP discovery	./smb-snmp-enum.sh masscan.json out-dir
ssl-check.sh	Checks exposed SSL/TLS certificates and validity	./ssl-check.sh hosts.csv out.txt
report-aggregator.py	Parses and aggregates data into an HTML report	python3 report-aggregator.py --hosts hosts.csv --masscan masscan.json --nmap nmap/*.xml --output report.html
extract_medium.py	Extracts only "Medium" severity rows from the report	./extract_medium.py --input report.html --output medium.csv

📝 Report Template
The HTML report is generated using templates/report.html. Feel free to customize the layout and style.

✅ Full Recon Workflow Example
# Start from the cloned repo
cd redteam

# Launch initial recon with automatic subnet detection
sudo ./recon-orchestrator.sh

# Once finished, generate a report
python3 report-aggregator.py --hosts reports/.../hosts_alive.csv \
                             --masscan reports/.../masscan.json \
                             --nmap reports/.../nmap/*.xml \
                             --output final-report.html
You can also extract just the medium-severity findings:

./extract_medium.py --input final-report.html --output medium.csv
