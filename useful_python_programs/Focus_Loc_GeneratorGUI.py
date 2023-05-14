#By Wendell08, Writes focuses loc and placeholder descriptions

import tkinter as tk
from tkinter import filedialog, Text
import os

line_loc_list = []
focus_name = ""
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
		self.open_file["text"] = "Open Focus File"
		self.open_file["command"] = self.select_focus_path
		self.open_file.pack(side="top")
		
		self.select_output = tk.Button(self)
		self.select_output["text"] = "Select Output"
		self.select_output["command"] = self.select_output_path
		self.select_output.pack(side="top")

		self.start_focus_label = tk.Label(self)
		self.start_focus_label["text"] = "Start from this Focus"
		self.start_focus_label["wraplength"] = 250
		self.start_focus_label.pack(side="top")

		self.starting_focus_entry = tk.Entry(self)
		self.starting_focus_entry["width"] = 40
		self.starting_focus_entry.pack(side="top")

		self.end_focus_label = tk.Label(self)
		self.end_focus_label["text"] = "Finish to this Focus"
		self.end_focus_label["wraplength"] = 250
		self.end_focus_label.pack(side="top")

		self.final_focus_entry = tk.Entry(self)
		self.final_focus_entry["width"] = 40
		self.final_focus_entry.pack(side="top")

		self.input_label = tk.Label(self)
		self.input_label["text"] = f"\nCurrent Focus File:\n{self.target_file}\n\n"
		self.input_label["wraplength"] = 250
		self.input_label.pack(side="top")

		self.output_label = tk.Label(self)
		self.output_label["text"] = f"\nCurrent Output:\n{self.target_output}\n\n"
		self.output_label["wraplength"] = 250
		self.output_label.pack(side="top")




	def select_focus_path(self):
		self.target_file = filedialog.askopenfilename(initialdir=get_path+r"\common\national_focus")
		self.input_label["text"] = f"\nCurrent Event File:\n{self.target_file}\n\n"

	def select_output_path(self):
		self.target_output = filedialog.askdirectory(initialdir=get_path+r"\useful_python_programs")
		self.output_label["text"] = f"\nCurrent Output:\n{self.target_output}\n\n"

	def run_app(self):
		shared_focus = False
		starting_focus = self.starting_focus_entry.get()
		end_focus = self.final_focus_entry.get()
		starting_focus_found = False
		with open(self.target_file, "r", encoding="utf-8") as inp:
			for line in inp:
				if "shared_focus" in line:
					shared_focus = True
				if not shared_focus == True:
					shared_focus = False
				if starting_focus_found == False:
					if starting_focus in line:
						starting_focus_found = True
					else:
						continue
				if shared_focus == True:
					if "	id = " in line and not "		" in line:
						line_loc_list.append(line[6:-1])
					if end_focus in line:
						break	
				if shared_focus == False:
					if "	id = " in line and not "			" in line and  "		" in line:
						line_loc_list.append(line[7:-1])		
					if end_focus in line:
						break
			with open(f"{self.target_output}\\Focus_l_english.yml", "a+") as out:
				for line in line_loc_list:			
					focus_name = line.replace("_", " ")[4:].title()
					out.write(f"{line}: \"{focus_name}\"\n")
				out.write("\n")
				for line in line_loc_list:
					out.write(f"{line}_desc: \"\"\n")
				out.write("\n")	





root = tk.Tk() 
root.title("Focus Loc Generator")
root.geometry("300x400")
app = App(master=root)
app.mainloop()