
'''
	NEW VERSION = CYTE.STRUCTS.SCAN.NODE.LIST
'''

'''
	import CYTE.STRUCTS.LIST as STRUCTS_DB_LIST
	LIST = STRUCTS_DB_LIST.FIND ()
'''

from tinydb import TinyDB, Query
import CYTE.STRUCTS.DB.PATH as STRUCTS_DB_PATH

def FIND ():
	PATH = STRUCTS_DB_PATH.FIND ()

	db = TinyDB (PATH)
	LIST = db.all ()
	
	return LIST