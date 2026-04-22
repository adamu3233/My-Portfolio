# TARGET THREAT PROFILE: CloudNano 
**Classification:** Passive Security Audit
**Operator:Mohammed Adamu** ## 1. Subdomain Discovery 
* **Tool Used:** Sublist3r (sublist3r -d yahoo.com -o ~/subdomains.txt)
* **Subdomains Found: 180
* login.yahoo.com — Primary authentication portal; high-value target for credential attacks
* api.login.yahoo.com — Exposed API login endpoint; indicates programmatic auth surface

## 2. Tech Stack Mapping 
* **Tool Used:** BuiltWith / Wappalyzer
* **Identified Technologies (CMS/CDN/Backend):**
* [Akamai (CDN) — High-volume content delivery and DDoS mitigation layer] 
* [React (Frontend Framework) — JavaScript UI library confirming modern SPA architecture] 

## 3. Major Exposure Points & Dangers 
*(List three major exposure points discovered during your OSINT audit and explain why they are dangerous)*
1. **[api.login.yahoo.com]:** Sublist3r revealed a publicly enumerable API endpoint dedicated to authentication.
An attacker can probe this endpoint for rate-limiting weaknesses,
attempt credential stuffing attacks using previously leaked username/password pairs, or fuzz the API for unauthenticated routes
2. **[opus.analytics.yahoo.com]:** Passive enumeration surfaced subdomains suggesting internal tooling and data pipelines.
Exposing analytics and scouting infrastructure at the public DNS level leaks organizational topology to adversaries at no cost to them — no scanning required.
If these subdomains host dashboards with weak or no authentication, an attacker could access business intelligence data, traffic patterns, or internal metrics. 
3. **[guce.yahoo.com]:** GDPR/consent management system; holds user consent records 
