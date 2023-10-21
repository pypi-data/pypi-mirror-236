





#
#	(rm -rf dist && python3 -m build --sdist && twine upload dist/*)
#


#
#	https://setuptools.pypa.io/en/latest/userguide/quickstart.html
#
#	https://github.com/pypa/sampleproject/blob/db5806e0a3204034c51b1c00dde7d5eb3fa2532e/setup.py
#
from setuptools import setup, find_packages


def SCAN_DESCRIPTION ():
	DESCRIPTION = ''
	try:
		with open ('CYTE.txt') as f:
			DESCRIPTION = f.read ()
		print (DESCRIPTION)
	except Exception as E:
		pass;
		
	return DESCRIPTION;

from glob import glob


NAME = "CYTE"
STRUCTURE = 'LOVELY/STRUCTURES/' + NAME
SCRIPT = 'LOVELY/STRUCTURES/SCRIPTS/cyte' 

setup (
    name = NAME,
	description = "Measurements (System International, US Customary, etc.)",
    version = "0.1.0",
    install_requires = [
		"BOTANY",
		"tinydb",
		"pydash"
	],	
	
	package_dir = { 
		"CYTE": STRUCTURE
	},
	
	#
	#	PACKAGE DATA
	#
	package_data = {
		'LOVELY/STRUCTURES': [ "*.HTML" ],
		"": [ "*.HTML" ]
    },
	include_package_data = True,
	
	project_urls = {
		"GitLab": "https://gitlab.com/reptilian_climates/cyte.git"
	},
	
	scripts = [ 
		SCRIPT
	],
	
	license = "the health license",
	long_description = SCAN_DESCRIPTION (),
	long_description_content_type = "text/plain"
)

