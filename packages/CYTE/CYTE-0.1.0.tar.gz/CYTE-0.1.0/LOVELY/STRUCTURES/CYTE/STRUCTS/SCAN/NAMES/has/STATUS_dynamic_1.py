



'''
	python3 STATUS.py "STRUCTS/SCAN/NAMES/has/STATUS_dynamic_1.py"
'''



def CHECK_1 ():
	import CYTE.STRUCTS.DB.ACCESS as ACCESS
	import CYTE.STRUCTS.SCAN.NAMES.has as STRUCT_HAS_NAME
	STRUCT = STRUCT_HAS_NAME.SEARCH (
		ACCESS.DB (),
		NAME = "PROTEIN"
	)
	
	print (STRUCT)

	import tinydb
	assert (type (STRUCT) == tinydb.table.Document)
	assert (STRUCT ["region"] == 1)
	
	
CHECKS = {
	"dynamic, has name": CHECK_1
}