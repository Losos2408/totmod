import re
from hoi4_parser import parser, get_mid_level_ideas, insert_remove_bytes, find_function, print_sexp_tree

ideas_folder = "../common/ideas/"
ideas_files = [
    "TNO_laws_economic.txt",
    "TNO_laws_military.txt",
    "TNO_laws_political.txt",
    "TNO_laws_social.txt"
]


def get_name_math_if_block(scope_node):
    math_list = []
    effct_limit_block = scope_node.children[2]
    name = effct_limit_block.children[1].children[2].children[1].children[2].text
    for child in effct_limit_block.children[2:-1]:
        math_list.append([child.text, child.start_byte])
    return [[name, math_list[0][1]]], math_list


# Here we do the ideas
ideas = list()
for filename in ideas_files:
    with open(ideas_folder + filename, "rb+") as file:
        tree = parser.parse(file.read())

    root_node = tree.root_node
    current_ideas = []
    get_mid_level_ideas(root_node, current_ideas)
    ideas.extend(current_ideas)
    removal = []
    insertion = []
    for idea in current_ideas:
        if len(idea.on_add) == 0:
            continue
        removal.extend(idea.on_add)
        insertion.append([
            b"\t\t\t\t" + idea.name.encode("utf-8") + b"_effect = yes\r\n",
            idea.on_add[0][1]
        ])
    string = insert_remove_bytes(root_node.text, insertion, removal)

    with open("output/" + filename, "wb+") as file:
        file.write(string)

with open("output/TNO_policy_effectiveness_law_data.txt", "w+", encoding="utf-8") as file:
    for idea in ideas:
        file.write(idea.name + "_effect = {\n")
        for effect in idea.on_add:
            file.write("\t" + effect[0].decode("utf-8") + "\n")
        file.write("}\n\n")

# Here we do the parse of the scripted effect files

with open("../common/scripted_effects/TNO_policy_effectiveness_scripted_effects.txt", "rb+") as file:
    tree = parser.parse(file.read())

root_node = tree.root_node

removal = []
insertion = []
function_node = find_function(root_node, "TNO_starting_policy_modifiers_setup")
for child in function_node.children[2].children[1:-1]:
    current_idea = get_name_math_if_block(child)
    insertion.extend(current_idea[0])
    removal.extend(current_idea[1])

for insert in insertion:
    insert[0] = b"\t\t" + insert[0] + b"_effect = yes\r\n"
string = insert_remove_bytes(root_node.text, insertion, removal)
with open("output/TNO_policy_effectiveness_scripted_effects.txt", "wb+") as file:
    file.write(string)
