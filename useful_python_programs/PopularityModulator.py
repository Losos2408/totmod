import csv
import random
import math
import os
import timeit
import datetime

#by uncountably




#States
#D-Dixie
#Y-Yankee
#M-Midwestern
#P-Pacific
#R-Rockies
#B-African-American
#S-Southwestern
#A-All
#State name-that state
#
#Parties
#P-NPP
#S-RDs
#R-Reps
#D-Dems
#C-Center
#L-Left
#F-Far Right
#Y-Yockeys
#
#Operations
#CAM-chained addition-multiplication
#A-Constant addition
#AS-Constant addition-subtraction
#MAS-Random-multiplication addition-subtraction
#M-Random-multiplication addition
#CMA-chained multiplication-addition
#CCMA-Conditional chained multiplication-addition
#P-Pie addition

this_path = os.path.realpath(__file__)
last_backslash_ind = this_path.rfind("\\")
this_path_folder = this_path[:last_backslash_ind]
programsfile = csv.reader(open(os.path.join(this_path_folder,"programs.txt"), "r"))
pie_popularities = [0.41, 0.25, 0.01, 0.15, 0.17, 0.01] #Rep Dem L C FR R, RD NPP Rep Dem L C FR R
popularities = [[0, 2, 0, 0, 0, 0, 0.1, 0], [0.8, 0.2, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0.1, 0], [1, 0, 0.1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0.1, 0, 0, 0, 0], [0.5, 0.5, 0, 0.1, 0, 0, 0.1, 0], [0.5, 0.5, 0, 0, 0, 0, 0, 0], [0.5, 0.6, 0, 0, 0, 0.1, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0.5, 0.5, 0, 0.1, 0, 0, 0.1, 0], [0.5, 0.5, 0, 0.1, 0, 0, 0.1, 0], [1, 0, 0, 0.1, 0, 0, 0, 0], [1, 0, 0, 0.1, 0, 0.1, 0, 0], [1, 0, 0, 0, 0, 0.1, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0.2, 0.8, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0.1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0.1, 0, 0, 0.1, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0.1, 0, 0, 0.1, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1.5, 0, 0, 0.1, 0, 0, 0, 0], [1, 0, 0.1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0.1, 0, 0, 0.1, 0], [1, 0, 0, 0, 0, 0.1, 0, 0], [0.5, 0.5, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]] #RD NPP Rep Dem L C FR R
states_l = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
yankee_states = ["Connecticut", "Delaware", "Maine", "Maryland", "Massachusetts", "New Hampshire", "New Jersey", "New York", "Pennsylvania", "Rhode Island", "Vermont"]
dixie_states = ["Arkansas", "Florida", "Georgia", "Kentucky", "North Carolina", "Oklahoma", "Tennessee", "Virginia", "West Virginia"]
aa_states = ["Alabama", "Louisiana", "Mississippi", "South Carolina"]
midwestern_states = ["Illinois", "Indiana", "Iowa", "Kansas", "Michigan", "Minnesota", "Missouri", "Nebraska", "North Dakota", "Ohio", "South Dakota", "Wisconsin"]
sw_states = ["Arizona", "New Mexico", "Texas"]
rockies_states = ["Colorado", "Idaho", "Montana", "Utah", "Wyoming"]
pacific_states = ["Alaska", "California", "Oregon", "Washington"]
months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
current_date = datetime.date(year=1962,month=1,day=1)
#print(current_date)
#print(current_date.year)
outputfile = open(os.path.join(this_path_folder,"data_all.csv"), "a")

programs = []
program_names = []
for line in programsfile:
	if "#" not in line[0][0]:
		programs.append(line)

for program in programs:
	program_names.append(programs[programs.index(program)][0])

#print(programs)
#print(program_names)
for name in program_names:
	print(name)

