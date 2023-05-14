import os
from os import listdir
from os import path
import re
import sys

path_list = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
file_folder = os.path.join(path_list, "localisation\\english")

if not "git-days-of-europe" in path_list:
	print("Please run the Script in git-days-of-europe\\useful_python_programs")
	sys.exit()

print(file_folder)

file_list = listdir(file_folder)
file_list.sort(key=lambda f: os.stat(file_folder+"\\"+f).st_size, reverse=True)

def fix_duplicates (loc_file):
	lines_to_write = []
	duplicates = 0
	print (loc_file)
	with open(f"{file_folder}/{loc_file}", "r", encoding="utf8") as inp:
		line_list = inp.readlines()
		for line in line_list:
			total_line_list.append(line)
			find_loc = line.find(":")
			loc = line[:find_loc]
			loc = re.sub (r"^0?\s*\"", "", loc)
			loc = re.sub (r"\s*$", "", loc)
			if not (loc == "" or "#" in loc or "l_english" in loc):
				loc_list.append(loc)
			if loc_list.count(loc) > 1 and not (loc == "" or "#" in loc or "l_english" in loc):
				duplicates += 1
				if total_line_list.count(line) > 1:
					print(f"\tDUPLICATE STRING {loc}")
				else:
					lines_to_write.append(f"#{line[:-1]} #duplicate loc key\n")
					print(f"\tDUPLICATE LOC KEY {loc}")
			else:
				lines_to_write.append(line)
				
	if duplicates != 0:
		print(f"WRITING TO FILE {loc_file}")
		with open(f"{file_folder}/{loc_file}", "w", encoding="utf8") as out:
			for line in lines_to_write:
				out.write(line)


total_line_list = []
duplicate_list = []
loc_list = []

for file in file_list:
	if "TNO_" in file:
		fix_duplicates(file)
		
for file in file_list:
	if not "TNO_" in file:
		fix_duplicates(file)