import sys
import os
import timeit

#by uncountably

#I. How to run the game.log Analyzer
#Running the game.log analyzer requires a command prompt/terminal and for you to have Python 3 installed on your computer. To run it, first navigate to the directory containing TNOGamelogAnalyzerMulti.py in the command prompt/terminal with the cd command. Now, type the name of the program (TNOGamelogAnalyzerMulti.py) into the command prompt, followed by the name of the directory containing your game.log files. The program will automatically scan the directory you give it, including all subdirectories, and find all files ending with the string "game.log" and analyze them.
#For example, if the program is stored in the folder C:\Users\uncountably\Documents\python-programs and the game.log files are stored in C:\Users\uncountably\cool-data, you would type
#cd C:\Users\uncountably\Documents\python-programs
#followed by
#TNOGamelogAnalyzerMulti.py C:\Users\uncountably\cool-data
#You will receive output in the command prompt indicating how often each tracked outcome occurred in all your input game.log files.
#II. Adding new data collection
#If you want to add a new outcome to collect data on, you can do that fairly easily by editing the Python file. In this example, we will add data collection for who becomes the leader of Samara. The first step will be to make a list of events, decisions, or focuses that we can use to determine who becomes leader, like so:
#SAM.36- Zykov
#SAM.38- Bunyachenko
#SAM.40- Maltsev
#Now, we need to enter the Python file. At the top, there is a long list of variable declarations, all of which are set to 0. We will add Samara ones in a new block like so:
#sam_zykov = 0
#sam_bunyachenko = 0
#sam_maltsev = 0
#Next, in the function scan_file, there is a list of global declarations. We will add these three variables to this list:
#global sam_zykov
#global sam_bunyachenko
#global sam_maltsev
#After this, there is a short list of string declarations beginning with usa_64 = "". Add 
#sam_leader = ""
#to this. Note that there is only one variable here, in contrast to the three earlier.
#Next, there is a for loop filled with if statements. We will add code here for detecting each Samara outcome and recording it. Each statement contains 2 lines: 1 detecting the outcome using text comparison, and 1 setting the string variable in accordance with the outcome. In our case, the statements will look like
#        if "SAM.36\n" in line:
#            sam_leader = "zykov"
#        if "SAM.38\n" in line:
#            sam_leader = "bunyachenko"
#        if "SAM.40\n" in line:
#            sam_leader = "maltsev"
#Finally, we need to add to the counters that track how many of each outcome we observe. This can be done by scrolling to the bottom of the function and adding three new if statements modeled off of the previous ones.
#    if sam_leader == "zykov":
#        sam_zykov += 1
#    elif sam_leader == "bunyachenko":
#        sam_bunyachenko += 1
#    elif sam_leader == "maltsev":
#        sam_maltsev += 1
#Now all we need to do is add the ability to print our results. At the bottom, add a new print statement to the print_results function. Base it off of the previous ones. The {} with numbers in them are used to display variables in the printed statements, and will display the variables listed in the format() statement in order (the first variable listed in the format() statement will go in the pair with a 0, second in the one with a 1, etc.).
#Now, just test to make sure all your code works.

count = 0

usa_64_bennett = 0
usa_64_johnson = 0
usa_64_wallace = 0
usa_64_kennedy = 0
usa_68_bennett = 0
usa_68_johnson = 0
usa_68_wallace = 0
usa_68_kennedy = 0
usa_68_goldwater = 0
usa_68_glenn = 0
usa_68_smith = 0
usa_68_harrington = 0

ahf_64_bose = 0
ahf_64_sahgal = 0
ahf_64_singh = 0
ahf_67_singh = 0
ahf_67_hazarika = 0
ahf_67_rahman = 0
ahf_67_thackeray = 0
ahf_67_advani = 0
ahf_67_bose = 0
ahf_67_pratap = 0
ahf_67_sahgal = 0
ahf_67_rao = 0
ahf_70_singh = 0
ahf_70_hazarika = 0
ahf_70_rahman = 0
ahf_70_thackeray = 0
ahf_70_advani = 0
ahf_70_bose = 0
ahf_70_pratap = 0
ahf_70_sahgal = 0
ahf_70_rao = 0
ahf_70_bhatt = 0
ahf_70_c_singh = 0

