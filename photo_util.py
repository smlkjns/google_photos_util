#!/usr/bin/python
import os
from exif import Image
from datetime import datetime

folder_path = input("Enter input path:")
output_path = input("Enter output path:")

mf_list = []

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if not file.endswith('.json'):
            file_path = root + "/" + file
            mf_list.append(file_path)

items = len(mf_list)
items_worked = 0

for file in mf_list:
    dt = False
    with open(file, 'rb') as opened_file:
        if file.endswith('.jpg'):
            try:
                opened_file_exif = Image(opened_file)
                dt_s = opened_file_exif.datetime_original
                dt = datetime.strptime(dt_s.split(" ")[0], "%Y:%m:%d")
            except:
                pass
        if dt == False:
            try:
                year = file.split("Photos from ")[1].split("/")[0]
                dt = datetime.strptime(year, "%Y")
            except:
                pass
        if dt==False:
            string_splits = file.split("/")[-1].split("_")
            for split in string_splits:
                try:
                    dt = datetime.strptime(split, "%Y%m%d")
                    break
                except:
                    pass
        if dt==False:
            string_splits = file.split("/")[-1].split("-")
            for split in string_splits:
                try:
                    dt = datetime.strptime(split, "%Y%m%d")
                    break
                except:
                    pass

        if dt != False:
            output_folder = output_path + "/" + dt.strftime("%Y") + " " + dt.strftime("%m") + " " + dt.strftime("%B")
        else:
            output_folder = output_path + "/Unknown date"
        output_file = output_folder + "/" + file.split("/")[-1]
        if not os.path.isfile(output_file):
            if not os.path.isdir(output_folder):
                os.system('mkdir "' + output_folder + '"')
            os.system('cp "' + file + '" "' + output_folder + '"')
    items_worked += 1
    print("-Processing " + str(items_worked) + " of " + str(items) + ", " + str(round((items_worked/items)*100, 1)) + "% completed", end="\r")
