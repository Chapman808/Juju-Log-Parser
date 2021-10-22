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


#generate log dictionary categorized by severity as well as megalist of all logs
logsBySeverity = dict ((severity,[]) for severity in severities)
allLogs = []
lines = logfile.readlines()
severity = ""
charmIsSelected = False
for i in range(len(lines)):
    line = lines[i].strip()
    fields = line.split(" ")
    if (len(fields) >= 4 and fields[2] in severities): #if line fits log format
        charm = fields[0].split(":")[0]
        if (charm == args.charm or args.charm is None): #if charm option is set, only operate if the charm matches the given charm
            charmIsSelected = True
            severity = fields[2]
            logsBySeverity.get(severity).append(line)
            allLogs.append(line)
        else:
            charmIsSelected = False
            
    #if this line does not fit the log format, we assume it is part of the entry before it (i.e. the previous entry contained newlines)
    #don't do anything if 
    elif (charmIsSelected):
        if (severity): logsBySeverity.get(severity)[-1] += " " + (line)
        allLogs[-1] += line


########
# prints charms that produced warning messages
########

charmsWithWarnings = set()
for entry in logsBySeverity.get("WARNING"):
    fields = entry.split(" ")
    charmsWithWarnings.add(fields[0].split(":")[0])
if (args.charm is None): print("Charms with WARNING severity messages: " + str(charmsWithWarnings))

print ("\n")


########
# Print Number of entries for each Severity
########

for severity, severityLog in logsBySeverity.items():
    logLen = len(severityLog)
    print ("Number of entries for severity " + severity + ": " + str(logLen))

print ("\n")

########
# Print Number of duplicates for each Severity
########

uniqueLogEntries = set()
duplicates = dict((severity, 0) for severity in severities.copy())
for severity, severityLog in logsBySeverity.items():
    for entry in severityLog:
        l = len(uniqueLogEntries)
        uniqueLogEntries.add(entry)
        if l == len(uniqueLogEntries): 
            duplicates[severity] += 1
print("Duplicate log entries:")
print(*duplicates.items(), sep="\n")

print ("\n")


########
# Print the proportions of each type of log message for each charm (or just the single charm).
########

#gather set of charms
charms = set()
for entry in allLogs: 
    charms.add(entry.split(" ")[0].split(":")[0])
#initialize data structure to store severities for each charm
severitiesTemplate = dict((severity, 0) for severity in severities)
severityValuesPerCharm = dict ((charmName, severitiesTemplate.copy()) for charmName in charms)
#loop through logs and add to severityValuesPerCharm
for severity, severityLog in logsBySeverity.items():
    for entry in severityLog:
        fields = entry.split(" ")
        curCharm = fields[0].split(":")[0]
        curCharmSeverities = severityValuesPerCharm[curCharm]
        curCharmSeverities[severity]  += 1
#print values
print ("Proportions of severities for each charm:")
for charm, severityOcurrences in severityValuesPerCharm.items():
    print (charm, *severityOcurrences.items())

print ("\n")


########
# Print total number of log messages per charm
########
print ("Total number of log messages for each charm:")
for charm, severityOcurrences in severityValuesPerCharm.items():
    total = sum (severityOcurrences.values())
    print (charm + ": " + str(total))

print ("\n")

########
# Print total number of log messages
########
totalEntries = len(allLogs)
print ("Total number of entries in log file: " + str(totalEntries))


logfile.close()
