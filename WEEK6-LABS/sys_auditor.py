import os
from datetime import datetime

# Capture disk space output
output = os.popen("df -h").read()

# Timestamp each entry
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Write to log
with open("/var/log/sys_audit.log", "a") as f:
    f.write(f"\n--- Audit Run: {timestamp} ---\n")
    f.write(output)

print("Audit complete. Written to /var/log/sys_audit.log")


