#Python analyser
#Written by doodger
####

#Imports

import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, Text
import re
import os


loc_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
loc_path = os.path.join(loc_path, r"localisation")
	
class App(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.file_name = ""
		self.line_breaks = False
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.file_select_loc = tk.Button(self)
		self.file_select_loc["text"] = "\nSelect a loc file"
		self.file_select_loc["command"] = self.select_file_path
		self.file_select_loc.pack(side="top")

		self.output_label = tk.Label(self)
		self.output_label["text"] = f"\nCurrent Loc File:\n{self.file_name}\n\n"
		self.output_label["wraplength"] = 250
		self.output_label.pack(side="top")

		self.run_script = tk.Button(self)
		self.run_script["text"] = "Run Program"
		self.run_script["command"] = self.plottingTheGraph
		self.run_script.pack(side="top")

		self.line_break_off = tk.Button(self)
		self.line_break_on = tk.Button(self)
		self.disable_line_breaks()

	def enable_line_breaks(self):	
		self.line_break_on.pack_forget()
		self.line_breaks = True
		self.line_break_off = tk.Button(self)
		self.line_break_off["text"] = "Disable line breaks count"
		self.line_break_off["command"] = self.disable_line_breaks
		self.line_break_off.pack(side="top")

	def disable_line_breaks(self):	
		self.line_break_off.pack_forget()
		self.line_breaks = False
		self.line_break_on = tk.Button(self)
		self.line_break_on["text"] = "Enable line breaks count"
		self.line_break_on["command"] = self.enable_line_breaks
		self.line_break_on.pack(side="top")

	def select_file_path(self):		
		self.file_name = filedialog.askopenfilename(initialdir=loc_path)
		self.output_label["text"] = f"\nCurrent Loc File:\n{self.file_name}\n\n"

	def countingLineLength(self):
		#Opening the file and treating it
		distributionOfLines = []
		print(self.file_name)
		with open(self.file_name, "r", encoding="utf-8") as locFile:
			lines = locFile.readlines()
			for i, line in enumerate(lines):
				line = re.sub(r"^.*:0? ", "", line)
				if self.line_breaks:
					quotation_marks = -(line.count('\\"')) #to not count escape characters
					line_breaks = (50*(line.count('\\n')))-(line.count('\\n')) #counting line breaks
				else:
					quotation_marks = 0
					line_breaks = 0
				char_count = len(line)+quotation_marks+line_breaks
				distributionOfLines.append(char_count)
				print(f"Line {i}: {char_count}") #display most recent line and line length

		distributionOfLines = [lines for lines in distributionOfLines if lines>200] #keeping only lines with more than a 100 characters
		return distributionOfLines
	#Plotting histogram
	def plottingTheGraph(self):
		x = self.countingLineLength()
		_, loc_file = os.path.split(self.file_name)
		plt.figure(1)
		plt.title(f"Distribution of {loc_file} loc size")
		plt.ylabel('Number of locs')
		plt.xlabel('Length of characters')
		axes = plt.gca()
		#axes.set_xlim([200,char_count]) #standard is 200 to 2500
		#axes.set_ylim([0,60]) #standard from 0 to 30
		plt.hist(x, bins = 30, histtype="step", label=loc_file) #plotting histogram
		plt.legend()
		plt.show()

root = tk.Tk()
root.geometry("260x300")
root.title("TNO Localisation Analyser")
app = App(master=root)
app.mainloop()
