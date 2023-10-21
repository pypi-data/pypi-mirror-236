


'''

INCLUDES = "VITAMIN B"

def FOR_EACH (STRUCT):
	STRUCT_NAMES = STRUCT ["names"]
		
	for STRUCT_NAME in STRUCT_NAMES:
		STRUCT_NAME = STRUCT_NAME.upper ()
	
		if (STRUCT_NAME.__contains__ (INCLUDES)):
			#Q = Query ()
			#EL = db.get (Q.REGION == STRUCT ["region"])
			
			return True

	return True

import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN as STRUCT_SCAN
STRUCTS = STRUCT_SCAN.START (
	STRUCTS_DB = ACCESS.DB (),
	FOR_EACH = FOR_EACH
)
'''

from tinydb import TinyDB, Query
import CYTE.STRUCTS.DB.PATH as STRUCTS_DB_PATH

def START (
	STRUCTS_DB = None,
	FOR_EACH = lambda : ()
):
	PATH = STRUCTS_DB_PATH.FIND ()

	db = TinyDB (PATH)
	LIST = db.all ()
	
	RETURNS = []
	
	for STRUCT in LIST:		
		if (FOR_EACH (STRUCT) == True):
			RETURNS.append (STRUCT)
				
	return RETURNS
	