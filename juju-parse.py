#The charms that produced warning messages (if not restricted to a single charm)
#The number of each severity of message.
#The number of duplicate messages (and their severity).
#The proportions of each type of log message for each charm (or just the single charm).
#The total number of log messages per charm.
#The total number of log messages.

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('file', metavar='filename', type=str, 
                    help='log file name')
parser.add_argument('--charm', type=str, help='show results for only the given charm name')
args = parser.parse_args()

severities = ["INFO", "DEBUG", "WARNING", "ERROR"]
logfile = open(args.file, 'r')

#generate log dictionary categorized by severity
logsBySeverity = dict ((severity,[]) for severity in severities)
lines = logfile.readlines()
for i in range(len(lines)):
    line = lines[i].strip()
    fields = line.split(" ")
    if (len(fields) >= 4 and fields[2] in severities):
        severity = fields[2]
        currentSeverityLog = logsBySeverity.get(severity)
        currentSeverityLog.append(line)
        currentEntry = len(currentSeverityLog) - 1
    else:
        #this appends all non-conforming lines to the last 'valid' entry
        currentSeverityLog[currentEntry] += " " + (line)

#prints charms that produced warning messages
charmsWithWarnings = set()
for entry in logsBySeverity.get("WARNING"):
    fields = entry.split(" ")
    charmsWithWarnings.add(fields[0])
if (args.charm is None): print("Charms with WARNING severity messages: " + str(charmsWithWarnings))

print ("\n")

#Print Number of entries for each Severity
for severity, severityLog in logsBySeverity.items():
    logLen = len(severityLog)
    print ("Number of entries for severity " + severity + ": " + str(logLen))
logfile.close()