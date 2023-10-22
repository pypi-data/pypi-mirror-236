




'''
	python3 STATUS.py "STRUCTS/SCULPT/names/status_cryo/STATUS_1.py"
'''


import CYTE.STRUCTS.SCAN.regions.find_next as FIND_NEXT_REGION
import CYTE.STRUCTS.SCULPT.STRUCT.insert as STRUCT_INSERT
import CYTE.STRUCTS.SCAN.struct.list as STRUCTS_LIST
	

def PATH (ADDRESS):
	import shutil

	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	
	SOURCE = normpath (join (THIS_FOLDER, "STRUCTS.JSON"))
	DEST = normpath (join (THIS_FOLDER, ADDRESS))
	
	shutil.copyfile (SOURCE, DEST)
	
	return DEST;
	
def DELETE_PATH (ADDRESS):
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	DEST = normpath (join (THIS_FOLDER, ADDRESS))
	
	import os
	os.remove (DEST)

	return;

def CHECK_1 ():
	ADDRESS = "STRUCTS_1_1.JSON"

	try:
		DELETE_PATH (ADDRESS)
	except Exception as E:
		print (E)

	
	import CYTE.STRUCTS.DB.ACCESS as ACCESS
	STRUCT_DB = ACCESS.DB (PATH (ADDRESS))
	
	import CYTE.STRUCTS.SCAN.NAMES.has as STRUCT_HAS_NAME
	STRUCT = STRUCT_HAS_NAME.SEARCH (
		STRUCT_DB,
		NAME = "PROTEIN"
	)
	assert (len (STRUCT ["names"]) == 1)
	assert (STRUCT ["names"][0] == "protein")
		
	#
	#
	#
	
	import CYTE.STRUCTS.SCULPT.names as SCULPT_NAMES
	SCULPT_NAMES.START (
		STRUCT_DB,
		REGION = 1,
		NAMES = [ "protein", "proteina" ]
	)
	STRUCT = STRUCT_HAS_NAME.SEARCH (
		STRUCT_DB,
		NAME = "PROTEIN"
	)
	
	print (STRUCT)
	
	assert (len (STRUCT ["names"]) == 2)
	assert (STRUCT ["names"][0] == "protein")
	assert (STRUCT ["names"][1] == "proteina")
	
	#
	#
	#
	

	DELETE_PATH (ADDRESS)

	return;
	
CHECKS = {
	"CHECK 1": CHECK_1
}