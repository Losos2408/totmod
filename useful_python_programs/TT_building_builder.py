#Made by Jakavel, please ping me if you experience any bugs

STATE_CATEGORIES = dict() #how many slots each type of terrain has
STATE_CATEGORIES["burgundian_mega_farm"] = 0
STATE_CATEGORIES["city"] = 14
STATE_CATEGORIES["enclave"] = 0
STATE_CATEGORIES["large_city"] = 18
STATE_CATEGORIES["large_town"] = 10
STATE_CATEGORIES["megalopolis"] = 25
STATE_CATEGORIES["metropolis"] = 22
STATE_CATEGORIES["pastoral"] = 2
STATE_CATEGORIES["rural"] = 4
STATE_CATEGORIES["small_island"] = 2
STATE_CATEGORIES["tiny_island"] = 0
STATE_CATEGORIES["town"] = 8
STATE_CATEGORIES["wasteland"] = 0

#All buildings that take up a state slot
ALL_BUILDINGS = ["dockyard", "synthetic_refinery", "fuel_silo", "thermoelectric_plant", "nuclear_reactor", "enrichment_plant", "missile_silo", "schools", "offices", "hospitals", "barracks", "prisons"]
import os

def print_both(string):
    """Print in both the console and in the GUI log."""
    print(string)
    log.insert("end", string)

def remove_comment(text):
    """Remove a hoi4 comment from a line of code"""
    removed_comment = ""
    for letter in text:
        if letter != "#":
            removed_comment += letter
        else:
            break
    return removed_comment
        

def get_states(tag, states):
    """Get all the states that TAG owns, how many slots and free slots they have and what buildings they have."""

    #declare some variables
    my_states = []
    total_buildings = dict()
    for building in ALL_BUILDINGS:
        total_buildings[building] = 0
    total_slots = 0
    total_free_slots = 0

    try:
        all_states = os.listdir(states)
    except FileNotFoundError:
        print_both("The file you entered was not found.")
        return (-1, -1)
    for state in all_states:
        #Open every state and check if TAG is it's owner
        f = open(states + "/" + state, "r")
        f_string = f.read()
        f_list = f_string.split("\n")
        if "owner = " + tag in f_string or "owner=" + tag in f_string:
            this_state = dict()
            this_state["name"] = state
            in_buildings = False #wether or not you are in the buildings = {} entry
            brackets = 0 #count brackets so you know when the bulding entry is closed
            #you need to count since naval bases and bunkers have additional brackets
            factor = 1.0 #buildings_max_level_factor
            buildings = 0
            is_core = False #if it's a non-core state it has a -50% free slots modifier
            for line in f_list:
                if "#" in line:
                    line = remove_comment(line)
                line_no_spaces = line.replace(" ", "")
                if "add_core_of=" in line_no_spaces and tag in line:
                    is_core = True
                elif "add_extra_state_shared_building_slots=" in line_no_spaces:
                    #in case slots has not yet been defined
                    try:
                        this_state["slots"]
                    except KeyError:
                        this_state["slots"] = 0
                    #add the amount of slots this effect adds
                    this_state["slots"] += int(line.split("=")[1])
                elif "buildings_max_level_factor=" in line_no_spaces:
                    #get everything right of an =
                    factor = float(line.split("=")[1])
                elif "state_category=" in line_no_spaces:
                    #get how many base slots this state has
                    this_category_diry = line_no_spaces.split("=")[1]
                    this_category = ""
                    #remove all " and tabs and anything else that might pop up
                    for letter in this_category_diry:
                        if letter.isalpha() or letter == "_":
                            this_category += letter
                    if this_category in STATE_CATEGORIES:
                        this_state["slots"] = STATE_CATEGORIES[this_category]
                    else:
                        #This state category was not found
                        print_both(line)
                        print_both("Unknown state category '{}' in state {}".format(this_category, this_state["name"]))
                        this_state["slots"] = 0
                    
                elif "buildings=" in line_no_spaces:
                    #when youÄre in the buildings you check for buildings that fill slots
                    in_buildings = True
                    brackets = 0
                if in_buildings:
                    if "{" in line:
                        brackets += 1
                    if "}" in line:
                        brackets -= 1
                        if brackets == 0:
                            in_buildings = False

                    if line.count("=") == 1: #some lines have 2 = in them, those are bunkers and naval bases, they don't take up slots so they don't matter
                        #remove all tabs and spaces from the line than save everything left of the = into name and everything right into amount
                        name, amount = line_no_spaces.replace("	", "").split("=")
                        if name in ALL_BUILDINGS:
                            #there is a building in this line
                            this_state[name] = int(amount) #set the level of the building in this state to amount
                            buildings += int(amount) #count the total for all buildings
                            total_buildings[name] += int(amount) #count the total for this type of building
            #I use int here because it acts like floor
            #It's better to underestimate the amount of slots so that you don't put too many buildings in one state ( which causes an error )
            #I could check how paradox rounds it but I can't be bothered to sicne I've yet to see a state with buildings_max_level_factor not set to 1
            this_state["slots"] = int(this_state["slots"]*factor) #multipy the amount of slots with buildings_max_level_factor
            if not is_core:
                this_state["slots"] = this_state["slots"] // 2 #-50% slot modifier if it's non core
                #I checked this time and it rounds down
            this_state["free_slots"] = this_state["slots"] - buildings #subtract buldings after the builgins were counted and the factor was appleid
            total_free_slots += this_state["free_slots"]
            total_slots += this_state["slots"]
            my_states.append(this_state)
        f.close()
    #stats is some statistics that are usefull later
    stats = dict()
    stats["total_buildings"] = total_buildings
    stats["total_slots"] = total_slots
    stats["total_free_slots"] = total_free_slots
    return my_states, stats

