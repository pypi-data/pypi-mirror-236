

'''
import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.TREES as TREES
TREES = TREES.FORMULATE (ACCESS.DB ())
'''

'''
{
	"region": 3,

	"names": [
		"LIPIDS",
		"TOTAL LIPID (FAT)"
	],
	
	"PART OF": [],
	"includes": [
		{
			"PART OF": 3,
			"names": [
				"FATTY ACIDS, TOTAL SATURATED"
			],
			"region": 4
		}	
	]
},
'''


import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.struct.list as STRUCTS_LIST
import CYTE.STRUCTS.SCAN.TREES.FN.ATTEMPT_TO_ATTACH as ATTEMPT_TO_ATTACH
import CYTE.STRUCTS.SCAN.TREES.SORT as SORT_TREES


import json


#
#	ATTACH { INNER } STRUCTURES
#
def ATTACH_INNER_STRUCTURES ():
	return



def FORMULATE (STRUCT_DB):
	STRUCTS = STRUCTS_LIST.FIND (STRUCT_DB)
	STRUCTS_COUNT = len (STRUCTS)
	
	print (json.dumps (STRUCTS, indent = 4))

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
		
			if (len (STRUCT ["PART OF"]) == 0):
				BRANCHES.append (STRUCT)
				
				STRUCTS.remove (STRUCT)	
				LAST_INDEX -= 1
				continue;				
			
			else:
				ATTACHED = ATTEMPT_TO_ATTACH.START (STRUCT, BRANCHES)
				if (ATTACHED == True):
					STRUCTS.remove (STRUCT)	
					LAST_INDEX -= 1
					continue;			
		
			SELECTOR += 1
	
	
		if (CYCLE == CYCLE_LIMIT):
			print ("CYCLE LIMIT REACHED", len (STRUCTS), "OF", STRUCTS_COUNT)
	
		CYCLE += 1

	SORT_TREES.START (BRANCHES)

	return BRANCHES