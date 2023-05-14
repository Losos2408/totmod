import os
from argparse import ArgumentParser

intro = '''# Use useful_python_programs/scars_thingy.py for ease of usage.

# TODO: (use CTRL + F to jump between these)
# 1) TITLE
# 2) INITIALS
# 3) DESCRIPTION

################
### 1) TITLE ###
################

defined_text = {
	name = Statelore_Get_Name'''
title_block = '''
	text = {
		trigger = {
			check_variable = { selected_lore = 1 }
		}
		localization_key = state_lore_name.1
	}'''
initial = '''
}

###################
### 2) INITIALS ###
###################

defined_text = {
	name = Statelore_Get_Initials'''
initial_block = '''
	text = {
		trigger = {
			check_variable = { lore_entries_onscreen^sl_i = 1 }
		}
		localization_key = state_lore_initials.1
	}'''
description = '''
}

######################
### 3) DESCRIPTION ###
######################
defined_text = {
	name = Statelore_Get_Desc'''
description_block = '''
	text = {
		trigger = {
			check_variable = { selected_lore = 1 }
		}
		localization_key = state_lore_desc.1
	}'''

end = '''
}
'''

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('number', metavar='number', type=int, help='''The number of blocks you want to do.''')
	args = parser.parse_args()
	number = args.number
	text = intro
	for i in range(1, number+1):
		text += title_block.replace('1', str(i))
	text += initial
	for i in range(1, number+1):
		text += initial_block.replace('1', str(i))
	text += description
	for i in range(1, number+1):
		text += description_block.replace('1', str(i))
	text += end

	output = open(os.path.join('..', 'common', 'scripted_localisation', 'TNO_state_lore_scripted_localisation.txt'), 'w+')
	output.write(text)
