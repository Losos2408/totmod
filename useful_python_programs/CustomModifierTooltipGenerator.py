import os
import re


tno_folders = [
r"C:\Users\DuoDex\Documents\Paradox Interactive\Hearts of Iron IV\mod\git-days-of-europe\common\ideas",
r"C:\Users\DuoDex\Documents\Paradox Interactive\Hearts of Iron IV\mod\git-days-of-europe\common\dynamic_modifiers"
]
cost_list = []
modifier = "misc_income_modifier"

for folder in tno_folders:
	for subdir,dirs,files in os.walk(folder):
		for file in files:
			bracket = 0
			with open(f"{subdir}\\{file}", "r", encoding="utf8") as inp:
				line_list = inp.readlines()
				for i, line in enumerate(line_list):
					if re.match(r"^\s*#", line):
						continue
					if "dynamic_modifiers" in subdir:
						if not "	" in line and "{" in line:
							idea_name = re.sub(r"^\s*", "", line)
							idea_name = re.sub(r"\s*=\s*{.*\s*$", "", idea_name)
						elif modifier in line:
							costs = re.sub(f"^\s*{modifier}\s*=\s*", "", line)
							costs = re.sub(r"\s*$", "", costs)
							cost = f"[?{costs}|3]"
							cost_list.append([idea_name, cost, False])
					else:
						if "		" in line and not "			" in line and "{" in line:
							idea_name = re.sub(r"^\s*", "", line)
							idea_name = re.sub(r"\s*=\s*{.*\s*$", "", idea_name)
						elif modifier in line:
							code_line = f'{modifier} = -?[0-9]*\.?[0-9]*'
							costs = re.findall(code_line, line, flags=re.IGNORECASE)
							cost = costs[0].replace(f"{modifier} = ", "")
							cost_list.append([idea_name, cost, True])

scripted_loc_string = ""
for idea, cost_value, is_idea in cost_list:
	print(idea, cost_value, is_idea)
	if is_idea == True:
		idea_trigger = f"trigger = {{ has_idea = {idea} }}"
	else:
		idea_trigger = f"trigger = {{ has_dynamic_modifier = {{ modifier = {idea} }} }}"
	with open("econ\\income_econ_scripted_loc.txt", "a+", encoding="utf8") as out:
		out.write(f'''defined_text = {{
	name = Get_{idea}IncomeModifierTT
	text = {{
		{idea_trigger}
		localization_key = {idea}_income_modifier_tt
	}}
}}
''')
	scripted_loc_string += f"[Get_{idea}IncomeModifierTT]"
	with open("econ\\income_econ.yml", "a+", encoding="utf8") as out:
		out.write(f'{idea}_income_modifier_tt: "\\n${idea}$§Y{cost_value}B§!"\n')

with open("econ\\income_econ.yml", "a+", encoding="utf8") as output:
	output.write(f'\n\necon_misc_income_modifier_tt: "{scripted_loc_string}"\n')

