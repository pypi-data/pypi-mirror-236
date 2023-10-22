

import copy

def is_included (region, list):
	for commodity in list:
		includes = commodity ["struct"] ["includes"]
	
		for included in includes:
			if (included == region):
				return [ True, commodity ]

	return [ False, "" ]

def calc (
	USDA_FOOD_DATA,
	RETURN
):
	list = copy.deepcopy (
		RETURN ["ingredients"]["quantified list"]
	)
	
	#directional_links = 
	
	#import CYTE.STRUCTS.SCAN.trees_form_1 as trees_form_1
	#trees = trees_form_1.start (STRUCT_DB)
	
	for ingredient in list:
		ingredient["struct"]["includes commodities"] = []
	
	grove = []
	
	selector = 0
	while (selector <= len (list) - 1):
		ingredient = list [selector]
	
		region = ingredient ["struct"]["region"]
	
		#print (
		#	ingredient ["struct"] ["names"], 
		#	ingredient ["struct"] ["includes"]
		#)
	
		[ included, commodity ] = is_included (
			ingredient ["struct"]["region"],
			list
		)
		if (included == True):
			commodity ["struct"] ["includes commodities"].append (
				copy.deepcopy (ingredient)
			)
			list.remove (ingredient)
		
		selector += 1
			
		
		print (region, "included:", included)
	
	return list