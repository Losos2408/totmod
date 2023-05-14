#By Wendell08, Writes events placeholder loc

import tkinter as tk
from tkinter import filedialog, Text
import os
import re
global target_output
global label_name
global inp_name

line_loc_list = []
get_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class App(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.target_file = ""
		self.target_output = os.path.dirname(os.path.realpath(__file__))
		self.line_breaks = False
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.run_application = tk.Button(self)
		self.run_application["text"] = "  Run Program  "
		self.run_application["command"] = self.run_app
		self.run_application.pack(side="top")

		self.open_file = tk.Button(self)
		self.open_file["text"] = "Open Event File"
		self.open_file["command"] = self.select_event_path
		self.open_file.pack(side="top")
		
		self.select_output = tk.Button(self)
		self.select_output["text"] = "Select Output"
		self.select_output["command"] = self.select_output_path
		self.select_output.pack(side="top")

		self.start_event_label = tk.Label(self)
		self.start_event_label["text"] = "Start from this Event"
		self.start_event_label["wraplength"] = 250
		self.start_event_label.pack(side="top")

		self.starting_event_entry = tk.Entry(self)
		self.starting_event_entry.pack(side="top")

		self.end_event_label = tk.Label(self)
		self.end_event_label["text"] = "Finish to this Event"
		self.end_event_label["wraplength"] = 250
		self.end_event_label.pack(side="top")

		self.final_event_entry = tk.Entry(self)
		self.final_event_entry.pack(side="top")

		self.input_label = tk.Label(self)
		self.input_label["text"] = f"\nCurrent Event File:\n{self.target_file}\n\n"
		self.input_label["wraplength"] = 250
		self.input_label.pack(side="top")

		self.output_label = tk.Label(self)
		self.output_label["text"] = f"\nCurrent Output:\n{self.target_output}\n\n"
		self.output_label["wraplength"] = 250
		self.output_label.pack(side="top")

	def select_event_path(self):
		self.target_file = filedialog.askopenfilename(initialdir=get_path+r"\events")
		self.input_label["text"] = f"\nCurrent Event File:\n{self.target_file}\n\n"

	def select_output_path(self):
		self.target_output = filedialog.askdirectory(initialdir=get_path+r"\useful_python_programs")
		self.output_label["text"] = f"\nCurrent Output:\n{self.target_output}\n\n"

	def run_app(self):
		starting_event = self.starting_event_entry.get()
		end_event = self.final_event_entry.get()
		starting_event_found = False
		bracket_count = 0
		end_event_found = False
		
		def find_text_in_triggered_text(text_line):
			desc_trigger_list = text_line.replace("\t", "").split(" ")
			find_text = desc_trigger_list.index("text")
			line_loc_list.append(desc_trigger_list[find_text+2])

		def append_to_list(text_line):
			out_line = re.sub(r"^.*= ", "", text_line)
			out_line = re.sub(r"#.*$", "", out_line)
			out_line = re.sub(r"\s*$", "", out_line)
			line_loc_list.append(out_line)

		with open(self.target_file, "r", encoding="utf-8") as inp:
			line_list = inp.readlines()
			for i, line in enumerate(line_list):
				n = 0
				if "{" in line:
					bracket_count += 1
				if "}" in line:
					bracket_count -= 1
				if starting_event_found == False:
					if starting_event in line and not "		" in line:
						starting_event_found = True
					else:
						continue
				if "title =" in line and not "		" in line and not "{" in line:
					append_to_list(line)
				if "title = {" in line and not "		" in line:
					if "}" in line:
						find_text_in_triggered_text(line)
						continue
					else:
						while not "text" in line_list[i+n]:
							n += 1
						find_text_in_triggered_text(line_list[i+n])

				if "desc =" in line and not "		" in line and not "{" in line:
					append_to_list(line)
				if "desc = {" in line and not "		" in line:
					if "}" in line:
						find_text_in_triggered_text(line)
					else:
						while not "text" in line_list[i+n]:
							n += 1
						find_text_in_triggered_text(line_list[i+n])

				if "		name =" in line and not "			" in line:
					append_to_list(line)
				if end_event in line and not "		" in line:
					end_event_found = True
				if end_event_found == True and bracket_count == 0:
					break

			print(line_loc_list)

			with open(f"{self.target_output}\Events_l_english.yml", "a+") as out:
				for checkline in line_loc_list:
					if ".t" in checkline:
						out.write("\n")
					out.write(f" {checkline}: \"\"\n")


	

root = tk.Tk() 
root.title("Event Loc Generator")
root.geometry("300x400")
app = App(master=root)
app.mainloop()
