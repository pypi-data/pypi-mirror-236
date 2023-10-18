



'''
	from CYTE.STRUCTS.DB.INSERT import INSERT
'''

from tinydb import TinyDB, Query
import CYTE.STRUCTS.DB.PATH as STRUCTS_DB_PATH

def INSERT_LIST (STRUCTS):
	PATH = STRUCTS_DB_PATH.FIND ()

	db = TinyDB (PATH)
	
	for STRUCT in STRUCTS:
		db.insert (STRUCT)