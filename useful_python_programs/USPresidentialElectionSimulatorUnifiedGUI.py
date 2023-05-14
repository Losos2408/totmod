import csv
import datetime
import os
import plotly
import plotly.graph_objs as graph
import random
import sys
import time
import timeit
import tkinter
import tkinter.filedialog as filedialog

############################################################################################################################################################################################################################
# US Presidential Election Simulator by uncountably																																										   #
# Simulates TNO US presidential elections																																												   #
# Also does Senate elections            																																												   #
# How to use: Double click the program and use the GUI, MAKE SURE TO SELECT AN OUTPUT FILE AS IT SAYS        																										 	   #
############################################################################################################################################################################################################################

#1. Create temp_RD_pop and temp_NPP_pop which are percentages of total RD_popularity and NPP_popularity
#2. Create RD_total_pop and NPP_total_pop which are sums of the party factions' popularities
#3. Convert each faction's popularity into a percentage of the party's total popularity
#4. Multiply the faction percents by the RD and NPP percents
#Bonus Popularity
#5. Increase the faction popularity for the RD and NPP factions running by 0.3 times the faction's pie popularity
#6. Raise the incumbent president's faction's popularity by 0.05
#End Bonus Popularity
#Begin NPP Vote Splitting
#7. Create the variables temp_NPP_unity (NPP unity/30) and temp_NPP_unity_minus (1 - temp_NPP_unity)
#8. Create the variables NPP_C_popularity_2 and NPP_FR_popularity_2 which are equal to NPP_C_popularity and NPP_FR_popularity
#9. Multiply NPP_C_popularity and NPP_FR_popularity by temp_NPP_unity, and the _2 versions by temp_NPP_unity_minus
#10. Add these popularities to RD_temp_pop and NPP_temp_pop as follows:
#-L and R always vote for the most left or most right candidate respectively
#-C and FR split votes unless a C or FR candidate is running
#End NPP Vote Splitting
#Begin RD Vote Splitting
#11. Create the variables temp_RD_unity (RD unity/30) and temp_RD_unity_minus (1 - temp_RD_unity)
#12. Create the variables RD_R_popularity_2 and RD_D_popularity_2 which are equal to RD_R_popularity and RD_D_popularity
#13. Multiply RD_R_popularity and RD_D_popularity by temp_RD_unity, and the _2 versions by temp_RD_unity_minus
#14. Add these popularities to RD_temp_pop and NPP_temp_pop as follows:
#-R and D break entirely for RD if an R or L candidate is running
#-R split if the election is D vs. C, and D split if the election is R vs. FR
#End RD Vote Splitting
#15. Add electoral votes for either RD or NPP based on which one has a greater party pop variable, with ties going NPP


#1: RD-R
#2: RD-D
#3: NPP-L
#4: NPP-C
#5: NPP-R
#6: NPP-FR

BONUS_POPULARITY_PRES_MULTIPLIER = 0.3
PRESIDENT_INCUMBENCY_BONUS_POPULARITY = 0.05
MAX_UNITY = 30
SAME_FACTION_UNITY = True
CLAMP_MIN = 0.001
CLAMP_MAX = 1000

data = []
statelist = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
elecvotelist = [10, 3, 5, 6, 40, 6, 8, 3, 14, 12, 4, 4, 26, 13, 9, 7, 9, 10, 4, 13, 14, 21, 10, 7, 12, 4, 5, 3, 4, 17, 4, 43, 13, 4, 26, 8, 6, 29, 4, 8, 4, 11, 25, 4, 3, 12, 9, 7, 12, 3]
startlist = []
endlist = []
this_path = os.path.realpath(__file__)
last_backslash_ind = this_path.rfind("\\")
this_path_folder = this_path[:last_backslash_ind]
gamelog_file = "NONE"
dataall_file = "NONE"
graphcsv_file = "NONE"
dataall_prefix = ""
graphcsv_prefix = ""
graph_filename = ""
outputfile = "SELECT AN OUTPUT FILE BEFORE DOING ANYTHING"


