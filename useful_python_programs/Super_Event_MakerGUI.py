#By Wendell08, Writes super event code

import tkinter as tk
from tkinter import filedialog, Text
import shutil
import os
import re

get_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

print(get_path)

super_event_ideas = os.path.join(get_path, r"common\ideas\TNO_Super_Events.txt")
super_event_gfx_file = os.path.join(get_path, r"interface\TNO_SG_Super_Event.gfx")
super_event_loc_file = os.path.join(get_path, r"localisation\english\TNO_Super_Events_l_english.yml")
super_event_music_txt = os.path.join(get_path, r"music\TNO_Superevents\TNO_Superevents.txt")
super_event_music_asset = os.path.join(get_path, r"music\TNO_Superevents\TNO_superevents.asset")

class App(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.select_image_file = ""
		self.select_music_file = ""
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.run_script = tk.Button(self)
		self.run_script["text"] = "Run Program"
		self.run_script["command"] = self.run_app
		self.run_script.pack(side="top")

		self.entry1text = tk.Label(self)
		self.entry1text["text"] = "Super Event ID"
		self.entry1text["wraplength"] = 260
		self.entry1text.pack(side="top")

		self.entry1 = tk.Entry(self)
		self.entry1["width"] = 40
		self.entry1.insert(0, "GERMAN_CIVIL_WAR")
		self.entry1.pack(side="top")

		self.select_image_button = tk.Button(self)
		self.select_image_button["text"] = "Select Super Event Image\n(.dds or .tga)"
		self.select_image_button["command"] = self.select_image_path
		self.select_image_button.pack(side="top")

		self.image_image = tk.Label(self)
		self.image_image["text"] = f"\nCurrent Image File:\n{self.select_image_file}\n"
		self.image_image["wraplength"] = 260
		self.image_image.pack(side="top")

		self.select_audio_button = tk.Button(self)
		self.select_audio_button["text"] = "Select Super Event Music(.ogg)"
		self.select_audio_button["command"] = self.select_music_path
		self.select_audio_button.pack(side="top")

		self.music_label = tk.Label(self)
		self.music_label["text"] = f"\nCurrent Music File:\n{self.select_music_file}\n"
		self.music_label["wraplength"] = 260
		self.music_label.pack(side="top")

		self.entry2text = tk.Label(self)
		self.entry2text["text"] = "Super Event Quote"
		self.entry2text["wraplength"] = 260
		#self.entry2text["height"] = 260
		self.entry2text.pack(side="top")

		self.entry2 = tk.Entry(self)
		self.entry2["width"] = 40
		self.entry2.pack(side="top")

		self.entry3text = tk.Label(self)
		self.entry3text["text"] = "Super Event Quote Author"
		self.entry3text["wraplength"] = 260
		self.entry3text.pack(side="top")

		self.entry3 = tk.Entry(self)
		self.entry3["width"] = 40
		self.entry3.pack(side="top")

		self.entry4text = tk.Label(self)
		self.entry4text["text"] = "Super Event Option"
		self.entry4text["wraplength"] = 260
		self.entry4text.pack(side="top")


		self.entry4 = tk.Entry(self)
		self.entry4["width"] = 40
		self.entry4.pack(side="top")

	def select_image_path(self):
		self.select_image_file = filedialog.askopenfilename(initialdir=os.path.join(get_path,r"gfx\superevent_pictures"))
		self.image_image["text"] = f"\nCurrent Image File:\n{os.path.split(self.select_image_file)[1]}\n"

	def select_music_path(self):
		self.select_music_file = filedialog.askopenfilename(initialdir=os.path.join(get_path,r"music\TNO_Superevents"))
		self.music_label["text"] = f"\nCurrent Music File:\n{os.path.split(self.select_music_file)[1]}\n"

	def run_app(self):
		super_event_name = "SE_"+self.entry1.get().upper()
		if re.match(r"^SE_SE_", super_event_name):
			super_event_name = super_event_name.replace("SE_SE_", "SE_")

		super_event_quote = self.entry2.get()
		super_event_author = self.entry3.get()
		super_event_option = self.entry4.get()

		_, super_event_image = os.path.split(self.select_image_file)
		_, super_event_music =  os.path.split(self.select_music_file)
		
		try:
			shutil.copy(self.select_image_file, os.path.join(get_path, r"gfx\superevent_pictures"))
		except:
			print("Image file already in Folder")
			pass
		try:
			shutil.copy(self.select_music_file, os.path.join(get_path, r"music\TNO_Superevents"))
		except:
			print("Music file already in Folder")
			pass

		#--------------------

		with open(super_event_ideas, "r") as inp:
			bracket = 0
			line_list = inp.readlines()
			for i, line_item in enumerate(line_list):
				bracket += line_item.count("{")
				bracket -= line_item.count("}")
				if i > 20 and bracket == 1:
					line_list[i] = f'''		{super_event_name} = {{ }}
		{super_event_name}_D = {{ }}
		{super_event_name}_A = {{ }}
{line_item}'''
			with open(super_event_ideas, "w") as out:
				for line_to_write in line_list:
					out.write(line_to_write)


		#--------------------

		with open(super_event_gfx_file) as inp:
			line_list = inp.readlines()
			for i, line_item in enumerate(line_list):
				if "SUPER_EVENT_MAKER_GUI" in line_item:
					line_list[i] = f'''	spriteType = {{
		name = "GFX_{super_event_name}"
		textureFile = "gfx/superevent_pictures/{super_event_image}"
	}}
	##USE SUPER_EVENT_MAKER_GUI IN USEFUL PYTHON PROGRAMS TO MAKE NEW SUPER EVENTS##
'''
			with open(super_event_gfx_file, "w") as out:
				for line_to_write in line_list:
					out.write(line_to_write)

		#--------------------

		with open(super_event_music_txt, "a+") as out:
			out.write(f'''

music = {{
	song = "TNO_{super_event_name}"
	chance = {{
		modifier = {{ factor = 0 }}
	}}
}}''')

		#--------------------

		with open(super_event_music_asset, "a+") as out:
					out.write(f'''

music = {{
	name = "TNO_{super_event_name}"
	file = "{super_event_music}"
}}''')
		
			#--------------------

		with open(super_event_loc_file, "a+") as out:
			super_event_loc_name = super_event_name.replace("SE_", "").replace("_", " ")
			out.write(f'''{super_event_name}: "{super_event_loc_name}"
{super_event_name}_D: "{super_event_quote}\\n- {super_event_author}"
{super_event_name}_A: "{super_event_option}"
TNO_{super_event_name}: "{super_event_loc_name}"
''')


		print("Finished superevent script execution")

root = tk.Tk()
root.geometry("300x640")
root.title("Super Event Maker")
app = App(master=root)
app.mainloop()
