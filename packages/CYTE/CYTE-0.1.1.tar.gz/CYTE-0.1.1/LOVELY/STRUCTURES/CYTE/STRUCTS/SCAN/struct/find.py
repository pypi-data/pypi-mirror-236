
'''
import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.struct.find as find_struct
struct = find_struct.start (
	ACCESS.DB (),
	field = "region",
	value = 1
)	
'''

from tinydb import Query

def start (
	STRUCTS_DB,
	field,
	value
):
	Q = Query ()
	EL = STRUCTS_DB.get (
		Q [field] ==value
	)
	
	return