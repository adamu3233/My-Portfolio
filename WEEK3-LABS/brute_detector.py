# Initialize counter to track number of attacks found
attack_count = 0

# Open source log for reading (the "dirty" data)
with open("auth_audit.log", "r") as log_file:
    # Open report file for writing (the "clean" output)
    with open("brute_report.txt", "w") as report_file:

        # Loop through each line in the log file
        for line in log_file:

            # Check if this line contains a failed password attempt
            if "Failed password" in line:
                # Write the suspicious line to our report
                report_file.write(line)

                # Increase our attack counter by 1
                attack_count = attack_count + 1

# Print summary report (outside the with blocks)
print(f"[*] Audit Complete. Extracted {attack_count} threat signatures to brute_report.txt")
