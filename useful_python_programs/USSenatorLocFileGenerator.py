import csv
import sys

#by uncountably

#converts a .csv file of senators into a loc file of senators
states_list = []
RD_R_list_1 = []
RD_R_list_2 = []
RD_D_list_1 = []
RD_D_list_2 = []
NPP_L_list_1 = []
NPP_L_list_2 = []
NPP_C_list_1 = []
NPP_C_list_2 = []
NPP_R_list_1 = []
NPP_R_list_2 = []
NPP_FR_list_1 = []
NPP_FR_list_2 = []

inputfile = open(sys.argv[1], "r")
outputfile = open(sys.argv[2], "a", encoding="utf-8")

data = csv.reader(inputfile)

def get_lists():
	for line in data:
		if "Democratic1" not in line:
			states_list.append(line[0])
			RD_R_list_1.append(line[1])
			RD_R_list_2.append(line[2])
			RD_D_list_1.append(line[3])
			RD_D_list_2.append(line[4])
			NPP_L_list_1.append(line[5])
			NPP_L_list_2.append(line[6])
			NPP_C_list_1.append(line[7])
			NPP_C_list_2.append(line[8])
			NPP_R_list_1.append(line[9])
			NPP_R_list_2.append(line[10])
			NPP_FR_list_1.append(line[11])
			NPP_FR_list_2.append(line[12])

def pre_write():
	outputfile.write("l_english:\n EMPTY_SENATOR: \"§REmpty/Unavailable§!§N\"\n")

def write_loc_file():
	print(states_list)
	for num, state in enumerate(states_list):
		outputfile.write(" RD_R_SENATOR_"+state.upper()+"_1: \"(§RR§!-§TD§! – §RRepublican§!) "+RD_R_list_1[num]+"\"\n")
		outputfile.write(" RD_R_SENATOR_"+state.upper()+"_2: \"(§RR§!-§TD§! – §RRepublican§!) "+RD_R_list_2[num]+"\"\n")
		outputfile.write(" RD_D_SENATOR_"+state.upper()+"_1: \"(§RR§!-§TD§! – §TDemocrat§!) "+RD_D_list_1[num]+"\"\n")
		outputfile.write(" RD_D_SENATOR_"+state.upper()+"_2: \"(§RR§!-§TD§! – §TDemocrat§!) "+RD_D_list_2[num]+"\"\n")
		outputfile.write(" NPP_L_SENATOR_"+state.upper()+"_1: \"(§ONPP§! – §VMarxist§!) "+NPP_L_list_1[num]+"\"\n")
		outputfile.write(" NPP_L_SENATOR_"+state.upper()+"_2: \"(§ONPP§! – §VMarxist§!) "+NPP_L_list_2[num]+"\"\n")
		outputfile.write(" NPP_C_SENATOR_"+state.upper()+"_1: \"(§ONPP§! – §KProgressive§!) "+NPP_C_list_1[num]+"\"\n")
		outputfile.write(" NPP_C_SENATOR_"+state.upper()+"_2: \"(§ONPP§! – §KProgressive§!) "+NPP_C_list_2[num]+"\"\n")
		outputfile.write(" NPP_R_SENATOR_"+state.upper()+"_1: \"(§ONPP§! – §OSovereigntist§!) "+NPP_R_list_1[num]+"\"\n")
		outputfile.write(" NPP_R_SENATOR_"+state.upper()+"_2: \"(§ONPP§! – §OSovereigntist§!) "+NPP_R_list_2[num]+"\"\n")
		outputfile.write(" NPP_FR_SENATOR_"+state.upper()+"_1: \"(§ONPP§! – §gNationalist§!) "+NPP_FR_list_1[num]+"\"\n")
		outputfile.write(" NPP_FR_SENATOR_"+state.upper()+"_2: \"(§ONPP§! – §gNationalist§!) "+NPP_FR_list_2[num]+"\"\n")
		outputfile.write("\n")

get_lists()
pre_write()
write_loc_file()