

'''
	python3 STATUS.py "STRUCTS/SCAN/TREES/STATUS_STATIC/STATUS_1.py"
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
	STRUCT_DB = ACCESS.DB (PATH (), sort_keys = True)
	STRUCT_TREES = TREES.FORMULATE (STRUCT_DB)
	print ("TREES", json.dumps (STRUCT_TREES, indent = 4))

	#STRUCT = FIND_STRUCT (NAME = "CARBOHYDRATES")

	def PRINT_TREE (STRUCTS, INDENT = 0):
		for STRUCT in STRUCTS:
		
			print (" " * INDENT, STRUCT ["names"])
			
			if ("includes" in STRUCT):
				PRINT_TREE (
					STRUCT ["includes"], 
					INDENT = (INDENT + 4)
				)

	PRINT_TREE (STRUCT_TREES)

	return;
	
	
	
CHECKS = {
	"CHECK 1": CHECK_1
}