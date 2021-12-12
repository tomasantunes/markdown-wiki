#!/usr/bin/env python

import datetime
import sys

wiki_folder = "wiki"

if (len(sys.argv) >= 2):
	time = str(datetime.datetime.now().replace(microsecond=0))
	text = sys.argv[1]
	if (text == "-l"):
		file_r = open(wiki_folder + "/logs/feed.md", "r")
		print(file_r.read())
		file_r.close()
	else:
		file = open(wiki_folder + "/logs/feed.md", "a")
		file.write("- " + time + " - " + text + "\n")
		file.close()
else:
	print("Invalid arguments.")
