

'''
"servingSize": 240,
"servingSizeUnit": "ml",
'''

from fractions import Fraction

def CALC (USDA_FOOD_DATA, USDA_FOOD_DATA_CALCULATED):
	assert ("servingSize" in USDA_FOOD_DATA)
	assert ("servingSizeUnit" in USDA_FOOD_DATA)
	
	
	
	SERVINGS_PER_PACKAGE = str (
		float (
			Fraction (PACKAGE_MASS ["SYSTEM INTERNATIONAL"] [0]) /
			Fraction (SERVINGS ["SIZE"] ["SYSTEM INTERNATIONAL"][0])
		)
	)

	return;