import random
import os
import shutil
import re

#by uncountably

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
event_file = "TNO_diplo_crisis.txt"

event_path =  f"{root_dir}\\events\\{event_file}"
output_file =  (f"{root_dir}\\events\\{event_file}_output.txt", "a")

possible_pics = ["GFX_report_event_saf_negotiations", "GFX_report_event_generic_usa_treaty", "GFX_report_event_generic_sign_treaty1", "GFX_report_event_generic_sign_treaty2", "GFX_report_event_generic_sign_treaty3", "GFX_report_event_iberia_ship_stairs", "GFX_report_event_italy_naval_ship", "GFX_report_event_us_navy"]
event_files = []
placeholder_pics = ["GFX_report_event_german_Army2", "GFX_report_event_lithuania_army"]


def get_files_from_folder(): #optional
	for file in os.listdir(f"{root_dir}\\useful_python_programs\\EventList"):
		if not file == "dummy.txt":
			event_files.append(file)
	with open(f"{root_dir}\\interface\\eventpictures.gfx", "r") as interface:
		line_list = interface.readlines()
		for i, line in enumerate(line_list):
			if "texturefile" in line and any(pic in line for pic in event_files):
				event_definition = re.sub(r"^\s*name = \"", "", line_list[i-1]) 
				event_definition = re.sub(r"\"\s*$", "", event_definition)
				print(event_definition)
				possible_pics.append(event_definition)

def main():
	with open(event_path, "r") as f:
		for line in f.readlines():
			if check_line(line):
				output_file.write("	picture = " + random.choice(possible_pics) + "\n")
			else:
				output_file.write(line)

def check_line(line):
	if line[:8] == "	picture" or line[:9] == "#	picture" or line[:9] == "	#picture" or line[:9] == "#    picture" or line[:9] == "    #picture": # not the best check but lazy
		return True
	elif any(pic in line for pic in placeholder_pics):
		return True
	else:
		return False

if __name__ == '__main__':
	main()

