import os
from hoi4_parser import parser

for filename in os.listdir("../history/states"):
    with open("../history/states/" + filename, "rb+") as file:
        tree = parser.parse(file.read())
    if 'ERROR' in tree.root_node.sexp():
        print(filename)
        break