def build_buildings(state, order, states_file):
    """Change sthe state file so it has the amouns of buildings described in order"""
    f = open(states_file + "/" + state["name"], "r")
    f_list = f.readlines() #save the whole file, writing in python clears the file
    f.close()
    f = open(states_file + "/" + state["name"], "w")
    lines_with_buildings = []
    for i, line in enumerate(f_list):
        #get the current level of buildings so that you don't destroy already existing buildings
        for building in ALL_BUILDINGS[7:]:
            if building in line:
                lines_with_buildings.append(i)
                current_amount = int(remove_comment(line.split("=")[1]))
                #increase for this building by the amount that's already present
                if not building in order:
                    order[building] = 0
                order[building] += current_amount
    
    for i, line in enumerate(f_list):
        #delete all lines with buildings (their amounts were already added to the order so they will be re-added to the file)
        if not i in lines_with_buildings:
            f.write(line)
            if "buildings={" in line.replace(" ", "") and not "buildings_max_level_factor" in line:
                #write the new amounts of buildings right after buildings = {
                for building in order:
                    f.write("\t\t\t" + building + " = " + str(order[building]) + "\n")
    f.close()

def do_everything():
    print_both("The GUI will probably freeze for a couple of seconds.")
    TAG = tag_entry.get()

    #Get the values from the fields, if a field is empty read it as 0
    DESIRED_BUILDINGS = [0 for i in range(12)]

    for i in range(0, 12):
        try:
            if building_entries[i].get() != "":
                int(building_entries[i].get())
        except ValueError:
            print_both("Desired {}: {} ← This isn't an intiger.".format(ALL_BUILDINGS[i], building_entries[i-7].get()))
            return -1
        if building_entries[i].get() == "":
            DESIRED_BUILDINGS[i] = 0
        else:
            DESIRED_BUILDINGS[i] = int(building_entries[i].get())

    STATES = path_entry.get()

    my_states, stats = get_states(TAG, STATES)
    if my_states == -1 and stats == -1:
        return -1 #an error happened in get_states()
    if len(my_states) == 0:
        print_both("{} owns no states.".format(TAG))
        print_both("Either 'TAG:' or 'Path to states file:' are wrong.")
        return -1

    #check if there are enough slots to build all the buildings
    if sum(DESIRED_BUILDINGS) > stats["total_slots"]:
        print("Error: there are more desired buildings than there are free slots in the states of your country.")
        print("You have {} slots but you're trying to fill them with {} buildings.".format(stats["total_slots"], sum(DESIRED_BUILDINGS)))
        import sys
        sys.exit()

    #some statistics I can print at the end
    fun_statistics = dict()
    fun_statistics["schools_before"] = stats["total_buildings"]["schools"]
    fun_statistics["offices_before"] = stats["total_buildings"]["offices"]
    fun_statistics["hospitals_before"] = stats["total_buildings"]["hospitals"]
    fun_statistics["barracks_before"] = stats["total_buildings"]["barracks"]
    fun_statistics["prisons_before"] = stats["total_buildings"]["prisons"]
    fun_statistics["thermoelectric_plant_before"] = stats["total_buildings"]["thermoelectric_plant"]
    fun_statistics["free_slots_before"] = stats["total_free_slots"]
    

    buildings_built = dict()
    buildings_built["schools"] = 0
    buildings_built["offices"] = 0
    buildings_built["hospitals"] = 0
    buildings_built["barracks"] = 0
    buildings_built["prisons"] = 0
    buildings_built["thermoelectric_plant"] = 0

    import random
    #get a list of how many slots are free in each building
    free_slots_weight = [i["free_slots"] for i in my_states]
    #an order is how many buildings need to be built in each state
    #the index of an order corresponds to an index of a state
    orders = [dict() for i in my_states]
    #a list of indexes that random.choices picks from
    states_index = list(range(len(my_states)))
    for i, building in enumerate(ALL_BUILDINGS):
        #how many buildings of this type have to be built
        to_build = DESIRED_BUILDINGS[i] - stats["total_buildings"][building]
        if to_build <= 0:
            continue #Don't bother with deleting buildings
        for i in range(to_build):
            #choose a random state to build in, this is weighed by the amount of free slots
            #so that bigger states are more likely to be picked and so that states wiht no slots aren't picked
            chosen_one = random.choices(states_index, weights=free_slots_weight)[0]

            #increase the order for this building by one
            if not building in orders[chosen_one]:
                orders[chosen_one][building] = 0
            orders[chosen_one][building] += 1

            #update all the data
            free_slots_weight[chosen_one] -= 1
            my_states[chosen_one]["free_slots"] -= 1
            buildings_built[building] += 1
            if not building in my_states[chosen_one]:
                my_states[chosen_one][building] = 0
            my_states[chosen_one][building] += 1
    for i, order in enumerate(orders):
        #fulfill every order
        build_buildings(my_states[i], order, STATES)

    #calculate some more stats
    fun_statistics["schools_after"] = fun_statistics["schools_before"] + buildings_built["schools"]
    fun_statistics["offices_after"] = fun_statistics["offices_before"] + buildings_built["offices"]
    fun_statistics["hospitals_after"] = fun_statistics["hospitals_before"] + buildings_built["hospitals"]
    fun_statistics["barracks_after"] = fun_statistics["barracks_before"] + buildings_built["barracks"]
    fun_statistics["prisons_after"] = fun_statistics["prisons_before"] + buildings_built["prisons"]
    fun_statistics["thermoelectric_plant_after"] = fun_statistics["thermoelectric_plant_before"] + buildings_built["thermoelectric_plant"]
    total_built = 0
    for building in ALL_BUILDINGS[7:]:
        total_built += buildings_built[building]
    total_built += buildings_built["thermoelectric_plant"]
    fun_statistics["free_slots_after"] = fun_statistics["free_slots_before"] - total_built
        

    #print the statistics
    print("╔═╗ ▄ ╔")
    print("║ ║ ║╔╝")
    print("║ ║ ╠╣ ")
    print("║ ║ ║╚╗")
    print("╚═╝ ▀ ╚")
    #the log has thinner spaces
    log.insert("end","╔═╗ ▄    ╔")
    log.insert("end","║    ║ ║╔╝")
    log.insert("end","║    ║ ╠╣ ")
    log.insert("end","║    ║ ║╚╗")
    log.insert("end","╚═╝ ▀    ╚")
    print_both("Some fun statistics:")
    print_both("{} went from having {} schools to {} schools.".format(TAG, fun_statistics["schools_before"], fun_statistics["schools_after"]))
    print_both("{} went from having {} offices to {} offices.".format(TAG, fun_statistics["offices_before"], fun_statistics["offices_after"]))
    print_both("{} went from having {} hospitals to {} hospitals.".format(TAG, fun_statistics["hospitals_before"], fun_statistics["hospitals_after"]))
    print_both("{} went from having {} barracks to {} barracks.".format(TAG, fun_statistics["barracks_before"], fun_statistics["barracks_after"]))
    print_both("{} went from having {} prisons to {} prisons.".format(TAG, fun_statistics["prisons_before"], fun_statistics["prisons_after"]))
    print_both("{} went from having {} thermoelectric plants to {} thermoelectric plants.".format(TAG, fun_statistics["thermoelectric_plant_before"], fun_statistics["thermoelectric_plant_after"]))
    
    print_both("A total of {} buildings were built.".format(total_built))
    print_both("{} went from having {} free slots to having {} free slots.".format(TAG, fun_statistics["free_slots_before"], fun_statistics["free_slots_after"]))
    print_both(" ")
    print_both("Success! ( but still launch the game and check if everything is ok )")
    return 1



