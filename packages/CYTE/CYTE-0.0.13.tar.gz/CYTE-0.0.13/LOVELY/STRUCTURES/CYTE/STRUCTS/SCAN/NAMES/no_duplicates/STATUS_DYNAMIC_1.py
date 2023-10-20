
'''
	python3 STATUS.py "STRUCTS/SCAN/NAMES/no_duplicates/STATUS_DYNAMIC_1.py"
'''

def CHECK_1 ():
	import CYTE.STRUCTS.DB.ACCESS as ACCESS
	from CYTE.STRUCTS.SCAN.NAMES.no_duplicates import STRUCTS_NAMES_NO_DUPLICATES
	STRUCTS_NAMES_NO_DUPLICATES (
		ACCESS.DB ()
	)
	
CHECKS = {
	"dynamic, no duplicates found": CHECK_1
}