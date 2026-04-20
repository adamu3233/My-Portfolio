import os
from datetime import datetime

# --- CHANGE THIS to your Windows DC IP ---
DC_IP = "10.0.2.15"

# Ping 4 times, suppress terminal output
response = os.system(f"ping -c 4 {DC_IP} > /dev/null 2>&1")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if response == 0:
    status = f"[{timestamp}] DC is UP ({DC_IP})"
else:
    status = f"[{timestamp}] DC is DOWN ({DC_IP})"

# Write result to log
with open("/var/log/dc_audit.log", "a") as f:
    f.write(status + "\n")

print(status)
