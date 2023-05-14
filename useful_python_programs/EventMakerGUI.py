import os
import tkinter
import tkinter.filedialog as filedialog
import string

#by uncountably

namespace = ""
startnum = 0
endnum = 0
this_path = os.path.realpath(__file__)
last_backslash_ind = this_path.rfind("\\")
this_path_folder = this_path[:last_backslash_ind]
output_folder = this_path_folder

class UI(tkinter.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.run_program = tkinter.Button(self)
		self.run_program["text"] = "Generate events"
		self.run_program["command"] = self.gen_events
		self.run_program.pack(side="top")
		
		self.namespace_label = tkinter.Label(self)
		self.namespace_label["text"] = "Namespace:"
		self.namespace_label.pack(side="top")
		
		self.namespace_entry_box = tkinter.Entry(self)
		self.namespace_entry_box.insert(0, "USA")
		self.namespace_entry_box.pack(side="top")
		
		self.startnum_label = tkinter.Label(self)
		self.startnum_label["text"] = "Start ID:"
		self.startnum_label.pack(side="top")
		
		self.startnum_entry_box = tkinter.Entry(self)
		self.startnum_entry_box.insert(0, "1")
		self.startnum_entry_box.pack(side="top")
		
		self.endnum_label = tkinter.Label(self)
		self.endnum_label["text"] = "End ID:"
		self.endnum_label.pack(side="top")
		
		self.endnum_entry_box = tkinter.Entry(self)
		self.endnum_entry_box.insert(0, "2")
		self.endnum_entry_box.pack(side="top")
		
		self.optionnum_label = tkinter.Label(self)
		self.optionnum_label["text"] = "Number of options:"
		self.optionnum_label.pack(side="top")
		
		self.optionnum_entry_box = tkinter.Entry(self)
		self.optionnum_entry_box.insert(0, "2")
		self.optionnum_entry_box.pack(side="top")
		
		self.filename_label = tkinter.Label(self)
		self.filename_label["text"] = "Filename:"
		self.filename_label.pack(side="top")
		
		self.filename_entry_box = tkinter.Entry(self)
		self.filename_entry_box.insert(0, "events.txt")
		self.filename_entry_box.pack(side="top")
		
		self.output_label = tkinter.Label(self)
		self.output_label["text"] = "Current output dir: "+output_folder
		self.output_label["justify"] = "center"
		self.output_label["wraplength"] = 250
		self.output_label.pack(side="top")
		
		self.file_select_output = tkinter.Button(self)
		self.file_select_output["text"] = "Select an output folder"
		self.file_select_output["command"] = self.output_filedialog_wrapper
		self.file_select_output.pack(side="top")
	
	def output_filedialog_wrapper(self):
		global output_folder
		output_folder = filedialog.askdirectory(initialdir=this_path,title="Select Folder")
		self.output_label["text"] = "Current output dir: "+output_folder
		self.output_label.pack(side="top")
		
	def gen_events(self):
		output = open(os.path.join(output_folder,self.filename_entry_box.get()), "a")
		namespace = self.namespace_entry_box.get()
		startnum = int(self.startnum_entry_box.get())
		endnum = int(self.endnum_entry_box.get())+1
		optioncount = int(self.optionnum_entry_box.get())
		for num in range(startnum, endnum):
			output.write("country_event = { #\n	id = "+namespace+"."+str(num)+"\n	immediate = { log = \"[GetDateText]: [Root.GetName]: event "+namespace+"."+str(num)+"\" }\n	title = "+namespace+"."+str(num)+".t\n	desc = "+namespace+"."+str(num)+".desc\n	#picture = \n	\n	is_triggered_only = yes\n	fire_only_once = yes\n	\n")
			for num2 in range(optioncount):
				option_letter = string.ascii_lowercase[num2]
				output.write("	option = { #\n		name = "+namespace+"."+str(num)+"."+option_letter+"\n		ai_chance = { factor = 1 }\n		\n	}\n")
			output.write("}\n\n")

		
		


root = tkinter.Tk()
root.geometry("300x400")
root.title("Event Maker")
app = UI(master=root)
app.mainloop()