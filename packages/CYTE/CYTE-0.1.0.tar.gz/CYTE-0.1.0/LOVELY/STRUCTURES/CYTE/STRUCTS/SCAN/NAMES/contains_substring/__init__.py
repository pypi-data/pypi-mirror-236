
'''
	contains substring
'''

'''
import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.NAMES.contains_substring as STRUCTS_WHERE_NAME_CONTAINS_SUBSTRING
STRUCTS = STRUCTS_WHERE_NAME_CONTAINS_SUBSTRING.FIND (
	ACCESS.DB (),
	"VITAMIN B"
)
'''

import CYTE.STRUCTS.SCAN as STRUCT_SCAN

def FIND (
	STRUCTS_DB,
	CONTAINS
):
	CONTAINS = CONTAINS.upper ()

	def FOR_EACH (STRUCT):
		STRUCT_NAMES = STRUCT ["names"]
			
		for STRUCT_NAME in STRUCT_NAMES:
			STRUCT_NAME = STRUCT_NAME.upper ()
		
			if (STRUCT_NAME.__contains__ (CONTAINS)):
				#Q = Query ()
				#EL = db.get (Q.REGION == STRUCT ["region"])
				
				return True

		return False
	
	STRUCTS = STRUCT_SCAN.START (
		FOR_EACH = FOR_EACH
	)


	return STRUCTS