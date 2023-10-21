
'''
	"packageWeight": "12 oz/340 g",
		
		"mass": {
			"per package, in grams": ,
			
			"per package": [{
				"unit": [ "gram" ],
				"amount": 
			}]
		}
		
	
	"packageWeight": "12 fl oz/355 mL",
	
		"volume": {
			"per package": [{
				"unit": [ "liter" ],
				"amount": 
			}]
		}
'''

import CYTE.FOOD.USDA.STRUCT_2.packageWeight.interpret as INTERPRETER

def INTERPRET (USDA_FOOD_DATA):
	assert ("packageWeight" in USDA_FOOD_DATA)
	
	RETURN = {}

	PARSED = INTERPRETER.INTERPRET (USDA_FOOD_DATA ["packageWeight"])
	print ("PARSED:", PARSED)

	if ("LITERS" in PARSED):
		RETURN ["volume"] = {
			"calculated": True,
			"per package, in liters": PARSED ["LITERS"]
		}
	else:
		RETURN ["volume"] = {
			"calculated": False
		}
		
	if ("GRAMS" in PARSED):
		RETURN ["mass"] = {
			"calculated": True,
			"per package, in grams": PARSED ["GRAMS"]
		}
	else:
		RETURN ["mass"] = {
			"calculated": False
		}

	return RETURN