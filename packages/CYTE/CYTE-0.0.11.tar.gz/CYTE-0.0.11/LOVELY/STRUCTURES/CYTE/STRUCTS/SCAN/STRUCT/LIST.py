

'''
	import CYTE.STRUCTS.SCAN.STRUCT.LIST as STRUCTS_LIST
	LIST = STRUCTS_LIST.FIND ()
'''

from tinydb import TinyDB, Query
import CYTE.STRUCTS.DB.PATH as STRUCTS_DB_PATH

def FIND ():
	PATH = STRUCTS_DB_PATH.FIND ()

	db = TinyDB (PATH)
	LIST = db.all ()
	
	return LIST