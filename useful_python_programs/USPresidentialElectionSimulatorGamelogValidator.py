import csv
import os
import sys

#by uncountably

this_path = os.path.realpath(__file__)
last_backslash_ind = this_path.rfind("\\")
this_path_folder = this_path[:last_backslash_ind]
gamelog_file = "NONE"
output_dir = sys.argv[1]

def detect_errors():
	is_fine = 0
	gamelog_file_path = os.path.realpath(gamelog_file)
	gamelog_file_path_folder = gamelog_file_path[:gamelog_file_path.rfind("\\")]
	file = open(gamelog_file, "r", errors="ignore")
	lines = file.readlines()
	dates = move_data_and_make_dates(gamelog_file_path_folder)
	for date in dates:
		if dates[date] != 100 and dates[date] != 102:
			print(f"Error detected at date {date[1:]}; has {dates[date]} instances")
			is_fine = 1
	return is_fine
	
def move_data_and_make_dates(path):
	file = open(gamelog_file, "r", errors="ignore")
	lines = file.readlines()
	data_moved = open(path+"\data_moved.csv", "a", errors="ignore")
	dates = {}
	for line in lines:
		if "THIS_IS_USEL_DATA" in line:
			data_moved.write("\""+line[line.rfind("[effectbase.cpp:2243]:") + 44:])
	with open(path+"\data_moved.csv", "r") as datafile2:
		data = csv.reader(datafile2, delimiter=",")
		for row in data:
			if row[0] not in dates:
				dates[row[0]] = 0
			dates[row[0]] += 1
	data_moved.close()
	os.remove(path+"\data_moved.csv")
	return dates

if __name__ == "__main__":
	gamelog_file = output_dir + "/game.log"
	is_fine = detect_errors()
	exit(is_fine)