#This is GUI code, it does GUI things
from tkinter import *

root = Tk()
root.title("Building Builder")

window = Frame(master=root, padx=20, pady=20)
window.pack()

tag_label = Label(window, text="TAG:")
tag_label.grid(row=0, column=0)
tag_entry = Entry(window, width=4)
tag_entry.grid(row=0, column=1)

path_label = Label(window, text="Path to states file:")
path_label.grid(row=1, column=0)
string_var = StringVar(window, "C:/Users/user/Documents/Paradox Interactive/Hearts of Iron IV/mod/git-days-of-europe/history/states", "DESIRED_BUILDINGS")
path_entry = Entry(window, textvariable=string_var,width=50)
path_entry.grid(row=1, column=1, columnspan=10, padx=5)

log = Listbox(window, width=60, height=20)
log.grid(row=0,rowspan=40, column=12)

building_labels = []
building_entries = []
for i, building in enumerate(ALL_BUILDINGS[0:]):
    building_labels.append(Label(window, text="Desired {}:".format(building)))
    building_labels[-1].grid(row=i+2, column=0)
    building_entries.append(Entry(window, width=3))
    building_entries[-1].grid(row=i+2, column=1)

start = Button(window, command=do_everything, text="Start")
start.grid(row=14, column=0, columnspan=2)

def about():
    from tkinter import messagebox
    messagebox.showinfo('How to use', "1) Enter the tag of your country in the first field.\n2) Enter the path to the states file in the second. If you're using windows you should only have to change the .../user/... part.)\n3)Type the desired number of buildings into the respective slots. This will take into account already constructed buildings. For example if a country has 2 schools and you set the desired schools to 5, only 3 aditional schools will be added. The gui won't destroy buildings so if you start it with all the fields empty it's not going to do anything.")

menubar = Menu(root)
help = Menu(menubar, tearoff=0)  
help.add_command(label="How to use", command=about)  
menubar.add_cascade(label="Help", menu=help)  
root.config(menu=menubar)


if __name__ == "__main__":
    root.mainloop()
