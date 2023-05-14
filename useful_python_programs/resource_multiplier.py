from pathlib import Path

if not Path("resource_multiplier_results").exists():
    Path("resource_multiplier_results").mkdir()
states = Path("../history/states")
for file in states.iterdir():
    if file.is_file():
        output_state = Path("resource_multiplier_results/" + file.name).open("w+")
        input_state = file.open("r+")

        for line in input_state:
            if "uranium = " in line:
                number = int(line.split(' ')[-1])
                output_state.write("\t\turanium = " + str(number*2) + "\n")
            elif "uranium=" in line:
                number = int(line.split('=')[-1])
                output_state.write("\t\turanium = " + str(number*2) + "\n")
            else:
                output_state.write(line)

        output_state.close()
        input_state.close()
