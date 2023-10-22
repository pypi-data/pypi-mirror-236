



'''
	python3 STATUS.py "STRUCTS/SCAN/trees_form_1/grow_with_clones/STATUS_1.py"
'''

import CYTE.STRUCTS.DB.ACCESS as ACCESS

import json

def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "structs.json"))

def CHECK_1 ():
	#STRUCT_DB = ACCESS.DB (PATH (), sort_keys = True)
	STRUCT_DB = ACCESS.DB ()

	import CYTE.STRUCTS.SCAN.trees_form_1.grow_with_clones as trees_form_1_grow_with_clones
	trees = trees_form_1_grow_with_clones.start (STRUCT_DB)
	
	import json
	print (json.dumps (trees, indent = 4))
	
	def print_trees (trees, level):
		for tree in trees:
			names = tree ['names']
			indent = "  " * level
		
			print (f'{ indent }{ names }')
			
			if ("includes structs" in tree):
				print_trees (tree ["includes structs"], level = level + 1)
	
	print_trees (trees, level = 0)
	
CHECKS = {
	"CHECK 1": CHECK_1
}