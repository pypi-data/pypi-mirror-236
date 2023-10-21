



'''
	python3 STATUS.py "FOOD/USDA/STRUCT_2/_status/STATUS_beet_juice_2412474.py"
'''

import json

import CYTE.FOOD.USDA.EXAMPLES as USDA_EXAMPLES
import CYTE.FOOD.USDA.STRUCT_2 as USDA_STRUCT_2
def CHECK_1 ():
	EXAMPLE = USDA_EXAMPLES.RETRIEVE ("BRANDED/BEET_JUICE_2412474.JSON")
	RETURN = USDA_STRUCT_2.CALC (EXAMPLE)
	
	print (json.dumps (RETURN, indent = 4))

	assert (RETURN ["volume"]["per package, in liters"] == "0.473176")
	assert (
		RETURN ["ingredients"]["unquantified string"] == 
		"BEET, CITRIC ACID"
	)
	
CHECKS = {
	"BEET JUICE 2642759": CHECK_1
}


