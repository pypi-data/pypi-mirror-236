


'''
import CYTE.STRUCTS.SCAN.net as net_build
struct_net = net_build.start ()
'''

'''
{
	"names": [
		"carbohydrates",
		"carbohydrate, by difference"
	],
	"region": 2,
	"includes": [ 7 ]
}
'''

import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.struct.list as STRUCTS_LIST

import json

def find_included (struct_to_find, structs):
	#for struct in structs:
	#	if 

	return

def start (STRUCT_DB):
	STRUCTS = STRUCTS_LIST.FIND (STRUCT_DB)
	STRUCTS_COUNT = len (STRUCTS)

	print ("structs count:", STRUCTS_COUNT)

	BRANCHES = []

	CYCLE_LIMIT = 20
	CYCLE = 1
	while (
		len (STRUCTS) >= 1 and
		CYCLE <= CYCLE_LIMIT
	):
		SELECTOR = 0
		LAST_INDEX = len (STRUCTS) - 1
		while (SELECTOR <= LAST_INDEX):
			STRUCT = STRUCTS [ SELECTOR ]
		
			includes = STRUCT ["includes"]
			
			if (len (includes) >= 1):
				print ('includes:', includes)
				
				included = find_included (STRUCT, STRUCTS)
			
			
			
			SELECTOR += 1
		
		
		if (CYCLE == CYCLE_LIMIT):
			print ("cycle limit reached", len (STRUCTS), "of", STRUCTS_COUNT)
	
		CYCLE += 1











