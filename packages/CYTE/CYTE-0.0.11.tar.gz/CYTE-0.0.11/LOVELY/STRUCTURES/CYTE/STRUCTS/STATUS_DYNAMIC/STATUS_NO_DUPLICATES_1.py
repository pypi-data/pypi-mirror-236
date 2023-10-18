
'''
	python3 STATUS.py "STRUCTS/STATUS/STATUS_NO_DUPLICATES_1.py"
'''


import json
import CYTE.STRUCTS.LIST as STRUCTS_DB_LIST
	
	
def CHECK_1 ():
	LIST = STRUCTS_DB_LIST.FIND ()

	print ("LIST:", json.dumps (LIST, indent = 4))
	print ("LIST:", len (LIST))

	REGIONS = []
	for STRUCT in LIST:
		if (STRUCT ["REGION"] in REGIONS):
			raise Exception ()

		REGIONS.append (STRUCT ["REGION"])
		
	assert (len (REGIONS) >= 52)


def CHECK_2 ():
	LIST = STRUCTS_DB_LIST.FIND ()

	print ("LIST:", json.dumps (LIST, indent = 4))
	print ("LIST:", len (LIST))

	NAMES = []
	for STRUCT in LIST:
		STRUCT_NAMES = STRUCT ["NAMES"]
		
		for NAME in STRUCT_NAMES:
			if (NAME in NAMES):
				raise Exception ()

			NAMES.append (NAME)
		
	print ("NAMES:", len (NAMES))
	assert (len (NAMES) >= 56)




CHECKS = {
	"LIST DOES NOT HAVE DUPLICATE REGIONS": CHECK_1,
	"LIST DOES NOT HAVE DUPLICATE NAMES": CHECK_2
}