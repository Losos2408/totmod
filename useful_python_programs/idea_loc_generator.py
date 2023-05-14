lista = range(101)
lista = map(lambda x: x*0.002, lista)
i = 0
text = """"""
for bonus in lista:
    text += f'''TNO_ECON_ARMY_IDEA_SPAM_{i}: "§YArmy§! research spending at [?army_idea_number]%"
'''
    i += 1
text += """	}
}"""
file = open("duodex_trolling_loc.txt","w+",encoding="utf-8")
for line in text:
    file.write(line)

