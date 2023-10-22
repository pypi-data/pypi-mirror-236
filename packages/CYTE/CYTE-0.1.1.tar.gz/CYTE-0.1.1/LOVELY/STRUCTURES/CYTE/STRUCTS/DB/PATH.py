

'''
	import CYTE.STRUCTS.DB.PATH as STRUCTS_DB_PATH
	PATH = STRUCTS_DB_PATH.FIND ()
'''

'''
	USE CUSTOM PATH:
	
	from CYTE.STRUCTS.DB.PATH import DB_PATH
'''

'''
def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "STRUCTS.JSON"))
'''


import pathlib
from os.path import dirname, join, normpath

THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()

PATHS = {
	"DB": normpath (join (THIS_FOLDER, "STRUCTS.JSON"))
}

def FIND ():
	return PATHS ["DB"]




