from hoi4_parser import parser, print_sexp_tree

with open("../common/scripted_effects/TNO_policy_effectiveness_scripted_effects.txt", "rb+") as file:
	tree = parser.parse(file.read())

print_sexp_tree(tree.root_node.sexp())
