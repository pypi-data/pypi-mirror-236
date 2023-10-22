
'''
import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.regions.find_next as FIND_NEXT_REGION
NEXT_REGION = FIND_NEXT_REGION.START (
	ACCESS.DB ()
)
'''

def START (STRUCT_DB):
	import CYTE.STRUCTS.DB.ACCESS as ACCESS
	import CYTE.STRUCTS.SCAN.struct.list as STRUCTS_LIST
	LIST = STRUCTS_LIST.FIND (STRUCT_DB)
	
	LIST.sort (key = lambda STRUCT : STRUCT ["region"])
	
	LAST_INDEX = len (LIST) - 1;
	
	return LIST [ LAST_INDEX ][ "region" ] + 1
	
	