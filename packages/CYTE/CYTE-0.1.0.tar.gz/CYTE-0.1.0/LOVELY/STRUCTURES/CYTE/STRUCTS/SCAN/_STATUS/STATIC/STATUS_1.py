

'''
python3 STATUS.py "STRUCTS/SCAN/_STATUS/STATIC/STATUS_1.py"
'''

import CYTE._ensure.eq as EQ


def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "STRUCTS.JSON"))

def CHECK_1 ():
	INCLUDES = "VITAMIN B1"

	def FOR_EACH (STRUCT):
		STRUCT_NAMES = STRUCT ["names"]
			
		for STRUCT_NAME in STRUCT_NAMES:
			STRUCT_NAME = STRUCT_NAME.upper ()
		
			if (STRUCT_NAME == INCLUDES.upper ()):
				return True

		return False

	import CYTE.STRUCTS.DB.ACCESS as ACCESS
	import CYTE.STRUCTS.SCAN as STRUCT_SCAN
	STRUCTS = STRUCT_SCAN.START (
		STRUCTS_DB = ACCESS.DB (PATH ()),
		FOR_EACH = FOR_EACH
	)
	
	print ("STRUCTS:", STRUCTS)

	EQ.CHECK (len (STRUCTS), 1)
	EQ.CHECK (STRUCTS[0]["region"], 20)

	return;
	
	
CHECKS = {
	"check 1": CHECK_1
}