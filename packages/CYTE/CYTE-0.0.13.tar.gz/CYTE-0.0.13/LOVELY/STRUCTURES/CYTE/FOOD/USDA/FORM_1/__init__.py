


'''
import CYTE.FOOD.USDA.FORM_1 as FORM_1
RETURN = FORM_1.MAKE ()
'''

def MAKE (
	USDA_FOOD_DATA
):
	REFORMATTED = {
		"PRODUCT": {
			"NAME": "",
			"FDC ID": "",
			"UPC": ""
		}
	}

	NOTES = []

	if ("description" in USDA_FOOD_DATA):
		REFORMATTED ["PRODUCT"] ["NAME"] = USDA_FOOD_DATA ["description"]
	else:
		NOTES.append ("'description' was not found.")
	
	if ("fdcId" in USDA_FOOD_DATA):
		REFORMATTED ["PRODUCT"] ["FDC ID"] = USDA_FOOD_DATA ["fdcId"]
	else:
		NOTES.append ("'fdcId' was not found.")
	
	#assert ("foodNutrients" in USDA_FOOD_DATA)
	#FOOD_NUTRIENTS = USDA_FOOD_DATA ["foodNutrients"]
	
	#assert ("labelNutrients" in USDA_FOOD_DATA)
	#LABEL_NUTRIENTS	= USDA_FOOD_DATA ["labelNutrients"]

	

	return {
		"FORM": REFORMATTED,
		"NOTES": NOTES
	}