def get_state_list(states):
	if states in states_l:
		return [states_l.index(states)]
	elif "A" in states:
		return list(range(0, 49))
	else:
		to_return = []
		if "Y" in states:
			for state in yankee_states:
				to_return.append(states_l.index(state))
		if "D" in states:
			for state in dixie_states:
				to_return.append(states_l.index(state))
		if "B" in states:
			for state in aa_states:
				to_return.append(states_l.index(state))
		if "M" in states:
			for state in midwestern_states:
				to_return.append(states_l.index(state))
		if "S" in states:
			for state in sw_states:
				to_return.append(states_l.index(state))
		if "R" in states:
			for state in rockies_states:
				to_return.append(states_l.index(state))
		if "P" in states:
			for state in pacific_states:
				to_return.append(states_l.index(state))
		return to_return

def get_parties_list(parties):
	to_return = []
	for char in parties:
		if char == "S":
			to_return.append(0)
		if char == "P":
			to_return.append(1)
		if char == "R":
			to_return.append(2)
		if char == "D":
			to_return.append(3)
		if char == "L":
			to_return.append(4)
		if char == "C":
			to_return.append(5)
		if char == "F":
			to_return.append(6)
		if char == "Y":
			to_return.append(7)
	return to_return

def get_parties_list_pie(parties):
	to_return = []
	for char in parties:
		if char == "R":
			to_return.append(0)
		if char == "D":
			to_return.append(1)
		if char == "L":
			to_return.append(2)
		if char == "C":
			to_return.append(3)
		if char == "F":
			to_return.append(4)
		if char == "Y":
			to_return.append(5)
	return to_return

def add_pie_pop(index,pop):
	pops_list = pie_popularities.copy()
	pops_list[index] += float(pop)
	total_pop = sum(pops_list)
	pop_difference = total_pop - 1.00
	changed_pop = pops_list[index]
	pops_list.remove(pops_list[index])
	pop_sum = math.fsum(pops_list)
	#print(pop_sum)
	#print(pop_difference)
	#print(changed_pop)
	pop_val_list = pops_list.copy()
	for num, elem in enumerate(pop_val_list):	
		elem /= pop_sum
		elem *= pop_difference
		pop_val_list[num] = elem
		#print(elem)
	output_list = []
	for num, elem in enumerate(pops_list):
		#print(elem)
		output_list.append(round(elem - pop_val_list[num], 3))
		#elem -= pop_val_list[num]
	output_list.insert(index,changed_pop)
	#print(pops_list)
	#print(pop_val_list)
	#print(output_list)
	for num, elem in enumerate(output_list):
		pie_popularities[num] = elem
	current_sum = sum(pie_popularities)
	if current_sum > 1.000:
		pie_popularities[0] -= (current_sum-1.000)
		pie_popularities[0] = round(pie_popularities[0], 3)
	elif current_sum < 1.000:
		pie_popularities[0] += (1.000-current_sum)
		pie_popularities[0] = round(pie_popularities[0], 3)
	#print(pie_popularities)

