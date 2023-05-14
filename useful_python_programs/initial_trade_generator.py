from pathlib import Path

HOIV_documents_folder = Path("../../..")

log_file = open(HOIV_documents_folder.joinpath("logs/game.log"), 'r+', encoding="utf8")

trade_partners = {}
current_tag = "ZZZ"
for line in log_file:
	if "PYTHON_Trade_Partners;" in line:
		current_tag = line.split(";")[1].strip()
		trade_partners[current_tag] = {}
	if "PYTHON_Trade_Opinion;" in line:
		trade_partners[current_tag][line.split(";")[2].strip()] = []
		trade_partners[current_tag][line.split(";")[2].strip()].append(line.split(";")[3].strip())
		trade_partners[current_tag][line.split(";")[2].strip()].append(line.split(";")[4].strip())
		trade_partners[current_tag][line.split(";")[2].strip()].append(line.split(";")[5].strip())
		trade_partners[current_tag][line.split(";")[2].strip()].append(line.split(";")[6].strip())

script_file = open(HOIV_documents_folder.joinpath("mod/git-days-of-europe/common/scripted_effects"
												  "/TNO_trade_tedium_scripted_effects.txt"), 'w+', encoding="utf8")

script_file.write('startup_trade_partners = {\n')
for tag in trade_partners:
	script_file.write('\t' + tag + ' = {\n')
	for partner in trade_partners[tag]:
		script_file.write('\t\tadd_to_array = { TNO_trade_partners = ' + partner + ' }\n')
		script_file.write('\t\tset_variable = { trade_opinion@' + partner + ' = ' + trade_partners[tag][partner][0] + ' }\n')
		script_file.write('\t\tset_variable = { trade_opinion_distance@' + partner + ' = ' + trade_partners[tag][partner][1] + ' }\n')
		script_file.write('\t\tset_variable = { trade_opinion_opinion@' + partner + ' = ' + trade_partners[tag][partner][2] + ' }\n')
		if trade_partners[tag][partner][3] != '0':
			script_file.write('\t\tset_variable = { trade_opinion_modifier@' + partner + ' = ' + trade_partners[tag][partner][3] + ' }\n')
	script_file.write('\t}\n')
script_file.write('}\n')
