

'''
	import CYTE.STRUCTS.DB.ACCESS as ACCESS
	import CYTE.STRUCTS.SCAN.struct.list as STRUCTS_LIST
	LIST = STRUCTS_LIST.FIND (ACCESS.DB ())
'''


def FIND (STRUCTS_DB, SORT = "region"):
	LIST = STRUCTS_DB.all ()
	
	if (SORT == "region"):
		LIST.sort (key = lambda STRUCT : STRUCT [SORT])
	
	return LIST