import os
from argparse import ArgumentParser

intro ='''### Use useful_python_progres/Mass_EventPic_GFXentry.py
spriteTypes = {'''

entry ='''
	spriteType = {
		name = "GFX_OMO_2022_event_picture_1"
		texturefile = "gfx/event_pictures/Omolon_2022_aprilfools/event_picture_1.dds"
	}'''

outro ='''
}'''

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('number', metavar='number', type=int, help='''Amount of scripted loc entries''')
	args = parser.parse_args()
	number = args.number
	text = intro
	for i in range(1, number+1):
		text += entry.replace('1', str(i))
	text += outro
	output = open(os.path.join('..', 'interface', 'omolon_2022', 'TNO_Omolon_2022_eventpics.gfx'), 'w+')
	output.write(text)
