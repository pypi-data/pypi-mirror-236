

'''
python3 STATUS.py "STRUCTS/SCAN/_STATUS/STATUS_dynamic_1.py"
'''


def CHECK_1 ():
	INCLUDES = "VITAMIN B1"

	def FOR_EACH (STRUCT):
		STRUCT_NAMES = STRUCT ["names"]
			
		for STRUCT_NAME in STRUCT_NAMES:
			STRUCT_NAME = STRUCT_NAME.upper ()
		
			if (STRUCT_NAME == INCLUDES.upper ()):
				return True

		return False

	import CYTE.STRUCTS.DB.ACCESS as ACCESS
	import CYTE.STRUCTS.SCAN as STRUCT_SCAN
	STRUCTS = STRUCT_SCAN.START (
		STRUCTS_DB = ACCESS.DB (),
		FOR_EACH = FOR_EACH
	)
	
	print ("STRUCTS:", STRUCTS)

	return;
	
	
CHECKS = {
	"check 1": CHECK_1
}