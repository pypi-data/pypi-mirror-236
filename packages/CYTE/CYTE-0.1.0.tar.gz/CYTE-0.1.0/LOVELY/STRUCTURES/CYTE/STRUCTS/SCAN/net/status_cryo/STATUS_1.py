

'''
	python3 STATUS.py "STRUCTS/SCAN/net/status_cryo/STATUS_1.py"
'''

import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.TREES as TREES

import json

def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "STRUCTS.JSON"))

def CHECK_1 ():
	#STRUCT_DB = ACCESS.DB (PATH (), sort_keys = True)
	STRUCT_DB = ACCESS.DB ()

	import CYTE.STRUCTS.SCAN.net as net_build
	struct_net = net_build.start (STRUCT_DB)
	

	

	
	
	
CHECKS = {
	"CHECK 1": CHECK_1
}