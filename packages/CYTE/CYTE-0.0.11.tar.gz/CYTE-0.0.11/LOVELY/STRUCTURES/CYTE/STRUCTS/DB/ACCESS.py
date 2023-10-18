

'''
	import CYTE.STRUCTS.DB.ACCESS as STRUCTS_DB
	DB = STRUCTS_DB.ACCESS ()
'''

from tinydb import TinyDB, Query
import CYTE.STRUCTS.DB.PATH as STRUCTS_DB_PATH

def ACCESS ():
	PATH = STRUCTS_DB_PATH.FIND ()
	DB = TinyDB (PATH)
	return DB;