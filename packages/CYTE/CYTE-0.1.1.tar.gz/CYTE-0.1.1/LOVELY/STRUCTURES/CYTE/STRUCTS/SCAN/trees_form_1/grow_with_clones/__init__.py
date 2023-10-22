

'''


'''

import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.struct.list as STRUCTS_LIST

import json


'''
class grow:
	pass;
'''
	

def start (STRUCT_DB):
	structs = STRUCTS_LIST.FIND (STRUCT_DB)
	structs_tally = len (structs)

	#
	#	this is a list of all the struct regions that have 
	#
	#	{
	#		1: 2	
	#	}
	#
	#	
	struct_region_tallies = {}

	def find_region (region):
		for struct in structs:
			if (struct ['region'] == region):
				return struct;
				
		raise Exception (f"'region' '{ region }' was not found in structs.")


	def build_tree (region):
		struct = find_region (region)
		struct ["includes structs"] = []
		
		includes = struct ["includes"]		
		for include in includes:
			struct ["includes structs"].append (build_tree (include))
		
		return struct;

	print ("structs tally:", structs_tally)

	

	trees = []


	selector = 0
	last_index = len (structs) - 1
	while (selector <= last_index):
		struct = structs [ selector ]
		
		struct ["includes structs"] = []
		includes = struct ["includes"]		
		for include in includes:
			struct ["includes structs"].append (build_tree (include))

		trees.append (struct)
		
		selector += 1
		
		
	return trees;
	