ita_scorza = 0
ita_dem = 0
ita_decol = 0
ita_recol = 0

wi_start = 0
wi_end = 0
wi_longyun_before = 0
wi_longyun_after = 0
wi_china = 0
wi_china_japan = 0
wi_japan = 0

def scan_file(file,filepath):
	global usa_64_bennett
	global usa_64_johnson
	global usa_64_wallace
	global usa_64_kennedy
	global usa_68_bennett
	global usa_68_johnson
	global usa_68_wallace
	global usa_68_kennedy
	global usa_68_goldwater
	global usa_68_glenn
	global usa_68_smith
	global usa_68_harrington
	global ahf_64_bose
	global ahf_64_sahgal
	global ahf_64_singh
	global ahf_67_singh
	global ahf_67_hazarika
	global ahf_67_rahman
	global ahf_67_advani
	global ahf_67_bose
	global ahf_67_pratap
	global ahf_67_sahgal
	global ahf_67_rao
	global ahf_67_thackeray
	global ahf_70_singh
	global ahf_70_hazarika
	global ahf_70_rahman
	global ahf_70_advani
	global ahf_70_bose
	global ahf_70_pratap
	global ahf_70_sahgal
	global ahf_70_rao
	global ahf_70_thackeray
	global ahf_70_bhatt
	global ahf_70_c_singh
	global ita_scorza
	global ita_dem
	global ita_decol
	global ita_recol
	global wi_start
	global wi_end
	global wi_longyun_before
	global wi_longyun_after
	global wi_china
	global wi_china_japan
	global wi_japan
	
	lines = file.readlines()
	
	usa_64 = ""
	usa_68 = ""
	ahf_64 = ""
	ahf_67 = ""
	ahf_70 = ""
	ita_path = ""
	ita_col = ""
	wi_result = ""
	for line_number, line in enumerate(lines):
		if "1964 elections: Bennett" in line:
			usa_64 = "bennett"
		if "1964 elections: Johnson" in line:
			usa_64 = "johnson"
		if "1964 elections: Wallace" in line:
			usa_64 = "wallace"
		if "1964 elections: Kennedy" in line:
			usa_64 = "kennedy"
		if "1968 elections: Bennett" in line:
			usa_68 = "bennett"
		if "1968 elections: Johnson" in line:
			usa_68 = "johnson"
		if "1968 elections: Wallace" in line:
			usa_68 = "wallace"
		if "1968 elections: Kennedy" in line:
			usa_68 = "kennedy"
		if "1968 elections: Goldwater" in line:
			usa_68 = "goldwater"
		if "1968 elections: Glenn" in line:
			usa_68 = "glenn"
		if "1968 elections: Smith" in line:
			usa_68 = "smith"
		if "1968 elections: Harrington" in line:
			usa_68 = "harrington"
		if "BEN_elections.9\n" in line:
			ahf_64 = "bose"
		if "BEN_elections.10\n" in line:
			ahf_64 = "sahgal"
		if "BEN_elections.11\n" in line:
			ahf_64 = "singh"
		if "BEN_elections.19\n" in line:
			ahf_67 = "bose"
		if "BEN_elections.20\n" in line:
			ahf_67 = "sahgal"
		if "BEN_elections.21\n" in line:
			ahf_67 = "pratap"
		if "BEN_elections.22\n" in line:
			ahf_67 = "hazarika"
		if "BEN_elections.23\n" in line:
			ahf_67 = "singh"
		if "BEN_elections.24\n" in line:
			ahf_67 = "advani"
		if "BEN_elections.33\n" in line:
			ahf_67 = "sahgal"
		if "BEN_elections.34\n" in line:
			ahf_67 = "rao"
		if "BEN_elections.35\n" in line:
			ahf_67 = "pratap"
		if "BEN_elections.36\n" in line:
			ahf_67 = "hazarika"
		if "BEN_elections.37\n" in line:
			ahf_67 = "singh"
		if "BEN_elections.46\n" in line:
			ahf_67 = "singh"
		if "BEN_elections.47\n" in line:
			ahf_67 = "pratap"
		if "BEN_elections.48\n" in line:
			ahf_67 = "thackeray"
		if "BEN_elections.49\n" in line:
			ahf_67 = "rahman"
		if "BEN_elections.58\n" in line:
			ahf_70 = "bose"
		if "BEN_elections.59\n" in line:
			ahf_70 = "singh"
		if "BEN_elections.60\n" in line:
			ahf_70 = "sahgal"
		if "BEN_elections.61\n" in line:
			ahf_70 = "pratap"
		if "BEN_elections.62\n" in line:
			ahf_70 = "advani"
		if "BEN_elections.63\n" in line:
			ahf_70 = "rahman"
		if "BEN_elections.72\n" in line:
			ahf_70 = "bhatt"
		if "BEN_elections.73\n" in line:
			ahf_70 = "singh"
		if "BEN_elections.74\n" in line:
			ahf_70 = "sahgal"
		if "BEN_elections.75\n" in line:
			ahf_70 = "pratap"
		if "BEN_elections.76\n" in line:
			ahf_70 = "charan_singh"
		if "BEN_elections.77\n" in line:
			ahf_70 = "rao"
		if "vc.19\n" in line:
			ita_path = "ciano"
		if "vc.20\n" in line:
			ita_path = "scorza"
		if "impurita.1\n" in line:
			ita_col = "decol"
		if "impurita.2\n" in line:
			ita_col = "recol"
		if "Western Insurrection started in" in line:
			wi_start = line
		if "winner/loser: ROOT: National Protection Army" in line:
			wi_end = line
		if "yun.133\n" in line:
			wi_result = "longyun_before"
		if "yun.128\n" in line:
			wi_result = "longyun_after"
		if "chi.6033\n" in line:
			wi_result = "china"
		if "chi.6036\n" in line:
			wi_result = "china_japan"
		if "japchiinteraction.4\n" in line:
			wi_result = "japan"
	if usa_64 == "bennett":
		usa_64_bennett += 1
	elif usa_64 == "johnson":
		usa_64_johnson += 1
	elif usa_64 == "wallace":
		usa_64_wallace += 1
	elif usa_64 == "kennedy":
		usa_64_kennedy += 1
	if usa_68 == "bennett":
		usa_68_bennett += 1
	elif usa_68 == "johnson":
		usa_68_johnson += 1
	elif usa_68 == "wallace":
		usa_68_wallace += 1
	elif usa_68 == "kennedy":
		usa_68_kennedy += 1
	elif usa_68 == "goldwater":
		usa_68_goldwater += 1
	elif usa_68 == "glenn":
		usa_68_glenn += 1
	elif usa_68 == "smith":
		usa_68_smith += 1
	elif usa_68 == "harrington":
		usa_68_harrington += 1
	if ahf_64 == "bose":
		ahf_64_bose += 1
	elif ahf_64 == "sahgal":
		ahf_64_sahgal += 1
	elif ahf_64 == "singh":
		ahf_64_singh += 1
	if ahf_67 == "bose":
		ahf_67_bose += 1
	elif ahf_67 == "sahgal":
		ahf_67_sahgal += 1
	elif ahf_67 == "singh":
		ahf_67_singh += 1
	elif ahf_67 == "pratap":
		ahf_67_pratap += 1
	elif ahf_67 == "hazarika":
		ahf_67_hazarika += 1
	elif ahf_67 == "advani":
		ahf_67_advani += 1
	elif ahf_67 == "rao":
		ahf_67_rao += 1
	elif ahf_67 == "thackeray":
		ahf_67_thackeray += 1
	elif ahf_67 == "rahman":
		ahf_67_rahman += 1
	if ahf_70 == "bose":
		ahf_70_bose += 1
	elif ahf_70 == "sahgal":
		ahf_70_sahgal += 1
	elif ahf_70 == "singh":
		ahf_70_singh += 1
	elif ahf_70 == "pratap":
		ahf_70_pratap += 1
	elif ahf_70 == "hazarika":
		ahf_70_hazarika += 1
	elif ahf_70 == "advani":
		ahf_70_advani += 1
	elif ahf_70 == "rao":
		ahf_70_rao += 1
	elif ahf_70 == "thackeray":
		ahf_70_thackeray += 1
	elif ahf_70 == "rahman":
		ahf_70_rahman += 1
	elif ahf_70 == "charan_singh":
		ahf_70_c_singh += 1
	elif ahf_70 == "bhatt":
		ahf_70_bhatt += 1
	if ita_path == "ciano":
		ita_dem += 1
	elif ita_path == "scorza":
		ita_scorza += 1
	if ita_col == "decol":
		ita_decol += 1
	if ita_col == "recol":
		ita_recol += 1
	if wi_result == "longyun_before":
		wi_longyun_before += 1
	elif wi_result == "longyun_after":
		wi_longyun_after += 1
	elif wi_result == "china":
		wi_china += 1
	elif wi_result == "china_japan":
		wi_china_japan += 1
	elif wi_result == "japan":
		wi_japan += 1
			

