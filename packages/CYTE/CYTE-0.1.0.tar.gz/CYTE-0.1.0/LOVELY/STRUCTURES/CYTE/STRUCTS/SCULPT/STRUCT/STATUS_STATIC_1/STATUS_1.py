




'''
	python3 STATUS.py "STRUCTS/SCULPT/STRUCT/STATUS_STATIC_1/STATUS_1.py"
'''

import CYTE.STRUCTS.DB.ACCESS as ACCESS
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

	

	STRUCT_DB = ACCESS.DB (PATH (ADDRESS))

	NEXT_REGION = FIND_NEXT_REGION.START (STRUCT_DB)
	assert (NEXT_REGION == 53), NEXT_REGION
	LIST = STRUCTS_LIST.FIND (ACCESS.DB ())
	assert (len (LIST) == 52), len (LIST)
	
	
	STRUCT_INSERT.START (
		STRUCT_DB,
		{
			'PART OF': [], 
			"names": [ 'EXAMPLE STRUCT' ]
		}
	)
	
	NEXT_REGION = FIND_NEXT_REGION.START (STRUCT_DB)
	assert (NEXT_REGION == 54), NEXT_REGION
	
	LIST = STRUCTS_LIST.FIND (STRUCT_DB, SORT = "region")
	#print (LIST)
	assert (len (LIST) == 53), len (LIST)
	
	DELETE_PATH (ADDRESS)

	return;
	
CHECKS = {
	"CHECK 1": CHECK_1
}