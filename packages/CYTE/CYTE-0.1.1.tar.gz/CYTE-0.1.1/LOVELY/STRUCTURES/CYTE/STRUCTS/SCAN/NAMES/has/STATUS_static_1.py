



'''
	python3 STATUS.py "STRUCTS/SCAN/NAMES/has/STATUS_static_1.py"
'''

def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "STRUCTS.JSON"))

def CHECK_1 ():
	import CYTE.STRUCTS.DB.ACCESS as ACCESS
	import CYTE.STRUCTS.SCAN.NAMES.has as STRUCT_HAS_NAME
	FOUND = STRUCT_HAS_NAME.SEARCH (
		ACCESS.DB (PATH ()),
		NAME = "PROTEIN",
		RETURN_BOOL = True
	)

	assert (FOUND == True)
	
def CHECK_2 ():
	import CYTE.STRUCTS.DB.ACCESS as ACCESS
	import CYTE.STRUCTS.SCAN.NAMES.has as STRUCT_HAS_NAME
	FOUND = STRUCT_HAS_NAME.SEARCH (
		ACCESS.DB (PATH ()),
		NAME = "PROTEINN",
		RETURN_BOOL = True
	)

	assert (FOUND == False)
	
	
CHECKS = {
	"static, has name 1": CHECK_1,
	"static, has name 2": CHECK_2
}