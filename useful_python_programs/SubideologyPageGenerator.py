# by Flaxbeard, generates an html file to show all subideologies

import shutil
import os
from wand import image

STYLE = '''
<style>
	html {
		background-color: #151817;
		color: #B2C9C2;
		font-family: Aldrich;
		font-size: 18px;
	}
	table {
		border-collapse: collapse;
	}
	td {
		text-align: center;
		padding: 5px;
		border-bottom: 2px solid #73EEE9;
	}
	td:first-child  {
		border-right: 2px dashed #E08282;
	}
	div {
		width: 130px;
		height: 85px;
    	align-items: center;
		justify-content: center;
		display: flex;
	}
	img {
		display: block;
	}
	h4 {
		color: #73EEE9;
		font-size: 16px;
		font-weight: normal;
		padding: 0;
		margin: 0;
		word-wrap: break-word;

		width: 130px;
		height: 70px;
		display: flex;
    	align-items: center;
		justify-content: center;
	}
</style>
'''

GITLAB_PREFIX = 'https://gitlab.com/the-new-order-team/git-days-of-europe/-/raw/toolbox-theory/useful_python_programs/subideology_page/'

get_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

print(get_path)

subideology_gfx_folder = os.path.join(get_path, 'gfx', 'interface', 'ideologies')

ideologies_file = os.path.join(get_path, 'common', 'ideologies', '00_ideologies.txt')
id_loc_file = os.path.join(get_path, 'localisation', 'english', 'TNO_Ideologies_l_english.yml')

out_folder = os.path.join(get_path, 'useful_python_programs', 'subideology_page')
out_page = os.path.join(out_folder, 'page.html')
out_page_wiki = os.path.join(out_folder, 'page_wiki.html')

ideologies = []
subideologies = {}

with open(ideologies_file) as i_file:
	i_file_contents = i_file.read().split('\n')
	
	current_ideology = ''
	for line in i_file_contents:
		if len(line) > 2 and line[0] == '\t' and line[1] != '\t':
			current_ideology = line[1:].split()[0]
			ideologies.append(current_ideology)
			subideologies[current_ideology] = []
		elif current_ideology and len(line) > 3 and line[3:].startswith(current_ideology):
			subideology = line[3:].split()[0]
			subideologies[current_ideology].append(subideology)

loc_mappings = {}
with open(id_loc_file, encoding='utf-8') as l_file:
	l_file_contents = l_file.read().split('\n')[1:]

	for line in l_file_contents:
		colon_idx = line.find(':')
		if colon_idx > 0:
			key = line[:colon_idx]
			
			quote_idx = line.find('"')
			value = line[quote_idx + 1:-1]
			
			loc_mappings[key] = value

if not os.path.isdir(out_folder):
	os.mkdir(out_folder)

out_html = f'<html>{STYLE}<body>\n<table>'

for ideology in ideologies:
	print(loc_mappings[ideology])

	out_html += f'<tr><td align="center"><h4>{loc_mappings[ideology]}</h4><div><img src="{GITLAB_PREFIX}./{ideology}_group.png"/></div></td>'


	icon_path = os.path.join(subideology_gfx_folder, f'{ideology}_group.dds')
	out_icon_path = os.path.join(out_folder, f'{ideology}_group.png')

	icon_exists = os.path.exists(icon_path)
	out_icon_exists = os.path.exists(out_icon_path)

	if icon_exists and not out_icon_exists:
		with image.Image(filename=icon_path) as img:
			img.compression = 'no'
			img.save(filename=out_icon_path)

	for subideology in subideologies[ideology]:
		if subideology[:-8] != ideology:
			locced_name = subideology
			if subideology in loc_mappings:
				locced_name = loc_mappings[subideology]
			else:
				locced_name = locced_name[:-8].replace('_', ' ')

			icon_path = os.path.join(subideology_gfx_folder, f'{subideology}.dds')
			out_icon_path = os.path.join(out_folder, f'{subideology}.png')

			icon_exists = os.path.exists(icon_path)
			out_icon_exists = os.path.exists(out_icon_path)

			if icon_exists and not out_icon_exists:
				with image.Image(filename=icon_path) as img:
					img.compression = 'no'
					img.save(filename=out_icon_path)
			
			icon_img = f'<img src="{GITLAB_PREFIX}./{subideology}.png"/>' if icon_exists else ''

			print(f'\t{subideology} {locced_name} {icon_exists}')

			out_html += f'<td align="center"><h4>{locced_name}</h4><div>{icon_img}</div></td>'


	out_html += f'</tr>'

out_html += '</table>\n</body></html>'

with open(out_page_wiki, 'w') as o_file:
	o_file.write(out_html)

out_html = out_html.replace(' align="center"', '').replace(GITLAB_PREFIX, '')
with open(out_page, 'w') as o_file:
	o_file.write(out_html)


