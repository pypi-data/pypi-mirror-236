


'''
from CYTE.STRUCTS.FIND import FIND_STRUCT
[ STRUCT, ID ] = FIND_STRUCT (NAME = "PROTEIN")
'''

from tinydb import TinyDB, Query
import CYTE.STRUCTS.DB.PATH as STRUCTS_DB_PATH

def FIND_STRUCT (
	NAME = ""
):
	PATH = STRUCTS_DB_PATH.FIND ()

	db = TinyDB (PATH)
	LIST = db.all ()
	
	for STRUCT in LIST:
		STRUCT_NAMES = STRUCT ["NAMES"]
		
		for STRUCT_NAME in STRUCT_NAMES:
			if (NAME == STRUCT_NAME):
				Q = Query ()
				EL = db.get (Q.REGION == STRUCT ["REGION"])
			
				return EL
				
	return None
	