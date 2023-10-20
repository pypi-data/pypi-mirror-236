


import CYTE.FOOD.USDA.STRUCT_2.energy as ENERGY
import CYTE.FOOD.USDA.STRUCT_2.mass as MASS

import CYTE.FOOD.USDA.STRUCT_2.packageWeight as PACKAGE_WEIGHT
import CYTE.FOOD.USDA.STRUCT_2.ingredients.quantified as QUANTIFIED_INGREDIENTS
import CYTE.FOOD.USDA.STRUCT_2.servings as SERVINGS


def CALC (USDA_FOOD_DATA):
	RETURN = {
		"product": {
			"name":	USDA_FOOD_DATA ["description"],
			"FDC ID": str (USDA_FOOD_DATA ["fdcId"]),
			"UPC": USDA_FOOD_DATA ["gtinUpc"]			
		},
		
		"brand": {
			"name":	USDA_FOOD_DATA ["brandName"],
			"owner": USDA_FOOD_DATA ["brandOwner"]
		},
		
		"defined": {
			"serving size": {}
		},
		
		"mass": {},
		"volume": {},
	
		"ingredients": {
			"quantified": [],
			"unquantified": {
				
			},
			"unquantified string": USDA_FOOD_DATA ["ingredients"]
		}
		
	}
	
	INTERPRETTED_PACKAGE_WEIGHT = PACKAGE_WEIGHT.INTERPRET (USDA_FOOD_DATA)
	if ("mass" in INTERPRETTED_PACKAGE_WEIGHT):
		RETURN ["mass"] = INTERPRETTED_PACKAGE_WEIGHT ["mass"]

	if ("volume" in INTERPRETTED_PACKAGE_WEIGHT):
		RETURN ["volume"] = INTERPRETTED_PACKAGE_WEIGHT ["volume"]

	RETURN ["defined"] ["serving size"] = SERVINGS.CALC (USDA_FOOD_DATA)

	RETURN ["ingredients"]["quantified"] = QUANTIFIED_INGREDIENTS.CALC (
		USDA_FOOD_DATA,
		RETURN
	)

	return RETURN