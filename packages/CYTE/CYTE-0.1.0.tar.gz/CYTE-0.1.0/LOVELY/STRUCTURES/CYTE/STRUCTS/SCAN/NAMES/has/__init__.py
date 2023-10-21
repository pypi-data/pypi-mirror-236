


'''
import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.NAMES.has as STRUCT_HAS_NAME
STRUCT = STRUCT_HAS_NAME.SEARCH (
	ACCESS.DB (),
	NAME = "PROTEIN"
)
'''

from tinydb import TinyDB, Query
import CYTE.STRUCTS.DB.PATH as STRUCTS_DB_PATH

def SEARCH (
	STRUCTS_DB,
	NAME = "",
	
	RETURN_BOOL = False
):
	LIST = STRUCTS_DB.all ()
	
	NAME = NAME.lower ()
	
	for STRUCT in LIST:
		STRUCT_NAMES = STRUCT ["names"]
		
		for STRUCT_NAME in STRUCT_NAMES:
			if (NAME == STRUCT_NAME.lower ()):			
				Q = Query ()
				EL = STRUCTS_DB.get (Q.region == STRUCT ["region"])
				
				if (RETURN_BOOL == True):
					return True
				else:
					return EL
				
				
	if (RETURN_BOOL == True):
		return False
		
	raise Exception (f'name "{ NAME }" was not found.')
	