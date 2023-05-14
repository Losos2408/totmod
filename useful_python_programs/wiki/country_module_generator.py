import os
import re
from collections import defaultdict
import yaml

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
history_folder = os.path.join(root_path, "history", "countries")
states_folder = os.path.join(root_path, "history", "states")

localisation_folder = os.path.join(root_path, "localisation")
flag_folder = os.path.join(root_path, "gfx", "flags")
flag_files = os.listdir(flag_folder)

mappings = {}

LOC_REGEX = re.compile('"(.*)"')
def read_mappings(filenames):
    for fn in filenames:
        with open(os.path.join(localisation_folder, fn), encoding="utf-8") as f:
            for line in f.read().split("\n")[1:]:
                if ":" in line:
                    k, v = line.split(":", 1)
                    key = k.strip()
                    value = v[1:].strip()
                    if LOC_REGEX.match(value):
                        value = LOC_REGEX.match(value)[1]

                        mappings[key] = value

def format_details(subtag_details, key):
    out = ""
    for subtag in subtag_details:
        if subtag_details[subtag][key]:
            out += f"            {subtag} = \"{subtag_details[subtag][key]}\",\n"
    return out[:-2]

read_mappings([ "TNO_victory_points_l_english.yml", "TNO_countries_l_english.yml", "TNO_countries_cosmetic_l_english.yml"])


ENTRY = """
    -- {name}
    {tag} = {{
        tag = "{tag}",
        page = "{name}",

        name = {{
            root = "{name}"
        }},

        adjective = {{
{adj}
        }},

        map_name = {{
{map_name}
        }},

        long_name = {{
{long_name}
        }},

        color = {{
{color}
        }},

        flag = {{
{flag}
        }},

        capital = {{
            root = "{capital}"
        }}
    }},

"""

out = "return {\n"

tags = [name.split("-")[0].strip() for name in os.listdir(history_folder)]

tag_subtags = defaultdict(lambda: {}, {
    "WIN": {
        "federated": {"cosmetic_tag": "WIN_federated"},
        "unitary": {"cosmetic_tag": "WIN_unitary"}
    },
})

subtag_colors_file = os.path.join(root_path, "common", "countries", "cosmetic.txt")
with open(subtag_colors_file) as f:
    for line in f.read().split("\n"):
        if len(line) > 4 and line[3] == "_" and line[:3] in tags:
            cosmetic_tag = line.split("=")[0].strip()
            if cosmetic_tag.endswith("_GER"):
                tag_subtags[cosmetic_tag[:3]]["reichskommissariat"] = {"cosmetic_tag": cosmetic_tag}
            elif cosmetic_tag.endswith("_SGR"):
                tag_subtags[cosmetic_tag[:3]]["speer"] = {"cosmetic_tag": cosmetic_tag}
            elif cosmetic_tag.endswith("_USA"):
                tag_subtags[cosmetic_tag[:3]]["ofn"] = {"cosmetic_tag": cosmetic_tag}
            elif cosmetic_tag.endswith("_OFN"):
                tag_subtags[cosmetic_tag[:3]]["ofn"] = {"cosmetic_tag": cosmetic_tag}
            elif cosmetic_tag.endswith("_regional_unifier"):
                tag_subtags[cosmetic_tag[:3]]["regional"] = {"cosmetic_tag": cosmetic_tag}
            elif cosmetic_tag.endswith("_unified"):
                tag_subtags[cosmetic_tag[:3]]["unified"] = {"cosmetic_tag": cosmetic_tag}
            elif cosmetic_tag.endswith("_collapsed") or cosmetic_tag.endswith("_collapse"):
                tag_subtags[cosmetic_tag[:3]]["collapsed"] = {"cosmetic_tag": cosmetic_tag}
            elif cosmetic_tag.endswith("_FFRPuppet"):
                tag_subtags[cosmetic_tag[:3]]["french"] = {"cosmetic_tag": cosmetic_tag}
            else:
                print(cosmetic_tag)

