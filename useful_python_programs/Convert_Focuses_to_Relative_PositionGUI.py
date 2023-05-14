import tkinter as tk
from tkinter import filedialog, Text
import os
from os import listdir
from os import path
import re

##by Wendell08
##Convert all focuses with normal positions to Relative ones

get_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	
class App(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def select_focus_path(self):		
		global file_names
		global target_file_list
		file_names = ""
		target_file_list = filedialog.askopenfilenames(initialdir=get_path)
		for file in target_file_list:
			file_name = os.path.split(file)
			file_names += str(file_name[-1])+", "
		self.update_display()

	def update_display(self):
		file_string.set(f"Current Focuses Files: {file_names}")
		self.input_text = tk.Label(root, textvariable=file_string, wraplength=200).place(x=58, y=100)

	def create_widgets(self):
		self.run_app = tk.Button(root, text="  Run Program  ", fg="black", command=self.find_and_apply_focuses_values).place(x=95, y=20)
		self.label1_text = tk.Label(root, text="Starting Focus ID to Convert", wraplength=150).place(x=70, y=180)
		self.label1 = tk.Entry(root)
		self.label1.place(x=82, y=210)
		self.label2_text = tk.Label(root, text="Ending Focus ID to Convert", wraplength=170).place(x=73, y=240)
		self.label2 = tk.Entry(root)
		self.label2.place(x=82, y=270)
		self.button_focus = tk.Button(root, text="Open Focus File", fg="black", command=self.select_focus_path).place(x=92, y=50)


	
	def find_and_apply_focuses_values(self):
		starting_focus = self.label1.get()
		ending_focus = self.label2.get()
		if starting_focus == "":
			starting_focus = None
		if ending_focus == "":
			ending_focus = None	
		for filename in target_file_list:
			print(f"Starting converting {filename}")
			with open(filename, "r", encoding="utf8") as inp:
				n = 1	
				m = 2
				bracket_count = 0
				focus_prereq = ""
				focus_id_list = []
				x_list = []
				y_list = []
				focus_prereq_list = []
				found_prerequisite = False
				starting_focus_found = False 
				ending_focus_found = False
				file_line_list = inp.readlines()
				for i, line in enumerate(file_line_list):
					bracket_count += line.count('{')
					bracket_count -= line.count('}')
					if "shared_focus = {" in line:
						n = 0
						m = 1
					elif "focus_tree = {" in line:
						n = 1
						m = 2
					try:
						if starting_focus in line:
							starting_focus_found = True
					except TypeError:
						starting_focus_found = True
						pass		

					if starting_focus_found == False:
						continue

					try:	
						if ending_focus in line:
							ending_focus_found = True
					except TypeError:
						pass

					if ending_focus_found == True and bracket_count == n:
						break

					if "relative_position_id" in line:
						print(f"{filename} already has relative_position_id")
						return

					if re.match("^\s*#", line):
						continue

					if "    " in line:
						line = line.replace("    ","\t")

					if ("\t"*m)+"id = " in line and not "\t\t\t" in line: 
						focus_id_to_add = re.sub("\s*id = ", "", line)
						focus_id_list.append(focus_id_to_add)
						found_prerequisite = False

					if "\tx = " in line and not ("\t"*(m+2)) in line:
						line_list = line[:-1].split(" ")
						x_value = int(line_list[2])
						x_list.append(x_value)

					if "\ty = " in line and not ("\t"*(m+2)) in line:
						line_list = line[:-1].split(" ")
						y_value = int(line_list[2])
						y_list.append(y_value)

					if "prerequisite = {" in line and found_prerequisite == False:
						found_prerequisite = True
						if "focus = " in line:
							focus_prereq = re.sub("\s*prerequisite = {\s*focus = ", "", line)
							focus_prereq = re.sub("}\s*", "", focus_prereq)
							focus_prereq_list.append(focus_prereq.replace(" ","")+"\n")
						else:
							focus_prereq = re.sub("\s*focus = ", "", file_line_list[i+1])
							focus_prereq_list.append(focus_prereq)

					if bracket_count == n and len(focus_id_list) >= 1:
						if found_prerequisite == False:
							focus_prereq_list.append("NO PREREQUISITE")
							found_prerequisite = True
						print(focus_id_to_add,focus_prereq)	
						print(len(focus_id_list))
						print(len(focus_prereq_list))
						print("---")

			print(focus_id_list)			
			print(focus_prereq_list)

			if bracket_count != 0:
				print(f"File has {bracket_count} extra/missing brackets, exiting script")
				return 

						
			with open(filename, "r", encoding="utf8") as inp:
				n = 1	
				m = 2
				focus_index = -1
				file_line_list = inp.readlines()
				bracket_count = 0
				starting_focus_found = False
				ending_focus_found = False
				skip_this_id = False
				for i, line in enumerate(file_line_list):
					bracket_count += line.count('{')
					bracket_count -= line.count('}')
					if "shared_focus = {" in line:
						n = 0
						m = 1
					elif "focus_tree = {" in line:
						n = 1
						m = 2
					try:
						if starting_focus in line:
							starting_focus_found = True
					except TypeError:
						starting_focus_found = True
						pass		

					if starting_focus_found == False:
						continue

					try:	
						if ending_focus in line:
							ending_focus_found = True
					except TypeError:
						pass
					if bracket_count == n:
						skip_this_id = False
						if ending_focus_found == True: 
							print(f"Finished with {filename}")
							break

					if re.match("^\s*#", line):
						continue

					if "    " in line:
						line = line.replace("    ","\t")

					if skip_this_id == False:
						if ("\t"*m)+"id = " in line and not "\t\t\t" in line: 
							focus_index += 1
							if focus_prereq_list[focus_index] == "NO PREREQUISITE":
								skip_this_id = True
								continue
							try:
								prereq_index = focus_id_list.index(focus_prereq_list[focus_index])
							except ValueError:
								skip_this_id = True
								continue
							

						if "\tx = " in line:
							line_list = line[:-1].split(" ")
							x_value = int(line_list[2])
							new_x_value = x_value-x_list[prereq_index]
							file_line_list[i] = re.sub("x = .*", "x = "+str(new_x_value), line)
						if "\ty = " in line:
							line_list = line[:-1].split(" ")
							y_value = int(line_list[2])
							new_y_value = y_value-y_list[prereq_index]
							file_line_list[i] = re.sub("y = .*", "y = "+str(new_y_value), line)+("\t"*bracket_count)+"relative_position_id = "+focus_prereq_list[focus_index]
			
			with open(filename, "w", encoding="utf8") as out:
				for line in file_line_list:
					out.write(line)


root = tk.Tk() 

global file_string
file_string = tk.StringVar()
file_string.set("")

root.geometry("280x330")
root.title("Convert to Relative IDs")
app = App(master=root)
app.mainloop()
