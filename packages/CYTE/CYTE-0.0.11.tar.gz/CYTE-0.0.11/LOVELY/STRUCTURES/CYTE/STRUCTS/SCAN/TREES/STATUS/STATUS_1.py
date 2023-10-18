

'''
	python3 STATUS.py "STRUCTS/SCAN/TREES/STATUS/STATUS_1.py"
'''

import CYTE.STRUCTS.SCAN.TREES as TREE_FORMULATOR
from CYTE.STRUCTS.SCAN.STRUCT.FIND import FIND_STRUCT

from CYTE.STRUCTS.DB.PATH import PATHS

import json

import pathlib
from os.path import dirname, join, normpath

THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()

def CHECK_1 ():
	PATHS ["DB"] = normpath (join (THIS_FOLDER, "DB.JSON"))
	TREES = TREE_FORMULATOR.FORMULATE ()
	print (json.dumps (TREES, indent = 4))

	STRUCT = FIND_STRUCT (NAME = "CARBOHYDRATES")


	return;
	
	
	
CHECKS = {
	"CHECK 1": CHECK_1
}