for tag in tags:

    if tag in ("ENG", "ZZZ"):
        pass

    history_file_name = [item for item in os.listdir(history_folder) if item.startswith(tag)][0]

    history_file = os.path.join(history_folder, history_file_name)

    capital = None
    with open(history_file, encoding="utf-8") as f:
        for line in f.read().split("\n"):
            stripped = line.strip()
            if stripped.startswith("capital") or stripped[1:].startswith("capital"):
                capital = stripped.split("=")[1].strip()
                if "#" in capital:
                    capital = capital.split("#")[0].strip()
            if stripped.startswith("ruling_party"):
                ruling_party = stripped.split("=")[1].strip()

    if capital:
        state_file_name = [item for item in os.listdir(states_folder) if item.startswith(capital)]
        if state_file_name:
            state_file_name = state_file_name[0]
            vp_no = ""
            vp_value = 0
            with open(os.path.join(states_folder, state_file_name)) as f:
                next_line = False
                for line in f.read().split("\n"):
                    stripped = line.strip()
                    if next_line:
                        next_line = False
                        vp_number, value = re.split("\s+", stripped)
                        if int(value) > vp_value:
                            vp_no = vp_number
                            vp_value = int(value)

                    if stripped.startswith("victory_points"):
                        if "}" in stripped:
                            vp_number, value = re.split("\s+", stripped.split("{")[1].strip()[:-1].strip())
                            if int(value) > vp_value:
                                vp_no = vp_number
                                vp_value = int(value)
                        else:
                            next_line = True
            capital = mappings.get(f"VICTORY_POINTS_{vp_no}", "missingno")
    
    if not capital:
        capital = "missingno"

    country_name = history_file_name[6:-4]
    country_file_name = country_name.replace(" ", "_")

    localisation_file_names = [item for item in os.listdir(localisation_folder) if item.startswith(f"TNO_{country_file_name}")]
    read_mappings(localisation_file_names)

    if tag == "USA":
        country_name = "United States of America"
    elif tag == "COG":
        country_name = "Zentralafrika"
    elif tag == "ANG":
        country_name = "Südwestafrika"

    subtag_details = {}
    for subtag, info in [("root", {})] + list(tag_subtags[tag].items()):
        is_root = (subtag == "root")

        cosmetic_tag = info.get("cosmetic_tag", tag)
        subtag_ruling = info.get("ruling_party", ruling_party)

        name = mappings.get(f"{cosmetic_tag}_{subtag_ruling}") or mappings.get(cosmetic_tag) or (country_name if is_root else None)
        longname = mappings.get(f"{cosmetic_tag}_{subtag_ruling}_DEF") or mappings.get(f"{cosmetic_tag}_DEF") or name
        adj = mappings.get(f"{cosmetic_tag}_{subtag_ruling}_ADJ") or mappings.get(f"{cosmetic_tag}_ADJ") or ("" if is_root else None)

        name = name.replace('"', '\\"') if name else None
        adj = adj.replace('"', '\\"') if adj else None
        longname = longname.replace('"', '\\"') if longname else None


        flag = f"{cosmetic_tag}_{subtag_ruling}.png" if f"{cosmetic_tag}_{subtag_ruling}.tga" in flag_files else (f"{cosmetic_tag}.png" if (f"{cosmetic_tag}.tga" in flag_files or is_root) else None)

        if tag == "CAN":
            flag = "CAN.png"

        if longname:
            longname = longname[0].upper() + longname[1:]

        colors_file = os.path.join(root_path, "common", "countries", "colors.txt")
        with open(colors_file) as f:
            next_line = False
            for line in f.read().split("\n"):
                if next_line:
                    if "HSV" in line:
                        continue
                    color = line.split("{")[1].split("}")[0].strip()
                    color = tuple([int(c) for c in re.split("\s+", color)])
                    next_line = False
                if line.startswith(tag):
                    next_line = True

        if cosmetic_tag != tag:
            subtag_colors_file = os.path.join(root_path, "common", "countries", "cosmetic.txt")
            with open(subtag_colors_file) as f:
                next_line = False
                for line in f.read().split("\n"):
                    if next_line:
                        if "HSV" in line:
                            continue
                        color = line.split("{")[1].split("}")[0].strip()
                        color = tuple([int(c) for c in re.split("\s+", color)])
                        next_line = False
                    if line.startswith(cosmetic_tag):
                        next_line = True
        
        flag = f"File:Flag_{flag}" if flag else None

        subtag_details[subtag] = {"map_name": name, "long_name": longname, "adj": adj, "flag": flag, "color": "#%02x%02x%02x" % color} 

    out += ENTRY.format(tag=tag, name=country_name, map_name=format_details(subtag_details, "map_name"), long_name=format_details(subtag_details, "long_name"), adj=format_details(subtag_details, "adj"), flag=format_details(subtag_details, "flag"), color=format_details(subtag_details, "color"), capital=capital)

out += """\n    -- England
    ENG = {
        tag = "ENG",
        page = "England",

        name = {
            root = "England",
            united_kingdom = "Britain",
            commonwealth_britain = "Britain"
        },

        adjective = {
            root = "English",
            united_kingdom = "British",
            commonwealth_britain = "British"
        },

        map_name = {
            root = "England",
            communist = "Commonwealth of England",
            socialist = "Commonwealth of England",
            united_kingdom = "United Kingdom",
            commonwealth_britain = "Commonwealth of Britain",
            commonwealth_england = "Commonwealth of England",
            commonwealth_england_and_wales = "Commonwealth of England and Wales",
            MILITARY_COMMAND = "English Military Command",
            england_and_wales = "Kingdom of England and Wales"
        },

        long_name = {
            root = "The Kingdom of England",
            communist = "The Commonwealth of England",
            socialist = "The Commonwealth of England",
            united_kingdom = "The United Kingdom",
            commonwealth_britain = "The Commonwealth of Britain",
            commonwealth_england = "The Commonwealth of England",
            commonwealth_england_and_wales = "The Commonwealth of England and Wales",
            MILITARY_COMMAND = "English Military Command",
            england_and_wales = "Kingdom of England and Wales"
        },

        color = {
            root = "#960000",
            united_kingdom = "#772121",
            commonwealth_britain = "#772121"
        },

        flag = {
            root = "File:Flag_ENG.png",
            communist = "File:Flag_ENG_communist.png",
            united_kingdom = "File:Flag_ENG_united_kingdom.png",
            commonwealth_britain = "File:Flag_ENG_commonwealth_britain.png",
            commonwealth_england = "File:Flag_ENG_commonwealth_england.png",
            commonwealth_england_and_wales = "File:Flag_ENG_commonwealth_england_and_wales.png",
            MILITARY_COMMAND = "File:Flag_ENG_MILITARY_COMMAND.png",
            england_and_wales = "File:Flag_ENG_england_and_wales.png"
        },

        capital = {
            root = "London"
        }
    }
}
"""

with open("out.txt", "w", encoding="utf-8") as f:
    f.write(out)