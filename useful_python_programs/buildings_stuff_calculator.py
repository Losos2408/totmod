with open("input/stuff.txt", "r+") as file:
    with open("output/stuff.csv", "w+") as output:
        for line in file:
            output.write(line.split("PYTHON_DEBUG_BUILDINGS;")[1])
