


'''
import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCULPT.names as SCULPT_NAMES

STRUCT_DB = ACCESS.DB ()
SCULPT_NAMES.START (
	STRUCT_DB,
	REGION = 10000,
	NAMES = []
)
'''


from tinydb import TinyDB, Query

def START (
	SCULPT_DB,
	REGION,
	NAMES
):
	Q = Query ()
	SCULPT_DB.update (
		{ 
			'names': NAMES
		}, 
		Q.region == REGION
	)

	return;