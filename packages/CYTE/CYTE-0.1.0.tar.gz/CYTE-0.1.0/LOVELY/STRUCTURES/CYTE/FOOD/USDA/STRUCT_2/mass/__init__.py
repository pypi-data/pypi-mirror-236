

'''
from CYTE.USDA.STRUCT_2.quantity 
'''

'''
	"12 fl oz/355 mL"
'''

'''
	1 mL == 
'''

import CYTE.FOOD.USDA.STRUCT_2.packageWeight.interpret as PACKAGE_WEIGHT

def CALC (USDA_FOOD_DATA):
	assert ("packageWeight" in USDA_FOOD_DATA)

	RETURN = {
		"per package": {
			"grams": ""
		}
	}

	PARSED_WEIGHT = PACKAGE_WEIGHT.INTERPRET (USDA_FOOD_DATA ["packageWeight"])
	print (PARSED_WEIGHT)

	return;