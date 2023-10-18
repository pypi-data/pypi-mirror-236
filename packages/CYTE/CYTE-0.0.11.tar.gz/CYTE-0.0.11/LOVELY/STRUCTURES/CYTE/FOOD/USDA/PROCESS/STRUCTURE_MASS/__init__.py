


'''
	import CYTE.FOOD.USDA.PROCESS.STUCTURE_MASS as STUCTURE_MASS
	STUCTURE_MASS.PROCESS ()
'''


'''
	NUTRIENT DATA:
		PORTION = [ 100, "g" ]
	
		"servingSize": 28,
		"servingSizeUnit": "g",
	
		{
			"type": "FoodNutrient",
			"nutrient": {
				"id": 1003,
				"number": "203",
				"name": "Protein",
				"rank": 600,
				"unitName": "g"
			},
			"foodNutrientDerivation": {
				"id": 70,
				"code": "LCCS",
				"description": "Calculated from value per serving size measure"
			},
			"id": 22687261,
			"amount": 21.43
		}
		
		[ 25.45, "g" ]
'''

#
#	THIS SEEMS TO BE AN UNREPORTED CONSTANT.
#
PORTION = [ 100, "g" ]

def PROCESS (
	NUTRIENT_DATA = {}
):
	return;