const fs = require("fs");
const ini = require("ini");
const core = require("@actions/core");
const process = require("process");
const structure = require("./structure.js");

const FilesToLint = fs.readdirSync("./languages/").filter(function(filePath) {
	return filePath.toLowerCase().endsWith(".ini");
});

var ExitCode = 0;

FilesToLint.forEach(function(filePath) {
	filePath = "./languages/" + filePath;

	const Parsed = ini.parse(fs.readFileSync(filePath, 'utf-8'))
	let warnings = 0;
	let errors = 0;

	// Ensure All Sections Defined in `structure`
	// exist in the parsed ini file
	Object.keys(structure).forEach(function(section) {
		if (Parsed[section] == null) {
			core.error(`Section '${section}' is required but not found`, { file: filePath });
			errors++;
		}
	});

	// Ensure All Sections in parsed ini file `Parsed` are known
	Object.keys(Parsed).forEach(function(section) {
		if (structure[section] == null) {
			core.warning(`Unknown Section '${section}'`, { file: filePath });
			warnings++;
		} else {
			// Ensure All Required Sub-Sections Defined in `structure[section]`
			// exist in the parsed ini file
			Object.keys(structure[section]).forEach(function(subSection) {
				if (structure[section][subSection].required) {
					if (Parsed[section][subSection] == null) {
						core.error(`Sub-Section '${subSection}' in Section '${section}' is required but not found`, { file: filePath });
						errors++;
					}
				}
			});

			// Ensure All Sub-Sections in parsed ini file `Parsed[section]` are known
			Object.keys(Parsed[section]).forEach(function(subSection) {
				if (structure[section][subSection] == null) {
					core.warning(`Unknown Sub-Section '${subSection}' in Section '${section}'`, { file: filePath });
					warnings++;
				}
			});
		}
	});

	if (errors == 0) {
		core.notice(`Ok (${warnings} ${warnings != 1 ? "Warnings" : "Warning"})`, { file: filePath });
	} else {
		ExitCode = 1;
	}
});

process.exit(ExitCode);
