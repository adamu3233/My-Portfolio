# CLOUDNANO REMEDIATION PLAN
**Operator:** Mohammed Adamu — S21 Vulnerability Triage

## TOP 5 CRITICAL FIXES
*(From the 20 raw findings, select the 5 that pose the greatest ACTUAL risk. Explain your reasoning.)*

1. **Unauthenticated AWS S3 Bucket Exposing Customer PII [CVSS 9.8]**
   * **Justification:** Likelihood is critical because the bucket requires zero authentication and is publicly
 reachable right now; Impact is maximum because exposed customer PII creates immediate regulatory liability under
 GDPR/CCPA — a CVSS 10.0 on an air-gapped router cannot compete with a live, open data breach.

2. **Remote Code Execution in Apache Struts — Internet-Facing Web Server [CVSS 9.8]**
   * **Justification:** Likelihood is high because this server is directly internet-facing with weaponized public exploits
 actively in use; Impact is severe because successful exploitation grants full remote control of the server and an
 immediate foothold into the internal network.

3. **SQL Injection — Customer Database Portal Login Page [CVSS 8.1]**
   * **Justification:** Likelihood is high because login pages are among the most actively targeted endpoints on any
 internet-facing system; Impact is critical because exploitation allows full customer database
 exfiltration and authentication bypass, directly compromising PII at scale.

4. **Cross-Site Scripting (XSS) — Public Support Forum [CVSS 8.8]**
   * **Justification:** Likelihood is high because the support forum is publicly accessible with no authentication
 barrier; Impact is significant because attackers can hijack authenticated customer sessions and execute account
 takeover at scale against real users.

5. **SMBv1 Enabled — Internal HR File Server [CVSS 9.0]**
   * **Justification:** Likelihood is moderate-high because any single compromised internal endpoint enables lateral
 movement via EternalBlue-style exploits; Impact is severe because the HR file server holds employee PII and represents
 a proven ransomware deployment target.
