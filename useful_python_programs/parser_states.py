import os
from hoi4_parser import parser, find_type, insert_remove_bytes

i = 1773

for filename in os.listdir("../history/states"):
    with open("../history/states/" + filename, "rb+") as file:
        tree = parser.parse(file.read())
    lista = find_type(tree.root_node, 'owner')
    for element in lista:
        if element.next_sibling.next_sibling.text == b'ARG':
            prov_node = find_type(tree.root_node, 'state_provinces')[0]
            provinces = [x.text.decode('utf-8') for x in filter(lambda x: x.type == 'number', prov_node.children)]
            if len(provinces) < 2:
                continue

            insert = [[f"provinces = {{ {provinces[0]} }}".encode('utf8'), prov_node.start_byte]]
            remove = [[prov_node.text, prov_node.start_byte]]
            text = insert_remove_bytes(tree.root_node.text, insert, remove)
            with open("output/" + filename, "wb+") as file:
                file.write(text)

            for province in provinces[1:]:
                new_state_fn = str(i) + '.txt'
                new_state = f"""
state={{
	id={i}
	name="STATE_{i}"
	manpower = 1
	
	state_category = enclave

	history={{
		owner = ARG
		add_core_of = ARG
	}}
	
	provinces={{ {province} }}
}}
"""
                with open("output/" + new_state_fn, "w+", encoding='utf8') as new_state_fl:
                    new_state_fl.write(new_state)
                i += 1


