


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
	NAME = ""
):
	LIST = STRUCTS_DB.all ()
	
	for STRUCT in LIST:
		STRUCT_NAMES = STRUCT ["NAMES"]
		
		for STRUCT_NAME in STRUCT_NAMES:
			if (NAME == STRUCT_NAME):
				Q = Query ()
				EL = STRUCTS_DB.get (Q.REGION == STRUCT ["REGION"])
				return EL
				
	raise Exception (f'name "{ NAME }" was not found.')
	