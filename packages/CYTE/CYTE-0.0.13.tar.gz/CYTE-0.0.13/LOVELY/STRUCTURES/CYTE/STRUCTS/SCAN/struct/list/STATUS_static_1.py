



'''
	python3 STATUS.py "STRUCTS/SCAN/struct/list/STATUS_static_1.py"
'''

def PATH ():
	import pathlib
	from os.path import dirname, join, normpath
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (THIS_FOLDER, "STRUCTS.JSON"))


def CHECK_1 ():
	import CYTE.STRUCTS.DB.ACCESS as ACCESS
	import CYTE.STRUCTS.SCAN.struct.list as STRUCTS_LIST
	LIST = STRUCTS_LIST.FIND (ACCESS.DB (PATH ()))

	assert (len (LIST) == 52), len(LIST)
	
	
CHECKS = {
	"static, list": CHECK_1
}