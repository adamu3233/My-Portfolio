#!/usr/bin/env python3



#THE CODE FOR MY SYSTEM AUDITOR vvvvvvv

import subprocess
import json
import os

print("[*] Initiating System Audit...")

process_list = subprocess.run(["ps", "aux"], capture_output=True, text=True)

if "unauthorized_cryptominer" in process_list.stdout:
	alert_data = {"event": "Unauthorized Process", "severity": "High", "process": "unauthorized_cryptominer"}

print("[+] Audit Complete.")

with open("security_alert.json", "w") as file:
        json.dump(alert_data, file, indent=4)



# The explanation of my code

#Import Statements

#Imports the subprocess module to run system commands like ps aux from within Python

#Imports the json module to format the alert data into proper JSON structure

#Imports os (though this isn't actually used in the current script)

#Status Message
#Prints "[*] Initiating System Audit..." to the terminal so the user knows the script has started running

#Process Capture
#Executes the Linux command ps aux which lists every running process on the system with full details

#Captures all that output as readable text and stores it in a variable called process_list

#Threat Detection
#Checks if the string "unauthorized_cryptominer" appears anywhere in the captured process list

#If found, it creates a dictionary (a key-value pair data structure) called alert_data containing:

#Event type: "Unauthorized Process"

#Severity level: "High"

#Process name: "unauthorized_cryptominer"

#Completion Message
#Prints "[+] Audit Complete." to indicate the script finished running

#JSON Export
#Opens a new file named security_alert.json in write mode

#Writes the alert_data dictionary to the file in JSON format

#Uses indent=4 to make the output nicely formatted and human-readable

#Expected Output When Threat is Detected
#Terminal shows: Initiating message, then audit complete message

#JSON file contains: Formatted alert with event, severity, and process name

#Expected Output When No Threat is Found
#Terminal shows: Initiating message, then audit complete message

#Script crashes with error: NameError: name 'alert_data' is not defined

#JSON file: Not created or remains unchanged



