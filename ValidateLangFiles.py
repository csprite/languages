#!/usr/bin/python
# Requires Python v3 Interpreter

import os
import sys
import glob
import configparser
import github_action_utils as gh

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
				gh.warning("", title="Section '" + Section + "' Not Found", file=f)
				break

			for SubSection in ConfigStructure[Section]:
				if not SubSection in config[Section]:
					gh.warning("", title="Sub-Section '" + SubSection + "' of '" + Section + "' Not Found", file=f)

	except Exception as e:
		gh.error(str(e), title="Unhandled Error Occurred", file=f)
		ExitCode = 1

sys.exit(ExitCode)

