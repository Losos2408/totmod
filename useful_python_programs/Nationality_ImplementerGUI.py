#Original code By Wendell08, modified for a culture maker by Krumtum

import tkinter as tk
from tkinter import filedialog, Text
import shutil
import os
import re
import sys

get_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

print(get_path)

nationality_scripted_loc = os.path.join(get_path, r"common\scripted_localisation\TNO_culture_scripted_localisation.txt")
nationality_scripted_gui = os.path.join(get_path, r"common\scripted_guis\eoanb_nationality_state.txt")
nationality_gfx = os.path.join(get_path, r"interface\culture_icon.gfx")
nationality_loc_file = os.path.join(get_path, r"localisation\english\nationality_l_english.yml")

class App(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.select_image_file = ""
		with open(nationality_scripted_loc, "r") as inpt:
			event_id = re.compile(r"check_variable = { nationality = ([0-9]+) }")
			lines = inpt.read()
			nationality_ids = event_id.findall(lines)
			self.old_id = int(nationality_ids[-1])
			print(self.old_id)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.run_script = tk.Button(self)
		self.run_script["text"] = "Run Program"
		self.run_script["command"] = self.run_app
		self.run_script.pack(side="top")

		self.entry1text = tk.Label(self)
		self.entry1text["text"] = "Culture Name"
		self.entry1text["wraplength"] = 260
		self.entry1text.pack(side="top")

		self.entry1 = tk.Entry(self)
		self.entry1["width"] = 40
		self.entry1.insert(0, "")
		self.entry1.pack(side="top")

		self.entrynumtext = tk.Label(self)
		self.entrynumtext["text"] = "Nationality ID"
		self.entrynumtext["wraplength"] = 260
		self.entrynumtext.pack(side="top")

		self.entrynum = tk.Entry(self)
		self.entrynum.insert(0, int(self.old_id)+1)
		self.entrynum.pack(side="top")

		self.select_image_button = tk.Button(self)
		self.select_image_button["text"] = "Select Nationality Image\n(.dds)"
		self.select_image_button["command"] = self.select_image_path
		self.select_image_button.pack(side="top")

		self.image_image = tk.Label(self)
		self.image_image["text"] = f"\nCurrent Image File:\n{self.select_image_file}\n"
		self.image_image["wraplength"] = 260
		self.image_image.pack(side="top")

	def select_image_path(self):
		self.select_image_file = filedialog.askopenfilename(initialdir=os.path.join(get_path,r"gfx\interface\ideas\culture"))
		self.image_image["text"] = f"\nCurrent Image File:\n{os.path.split(self.select_image_file)[1]}\n"

	def run_app(self):
		nationality_name = self.entry1.get()
		custom_id = int(self.entrynum.get())

		_, nationality_image = os.path.split(self.select_image_file)

		try:
			shutil.copy(self.select_image_file, os.path.join(get_path, r"gfx\interface\culture"))
		except:
			print("Image file already in Folder")
			pass

		

		with open(nationality_scripted_loc, "r") as inp:
			line_list = inp.readlines()
			for i, line_item in enumerate(line_list):
				if f"check_variable = {{ nationality = {self.old_id} }}" in line_item:
					print(line_item)
					line_list[i+3] += f'''\n	text = {{
		trigger = {{
			check_variable = {{ nationality = {custom_id} }}
		}}
		localization_key = var_nationality.{custom_id}
	}}
'''
			with open(nationality_scripted_loc, "w") as out:
				for line_to_write in line_list:
					out.write(line_to_write)
		#--------------------

		with open(nationality_scripted_gui, "r") as inp:
			line_list = inp.readlines()
			for i, line_item in enumerate(line_list):
				if f"check_variable = {{ nationality = {self.old_id} }}" in line_item:
					print(line_item)
					line_list[i+1] += f'''			culture_{nationality_name}_group_visible = {{
				check_variable = {{ nationality = {custom_id} }}
			}}
'''
			with open(nationality_scripted_gui, "w") as out:
				for line_to_write in line_list:
					out.write(line_to_write)
		#--------------------

		with open(nationality_gfx) as inp:
			line_list = inp.readlines()
			for i, line_item in enumerate(line_list):
				if "NATIONALITY_MAKERGUI" in line_item:
					line_list[i] = f'''	spriteType = {{
		name = "GFX_culture_{custom_id}"
		texturefile = "gfx/interface/culture/{nationality_image}"
	}}
	##USE NATIONALITY_MAKERGUI IN USEFUL PYTHON PROGRAMS TO IMPLEMENT CULTURES##
'''
			with open(nationality_gfx, "w") as out:
				for line_to_write in line_list:
					out.write(line_to_write)

		#--------------------
		#--------------------

		with open(nationality_loc_file, "a+") as out:
			out.write(f'''
  var_nationality.{custom_id}: "{nationality_name.capitalize().replace("_", " ")}"
''')
		self.old_id = custom_id
		print("Finished nationality creation")


root = tk.Tk()
root.geometry("300x640")
root.title("Nationality Maker")
app = App(master=root)
app.mainloop()