class SimulatorUI(tkinter.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		global dataall_prefix
		self.extract_gamelog = tkinter.Button(self)
		self.extract_gamelog["text"] = "Extract from a game.log file"
		self.extract_gamelog["command"] = self.extract_and_sort_wrapper
		self.extract_gamelog["state"] = "disabled"
		self.extract_gamelog.pack(side="top")
		
		self.sim_elections = tkinter.Button(self)
		self.sim_elections["text"] = "Simulate elections from a data_all.csv file and also output a graph.csv file"
		self.sim_elections["command"] = self.sim_elections_wrapper
		self.sim_elections["state"] = "disabled"
		self.sim_elections.pack(side="top")
		
		self.create_graph = tkinter.Button(self)
		self.create_graph["text"] = "Convert a graph.csv file into an actual graph"
		self.create_graph["command"] = self.make_graph_normal_wrapper
		self.create_graph["state"] = "disabled"
		self.create_graph.pack(side="top")
		
		self.create_graph_senate = tkinter.Button(self)
		self.create_graph_senate["text"] = "Convert a graph.csv file into a senate graph"
		self.create_graph_senate["command"] = self.make_graph_senate_wrapper
		self.create_graph_senate["state"] = "disabled"
		self.create_graph_senate.pack(side="top")
		
		self.gamelog_label = tkinter.Label(self)
		self.gamelog_label["text"] = "Current game.log file: "+gamelog_file
		self.gamelog_label["justify"] = "center"
		self.gamelog_label["wraplength"] = 450
		self.gamelog_label.pack(side="top")
		
		self.file_select_gamelog = tkinter.Button(self)
		self.file_select_gamelog["text"] = "Select a game.log file"
		self.file_select_gamelog["command"] = self.gamelog_filedialog_wrapper
		self.file_select_gamelog.pack(side="top")
		
		self.dataall_label = tkinter.Label(self)
		self.dataall_label["text"] = "Current data_all.csv file: "+dataall_file
		self.dataall_label["justify"] = "center"
		self.dataall_label["wraplength"] = 450
		self.dataall_label.pack(side="top")
		
		self.file_select_dataall = tkinter.Button(self)
		self.file_select_dataall["text"] = "Select a data_all.csv file"
		self.file_select_dataall["command"] = self.dataall_filedialog_wrapper
		self.file_select_dataall.pack(side="top")
		
		self.graphcsv_label = tkinter.Label(self)
		self.graphcsv_label["text"] = "Current graph.csv file: "+graphcsv_file
		self.graphcsv_label["justify"] = "center"
		self.graphcsv_label["wraplength"] = 450
		self.graphcsv_label.pack(side="top")
		
		self.file_select_graphcsv = tkinter.Button(self)
		self.file_select_graphcsv["text"] = "Select a graph.csv file"
		self.file_select_graphcsv["command"] = self.graphcsv_filedialog_wrapper
		self.file_select_graphcsv.pack(side="top")
		
		self.dataall_prefix_entry_label = tkinter.Label(self)
		self.dataall_prefix_entry_label["text"] = "Prefix for your data_all.csv file"
		self.dataall_prefix_entry_label.pack(side="top")
		
		self.dataall_prefix_entry_box = tkinter.Entry(self)
		self.dataall_prefix_entry_box.pack(side="top")
		
		self.graphcsv_prefix_entry_label = tkinter.Label(self)
		self.graphcsv_prefix_entry_label["text"] = "Prefix for your graph.csv file"
		self.graphcsv_prefix_entry_label.pack(side="top")
		
		self.graphcsv_prefix_entry_box = tkinter.Entry(self)
		self.graphcsv_prefix_entry_box.pack(side="top")
		
		self.graph_prefix_entry_label = tkinter.Label(self)
		self.graph_prefix_entry_label["text"] = "Filename for your graph .html file"
		self.graph_prefix_entry_label.pack(side="top")
		
		self.graph_prefix_entry_box = tkinter.Entry(self)
		self.graph_prefix_entry_box.pack(side="top")
		
		self.output_label = tkinter.Label(self)
		self.output_label["text"] = "Current output file: "+outputfile
		self.output_label["justify"] = "center"
		self.output_label["wraplength"] = 450
		self.output_label.pack(side="top")
		
		self.file_select_output = tkinter.Button(self)
		self.file_select_output["text"] = "Select an output file"
		self.file_select_output["command"] = self.output_filedialog_wrapper
		self.file_select_output.pack(side="top")
		
#		self.processing_text = tkinter.StringVar()
		
#		self.processing_informer = tkinter.Label(self)
#		self.processing_informer["textvariable"] = self.processing_text
#		self.processing_informer.pack(side="top")
		
#		self.processing_quote = tkinter.Label(self)
#		cur_proc_quote = processing_quotes[0]
#		self.processing_quote["text"] = cur_proc_quote
#		self.processing_quote.pack(side="bottom")
	
	def extract_and_sort_wrapper(self):
		global dataall_prefix
#		cur_proc_quote = (processing_quotes[1])
#		self.processing_quote["text"] = cur_proc_quote
		dataall_prefix = self.dataall_prefix_entry_box.get()
#		self.processing_text.set("Processing...")
#		self.after(1000)
		extract_and_sort()
#		self.processing_text.set("")
		
	def sim_elections_wrapper(self):
		global graphcsv_prefix
		graphcsv_prefix = self.graphcsv_prefix_entry_box.get()
#		self.processing_informer["text"] = "Processing..."
#		self.processing_informer.pack(side="top")
		convert_csv_to_data_array(dataall_file)
		dates = get_date_list(dataall_file)
		sim_election_multiple_parties_dates(statelist,elecvotelist,dates)
#		self.processing_informer["text"] = ""
#		self.processing_informer.pack(side="top")
	
	def make_graph_normal_wrapper(self):
		global graph_filename
		graph_filename = self.graph_prefix_entry_box.get()
#		self.processing_informer["text"] = "Processing..."
#		self.processing_informer.pack(side="top")
		make_graph_normal(graphcsv_file, os.path.dirname(os.path.realpath(graphcsv_file)))
#		self.processing_informer["text"] = ""
#		self.processing_informer.pack(side="top")
	
	def make_graph_senate_wrapper(self):
		global graph_filename
		graph_filename = self.graph_prefix_entry_box.get()
#		self.processing_informer["text"] = "Processing..."
#		self.processing_informer.pack(side="top")
		make_graph_senate(graphcsv_file, os.path.dirname(os.path.realpath(graphcsv_file)))
#		self.processing_informer["text"] = ""
#		self.processing_informer.pack(side="top")
		
	def gamelog_filedialog_wrapper(self):
		global gamelog_file
		gamelog_file = filedialog.askopenfilename(initialdir=this_path,title="Select File",filetypes=[("game.log files", "*game.log")])
		self.extract_gamelog["state"] = "active"
		self.gamelog_label["text"] = "Current game.log file: "+gamelog_file
		self.gamelog_label.pack(side="top")
	
	def dataall_filedialog_wrapper(self):
		global dataall_file
		dataall_file = filedialog.askopenfilename(initialdir=this_path,title="Select File",filetypes=[("data_all.csv files", "*data_all.csv")])
		self.sim_elections["state"] = "active"
		self.dataall_label["text"] = "Current data_all.csv file: " + dataall_file
		self.dataall_label.pack(side="top")
	
	def graphcsv_filedialog_wrapper(self):
		global graphcsv_file
		graphcsv_file = filedialog.askopenfilename(initialdir=this_path,title="Select File",filetypes=[("graph.csv files", "*graph.csv")])
		self.create_graph["state"] = "active"
		self.create_graph_senate["state"] = "active"
		self.graphcsv_label["text"] = "Current graph.csv file: " + graphcsv_file
		self.graphcsv_label.pack(side="top")
	
	def output_filedialog_wrapper(self):
		global outputfile
		outputfilepath = filedialog.askopenfilename(initialdir=this_path,title="Select File",filetypes=[(".txt files", "*.txt")])
		outputfile = open(outputfilepath, "a", errors="ignore")
		self.output_label["text"] = "Current output file: " + outputfilepath
		self.output_label.pack(side="top")

	






class Results(object):
	def __init__(self, winner, RD_votes, NPP_votes, RD_states, senators):
		self.winner = ""
		self.RD_votes = 0
		self.NPP_votes = 0
		self.RD_states = []
		self.senators = []

class StateResults(object):
	def __init__(self):
		self.senator1 = 0
		self.senator2 = 0
		self.president = ""

def extract_and_sort():
	start_time = timeit.default_timer()
	outputfile.write("\nExtracting data from game.log file at "+gamelog_file)
	gamelog_file_path = os.path.realpath(gamelog_file)
	gamelog_file_path_folder = gamelog_file_path[:gamelog_file_path.rfind("\\")]
	file = open(gamelog_file, "r", errors="ignore")
	data_combined = open(gamelog_file_path_folder+"\\"+dataall_prefix+"data_all.csv", "a", errors="ignore")
	lines = file.readlines()
	dates = move_data_and_make_dates(gamelog_file_path_folder)
	for date in dates:
		for line in lines:
			if date in line:
				if "THIS_IS_USEL_DATA_3" in line:
					quot = "\""
					line2 = quot + line[line.rfind("[effectbase.cpp:2243]:") + 44:]
					data_combined.write(line2)
		for line in lines:
			if date in line:
				if "THIS_IS_USEL_DATA_1" in line:
					quot = "\""
					line2 = quot + line[line.rfind("[effectbase.cpp:2243]:") + 44:]
					data_combined.write(line2)
		for line in lines:
			if date in line:
				if "THIS_IS_USEL_DATA_2" in line:
					quot = "\""
					line2 = quot + line[line.rfind("[effectbase.cpp:2243]:") + 44:]
					data_combined.write(line2)
	end_time = timeit.default_timer()
	elapsed_time = round(1000*(end_time-start_time))
	print("Extracted data from game.log in {} ms".format(elapsed_time))
	outputfile.write("\nExtracted data from game.log file at " + gamelog_file + " in " + str(elapsed_time) + " ms")
	
def move_data_and_make_dates(path):
	file = open(gamelog_file, "r", errors="ignore")
	lines = file.readlines()
	data_moved = open(path+"\data_moved.csv", "x", errors="ignore")
	dates = []
	for line in lines:
		if "THIS_IS_USEL_DATA" in line:
			data_moved.write("\""+line[line.rfind("[effectbase.cpp:2243]:") + 44:])
	with open(path+"\data_moved.csv", "r") as datafile2:
		data = csv.reader(datafile2, delimiter=",")
		for row in data:
			if row[0] not in dates:
				dates.append(row[0])
	data_moved.close()
	os.remove(path+"\data_moved.csv")
	return dates

def convert_csv_to_data_array(dataall_file):
	with open(dataall_file,newline='') as datafile2:
		data0 = csv.reader(datafile2, delimiter=",")
		for row in data0:
			data.append(row)

def sim_election(RD,NPP,RD_R_bonus,RD_D_bonus,NPP_L_bonus,NPP_C_bonus,NPP_R_bonus,NPP_FR_bonus,RD_R_pie,RD_D_pie,NPP_L_pie,NPP_C_pie,NPP_R_pie,NPP_FR_pie,RD_cand,NPP_cand,RD_unity,NPP_unity,pres_party,senator1,senator2,print_flag):
	result = StateResults()
	
	RD = CLAMP_MIN if RD < CLAMP_MIN else CLAMP_MAX if RD > CLAMP_MAX else RD
	NPP = CLAMP_MIN if NPP < CLAMP_MIN else CLAMP_MAX if NPP > CLAMP_MAX else NPP
	RD_R_bonus = CLAMP_MIN if RD_R_bonus < CLAMP_MIN else CLAMP_MAX if RD_R_bonus > CLAMP_MAX else RD_R_bonus
	RD_D_bonus = CLAMP_MIN if RD_D_bonus < CLAMP_MIN else CLAMP_MAX if RD_D_bonus > CLAMP_MAX else RD_D_bonus
	NPP_L_bonus = CLAMP_MIN if NPP_L_bonus < CLAMP_MIN else CLAMP_MAX if NPP_L_bonus > CLAMP_MAX else NPP_L_bonus
	NPP_C_bonus = CLAMP_MIN if NPP_C_bonus < CLAMP_MIN else CLAMP_MAX if NPP_C_bonus > CLAMP_MAX else NPP_C_bonus
	NPP_R_bonus = CLAMP_MIN if NPP_R_bonus < CLAMP_MIN else CLAMP_MAX if NPP_R_bonus > CLAMP_MAX else NPP_R_bonus
	NPP_FR_bonus = CLAMP_MIN if NPP_FR_bonus < CLAMP_MIN else CLAMP_MAX if NPP_FR_bonus > CLAMP_MAX else NPP_FR_bonus
	
	total_pop = RD + NPP
	RD_percent = RD / total_pop
	NPP_percent = NPP / total_pop #step 1
	
	if print_flag:
		print("total_pop: " + str(total_pop) + " RD_percent: " + str(RD_percent) + " NPP_percent: " + str(NPP_percent))
	
	RD_total = RD_R_bonus + RD_D_bonus
	NPP_total = NPP_L_bonus + NPP_C_bonus + NPP_R_bonus + NPP_FR_bonus #step 2
	
	if print_flag:
		print("RD_total: " + str(RD_total) + " NPP_total: " + str(NPP_total))
	
	RD_R_bonus_pres = RD_R_bonus / RD_total
	RD_D_bonus_pres = RD_D_bonus / RD_total
	NPP_L_bonus_pres = NPP_L_bonus / NPP_total
	NPP_C_bonus_pres = NPP_C_bonus / NPP_total
	NPP_R_bonus_pres = NPP_R_bonus / NPP_total
	NPP_FR_bonus_pres = NPP_FR_bonus / NPP_total #step 3
	
	if print_flag:
		print("RD_R_bonus: " + str(RD_R_bonus) + " RD_D_bonus: " + str(RD_D_bonus) + " NPP_L_bonus: " + str(NPP_L_bonus) + " NPP_C_bonus: " + str(NPP_C_bonus) + " NPP_FR_bonus: " + str(NPP_FR_bonus) + " NPP_R_bonus: " + str(NPP_R_bonus))
	
	RD_R_bonus_pres *= RD_percent
	RD_D_bonus_pres *= RD_percent
	NPP_L_bonus_pres *= NPP_percent
	NPP_C_bonus_pres *= NPP_percent
	NPP_R_bonus_pres *= NPP_percent
	NPP_FR_bonus_pres *= NPP_percent #step 4
	
	if print_flag:
		print("RD_R_bonus: " + str(RD_R_bonus) + " RD_D_bonus: " + str(RD_D_bonus) + " NPP_L_bonus: " + str(NPP_L_bonus) + " NPP_C_bonus: " + str(NPP_C_bonus) + " NPP_FR_bonus: " + str(NPP_FR_bonus) + " NPP_R_bonus: " + str(NPP_R_bonus))
	
	if RD_cand == 1:
		RD_R_bonus_pres += (BONUS_POPULARITY_PRES_MULTIPLIER * RD_R_pie)
	elif RD_cand == 2:
		RD_D_bonus_pres += (BONUS_POPULARITY_PRES_MULTIPLIER * RD_D_pie)
	if NPP_cand == 3:
		NPP_L_bonus_pres += (BONUS_POPULARITY_PRES_MULTIPLIER * NPP_L_pie)
	elif NPP_cand == 4:
		NPP_C_bonus_pres += (BONUS_POPULARITY_PRES_MULTIPLIER * NPP_C_pie)
	elif NPP_cand == 5:
		NPP_R_bonus_pres += (BONUS_POPULARITY_PRES_MULTIPLIER * NPP_R_pie)
	elif NPP_cand == 6:
		NPP_FR_bonus_pres += (BONUS_POPULARITY_PRES_MULTIPLIER * NPP_FR_pie) #step 5
	
	if pres_party == 1:
		RD_R_bonus_pres += PRESIDENT_INCUMBENCY_BONUS_POPULARITY
	elif pres_party == 2:
		RD_D_bonus_pres += PRESIDENT_INCUMBENCY_BONUS_POPULARITY
	elif pres_party == 3:
		NPP_L_bonus_pres += PRESIDENT_INCUMBENCY_BONUS_POPULARITY
	elif pres_party == 4:
		NPP_C_bonus_pres += PRESIDENT_INCUMBENCY_BONUS_POPULARITY
	elif pres_party == 5:
		NPP_R_bonus_pres += PRESIDENT_INCUMBENCY_BONUS_POPULARITY
	elif pres_party == 6:
		NPP_FR_bonus_pres += PRESIDENT_INCUMBENCY_BONUS_POPULARITY #step 6
	
	if print_flag:
		print("RD_R_bonus: " + str(RD_R_bonus) + " RD_D_bonus: " + str(RD_D_bonus) + " NPP_L_bonus: " + str(NPP_L_bonus) + " NPP_C_bonus: " + str(NPP_C_bonus) + " NPP_FR_bonus: " + str(NPP_FR_bonus) + " NPP_R_bonus: " + str(NPP_R_bonus))
	
	RD_overall = 0
	NPP_overall = 0
	
	NPP_unity_temp = NPP_unity / MAX_UNITY
	NPP_disunity = 1 - NPP_unity_temp #step 7
	NPP_C_bonus_splitters = NPP_C_bonus_pres
	NPP_FR_bonus_splitters = NPP_FR_bonus_pres #step 8
	NPP_C_bonus_pres *= NPP_unity_temp
	NPP_FR_bonus_pres *= NPP_unity_temp
	NPP_C_bonus_splitters *= NPP_disunity
	NPP_FR_bonus_splitters *= NPP_disunity #step 9
	
	if print_flag:
		print("NPP_unity: " + str(NPP_unity_temp) + " NPP_disunity: " + str(NPP_disunity) + " NPP_C_bonus_splitters: " + str(NPP_C_bonus_splitters) + " NPP_C_bonus: " + str(NPP_C_bonus) + " NPP_FR_bonus: " + str(NPP_FR_bonus) + " NPP_FR_bonus_splitters: " + str(NPP_FR_bonus_splitters))
	
	if NPP_cand > 4:
		RD_overall += NPP_L_bonus_pres
	else:
		NPP_overall += NPP_L_bonus_pres
	if NPP_cand < 5:
		RD_overall += NPP_R_bonus_pres
	else:
		NPP_overall += NPP_R_bonus_pres
	NPP_overall += NPP_C_bonus_pres
	NPP_overall += NPP_FR_bonus_pres
	if NPP_cand != 4:
		RD_overall += NPP_C_bonus_splitters
	if NPP_cand != 6:
		RD_overall += NPP_FR_bonus_splitters
	if SAME_FACTION_UNITY:
		if NPP_cand == 4:
			NPP_overall += NPP_C_bonus_splitters
		if NPP_cand == 6:
			NPP_overall += NPP_FR_bonus_splitters #step 10
	
	if print_flag:
		print("RD_overall: " + str(RD_overall) + " NPP_overall: " + str(NPP_overall))
	
	RD_unity_temp = RD_unity / MAX_UNITY
	RD_disunity = 1 - RD_unity_temp #step 11
	RD_D_bonus_splitters = RD_D_bonus_pres
	RD_R_bonus_splitters = RD_R_bonus_pres #step 12
	RD_D_bonus_pres *= RD_unity_temp
	RD_R_bonus_pres *= RD_unity_temp
	RD_D_bonus_splitters *= RD_disunity
	RD_R_bonus_splitters *= RD_disunity #step 13
	
	if print_flag:
		print("RD_unity: " + str(RD_unity_temp) + " RD_disunity: " + str(RD_disunity) + " RD_R_bonus_splitters: " + str(RD_R_bonus_splitters) + " RD_R_bonus: " + str(RD_R_bonus_pres) + " RD_D_bonus: " + str(RD_D_bonus_pres) + " RD_D_bonus_splitters: " + str(RD_D_bonus_splitters))
	
	if RD_cand == 1 and NPP_cand != 6: #Most of this code is redundant honestly
		RD_overall += (RD_R_bonus_pres + RD_D_bonus_pres)
	elif RD_cand == 2 and NPP_cand != 4:
		RD_overall += (RD_R_bonus_pres + RD_D_bonus_pres)
	elif RD_cand == 1 and NPP_cand == 6:
		RD_overall += (RD_R_bonus_pres + RD_D_bonus_pres)
		NPP_overall += RD_D_bonus_splitters
	elif RD_cand == 2 and NPP_cand == 4:
		RD_overall += (RD_R_bonus_pres + RD_D_bonus_pres)
		NPP_overall += RD_R_bonus_splitters
	if SAME_FACTION_UNITY:
		if RD_cand == 1:
			RD_overall += RD_R_bonus_splitters
		if RD_cand == 2:
			RD_overall += RD_D_bonus_splitters #step 14
	
	RD_overall = round(RD_overall, 3)
	NPP_overall = round(NPP_overall, 3)
	
	if print_flag:
		print("RD_overall: " + str(RD_overall) + " NPP_overall: " + str(NPP_overall))
	
	if RD_overall > NPP_overall:
		result.president = "RD"
	else:
		result.president = "NPP" #step 15
	
	#Begin Senate Election (senator 1)
	
	RD_total = RD_R_bonus + RD_D_bonus
	NPP_total = NPP_L_bonus + NPP_C_bonus + NPP_R_bonus + NPP_FR_bonus #step 1
	
	if print_flag:
		print("RD_total: " + str(RD_total) + " NPP_total: " + str(NPP_total))
	
	RD_R_bonus_sen = RD_R_bonus / RD_total
	RD_D_bonus_sen = RD_D_bonus / RD_total
	NPP_L_bonus_sen = NPP_L_bonus / NPP_total
	NPP_C_bonus_sen = NPP_C_bonus / NPP_total
	NPP_R_bonus_sen = NPP_R_bonus / NPP_total
	NPP_FR_bonus_sen = NPP_FR_bonus / NPP_total #step 2
	
	if print_flag:
		print("RD_R_bonus: " + str(RD_R_bonus_sen) + " RD_D_bonus: " + str(RD_D_bonus_sen) + " NPP_L_bonus: " + str(NPP_L_bonus_sen) + " NPP_C_bonus: " + str(NPP_C_bonus_sen)
		+ " NPP_R_bonus: " + str(NPP_R_bonus_sen) + " NPP_FR_bonus: " + str(NPP_FR_bonus_sen))
	
	RD_R_bonus_primary = RD_R_bonus_sen
	RD_D_bonus_primary = RD_D_bonus_sen
	NPP_L_bonus_primary = NPP_L_bonus_sen
	NPP_C_bonus_primary = NPP_C_bonus_sen
	NPP_R_bonus_primary = NPP_R_bonus_sen
	NPP_FR_bonus_primary = NPP_FR_bonus_sen #step 3
	
	#incumbency bonus
	if senator1 == 1:
		RD_R_bonus_primary += RD_R_pie * 0.002
	elif senator1 == 2:
		RD_D_bonus_primary += RD_D_pie * 0.002
	elif senator1 == 3:
		NPP_L_bonus_primary += NPP_L_pie * 0.002
	elif senator1 == 4:
		NPP_C_bonus_primary += NPP_C_pie * 0.002
	elif senator1 == 5:
		NPP_R_bonus_primary += NPP_R_pie * 0.002
	elif senator1 == 6:
		NPP_FR_bonus_primary += NPP_FR_pie * 0.002 #step 4
	
	#presidential penalty
	if pres_party == 1:
		RD_R_bonus_primary -= 0.1
	elif pres_party == 2:
		RD_D_bonus_primary -= 0.1
	elif pres_party == 3:
		NPP_L_bonus_primary -= 0.1
	elif pres_party == 4:
		NPP_C_bonus_primary -= 0.1
	elif pres_party == 5:
		NPP_R_bonus_primary -= 0.1
	elif pres_party == 6:
		NPP_FR_bonus_primary -= 0.1 #step 5
		
	#opposition bonus
	if senator1 == 1:
		NPP_FR_bonus_primary += 0.05
	elif senator1 == 2:
		NPP_C_bonus_primary += 0.05
	elif senator1 == 3:
		RD_D_bonus_primary += 0.05
	elif senator1 == 4:
		RD_D_bonus_primary += 0.05
	elif senator1 == 5:
		RD_R_bonus_primary += 0.05
	elif senator1 == 6:
		RD_R_bonus_primary += 0.05 #step 6
	
	RD_senate_cand = 2 if RD_D_bonus_primary > RD_R_bonus_primary else 1
	if NPP_L_bonus_primary > NPP_C_bonus_primary and NPP_L_bonus_primary > NPP_FR_bonus_primary and NPP_L_bonus_primary > NPP_R_bonus_primary:
		NPP_senate_cand = 3
	elif NPP_C_bonus_primary > NPP_L_bonus_primary and NPP_C_bonus_primary > NPP_FR_bonus_primary and NPP_C_bonus_primary > NPP_R_bonus_primary:
		NPP_senate_cand = 4
	elif NPP_R_bonus_primary > NPP_L_bonus_primary and NPP_R_bonus_primary > NPP_FR_bonus_primary and NPP_R_bonus_primary > NPP_FR_bonus_primary:
		NPP_senate_cand = 5
	elif NPP_FR_bonus_primary > NPP_L_bonus_primary and NPP_FR_bonus_primary > NPP_FR_bonus_primary and NPP_FR_bonus_primary > NPP_R_bonus_primary:
		NPP_senate_cand = 6
	elif NPP_C_bonus_primary > NPP_FR_bonus_primary:
		NPP_senate_cand = 4
	elif NPP_FR_bonus_primary > NPP_C_bonus_primary:
		NPP_senate_cand = 6
	else:
		NPP_senate_cand = 4 #step 7
	
	if print_flag:
		print("RD_senate_cand: " + str(RD_senate_cand) + "NPP_senate_cand: " + str(NPP_senate_cand))
	
	total_pop = RD + NPP
	RD_percent = RD / total_pop
	NPP_percent = NPP / total_pop #step 8
	
	if print_flag:
		print("total_pop: " + str(total_pop) + " RD_percent: " + str(RD_percent) + " NPP_percent: " + str(NPP_percent))
	
	RD_R_bonus_sen *= RD_percent
	RD_D_bonus_sen *= RD_percent
	NPP_L_bonus_sen *= NPP_percent
	NPP_C_bonus_sen *= NPP_percent
	NPP_FR_bonus_sen *= NPP_percent
	NPP_R_bonus_sen *= NPP_percent
	
	RD_overall = 0
	NPP_overall = 0
	
	NPP_unity_temp = NPP_unity / MAX_UNITY
	NPP_disunity = 1 - NPP_unity_temp #step 9
	NPP_C_bonus_splitters = NPP_C_bonus
	NPP_FR_bonus_splitters = NPP_FR_bonus #step 10
	NPP_C_bonus_sen *= NPP_unity_temp
	NPP_FR_bonus_sen *= NPP_unity_temp
	NPP_C_bonus_splitters *= NPP_disunity
	NPP_FR_bonus_splitters *= NPP_disunity #step 11
	
	if print_flag:
		print("NPP_unity: " + str(NPP_unity_temp) + " NPP_disunity: " + str(NPP_disunity) + " NPP_C_bonus_splitters: " + str(NPP_C_bonus_splitters) + " NPP_C_bonus: " + str(NPP_C_bonus) + " NPP_FR_bonus: " + str(NPP_FR_bonus) + " NPP_FR_bonus_splitters: " + str(NPP_FR_bonus_splitters))
		
	#incumbency bonus
	if senator1 == 1:
		RD_R_bonus_sen += RD_R_pie * 0.002
	elif senator1 == 2:
		RD_D_bonus_sen += RD_D_pie * 0.002
	elif senator1 == 3:
		NPP_L_bonus_sen += NPP_L_pie * 0.002
	elif senator1 == 4:
		NPP_C_bonus_sen += NPP_C_pie * 0.002
	elif senator1 == 5:
		NPP_R_bonus_sen += NPP_R_pie * 0.002
	elif senator1 == 6:
		NPP_FR_bonus_sen += NPP_FR_pie * 0.002 #step 12
	
	#presidential penalty
	if pres_party == 1:
		RD_R_bonus_sen -= 0.1
	elif pres_party == 2:
		RD_D_bonus_sen -= 0.1
	elif pres_party == 3:
		NPP_L_bonus_sen -= 0.1
	elif pres_party == 4:
		NPP_C_bonus_sen -= 0.1
	elif pres_party == 5:
		NPP_R_bonus_sen -= 0.1
	elif pres_party == 6:
		NPP_FR_bonus_sen -= 0.1 #step 13
		
	#opposition bonus
	if senator1 == 1:
		NPP_FR_bonus_sen += 0.05
	elif senator1 == 2:
		NPP_C_bonus_sen += 0.05
	elif senator1 == 3:
		RD_D_bonus_sen += 0.05
	elif senator1 == 4:
		RD_D_bonus_sen += 0.05
	elif senator1 == 5:
		RD_R_bonus_sen += 0.05
	elif senator1 == 6:
		RD_R_bonus_sen += 0.05 #step 14
	
	if NPP_senate_cand > 4:
		RD_overall += NPP_L_bonus_sen
	else:
		NPP_overall += NPP_L_bonus_sen
	if NPP_senate_cand < 5:
		RD_overall += NPP_R_bonus_sen
	else:
		NPP_overall += NPP_R_bonus_sen
	NPP_overall += NPP_C_bonus_sen
	NPP_overall += NPP_FR_bonus_sen
	if NPP_senate_cand != 4:
		RD_overall += NPP_C_bonus_splitters
	if NPP_senate_cand != 6:
		RD_overall += NPP_FR_bonus_splitters
	if SAME_FACTION_UNITY:
		if NPP_senate_cand == 4:
			NPP_overall += NPP_C_bonus_splitters
		if NPP_senate_cand == 6:
			NPP_overall += NPP_FR_bonus_splitters #step 15
	
	if print_flag:
		print("RD_overall: " + str(RD_overall) + " NPP_overall: " + str(NPP_overall))
	
	RD_unity_temp = RD_unity / MAX_UNITY
	RD_disunity = 1 - RD_unity_temp #step 16
	RD_D_bonus_splitters = RD_D_bonus_sen
	RD_R_bonus_splitters = RD_R_bonus_sen #step 17
	RD_D_bonus_sen *= RD_unity_temp
	RD_R_bonus_sen *= RD_unity_temp
	RD_D_bonus_splitters *= RD_disunity
	RD_R_bonus_splitters *= RD_disunity #step 18
	
	if print_flag:
		print("RD_unity: " + str(RD_unity_temp) + " RD_disunity: " + str(RD_disunity) + " RD_R_bonus_splitters: " + str(RD_R_bonus_splitters) + " RD_R_bonus: " + str(RD_R_bonus) + " RD_D_bonus: " + str(RD_D_bonus) + " RD_D_bonus_splitters: " + str(RD_D_bonus_splitters))
	
	if RD_senate_cand == 1 and NPP_senate_cand != 6: #Most of this code is redundant honestly
		RD_overall += (RD_R_bonus_sen + RD_D_bonus_sen)
	elif RD_senate_cand == 2 and NPP_senate_cand != 4:
		RD_overall += (RD_R_bonus_sen + RD_D_bonus_sen)
	elif RD_senate_cand == 1 and NPP_senate_cand == 6:
		RD_overall += (RD_R_bonus_sen + RD_D_bonus_sen)
		NPP_overall += RD_D_bonus_splitters
	elif RD_senate_cand == 2 and NPP_senate_cand == 4:
		RD_overall += (RD_R_bonus_sen + RD_D_bonus_sen)
		NPP_overall += RD_R_bonus_splitters
	if SAME_FACTION_UNITY:
		if RD_senate_cand == 1:
			RD_overall += RD_R_bonus_splitters
		if RD_senate_cand == 2:
			RD_overall += RD_D_bonus_splitters #step 19
	
	RD_overall = round(RD_overall, 3)
	NPP_overall = round(NPP_overall, 3)
	
	if RD_overall > NPP_overall:
		result.senator1 = RD_senate_cand
	elif NPP_overall > RD_overall:
		result.senator1 = NPP_senate_cand
	else:
		result.senator1 = senator1
	
	#this is literally the worst way i could code this
	#Senate Election (senator 2)
	RD_total = RD_R_bonus + RD_D_bonus
	NPP_total = NPP_L_bonus + NPP_C_bonus + NPP_R_bonus + NPP_FR_bonus #step 1
	
	if print_flag:
		print("RD_total: " + str(RD_total) + " NPP_total: " + str(NPP_total))
	
	RD_R_bonus_sen = RD_R_bonus / RD_total
	RD_D_bonus_sen = RD_D_bonus / RD_total
	NPP_L_bonus_sen = NPP_L_bonus / NPP_total
	NPP_C_bonus_sen = NPP_C_bonus / NPP_total
	NPP_R_bonus_sen = NPP_R_bonus / NPP_total
	NPP_FR_bonus_sen = NPP_FR_bonus / NPP_total #step 2
	
	if print_flag:
		print("RD_R_bonus: " + str(RD_R_bonus_sen) + " RD_D_bonus: " + str(RD_D_bonus_sen) + " NPP_L_bonus: " + str(NPP_L_bonus_sen) + " NPP_C_bonus: " + str(NPP_C_bonus_sen)
		+ " NPP_R_bonus: " + str(NPP_R_bonus_sen) + " NPP_FR_bonus: " + str(NPP_FR_bonus_sen))
	
	RD_R_bonus_primary = RD_R_bonus_sen
	RD_D_bonus_primary = RD_D_bonus_sen
	NPP_L_bonus_primary = NPP_L_bonus_sen
	NPP_C_bonus_primary = NPP_C_bonus_sen
	NPP_R_bonus_primary = NPP_R_bonus_sen
	NPP_FR_bonus_primary = NPP_FR_bonus_sen #step 3
	
	#incumbency bonus
	if senator2 == 1:
		RD_R_bonus_primary += RD_R_pie * 0.002
	elif senator2 == 2:
		RD_D_bonus_primary += RD_D_pie * 0.002
	elif senator2 == 3:
		NPP_L_bonus_primary += NPP_L_pie * 0.002
	elif senator2 == 4:
		NPP_C_bonus_primary += NPP_C_pie * 0.002
	elif senator2 == 5:
		NPP_R_bonus_primary += NPP_R_pie * 0.002
	elif senator2 == 6:
		NPP_FR_bonus_primary += NPP_FR_pie * 0.002 #step 4
	
	#presidential penalty
	if pres_party == 1:
		RD_R_bonus_primary -= 0.1
	elif pres_party == 2:
		RD_D_bonus_primary -= 0.1
	elif pres_party == 3:
		NPP_L_bonus_primary -= 0.1
	elif pres_party == 4:
		NPP_C_bonus_primary -= 0.1
	elif pres_party == 5:
		NPP_R_bonus_primary -= 0.1
	elif pres_party == 6:
		NPP_FR_bonus_primary -= 0.1 #step 5
		
	#opposition bonus
	if senator2 == 1:
		NPP_FR_bonus_primary += 0.05
	elif senator2 == 2:
		NPP_C_bonus_primary += 0.05
	elif senator2 == 3:
		RD_D_bonus_primary += 0.05
	elif senator2 == 4:
		RD_D_bonus_primary += 0.05
	elif senator2 == 5:
		RD_R_bonus_primary += 0.05
	elif senator2 == 6:
		RD_R_bonus_primary += 0.05 #step 6
	
	RD_senate_cand = 2 if RD_D_bonus_primary > RD_R_bonus_primary else 1
	if NPP_L_bonus_primary > NPP_C_bonus_primary and NPP_L_bonus_primary > NPP_FR_bonus_primary and NPP_L_bonus_primary > NPP_R_bonus_primary:
		NPP_senate_cand = 3
	elif NPP_C_bonus_primary > NPP_L_bonus_primary and NPP_C_bonus_primary > NPP_FR_bonus_primary and NPP_C_bonus_primary > NPP_R_bonus_primary:
		NPP_senate_cand = 4
	elif NPP_R_bonus_primary > NPP_L_bonus_primary and NPP_R_bonus_primary > NPP_FR_bonus_primary and NPP_R_bonus_primary > NPP_FR_bonus_primary:
		NPP_senate_cand = 5
	elif NPP_FR_bonus_primary > NPP_L_bonus_primary and NPP_FR_bonus_primary > NPP_FR_bonus_primary and NPP_FR_bonus_primary > NPP_R_bonus_primary:
		NPP_senate_cand = 6
	elif NPP_C_bonus_primary > NPP_FR_bonus_primary:
		NPP_senate_cand = 4
	elif NPP_FR_bonus_primary > NPP_C_bonus_primary:
		NPP_senate_cand = 6
	else:
		NPP_senate_cand = 4 #step 7
	
	if print_flag:
		print("RD_senate_cand: " + str(RD_senate_cand) + "NPP_senate_cand: " + str(NPP_senate_cand))
	
	total_pop = RD + NPP
	RD_percent = RD / total_pop
	NPP_percent = NPP / total_pop #step 8
	
	if print_flag:
		print("total_pop: " + str(total_pop) + " RD_percent: " + str(RD_percent) + " NPP_percent: " + str(NPP_percent))
	
	RD_R_bonus_sen *= RD_percent
	RD_D_bonus_sen *= RD_percent
	NPP_L_bonus_sen *= NPP_percent
	NPP_C_bonus_sen *= NPP_percent
	NPP_FR_bonus_sen *= NPP_percent
	NPP_R_bonus_sen *= NPP_percent
	
	RD_overall = 0
	NPP_overall = 0
	
	NPP_unity_temp = NPP_unity / MAX_UNITY
	NPP_disunity = 1 - NPP_unity_temp #step 9
	NPP_C_bonus_splitters = NPP_C_bonus
	NPP_FR_bonus_splitters = NPP_FR_bonus #step 10
	NPP_C_bonus_sen *= NPP_unity_temp
	NPP_FR_bonus_sen *= NPP_unity_temp
	NPP_C_bonus_splitters *= NPP_disunity
	NPP_FR_bonus_splitters *= NPP_disunity #step 11
	
	if print_flag:
		print("NPP_unity: " + str(NPP_unity_temp) + " NPP_disunity: " + str(NPP_disunity) + " NPP_C_bonus_splitters: " + str(NPP_C_bonus_splitters) + " NPP_C_bonus: " + str(NPP_C_bonus_sen) + " NPP_FR_bonus: " + str(NPP_FR_bonus_sen) + " NPP_FR_bonus_splitters: " + str(NPP_FR_bonus_splitters))
		
	#incumbency bonus
	if senator2 == 1:
		RD_R_bonus_sen += RD_R_pie * 0.002
	elif senator2 == 2:
		RD_D_bonus_sen += RD_D_pie * 0.002
	elif senator2 == 3:
		NPP_L_bonus_sen += NPP_L_pie * 0.002
	elif senator2 == 4:
		NPP_C_bonus_sen += NPP_C_pie * 0.002
	elif senator2 == 5:
		NPP_R_bonus_sen += NPP_R_pie * 0.002
	elif senator2 == 6:
		NPP_FR_bonus_sen += NPP_FR_pie * 0.002 #step 12
	
	#presidential penalty
	if pres_party == 1:
		RD_R_bonus_sen -= 0.1
	elif pres_party == 2:
		RD_D_bonus_sen -= 0.1
	elif pres_party == 3:
		NPP_L_bonus_sen -= 0.1
	elif pres_party == 4:
		NPP_C_bonus_sen -= 0.1
	elif pres_party == 5:
		NPP_R_bonus_sen -= 0.1
	elif pres_party == 6:
		NPP_FR_bonus_sen -= 0.1 #step 13
		
	#opposition bonus
	if senator2 == 1:
		NPP_FR_bonus_sen += 0.05
	elif senator2 == 2:
		NPP_C_bonus_sen += 0.05
	elif senator2 == 3:
		RD_D_bonus_sen += 0.05
	elif senator2 == 4:
		RD_D_bonus_sen += 0.05
	elif senator2 == 5:
		RD_R_bonus_sen += 0.05
	elif senator2 == 6:
		RD_R_bonus_sen += 0.05 #step 14
	
	if NPP_senate_cand > 4:
		RD_overall += NPP_L_bonus_sen
	else:
		NPP_overall += NPP_L_bonus_sen
	if NPP_senate_cand < 5:
		RD_overall += NPP_R_bonus_sen
	else:
		NPP_overall += NPP_R_bonus_sen
	
	NPP_overall += NPP_C_bonus_sen
	NPP_overall += NPP_FR_bonus_sen
	if NPP_senate_cand != 4:
		RD_overall += NPP_C_bonus_splitters
	if NPP_senate_cand != 6:
		RD_overall += NPP_FR_bonus_splitters
	if SAME_FACTION_UNITY:
		if NPP_senate_cand == 4:
			NPP_overall += NPP_C_bonus_splitters
		if NPP_senate_cand == 6:
			NPP_overall += NPP_FR_bonus_splitters #step 15
	
	if print_flag:
		print("RD_overall: " + str(RD_overall) + " NPP_overall: " + str(NPP_overall))
	
	RD_unity_temp = RD_unity / MAX_UNITY
	RD_disunity = 1 - RD_unity_temp #step 16
	RD_D_bonus_splitters = RD_D_bonus_sen
	RD_R_bonus_splitters = RD_R_bonus_sen #step 17
	RD_D_bonus_sen *= RD_unity_temp
	RD_R_bonus_sen *= RD_unity_temp
	RD_D_bonus_splitters *= RD_disunity
	RD_R_bonus_splitters *= RD_disunity #step 18
	
	if print_flag:
		print("RD_unity: " + str(RD_unity_temp) + " RD_disunity: " + str(RD_disunity) + " RD_R_bonus_splitters: " + str(RD_R_bonus_splitters) + " RD_R_bonus: " + str(RD_R_bonus_sen) + " RD_D_bonus: " + str(RD_D_bonus_sen) + " RD_D_bonus_splitters: " + str(RD_D_bonus_splitters))
	
	if RD_senate_cand == 1 and NPP_senate_cand != 6: #Most of this code is redundant honestly
		RD_overall += (RD_R_bonus_sen + RD_D_bonus_sen)
	elif RD_senate_cand == 2 and NPP_senate_cand != 4:
		RD_overall += (RD_R_bonus_sen + RD_D_bonus_sen)
	elif RD_senate_cand == 1 and NPP_senate_cand == 6:
		RD_overall += (RD_R_bonus_sen + RD_D_bonus_sen)
		NPP_overall += RD_D_bonus_splitters
	elif RD_senate_cand == 2 and NPP_senate_cand == 4:
		RD_overall += (RD_R_bonus_sen + RD_D_bonus_sen)
		NPP_overall += RD_R_bonus_splitters
	if SAME_FACTION_UNITY:
		if RD_senate_cand == 1:
			RD_overall += RD_R_bonus_splitters
		if RD_senate_cand == 2:
			RD_overall += RD_D_bonus_splitters #step 19
	
	RD_overall = round(RD_overall, 3)
	NPP_overall = round(NPP_overall, 3)
	
	if RD_overall > NPP_overall:
		result.senator2 = RD_senate_cand
	elif NPP_overall > RD_overall:
		result.senator2 = NPP_senate_cand
	else:
		result.senator2 = senator2
	
	return result
	
	

def sim_election_in_statelist(statelist,elecvotelist,RD_cand,NPP_cand,date,date_num):
	RD_elec_votes = 0
	NPP_elec_votes = 0
	RD_states = []
	NPP_states = []
	begin = startlist[date_num]
	finish = endlist[date_num]
	data2 = list(data[slice(begin,finish)])
	Results.senators = []
	senator_dict = {1: "Republican", 2: "Democratic", 3: "L-NPP", 4: "C-NPP", 5: "R-NPP", 6: "FR-NPP"}
	for row in data2:
		if "RD_pie" in row:
			RD_R_pie = float(row[3])
			RD_D_pie = float(row[4])
			pres_party = int(row[6])
			RD_unity = float(row[8])
		if "NPP_pie" in row:
			NPP_L_pie = float(row[3])
			NPP_C_pie = float(row[4])
			NPP_R_pie = float(row[5])
			NPP_FR_pie = float(row[6])
			NPP_unity = float(row[8])
	for state_num, state in enumerate(statelist):
		for row in data2:
			if state in row:
				if "Bonus" not in row:
					RD_pop = float(row[3])
					NPP_pop = float(row[5])
					senator_1 = int(row[7])
					senator_2 = int(row[9])
				if "Bonus" in row:
					RD_R_bonus = float(row[7])
					RD_D_bonus = float(row[9])
					NPP_L_bonus = float(row[11])
					NPP_C_bonus = float(row[13])
					NPP_FR_bonus = float(row[15])
					NPP_R_bonus = float(row[17])
					#if state == "New Jersey":
					#	winner = sim_election(RD_pop,NPP_pop,RD_R_bonus,RD_D_bonus,NPP_L_bonus,NPP_C_bonus,NPP_R_bonus,NPP_FR_bonus,RD_R_pie,RD_D_pie,NPP_L_pie,NPP_C_pie,NPP_R_pie,NPP_FR_pie,RD_cand,NPP_cand,RD_unity,NPP_unity,pres_party,senator_1,senator_2,True)
					#else:
					winner = sim_election(RD_pop,NPP_pop,RD_R_bonus,RD_D_bonus,NPP_L_bonus,NPP_C_bonus,NPP_R_bonus,NPP_FR_bonus,RD_R_pie,RD_D_pie,NPP_L_pie,NPP_C_pie,NPP_R_pie,NPP_FR_pie,RD_cand,NPP_cand,RD_unity,NPP_unity,pres_party,senator_1,senator_2,False)
					if winner.president == "RD":
						RD_elec_votes += elecvotelist[state_num]
						RD_states.append(state)
					if winner.president == "NPP":
						NPP_elec_votes += elecvotelist[state_num]
						NPP_states.append(state)
					Results.senators.append(winner.senator1)
					Results.senators.append(winner.senator2)
					outputfile.write(state + " elected a " + senator_dict[winner.senator1] + " senator for position 1 and a " + senator_dict[winner.senator2] + " senator for position 2.\n")
	if RD_elec_votes <= NPP_elec_votes:
		Results.winner = "NPP"
		Results.RD_votes = RD_elec_votes
		Results.NPP_votes = NPP_elec_votes
		Results.RD_states = RD_states
		outputfile.write("Winner: " + Results.winner + "\n")
		outputfile.write("RD Electoral Votes: " + str(Results.RD_votes) + "\n")
		outputfile.write("NPP Electoral Votes: " + str(Results.NPP_votes) + "\n")
		return Results
	if RD_elec_votes > NPP_elec_votes:
		Results.winner = "RD"
		Results.RD_votes = RD_elec_votes
		Results.NPP_votes = NPP_elec_votes
		Results.RD_states = RD_states
		outputfile.write("\nWinner: " + Results.winner+"\n")
		outputfile.write("RD Electoral Votes: " + str(Results.RD_votes) + "\n")
		outputfile.write("NPP Electoral Votes: " + str(Results.NPP_votes) + "\n")
		return Results


def sim_election_multiple_times(statelist,elecvotelist,RD_cand,NPP_cand,date,date_num,graphfile):
	RD_wins = 0
	NPP_wins = 0
	total_RD_elec = 0
	total_NPP_elec = 0
	RD_dict = {1: 'Republican', 2: 'Democratic'}
	NPP_dict = {3: 'Left-NPP', 4: 'Center-NPP', 5: 'Yockey', 6: 'Far Right-NPP'}
	RD_cand_name = RD_dict[RD_cand]
	NPP_cand_name = NPP_dict[NPP_cand]
	RD_state_wins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	senator_count = [0, 0, 0, 0, 0, 0]
	outputfile.write("\n\nA {0} candidate vs. a {1} candidate\n\n".format(RD_cand_name, NPP_cand_name))
	senator_string = ""
	for _ in range(1):
		result = sim_election_in_statelist(statelist, elecvotelist, RD_cand, NPP_cand, date, date_num)
		if result.winner == "RD":
			RD_wins += 1
		if result.winner == "NPP":
			NPP_wins += 1
		total_RD_elec += result.RD_votes
		total_NPP_elec += result.NPP_votes
		for state in result.RD_states:
			for state_num, state2 in enumerate(statelist):
				if state == state2:
					RD_state_wins[state_num] += 1
		for senator in result.senators:
			senator_count[senator - 1] += 1
			senator_string += str(senator)
	RD_dict = {1: 'Republican', 2: 'Democratic'}
	NPP_dict = {3: 'Left-NPP', 4: 'Center-NPP', 5: 'Yockey', 6: 'Far Right-NPP'}
	RD_cand_name = RD_dict[RD_cand]
	NPP_cand_name = NPP_dict[NPP_cand]
	RD_percent = 100 * (RD_wins)
	NPP_percent = 100 * (NPP_wins)
	for state_num, state in enumerate(statelist):
		if state != "Hawaii":
			if RD_state_wins[state_num] == 1:
				outputfile.write("\n{0} was won by the RDs".format(state))
			else:
				outputfile.write("\n{0} was won by the NPP".format(state))
		if state == "Hawaii":
			outputfile.write("\nThe rightful American territory of Hawaii is in the hands of the Japanese for now, meaning no elections can be held there")
	outputfile.write("\nThe {0} candidate won {2} times with {4} electoral votes, and the {1} candidate won {3} times with {5} electoral votes\n".format(RD_cand_name, NPP_cand_name, RD_wins, NPP_wins, total_RD_elec, total_NPP_elec))
	outputfile.write("The Senate contains {0} Republican(s), {1} Democrat(s), {2} L-NPP, {3} C-NPP, {4} Yockeys, and {5} FR-NPP\n".format(senator_count[0], senator_count[1], senator_count[2], senator_count[3], senator_count[4], senator_count[5]))
	graphfile.write("{0},{1},{2},{3},{4},{5},{7},{8},{9},{10},{11},{12},{13},\"{6}\"\n".format(RD_percent, NPP_percent, total_RD_elec, total_NPP_elec, RD_cand, NPP_cand, date, senator_count[0], senator_count[1], senator_count[2], senator_count[3], senator_count[4], senator_count[5], senator_string))
	
def sim_election_multiple_parties_dates(statelist,elecvotelist,datelist):
	dataall_file_path = os.path.realpath(dataall_file)
	dataall_file_path_folder = dataall_file_path[:dataall_file_path.rfind("\\")]
	graphfile = open(dataall_file_path_folder+"\\"+graphcsv_prefix+"graph.csv", "a", errors="ignore")
	start_time = timeit.default_timer()
	outputfile.write("\nSimulating elections from data file at "+dataall_file)
	for date_num, date in enumerate(datelist):
		outputfile.write("\n\n"+date+"\n\n")
		sim_election_multiple_times(statelist,elecvotelist,1,4,date,date_num,graphfile) #Rep vs. C-NPP
		sim_election_multiple_times(statelist,elecvotelist,1,6,date,date_num,graphfile) #Rep vs. FR-NPP
		sim_election_multiple_times(statelist,elecvotelist,2,4,date,date_num,graphfile) #Dem vs. C-NPP
		sim_election_multiple_times(statelist,elecvotelist,2,6,date,date_num,graphfile) #Dem vs. FR-NPP
	end_time = timeit.default_timer()
	elapsed_time = round(1000*(end_time-start_time))
	print("Election simulations completed in {} ms".format(elapsed_time))
	outputfile.write("\nSimulating elections from data file at " + dataall_file + " in " + str(elapsed_time) + " ms")

def get_date_list(dataall_file):
	dates = []
	with open(dataall_file,newline='') as datafile2:
		data2 = csv.reader(datafile2, delimiter=",")
		for row_num, row in enumerate(data2):
			if row[0] not in dates:
				dates.append(row[0])
				startlist.append(row_num)
				if len(dates) > 1:
					endlist.append(row_num)
		endlist.append(endlist[-1] + (endlist[-1] - endlist[-2]))
	return dates

def make_graph_normal(graphcsv_file, path):
	dates = []
	dates2 = []
	RD_evs_RC = []
	RD_evs_RF = []
	RD_evs_DC = []
	RD_evs_DF = []
	NPP_evs_RC = []
	NPP_evs_RF = []
	NPP_evs_DC = []
	NPP_evs_DF = []
	RD_R_senators = []
	RD_D_senators = []
	NPP_L_senators = []
	NPP_C_senators = []
	NPP_R_senators = []
	NPP_FR_senators = []
	
	start_time = timeit.default_timer()
	outputfile.write("\nGenerating graph from data file at "+graphcsv_file)
	with open(graphcsv_file,newline='') as datafile2:
		data0 = csv.reader(datafile2, delimiter=",")
		for row in data0:
			if int(row[4]) == 1 and int(row[5]) == 4:
				RD_evs_RC.append(float(row[2]))
				NPP_evs_RC.append(float(row[3]))
			if int(row[4]) == 1 and int(row[5]) == 6:
				RD_evs_RF.append(float(row[2]))
				NPP_evs_RF.append(float(row[3]))
			if int(row[4]) == 2 and int(row[5]) == 4:
				RD_evs_DC.append(float(row[2]))
				NPP_evs_DC.append(float(row[3]))
			if int(row[4]) == 2 and int(row[5]) == 6:
				RD_evs_DF.append(float(row[2]))
				NPP_evs_DF.append(float(row[3]))
			if row[13] not in dates:
				dates.append(row[13])
			if int(row[4]) == 1 and int(row[5]) == 4: #only want one presidential pairing since it's irrelevant to the senate (coattails effect maybe? but also please no)
				RD_R_senators.append(int(row[6]))
				RD_D_senators.append(int(row[7]))
				NPP_L_senators.append(int(row[8]))
				NPP_C_senators.append(int(row[9]))
				NPP_R_senators.append(int(row[10]))
				NPP_FR_senators.append(int(row[11]))
	
	for date_num, date in enumerate(dates):
		date1 = date.split(sep=", ")[1]
		day = date1.split(sep=" ")[0]
		month0 = date1.split(sep=" ")[1]
		year = date.split(sep=", ")[2]
		monthdict = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
		month = monthdict[month0]
		dates2.append(datetime.date(int(year),month,int(day)))
	
	trace_ev_rc_rd = graph.Scatter(
		x = dates2,
		y = RD_evs_RC,
		mode = "lines",
		visible=True,
		name = "RD (Rep v. C-NPP) Electoral Votes"
	)
	trace_ev_rc_npp = graph.Scatter(
		x = dates2,
		y = NPP_evs_RC,
		mode = "lines",
		visible=True,
		name = "NPP (Rep v. C-NPP) Electoral Votes"
	)
	
	trace_ev_rf_rd = graph.Scatter(
		x = dates2,
		y = RD_evs_RF,
		mode = "lines",
		visible=True,
		name = "RD (Rep v. FR-NPP) Electoral Votes"
	)
	trace_ev_rf_npp = graph.Scatter(
		x = dates2,
		y = NPP_evs_RF,
		mode = "lines",
		visible=True,
		name = "NPP (Rep v. FR-NPP) Electoral Votes"
	)
	
	trace_ev_dc_rd = graph.Scatter(
		x = dates2,
		y = RD_evs_DC,
		mode = "lines",
		visible=True,
		name = "RD (Dem v. C-NPP) Electoral Votes"
	)
	trace_ev_dc_npp = graph.Scatter(
		x = dates2,
		y = NPP_evs_DC,
		mode = "lines",
		visible=True,
		name = "NPP (Dem v. C-NPP) Electoral Votes"
	)
	
	trace_ev_df_rd = graph.Scatter(
		x = dates2,
		y = RD_evs_DF,
		mode = "lines",
		visible=True,
		name = "RD (Dem v. FR-NPP) Electoral Votes"
	)
	trace_ev_df_npp = graph.Scatter(
		x = dates2,
		y = NPP_evs_DF,
		mode = "lines",
		visible=True,
		name = "NPP (Dem v. FR-NPP) Electoral Votes"
	)
	
	trace_senators_rd_r = graph.Scatter(
		x = dates2,
		y = RD_R_senators,
		mode = "lines",
		visible=True,
		name = "Republican't Senators"
	)
	trace_senators_rd_d = graph.Scatter(
		x = dates2,
		y = RD_D_senators,
		mode = "lines",
		visible=True,
		name = "DemoKKKratic Senators"
	)
	trace_senators_npp_l = graph.Scatter(
		x = dates2,
		y = NPP_L_senators,
		mode = "lines",
		visible=True,
		name = "Commie Senators"
	)
	trace_senators_npp_c = graph.Scatter(
		x = dates2,
		y = NPP_C_senators,
		mode = "lines",
		visible=True,
		name = "Pinko Senators"
	)
	trace_senators_npp_r = graph.Scatter(
		x = dates2,
		y = NPP_R_senators,
		mode = "lines",
		visible=True,
		name = "Nazi Senators"
	)
	trace_senators_npp_fr = graph.Scatter(
		x = dates2,
		y = NPP_FR_senators,
		mode = "lines",
		visible=True,
		name = "Racist Senators"
	)
	evs_line = graph.Scatter(
		x = dates2,
		y = [268 for _ in dates2],
		mode = "lines",
		visible = True,
		name = "EVs to Win",
		line = dict(
			color = "#000000"
		)
	)
	
	updatemenus=list([
		dict(
			buttons=list([ 
				dict(
					args=[{"visible": [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]}],
					label='All Graphs',
					method='update'
				),
				dict(
					args=[{"visible": [True,True,False,False,False,False,False,False,False,False,False,False,False,False,True]}],
					label='Rep vs. C-NPP Electoral Votes',
					method='update'
				),
				dict(
					args=[{"visible": [False,False,True,True,False,False,False,False,False,False,False,False,False,False,True]}],
					label='Rep vs. FR-NPP Electoral Votes',
					method='update'
				),
				dict(
					args=[{"visible": [False,False,False,False,True,True,False,False,False,False,False,False,False,False,True]}],
					label='Dem vs. C-NPP Electoral Votes',
					method='update'
				),
				dict(
					args=[{"visible": [False,False,False,False,False,False,True,True,False,False,False,False,False,False,True]}],
					label='Dem vs. FR-NPP Electoral Votes',
					method='update'
				),
				dict(
					args=[{"visible": [False,False,False,False,False,False,False,False,True,True,True,True,True,True,False]}],
					label='Senators',
					method='update'
				)
			]),
			direction = 'down',
			pad = {'r': 10, 't': 10},
			showactive = True,
			x = 0.1,
			xanchor = 'left',
			y = 1.1,
			yanchor = 'top' 
		),
	])
	
	layout = dict(updatemenus=updatemenus)
	
	
	layout['updatemenus'] = updatemenus
	
	data = [trace_ev_rc_rd, trace_ev_rc_npp, trace_ev_rf_rd, trace_ev_rf_npp, trace_ev_dc_rd, trace_ev_dc_npp, trace_ev_df_rd, trace_ev_df_npp,
	trace_senators_rd_r, trace_senators_rd_d, trace_senators_npp_l, trace_senators_npp_c, trace_senators_npp_r, trace_senators_npp_fr, evs_line]
	fig = dict(data=data, layout=layout)
	#fig.add_shape(
	#	dict(
	#		type = "line",
	#		x0 = 0,
	#		x1 = 1,
	#		y0 = 268,
	#		y1 = 268
	#	)
	#)
	plotly.offline.plot(fig, filename = (path + "\\" + graph_filename + ".html"))
	end_time = timeit.default_timer()
	elapsed_time = round(1000*(end_time-start_time))
	print("Graph file creation completed in {} ms".format(elapsed_time))
	outputfile.write("\nCreated graph from data file at "+graphcsv_file+" in "+str(elapsed_time)+" ms")
	
def get_fig(senators, dates):
	full_data = []
	dates2 = []
	locations = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
	senator_dict = {1: "Republican", 2: "Democratic", 3: "L-NPP", 4: "C-NPP", 5: "R-NPP", 6: "FR-NPP"}
	
	for date_num, date in enumerate(dates):
		date1 = date.split(sep=", ")[1]
		day = date1.split(sep=" ")[0]
		month0 = date1.split(sep=" ")[1]
		year = date.split(sep=", ")[2]
		monthdict = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
		month = monthdict[month0]
		dates2.append(datetime.date(int(year),month,int(day)))
	
		full_data.append(dict(
			type = "choropleth",
			locations = locations,
			z = senators[date_num],
			locationmode = 'USA-states',
			colorscale = [[0, "#d63a3a"], [0.2, "#14148c"], [0.4, "#780f14"], [0.6, "#ed8282"], [0.8, "#915609"], [1.0, "#828282"]],
			colorbar_title = "Senator",
		))
		
	
	
	steps = [] # https://amaral.northwestern.edu/blog/step-step-how-plot-map-slider-represent-time-evolu

	for i in range(len(dates2)):
		step = dict(method = 'restyle',
					args = ['visible', [False] * len(dates2)],
					label = str(dates2[i]))
		step['args'][1][i] = True
		steps.append(step)
	
	sliders = [dict(active=0, pad={"t": 1}, steps=steps)]
	
	updatemenus=list([
		dict(
			buttons=list([ 
				dict(
					args=[{"visible": [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]}],
					label='Senator 1',
					method='update'
				),
				dict(
					args=[{"visible": [True,True,False,False,False,False,False,False,False,False,False,False,False,False,True]}],
					label='Senator 2',
					method='update'
				),
			]),
			direction = 'down',
			pad = {'r': 10, 't': 10},
			showactive = True,
			x = 0.1,
			xanchor = 'left',
			y = 1.1,
			yanchor = 'top' 
		),
	])
	layout = dict(
		title_text = 'Senator 1',
		geo_scope='usa',
		sliders = sliders,
	)
	fig = dict(
		data = full_data,
		layout = layout,
	)
	return fig
	
def make_graph_senate(graphcsv_file, path):
	dates = []
	senators = []
	senators2 = []
	locations = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
	
	start_time = timeit.default_timer()
	outputfile.write("\nGenerating senate graph from data file at "+graphcsv_file)
	with open(graphcsv_file,newline='') as datafile2:
		data0 = csv.reader(datafile2, delimiter=",")
		for row in data0:
			if int(row[4]) == 1 and int(row[5]) == 4: #only want one presidential pairing since it's irrelevant to the senate
				senators.append(int(row[12]))
			if row[13] not in dates:
				dates.append(row[13])
	
	senators_seat1 = [[int(str(senate)[2 * i]) for i in range(len(locations))] for senate in senators]
	senators_seat1.reverse()
	senators_seat2 = [[int(str(senate)[1 + (2 * i)]) for i in range(len(locations))] for senate in senators]
	senators_seat2.reverse()
	
	fig1 = get_fig(senators_seat1, dates)
	plotly.offline.plot(fig1, filename = (path + "\\" + graph_filename + "_1.html"))
	fig2 = get_fig(senators_seat1, dates)
	plotly.offline.plot(fig2, filename = (path + "\\" + graph_filename + "_2.html"))
	end_time = timeit.default_timer()
	elapsed_time = round(1000*(end_time-start_time))
	print("Graph file creation completed in {} ms".format(elapsed_time))
	outputfile.write("\nCreated senate graph from data file at " + graphcsv_file + " in " + str(elapsed_time) + " ms")


root = tkinter.Tk()
root.iconbitmap(this_path_folder+"\eagle.ico")
root.geometry("500x700")
root.title("TNO US Presidential Election Simulator")
app = SimulatorUI(master=root)
app.mainloop()