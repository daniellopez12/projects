'''
Created on Jul 3, 2013
USB image update folder automator: This tool will create a set of template folders based
on an image release and create a DONTINDX.MSA
@author: DLOPEZ42
'''
import os
import re
import shutil

print "--- USB Update Folder Automator Script: Started --- "

# USB image update regions
img_updt_regions = ["Australia", "China", "EU-Lang pack1 DE-DE_EN-GB_RU-RU_TR-TR", "EU-Lang pack2 DE-DE_EN-GB_PL-PL_RU-RU",
                            "EU-Lang pack3 DE-DE_EN-GB_FR-FR_IT-IT", "EU-Lang pack4 DE-DE_EN-GB_FR-FR_SV-SE",
                            "EU-Lang pack5 EN-GB_ES-ES_FR-FR_PT-PT", "EU-Lang pack6 DE-DE_EN-GB_FR-FR_NL-NL", "Export", "Export_China_Lang_pack",
                            "NA","NA_BETA", "SA"]

# Check for valid update folder path entry
while True:
    update_fldr_path = raw_input("Enter the path to where you will like to create template folders: ")
    if os.path.exists(update_fldr_path) == True:
        break
    else:
        print "The path you provided does not exist. Please enter a valid path."

# Check for proper Julian date entry
while True:
    image_julian_date = raw_input("Enter the Julian date of the release: ")
    if not re.match("^[0-9]{5}$", image_julian_date): # Check for 5 digit characters only
        print "A Sync Release date is composed of last two digits of the year and three Julian date digits (i.e. 12285). Please try again."
    else:
        break

# Check for proper image flavor entry
while True:
    image_flavor = raw_input("Signed or Unsigned?: ")
    if image_flavor in("Signed", "signed", "Unsigned", "unsigned"):
        break
    else:
        print "Please enter a valid response."

# Check image flavor and iterate through list of image update regions to create folder names with Julian date
if image_flavor in("Signed", "signed"):
    for index in range(len(img_updt_regions)):
        if not os.path.exists(update_fldr_path + "\\" + image_julian_date + "_Signed_" + img_updt_regions[index]): os.makedirs(update_fldr_path + "\\" +  image_julian_date + "_Signed_" + img_updt_regions[index])
        doNotIndexFile = open(update_fldr_path + "\\" + image_julian_date + "_Signed_" + img_updt_regions[index] + "\\" + "DONTINDX.MSA", "w") # add do not index file inside each folder
        doNotIndexFile.close()
elif image_flavor in ("Unsigned", "unsigned"):
    for index in range(len(img_updt_regions)):
        if not os.path.exists(update_fldr_path + "\\" + image_julian_date + "_Unsigned_" +  img_updt_regions[index]): os.makedirs(update_fldr_path + "\\" +  image_julian_date + "_Unsigned_" + img_updt_regions[index])
        doNotIndexFile = open(update_fldr_path + "\\" + image_julian_date + "_Unsigned_" + img_updt_regions[index] + "\\" + "DONTINDX.MSA", "w") # add do not index file inside each folder
        doNotIndexFile.close()    

print "USB image update folders have been created."

while True:
    cont_script = raw_input("Would you like to continue with the copy portion of the script? (y/n): ")
    if cont_script in("Y", "y", "N", "n"):
        break
    else:
        print "Please enter 'y' or 'n'"
    
# if user decides to continue script run the following code    
if cont_script in ("Y", "y"):
    
    # Check for valid path to where .lst file to copy resides
    while True:
        cp_path = raw_input("Enter the path to where the lst (BOM) & SyncMyRide folder you wish to copy resides: ")
        if os.path.exists(cp_path) == True:
            break
        else:
            print "The path you provided does not exist. Please enter a valid path."
    
    #Copy the .lst to every folder in either the signed or unsigned path location(s)
    if image_flavor in("Signed", "signed"):
        for index in range(len(img_updt_regions)):
            shutil.copy2(cp_path + "\\autoinstall.lst", update_fldr_path + "\\" + image_julian_date + "_Signed_" + img_updt_regions[index])
            shutil.copytree(cp_path  + "\\SyncMyRide", update_fldr_path + "\\" + image_julian_date + "_Signed_" + img_updt_regions[index] + "\\SyncMyRide")
    elif image_flavor in ("Unsigned", "unsigned"):
        for index in range(len(img_updt_regions)):
            shutil.copy2(cp_path + "\\autoinstall.lst", update_fldr_path + "\\" + image_julian_date + "_Unsigned_" + img_updt_regions[index])
            shutil.copytree(cp_path + "\\SyncMyRide", update_fldr_path + "\\" + image_julian_date + "_Unsigned_" + img_updt_regions[index]+ "\\SyncMyRide")
                   
print "SyncMyRide folder copied to all release folders."    
print "--- USB Update Folder Automator Script: finished --- "
#raw_input()