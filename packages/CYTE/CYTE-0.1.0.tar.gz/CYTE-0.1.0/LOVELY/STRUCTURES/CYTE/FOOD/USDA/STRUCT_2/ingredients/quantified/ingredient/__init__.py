
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

from fractions import Fraction

PORTION = 100

def CALC (
	FOOD_NUTRIENT,
	USDA_FOOD_DATA_CALCULATED
):
	NAME = FOOD_NUTRIENT ["nutrient"] ["name"]
	'''
		find the struct with that name,
		in the structs DB
	'''
	
	SERVINGS_PER_PACKAGE = Fraction (USDA_FOOD_DATA_CALCULATED ["defined"] ["servings per package"])
		
	AMOUNT_PER_PACKAGE = (
		Fraction (NUTRIENT ["amount"]) /
		PORTION				
	) * SERVINGS_PER_PACKAGE
	
	AMOUNT_PER_SERVING = (
		Fraction (NUTRIENT ["amount"]) /
		PORTION				
	) * Fraction (AMOUNT_IN_SERVING)

	return {
		"name": NAME,
		
		"quantity per package": {
			
		}
	}