from pathlib import Path

history_folder = Path("..", "history", "countries")
for file in history_folder.iterdir():
	correct_ending = True
	with file.open("r+", encoding="utf8") as f:
		last_line = f.readlines()[-1]
		if last_line[-1] != "\n":
			correct_ending = False
	if not correct_ending:
		with file.open("a+", encoding="utf8") as f:
			f.write('\n')
