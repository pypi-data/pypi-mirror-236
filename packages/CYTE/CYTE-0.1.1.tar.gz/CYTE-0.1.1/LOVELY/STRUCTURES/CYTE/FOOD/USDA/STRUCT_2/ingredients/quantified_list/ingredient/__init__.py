
'''
These are based on a portion of 100
	"defined": {
		"servings per package": "1.9715666666666667",
		"serving size": {
			"unit": "ml",
			"amount": "240"
		}
	}
	"mass": {
		"calculated": false
	},
	"volume": {
		"calculated": true,
		"per package, in liters": "0.473176"
	},
'''

'''
These are based on serving size:
	"labelNutrients": {
		"iron": {
			"value": 1.08
		}
	}
'''

'''

'''

import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.NAMES.has as STRUCT_HAS_NAME

from fractions import Fraction

#
#	??
#		either 100mL or 100g
#
PORTION = 100

def CALC (
	FOOD_NUTRIENT,
	USDA_FOOD_DATA_CALCULATED
):
	name = FOOD_NUTRIENT ["nutrient"] ["name"]
	
	print ("food nutrient:", FOOD_NUTRIENT)
	
	assert ("amount" in FOOD_NUTRIENT), FOOD_NUTRIENT;
	assert ("unitName" in FOOD_NUTRIENT ["nutrient"]), FOOD_NUTRIENT;
	unit = FOOD_NUTRIENT ["nutrient"]["unitName"]
	
	'''
		find the struct with that name,
		in the structs DB
	'''
	struct = STRUCT_HAS_NAME.SEARCH (
		ACCESS.DB (),
		NAME = name
	)
	names = struct ["names"]
		
	servings_per_package = Fraction (USDA_FOOD_DATA_CALCULATED ["defined"]["servings per package"])
	amount_in_serving = Fraction (USDA_FOOD_DATA_CALCULATED ["defined"]["serving size"]["amount"])
		
	amount_per_package = (
		Fraction (FOOD_NUTRIENT ["amount"]) /
		PORTION				
	) * servings_per_package * amount_in_serving
	
	amount_per_serving = (
		Fraction (FOOD_NUTRIENT ["amount"]) /
		PORTION				
	) * amount_in_serving

	return {
		"name": name,
		
		"struct": struct,

		"quantity per package, float": {
			"amount": float (amount_per_package),
			"unit": unit
		},
		"quantity per package, fraction string": {
			"amount": str (amount_per_package),
			"unit": unit
		},
		
		"quantity per serving, float": {
			"amount": float (amount_per_serving),
			"unit": unit
		},
		"quantity per serving, fraction string": {
			"amount": str (amount_per_serving),
			"unit": unit
		}
	}