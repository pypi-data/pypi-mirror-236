


'''
import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCULPT.STRUCT.insert as STRUCT_INSERT
STRUCTS = STRUCT_INSERT.START (
	ACCESS.DB (),
	{
		'PART OF': [], 
		"names": [ '' ]
	}
)
'''

import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.regions.find_next as FIND_NEXT_REGION


def START (STRUCT_DB, STRUCT):
	NEXT_REGION = FIND_NEXT_REGION.START (
		STRUCT_DB
	)
	
	STRUCT ["region"] = NEXT_REGION
	ID = STRUCT_DB.insert (STRUCT)
	assert (type (ID) == int)
