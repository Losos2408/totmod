from tree_sitter import Language, Parser
import re

Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',

    # Include one or more languages
    [
        'tree-sitter-HoI4',
    ]
)

HOI4_LANGUAGE = Language('build/my-languages.so', 'HoI4')

parser = Parser()
parser.set_language(HOI4_LANGUAGE)


def print_sexp_tree(text: str):
    lines = text.split(" ")
    depth = 0
    for line in lines:
        output = ""
        for i in range(0, depth):
            output += "  "
        for char in line:
            if char == "(":
                depth += 1
            if char == ")":
                depth -= 1
        output += line
        print(output)


def find_type(root_node, type) -> list:
    result = []
    for i_child in root_node.children:
        if i_child.type == type:
            result.append(i_child)
        else:
            result.extend(find_type(i_child, type))
    return result


def find_function(root_node, name):
    for i_child in root_node.children:
        for j_child in i_child.children:
            if j_child.children[0].text.decode("utf-8") == name:
                return j_child


class Idea:
    def __init__(self, name, on_add):
        self.name = name
        self.on_add = on_add


def get_mid_level_ideas(node, ideas):
    if node.type == "mid_level_idea":
        ideas.append(parse_mid_level_ideas(node))
        return
    for child in node.children:
        get_mid_level_ideas(child, ideas)


def parse_mid_level_ideas(node):
    name = node.children[0].text.decode("utf-8")
    on_add_math = []
    for child in node.children[2].children:
        if child.type == "on_add":
            for j_child in child.children[2].children:
                if j_child.type == "variable_math_effect":
                    on_add_math.append([j_child.text, j_child.start_byte])
    return Idea(name, on_add_math)


# The text inserts and text excerpts need to be sorted
def insert_remove_bytes(text, text_inserts=None, text_excerpts=None):
    if text_excerpts is None:
        text_excerpts = []
    if text_inserts is None:
        text_inserts = []

    removal_indexes = []
    for remove in text_excerpts:
        start = remove[1]
        end = remove[1] + len(remove[0])
        removal_indexes.append([start, end])

    for i in range(0, len(removal_indexes)):
        remove = removal_indexes[i]
        diff = remove[1] - remove[0]
        text = text[:remove[0]] + text[remove[1]:]
        for j in range(i + 1, len(removal_indexes)):
            j_remove = removal_indexes[j]
            if remove[0] <= j_remove[0] < remove[1] or remove[0] < j_remove[1] <= remove[1]:
                raise Exception("overlapping removal stuff")
            j_remove[0] -= diff
            j_remove[1] -= diff
        for insert in text_inserts:
            if remove[0] <= insert[1] <= remove[1]:
                insert[1] = remove[0]
            elif remove[1] <= insert[1]:
                insert[1] -= diff

    for i in reversed(range(0, len(text_inserts))):
        insert_text = text_inserts[i][0]
        pos = text_inserts[i][1]
        text = text[:pos] + insert_text + text[pos:]
    return text
