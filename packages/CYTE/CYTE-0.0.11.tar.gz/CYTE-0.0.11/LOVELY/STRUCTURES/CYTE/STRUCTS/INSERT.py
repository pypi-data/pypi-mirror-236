

'''
	NEW VERSION -> CYTE.STRUCTS.SCAN.INSERT
'''

'''
	from CYTE.STRUCTS.DB.INSERT import INSERT
'''

from tinydb import TinyDB, Query
import CYTE.STRUCTS.DB.PATH as STRUCTS_DB_PATH

def INSERT (STRUCT):
	PATH = STRUCTS_DB_PATH.FIND ()

	db = TinyDB (PATH)
	Q = Query ()
	
	FOUND = db.search (
		Q.REGION == STRUCT ["REGION"]
	)
	if (len (FOUND) >= 1):
		raise Exception ("REGION NUMBER ALREADY EXISTS")
	
	
	db.insert (STRUCT)