lista = range(101)
lista = map(lambda x: x*0.002, lista)
i = 0
text = """"""
for bonus in lista:
    text += f'''		TNO_ECON_ARMY_IDEA_SPAM_{i} = {{
			research_bonus = {{
				infantry_weapons = {bonus:.3}
				motorized_equipment = {bonus:.3}
				land_doctrine = {bonus:.3}
				support_tech = {bonus:.3}
				special_forces_tech = {bonus:.3}
				armor = {bonus:.3}
				artillery = {bonus:.3}
				air_equipment = {bonus:.3}
				air_doctrine = {bonus:.3}
			}}
			
		}}
'''
    i += 1
text += """	}
}"""
file = open("duodex_trolling.txt","w+",encoding="utf-8")
for line in text:
    file.write(line)