def modulate_pops(command):
	components = command.split(",")
	#print(components)
	states = components[0]
	parties = components[1]
	operation = components[2]
	num_1 = components[3]
	#print(num_1)
	if len(components) > 4:
		num_2 = components[4]
	if len(components) > 5:
		num_3 = components[5]
	if operation == "P":
		party_indices = get_parties_list_pie(parties)
	else:
		party_indices = get_parties_list(parties)
	state_indices = get_state_list(states)	
	if operation == "M":
		for index in state_indices:
			randval = random.random()
			#print(randval)
			change = float(randval) * float(num_1)
			for index2 in party_indices:
				popularities[index][index2] += change
				popularities[index][index2] = round(popularities[index][index2], 3)
	if operation == "A":
		for index in state_indices:
			for index2 in party_indices:
				popularities[index][index2] += float(num_1)
				popularities[index][index2] = round(popularities[index][index2], 3)
	if operation == "AS":
		for index in state_indices:
			popularities[index][party_indices[0]] += float(num_1)
			popularities[index][party_indices[0]] = round(popularities[index][party_indices[0]], 3)
			for index2 in party_indices[1:]:
				popularities[index][index2] -= float(num_1)
				popularities[index][index2] = round(popularities[index][index2], 3)
	if operation == "MAS":
		for index in state_indices:
			randval = random.random()
			change = float(randval) * float(num_1)
			popularities[index][party_indices[0]] += float(num_1)
			popularities[index][party_indices[0]] = round(popularities[index][party_indices[0]], 3)
			for index2 in party_indices[1:]:
				popularities[index][index2] -= float(num_1)
				popularities[index][index2] = round(popularities[index][index2], 3)
	if operation == "CAM":
		for index in state_indices:
			randval = random.random()
			change = float(randval) + float(num_1)
			change *= float(num_2)
			popularities[index][party_indices[0]] += change
			popularities[index][party_indices[0]] = round(popularities[index][party_indices[0]], 3)
			change *= float(num_3)
			for index2 in party_indices[1:]:
				popularities[index][index2] += change
				popularities[index][index2] = round(popularities[index][index2], 3)
	if operation == "CMA":
		for index in state_indices:
			randval = random.random()
			change = float(randval) * float(num_1)
			change += float(num_2)
			popularities[index][party_indices[0]] += change
			popularities[index][party_indices[0]] = round(popularities[index][party_indices[0]], 3)
			change *= float(num_3)
			for index2 in party_indices[1:]:
				popularities[index][index2] += change
				popularities[index][index2] = round(popularities[index][index2], 3)
	if operation == "CCMA":
		for index in state_indices:
			if popularities[index][party_indices[0]] > popularities[index][party_indices[1]]:
				randval = random.random()
				change = float(randval) * float(num_1)
				change += float(num_2)
				popularities[index][party_indices[0]] += change
				popularities[index][party_indices[0]] = round(popularities[index][party_indices[0]], 3)
				change *= float(num_3)
				for index2 in party_indices[1:]:
					popularities[index][index2] += change
					popularities[index][index2] = round(popularities[index][index2], 3)
	if operation == "P":
		for index in party_indices:
			add_pie_pop(index,num_1)
	#print(popularities)

def add_time(program):
	global current_date
	#print(program)
	to_add = program.split(",")[1]
	this_timedelta = datetime.timedelta(days=int(to_add))
	current_date += this_timedelta
	output_data()

def run_program(program):
	#print(current_date)
	#print(program)
	start_time = timeit.default_timer()
	if program[1] == "Composite":
		for prgm in program[2:]:
			if "Time" in prgm:
				add_time(prgm)
			else:
				run_program(programs[program_names.index(prgm)])
	else:
		for command in program[1:]:
			#print(command)
			modulate_pops(command)
	end_time = timeit.default_timer()
	elapsed_time = round(1000*(end_time-start_time))
	print("Took {} ms to run program {}".format(elapsed_time,program[0]))
#

#for program in programs:
#	run_program(program)

def output_data():
	outputfile.write("\" 1:00, "+str(current_date.day)+" "+months[current_date.month]+", "+str(current_date.year)+"\",United States of America,RD_pie,"+str(pie_popularities[0])+","+str(pie_popularities[1])+"\n")
	outputfile.write("\" 1:00, "+str(current_date.day)+" "+months[current_date.month]+", "+str(current_date.year)+"\",United States of America,NPP_pie,"+str(pie_popularities[2])+","+str(pie_popularities[3])+str(pie_popularities[4])+","+str(pie_popularities[5])+"\n")
	for num, state in enumerate(states_l):
		outputfile.write("\" 1:00, "+str(current_date.day)+" "+months[current_date.month]+", "+str(current_date.year)+","+state+",RD,"+str(popularities[num][0])+",NPP,"+str(popularities[num][1])+"\n")
	for num, state in enumerate(states_l):
		outputfile.write("\" 1:00, "+str(current_date.day)+" "+months[current_date.month]+", "+str(current_date.year)+","+state+",Bonus,,Popularity,,R,"+str(popularities[num][2])+",D,"+str(popularities[num][3])+",L,"+str(popularities[num][4])+",C,"+str(popularities[num][5])+",F,"+str(popularities[num][6])+",Y,"+str(popularities[num][7])+"\n")

def main_loop():
	to_run = input("Enter the name of a program: ")
	if to_run in program_names:
		run_program(programs[program_names.index(to_run)])
		main_loop()
	elif to_run == "Finish":
		#output data
		print("Finishing and exporting data.")
		output_data()
		print(current_date)
		print(pie_popularities)
		print(popularities)
	else:
		print("Enter a valid program name.")
		main_loop()

main_loop()















