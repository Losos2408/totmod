import os
import tkinter as tk
import tkinter.filedialog as filedialog
import re
#by Wendell08, makes easier to make scripted effects with multiple variables operations

namespace = ""
startnum = 0
endnum = 0
this_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
class UI(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.temp_vars = False
		self.output_file = ""
		self.pack()
		self.create_widgets()
		self.get_code_text("<Return>")
	def create_widgets(self):
		self.math_label = tk.Label(self)
		self.math_label["font"] = ("Arial", 14)
		self.math_label["text"] = "Input:"
		self.math_label.pack(side="top")
		
		self.math_entry_box = tk.Entry(self)
		self.math_entry_box["font"] = ("Arial", 18)
		self.math_entry_box["width"] = 50
		self.math_entry_box.insert(0, "a = b * c + ( d / e )")
		self.math_entry_box.bind("<Return>",self.get_code_text)
		self.math_entry_box.pack(side="top")

		self.output_label = tk.Label(self)
		self.output_label["font"] = ("Arial", 13)
		self.output_label["text"] = "\nCurrent output file: "+self.output_file+"\n"
		self.output_label["wraplength"] = 550
		self.output_label.pack(side="top")
		
		self.file_select_output = tk.Button(self)
		self.file_select_output["font"] = ("Arial", 14)
		self.file_select_output["text"] = "Select an output file"
		self.file_select_output["command"] = self.output_filedialog_wrapper
		self.file_select_output.pack(side="top")

		self.line_entry = tk.Label(self)
		self.line_entry["font"] = ("Arial", 12)
		self.line_entry["text"] = "Line to Write:"
		self.line_entry.pack(side="top")
		
		self.line_entry_box = tk.Entry(self)
		self.line_entry_box["font"] = ("Arial", 14)
		self.line_entry_box.insert(0, "5")
		self.line_entry_box.pack(side="top")

		self.temp_vars_button = tk.Button(self)
		self.temp_vars_button["font"] = ("Arial", 14)
		self.temp_vars_button["text"] = "Enable Temporary Variables"
		self.temp_vars_button["command"] = self.enable_temp_vars
		self.temp_vars_button.pack(side="top")

		self.run_program = tk.Button(self)
		self.run_program["font"] = ("Arial", 14)
		self.run_program["text"] = "Generate code"
		self.run_program["command"] = self.gen_code
		self.run_program.pack(side="top")
		
		self.guide_text = tk.Label(self)
		self.guide_text["font"] = ("Arial", 12)
		self.guide_text["wraplength"] = 250
		self.guide_text["text"] = '''ACCEPTED COMMANDS:
SPACE: Delimeter for all operations, WILL NOT WORK WITHOUT USING SPACES
ENTER: Refresh code preview
+: Adds to a Variable
-: Subctracts from a Variable
*: Multiply a Variable
/ or \\: Divides a Variable
%; Remainder of a Variable
(2*2): Groups a math operation'''
		self.guide_text["justify"] = "left"
		self.guide_text.pack(side="left")

		self.code_text_label = tk.Label(self)
		self.code_text_label["font"] = ("Arial", 12)
		self.code_text_label["text"] = "\nCODE PREVIEW:\n"
		self.code_text_label["wraplength"] = 450
		self.code_text_label["justify"] = "left"
		self.code_text_label.pack(side="top")

	def enable_temp_vars(self):	
		if self.temp_vars == False:
			self.temp_vars = True
			self.temp_vars_button["text"] = "Disable Temporary Variables"
		elif self.temp_vars == True:
			self.temp_vars = False
			self.temp_vars_button["text"] = "Enable Temporary Variables"
		self.get_code_text("<Return>")
	
	def output_filedialog_wrapper(self):
		self.output_file = filedialog.askopenfilename(initialdir=this_path,title="Select Folder")
		self.output_label["text"] = "\nCurrent output dir: "+self.output_file+"\n"
		self.output_label.pack(side="top")
		
	def get_code_text(self, event):
		temp_var = ""
		if self.temp_vars:
			temp_var = "temp_"
		text_items = []
		parenthesis_math = []
		parenthesis = 0
		code_text = ""
		def generate_code_label(code_list):
			code_output = ""
			for i, item in enumerate(code_list):
				if item == "+":
					code_output += f"add_to_{temp_var}variable = {{ {code_list[0]} = {code_list[i+1]} }}\n"
				if item == "-":
					code_output += f"subtract_from_{temp_var}variable = {{ {code_list[0]} = {code_list[i+1]} }}\n"
				if item == "*":
					code_output += f"multiply_{temp_var}variable = {{ {code_list[0]} = {code_list[i+1]} }}\n"
				if item == "/" or item ==  "\\":
					code_output += f"divide_{temp_var}variable = {{ {code_list[0]} = {code_list[i+1]} }}\n"
				if item == "%":
					code_output += f"modulo_{temp_var}variable = {{ {code_list[0]} = {code_list[i+1]} }}\n"
				if item == "=":
					code_output += f"set_{temp_var}variable = {{ {code_list[0]} = {code_list[i+1]} }}\n"
			return code_output
		words = self.math_entry_box.get().split(" ")
		for word in words:
			if word == "(":
				parenthesis += 1
				parenthesis_math.append([])
				continue
			elif word == ")":
				print(parenthesis_math)
				parenthesis -= 1
				code_text += generate_code_label(parenthesis_math[parenthesis])
				if parenthesis >= 1:
					parenthesis_math[parenthesis-1].append(parenthesis_math[parenthesis][0])
				else:
					text_items.append(parenthesis_math[parenthesis][0])
				parenthesis_math[parenthesis] = []
				continue
			if parenthesis >= 1:
				parenthesis_math[parenthesis-1].append(word)
				print(parenthesis_math)
			else:
				text_items.append(word)
		code_text += generate_code_label(text_items)
		self.code_text_label["text"] = "\nCODE PREVIEW:\n"+code_text
		print(code_text)
		
	def gen_code(self):
		self.get_code_text("<Return>")
		code_list = self.code_text_label["text"].replace("\nCODE PREVIEW:\n" ,"")
		code_list = code_list.split("\n")
		print(code_list)
		line_num = int(self.line_entry_box.get())-1
		print(self.output_file)
		with open(self.output_file, "r", encoding="utf8") as inp:
			bracket_count = 0
			line_list = inp.readlines()
			print(len(line_list))
			for i, line in enumerate(line_list):
				bracket_count += line.count("{")
				bracket_count -= line.count("}")
				if i == line_num:
					old_text = line_list[line_num]
					line_list[line_num] = ""
					for code in code_list:
						line_list[line_num] += ("\t"*bracket_count)+code+"\n"
					line_list[line_num] += old_text
		with open(self.output_file, "w", encoding="utf8") as out:
			[out.write(line) for line in line_list]

root = tk.Tk()
root.geometry("700x600")
root.title("Variable Math Generator")
app = UI(master=root)
app.mainloop()