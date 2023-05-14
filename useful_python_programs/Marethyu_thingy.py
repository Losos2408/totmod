import yaml

from pathlib import Path

state_folder = Path("..", "history", "states")
victory_point_loc = Path("..", "localisation", "english", "TNO_victory_points_l_english.yml")\
	.open('r+', encoding="utf-8-sig")
state_loc = Path("..", "localisation", "english", "state_names_l_english.yml")\
	.open('r+', encoding="utf-8-sig")
output_states = open('Marethyu_states.csv', 'w+', encoding='utf-8')
output = open('Marethyu.csv', 'w+', encoding='utf-8')

vp_names = {}
state_names = {}
state_vps = {}

for line in victory_point_loc:
	if "VICTORY_POINTS_" in line and "VICTORY_POINTS_TOOLTIP" not in line:
		number = line.split(':')[0].split('_')[2]
		if number not in vp_names:
			name = line.split(':')[1].split('#')[0].strip('0').strip('1').strip(' ').strip('\n').strip('\"')
			vp_names[number] = name

for line in state_loc:
	if "STATE_" in line:
		number = line.split(':')[0].split('_')[1]
		if number not in state_names:
			name = line.split(':')[1].split('#')[0].strip('0').strip(' ').strip('\n').strip('\"')
			state_names[number] = name

output_states.write('STATE ID,NAME\n')
for id, name in state_names.items():
	output_states.write(id)
	output_states.write(',')
	output_states.write(name)
	output_states.write('\n')

for file in state_folder.iterdir():
	state_file = file.open('r+', encoding='utf-8')
	state_num = state_file.name.split('\\')[-1].split(' ')[0].split('-')[0]
	state_vps[state_num] = {}
	print(state_num)
	for line in state_file:
		if 'victory_points' in line:
			divided = line.split('#')[0].split(' ')
			vp_num = ''
			if len(divided) > 4:
				vp_num = divided[3]
			else:
				vp_num = next(state_file).split(' ')[0].strip('\t')
			try:
				state_vps[state_num][vp_num] = vp_names[vp_num]
			except KeyError:
				state_vps[state_num][vp_num] = state_names[state_num]

output.write('STATE ID,STATE NAME,VP ID,VP NAME\n')
for state, vps in state_vps.items():
	for vp in vps:
		output.write(state)
		output.write(',')
		output.write(state_names[state])
		output.write(',')
		output.write(vp)
		output.write(',')
		output.write(vps[vp])
		output.write('\n')
