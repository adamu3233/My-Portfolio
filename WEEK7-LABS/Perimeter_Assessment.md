# TITANCORP: PERIMETER ASSESSMENT REPORT
**Operator:** Mohammed Adamu
 **Target Subnet:** 172.88.0.0/24

## PHASE 1: ACTIVE ENUMERATION (NMAP)
*(List the live IPs discovered and their running services/versions)*
* **Host 1 (172.88.0.10):** nginx 1.14.2 - HTTP on port 80
* **Host 2 (172.88.0.15):** Redis (cache database) - port 6379
* **Host 3 (172.88.0.20):** Apache httpd 2.4.66 - HTTP on port 80

## PHASE 2: VULNERABILITY AUDIT (NIKTO)
*(Run Nikto against the TWO web servers discovered above. List one major finding for each.)*
* **Web Server 1 Finding:** (172.88.0.10):** Missing X-Frame-Options header — site is vulnerable to clickjacking attacks.
 Flagged by Nikto v2.1.5.
* **Web Server 2 Finding:** (172.88.0.20):** HTTP TRACE method enabled — host is vulnerable to Cross-Site Tracing (XST),
 allowing attackers to steal session cookies and auth headers. Flagged by Nikto v2.1.5 (OSVDB-877). 

## PHASE 3: RISK TRIAGE
*(Review your findings. Identify the SINGLE highest-risk vulnerability across the entire DMZ. Justify why it is the top priority using the Likelihood x Impact formula.)*

* **Top Priority Remediation:** Outdated nginx 1.14.2 on 172.88.0.10
* **Justification:** nginx 1.14.2 was released in 2018 and has multiple known CVEs publicly documented, making exploitation
 highly likely by any attacker who scans the server version; if exploited on this internet-facing host,
 the impact is full web server compromise and potential lateral movement into the internal network.
