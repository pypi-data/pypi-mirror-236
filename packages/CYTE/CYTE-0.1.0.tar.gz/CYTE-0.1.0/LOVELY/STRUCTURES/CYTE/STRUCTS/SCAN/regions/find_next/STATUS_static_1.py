

'''
	python3 STATUS.py "STRUCTS/SCAN/regions/find_next/STATUS_dynamic_1.py"
'''

import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.regions.find_next as FIND_NEXT_REGION

def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "STRUCTS.JSON"))

def CHECK_1 ():
	NEXT_REGION = FIND_NEXT_REGION.START (
		ACCESS.DB (PATH ())
	)
	
	assert (NEXT_REGION == 53), NEXT_REGION

	return;
	
CHECKS = {
	"CHECK 1": CHECK_1
}