dir = sys.argv[1]
start_time = timeit.default_timer()
for path, subdirs, files in os.walk(dir):
	for file in files:
		filepath=os.path.join(path,file)
		#print(str(filepath))
		if str(filepath).endswith("game.log"):
			print(str(filepath))
			with open(filepath, "r", encoding="utf8") as f:
				scan_file(f,filepath)

end_time = timeit.default_timer()
elapsed_time = round((end_time-start_time)*1000)
print("Took {} ms".format(elapsed_time))
def print_results():
	print("USA: \nBennett '64 {0}\nLBJ '64 {1}\nWallace '64 {2}\nRFK '64 {3}\nBennett '68 {4}\nLBJ '68 {5}\nWallace '68 {6}\nRFK '68 {7}\nGoldwater '68 {8}\nGlenn '68 {9}\nSmith '68 {10}\nHarrington '68 {11}".format(usa_64_bennett, usa_64_johnson, usa_64_wallace, usa_64_kennedy, usa_68_bennett, usa_68_johnson, usa_68_wallace, usa_68_kennedy, usa_68_goldwater, usa_68_glenn, usa_68_smith, usa_68_harrington))
	print("\nAzad Hind: \nBose '64 {0}\nSahgal '64 {1}\nSingh '64 {2}\nBose '67 {3}\nSahgal '67 {4}\nSingh '67 {5}\nPratap '67 {6}\nHazarika '67 {7}\nAdvani '67 {8}\nRao '67 {9}\nThackeray '67 {10}\nRahman '67 {11}".format(ahf_64_bose, ahf_64_sahgal, ahf_64_singh, ahf_67_bose, ahf_67_sahgal, ahf_67_singh, ahf_67_pratap, ahf_67_hazarika, ahf_67_advani, ahf_67_rao, ahf_67_thackeray, ahf_67_rahman))
	print("Bose '70 {0}\nSahgal '70 {1}\nSingh '70 {2}\nPratap '70 {3}\nAdvani '70 {4}\nRao '70 {5}\nThackeray '70 {6}\nRahman '70 {7}\nCharan Singh '70 {8}\nBhatt '70 {9}".format(ahf_70_bose, ahf_70_sahgal, ahf_70_singh, ahf_70_pratap, ahf_70_advani, ahf_70_rao, ahf_70_thackeray, ahf_70_rahman, ahf_70_c_singh, ahf_70_bhatt))
	print("\nItaly: \nDemocratic Italy {0}\nScorza {1}\nDecolonization {2}\nRecolonization {3}".format(ita_dem, ita_scorza, ita_decol, ita_recol))
	print("\nChina: \n{0}\n{1}\nLong Yun {2}\nLong Yun after Japanese Intervention {3}\nChina {4}\nChina-Japan {5}\nJapan {6}".format(wi_start, wi_end, wi_longyun_before, wi_longyun_after, wi_china, wi_china_japan, wi_japan))

print_results()
