#!/usr/bin/python
#---------------------------------------
# docx2txt.py
# Author: dlopzv
# 06.02.2020
# LAST CHANGE:
# 06.02.2020
#---------------------------------------
# usage: python docx2txt.py
#
# example:
# python docx2txt.py
#
# features:
# check a directory and all its subdirectories
# convert all .docx files to .txt
#.txt file is saved in same directory as detected .docx
#
# real world needs:
# transform .docx files sent by localization teams into .txt format
# to upload them to Amazon Broadcast

import os
import textract

# Set your own source directoy below
source_directory = r'/Users/dlopzv/WorkDocs/My Documents/Projects/Onboarding VTT Transcripts Files'

for subdir, dirs, files in os.walk(source_directory):
    for filename in files:
        filepath = subdir + os.sep + filename

        if filepath.endswith(".docx"):
            file, extension = os.path.splitext(filepath)
            print (filepath)
            dest_file_path = file + '.txt'

            # replace following line with location of your .docx file
            process_file = textract.process(filepath)

            # We create and open the new and we prepare to write the Binary Data
            # which is represented by the wb - Write Binary
            write_text_file = open(dest_file_path, "wb")

            # write the content and close the newly created file
            write_text_file.write(process_file)
            write_text_file.close()
"""
            # delete the first two lines (includind new lines) of the .txt file
            with open(dest_file_path, 'r') as fin:
                data = fin.read().splitlines(True)
            with open(dest_file_path, 'w') as fout:
                fout.writelines(data[1:])
"""
