from os import listdir
from os import path
from codecs import open
from shutil import copyfile
import copy
import re
import os
import sys
#by Wendell08, run this script and get a log of what loc strings quotes are missing 

tno_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if not "git-days-of-europe" in tno_path:
	print("Please run this Script in git-days-of-europe\\useful_python_programs")
	sys.exit()
loc_path = tno_path+r"\localisation"

try:
	os.remove(f"{os.path.dirname(os.path.realpath(__file__))}\\missing_quotes.yml")
except:
	pass

for subdir, dirs, files in os.walk(loc_path):
	for file in files:
		with open(f"{subdir}\\{file}", "r", encoding="utf-8") as inp:
			line_list = inp.readlines()
			for i, line in enumerate(line_list):
				if re.match("^\s*#", line):
					continue
				if "l_english" in line or not ":" in line:
					continue
				quote_count = 0
				quote_count += line.count("\"")
				if quote_count % 2 != 0 and not quote_count == 0:
					with open(f"missing_quotes.yml", "a+", encoding="utf-8") as out:
						string_to_print = f"({i+1}, {file})\n{line}\n"
						print(string_to_print)
						out.write(string_to_print)



