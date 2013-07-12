'''
Created on Jul 1, 2013
--- USB image update file Checker ---
This script will parse out all the filenames out of the .lst (BOM) and check to see if all of 
those files exist in the /SyncMyRide folder. A quick summary and final report is created listing
all of the files that don't match and/or don't exist in the folder. 
type: Quality assurance
@author: DLOPEZ42
'''

import os
import re
import sys
from collections import Counter

def list_of_paths(path_to_search):
    "Creates a text file with lists of path of every .lst for a given location"
    
    listOfPaths = open("listOfPaths.txt", "w")
    
    # Extension of files to check in path where files exist
    BOM_ext = ('.*\.lst|.*\.LST')
    
    # Initialize a temporary lists collection for processing
    temp_list = []
    
    # Traverse directory and write all file names to text file
    for r, d, f in os.walk(path_to_search):
        for files in f:
            if re.match(BOM_ext, files):
                temp_list.append(os.path.join(r, files))
    
    temp_set = set(temp_list)
    for item in temp_set:
        listOfPaths.write(item + "\n")
    
    listOfPaths.close()
    return

def bom_into_fileList(path_to_lst):
    "Parses a given .lst into a list data structure of filenames"
    
    # Extension of files to extract out of the LST
    file_ext = ('.*\.cab|.*\.zip|.*\.CAB|.*\.ZIP') 
    
    temp_open_file = open(path_to_lst, "r")
    
    temp_list = []
    
    with temp_open_file as f:
        for word in (line.strip() for line in f ):
            if re.match(file_ext, word):
                temp_list.append(remBackSlash(word))
    
    temp_set = set(temp_list)

    temp_open_file.close()
    
    return temp_set

def fileList_from_SyncMyRide(path_to_syncmyride):
    "Search \SyncMyRide folder and creates a list data structure of filenames"
    
    # Extension of files to check in path where files exist
    file_ext = ('.*\.cab|.*\.zip|.*\.CAB|.*\.ZIP') 

    temp_list = []
    
    for r, d, f in os.walk(path_to_syncmyride):
        for files in f:
            if re.match(file_ext, files):
                temp_list.append(os.path.basename(files))
    
    temp_set = set(temp_list)
    
    return temp_set

def remBackSlash(text, there=re.compile('.*' + re.escape('\\'))):
    "Removes the rest of the string before the '\' (Backslash)"
    return there.sub('', text)


print "--- Starting USB image update file checker script --- \n"

# Receive user input of where path of delivered files reside
while True:
    path_delivered_files = raw_input("Enter the path to where the delivered files reside: ");
    if os.path.exists(path_delivered_files) == True:
        break
    else:
        print "The path you input does not exist. Please enter a valid path."
 
list_of_paths(path_delivered_files)

# Check that file containing the directories where the script will check is present, if not cancel execution
try:
    with open('listOfPaths.txt'):pass
except IOError:
    sys.exit('''The file 'listOfPaths.txt' was not found in the directory where the .exe resides.
please add it and restart the program execution. \n''')

# Open 'listOfPaths.txt' to start transactions
list_of_paths_to_check = open("listOfPaths.txt", "r")

# Read path location file and add to tuple data structure  
list_of_lst_files = [line.strip() for line in list_of_paths_to_check.readlines()]

# Check that each path in the list of paths exist otherwise cancel execution and inform user
for path in list_of_lst_files:
    if os.path.exists(path) == False:
        sys.exit("'"+ path + "' is not a valid path . Please modify to a valid path and restart script. \n")

# Prepares a text file for final comparison results 
cmp_final_report = open("BOM_vs_SyncMyRide_Final_Report.txt", "w")

print "\nComparing BOM (.lst) vs. Files inside the \SyncMyRide folder now ... \n"

# Perform analysis of the files in each BOM vs. its respective \SyncMyRide folder
for lstPath in list_of_lst_files:
    cmp_final_report.write('-----------------------------------------------------------------------------\n')
    cmp_final_report.write(lstPath + "\n")
    files_inside_lst = bom_into_fileList(lstPath)
    SyncMyRide_fileList = fileList_from_SyncMyRide(lstPath.replace('autoinstall.lst',"SyncMyRide"))
    temp_intsct_fileList = files_inside_lst.intersection(SyncMyRide_fileList) # new set with elements common to s and t
    for element in temp_intsct_fileList:
        cmp_final_report.write(element + " | Found (=) \n")
    temp_sym_diff = files_inside_lst.symmetric_difference(SyncMyRide_fileList) #new set with elements in either s or t but not both
    for item in temp_sym_diff:
        if re.match('DA5T-14D544-B.\.ZIP', item): # Ignore the .sec image since is not listed in the BOM
            cmp_final_report.write(item + " | .SEC File (n/a) \n")
        else:
            cmp_final_report.write(item + " | MISSING (?) \n")

cmp_final_report.close()

#Opening final FPN report for analysis
cmp_final_report = open("BOM_vs_SyncMyRide_Final_Report.txt", "r")

#Create a collection of strings + amount of counts inside FPN final report
cnt = Counter() 
for line in cmp_final_report:
    for word in line.split():
        cnt[word] +=1

#Print quick overview summary for user
print "### Summary of BOM vs. \SyncMyRide files comparison #### "
print "There were %s" %cnt['(=)'] + " that matched your both your BOM and \SynMyRide Folder(s)"
print "There were %s" %cnt['(?)'] + " that did NOT exist in either your BOM or the \SynMyRide Folder(s)\n"

print "--- USB image update file checker script has finished ---"
print "Press ENTER to close window"
raw_input()