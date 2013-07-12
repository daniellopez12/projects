'''
Created on Jun 25, 2013
--- Ford Part Number (FPN) Checker ---
This script will look at a directory and create a list of FPN. 
It will then compare this file with a another provided list and create a report of matching,
unmatching, or non-existant files.
@author: DLOPEZ42
'''

import os
import re
import sys
from collections import Counter


print "--- FPN Checker Script: Started ---\n"

# Receive user input of where path of delivered files reside
while True:
    path_delivered_files = raw_input("Enter the path to where the delivered files reside: ");
    if os.path.exists(path_delivered_files) == True:
        break
    else:
        print "The path you input does not exist. Please enter a valid path."

# Extension of files to check in path where files exist
file_ext = ('.*\.cab|.*\.zip|.*\.CAB|.*\.ZIP') 

# Opens and creates a new text file to store Microsoft FPN list
ms_fpn_list = open("ms_fpn_list.txt", "w")

# Initialize a temporary lists collection for processing
temp_list = []

# Traverse directory and write all file names to text file
for r, d, f in os.walk(path_delivered_files):
    for files in f:
        if re.match(file_ext, files):
            temp_list.append(os.path.splitext(files)[0])            

# Creates a unique set of file part numbers and writes to file
temp_set = set(temp_list)
for item in temp_set:
    if item.endswith(".sec"):
        print "\n\tprocessing ---> Ingored .sec files \n"
    elif item.startswith("VIN"):
        print "\n\tprocessing ---> Ignored files starting with 'VIN' (i.e. VINcop) \n"
    else:
        ms_fpn_list.write(item + "\n")
        
print "\nCreated file '", ms_fpn_list.name,"' with list of Microsoft delivered FPNs. \n"
ms_fpn_list.close()

# Check of Ford's FPN list is present, if not cancel execution
try:
    with open('ford_fpn_list.txt'):pass
except IOError:
    sys.exit('''The file 'ford_fpn_list.txt' was not found in the directoy where the FPN_checker.exe resides.
please add it and restart the program execution. \n''')

print "\nStarting comparison between Ford vs. Microsoft Part numbers now...\n"

# Opens all file storing Ford's FPN list + creates new report file
ms_fpn_list = open("ms_fpn_list.txt", "r")
ford_fpn_list = open("ford_fpn_list.txt", "r")
fpn_final_report = open("fpn_final_report.txt", "w")

#Compare Ford vs. MS FPN's and write out matched vs. not matched
with ms_fpn_list as f:
    haystack = f.read()
    
if not haystack:
    sys.exit("Could not read Microsoft FPN list \n")
    
with ford_fpn_list as f:
    for needle in (line.strip() for line in f):
        if needle in haystack:
            fpn_final_report.write( needle + ' | Match (=) \n')
        else:
            fpn_final_report.write( needle + ' | Does NOT match (-) \n')

#Closed all opened files
ms_fpn_list.close()
ford_fpn_list.close()
fpn_final_report.close()

# Opens all file storing Ford's FPN list + creates new report file
ms_fpn_list = open("ms_fpn_list.txt", "r")
ford_fpn_list = open("ford_fpn_list.txt", "r")
fpn_final_report = open("fpn_final_report.txt", "a")

#Compare Ms vs. Ford FPN's and write out any non-existant files
with ford_fpn_list as x:
    scene = x.read()

with ms_fpn_list as x:
    for waldo in (line.strip() for line in x):
        if waldo not in scene:
            fpn_final_report.write( waldo + ' | Does NOT exist in your list (?) \n')
x.close()
            
print "\nFinished comparing file. 'Fpn_final_report.txt' was created.\n"

#Closed all opened files
ms_fpn_list.close()
ford_fpn_list.close()
fpn_final_report.close()

#Opening final FPN report for analysis
fpn_final_report = open("fpn_final_report.txt", "r")

#Create a collection of strings + amount of counts inside FPN final report
cnt = Counter() 
for line in fpn_final_report:
    for word in line.split():
        cnt[word] +=1

#Print quick overview summary for user
print "\n### Summary of Ford vs. MS FPN lists ###"
print "There were %s" %cnt['(=)'] + " that matched your Ford FPN list"
print "There were %s" %cnt['(-)'] + " that did NOT matched your Ford FPN list"
print "There were %s" %cnt['(?)'] + " that did NOT exist in your Ford FPN list\n"

print "\n--- FPN Checker Script: Finish ---"
print "Press ENTER to close window"
raw_input()