# W7 TLAB — Operation Shadow Map: Perimeter Assessment

## 🎯 Objective
Perform a full-scope reconnaissance and vulnerability assessment of a simulated 
corporate subnet (172.88.0.0/24) representing an acquired company's DMZ environment.

---

## 🛠️ Tools Used
| Tool | Purpose |
|------|---------|
| **Nmap** | Host discovery and service version detection |
| **Nikto** | Web application vulnerability scanning |
| **Docker** | Simulated target environment (provisioned via TA script) |

---

## ⚙️ Phase 1 — Active Recon (Nmap)

Performed a ping sweep of the entire /24 subnet to identify live hosts,
then ran an aggressive version scan to fingerprint exact software versions.

**Live Hosts Discovered:**
- `172.88.0.10` — nginx 1.14.2 (HTTP port 80)
- `172.88.0.15` — Redis cache (port 6379)
- `172.88.0.20` — Apache httpd 2.4.66 (HTTP port 80)

**Key Concept:** Version detection (-sV) reveals exact software versions,
which can be cross-referenced against known CVE databases to find exploits.

---

## ⚙️ Phase 2 — Vulnerability Audit (Nikto)

Ran Nikto against both web servers to identify misconfigurations and
missing security controls.

**172.88.0.10 (nginx):**
- Missing `X-Frame-Options` header → vulnerable to clickjacking attacks

**172.88.0.20 (Apache):**
- HTTP TRACE method enabled → vulnerable to Cross-Site Tracing (XST),
  allowing attackers to steal session cookies and auth tokens (OSVDB-877)

---

## ⚙️ Phase 3 — Risk Triage

**Top Priority: nginx 1.14.2 on 172.88.0.10**

> Risk = Likelihood × Impact

- **Likelihood:** HIGH — nginx 1.14.2 is from 2018 with multiple published CVEs,
  making exploitation trivial for any attacker who identifies the version
- **Impact:** HIGH — successful exploitation could result in full web server
  compromise and lateral movement into the internal network

---

## 💡 Key Takeaways
- Ping sweeps identify live hosts but always include the gateway (172.88.0.1) — 
  a real analyst filters this out
- Default Nmap scans only cover the top 1000 ports — Redis on 6379 was missed 
  until manually confirmed via Docker
- Outdated software versions are higher priority than missing headers because 
  they enable direct exploitation, not just attack assistance
- Always run both Nmap AND an application scanner like Nikto — they catch 
  different vulnerability classes
