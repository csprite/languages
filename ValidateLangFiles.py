#!/usr/bin/python
# Requires Python v3 Interpreter

import os
import sys
import glob
import configparser

ConfigStructure = {
	"file_menu": [ "file", "new", "open" ],
	"help_menu": [ "help", "about", "github" ],
	"open_file_popup": [ "open_file" ],
	"new_document_popup": [
		"title", "width_input", "height_input",
		"ok_button", "cancel_button"
	],
	"about_csprite_popup": [
		"title", "contributors_header", "contributors_paragraph",
		"contributors_link", "os_projects_header", "os_projects_text",
		"close_button"
	],
	"unicode_range": [ "range" ]
}

Files = []
ExitCode = 0

for f in glob.glob("./*.ini"):
	if os.path.isfile(f):
		Files.append(f)

for f in Files:
	try:
		config=configparser.ConfigParser()
		config.read(f)

		for Section in ConfigStructure:
			if not Section in config:
				sys.stdout.write("::warning file=\"" + f + "\",title=\"Section '" + Section + "' Not Found\"\n")
				break

			for SubSection in ConfigStructure[Section]:
				if not SubSection in config[Section]:
					sys.stdout.write("::warning file=\"" + f + "\",title=\"Sub-Section '" + SubSection + "' of '" + Section + "' Not Found\"\n")

	except Exception as e:
		sys.stdout.write(f"::error file='{f}',title='Unhandled Error Occurred'::'{str(e)}'\n")
		ExitCode = 1

sys.exit(ExitCode)
