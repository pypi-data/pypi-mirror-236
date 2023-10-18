


'''
import CYTE.FOOD.NIH.STRUCT_2 as STRUCT_2
RETURN = STRUCT_2.CALC ()
'''

import CYTE.SUPPLEMENTS.NIH.STRUCT_2.FORM as FORM 
import CYTE.SUPPLEMENTS.NIH.STRUCT_2.DEFINED.SERVING_SIZE_QUANTITY as DEFINED_SERVING_SIZE_QUANTITY 
import CYTE.SUPPLEMENTS.NIH.STRUCT_2.ingredients.quantified as INGREDIENTS_QUANTIFIED 

def CALC (NIH_SUPPLEMENT_DATA):
	assert ("fullName" in NIH_SUPPLEMENT_DATA)
	assert ("brandName" in NIH_SUPPLEMENT_DATA)
	assert ("id" in NIH_SUPPLEMENT_DATA)

	RETURN = {
		"product": {
			"name":	NIH_SUPPLEMENT_DATA ["fullName"],
			"DSLD": NIH_SUPPLEMENT_DATA ["id"],
			"UPC": NIH_SUPPLEMENT_DATA ["upcSku"]			
		},
		
		"brand": {
			"name":	NIH_SUPPLEMENT_DATA ["brandName"]
		},
		
		"form": {},
		
		"defined": {
			"serving size": {}
		},
		
		"ingredients": {
			"quantified": [],
			"unquantified": []
		}
	}
	
	RETURN ["form"]["unit"] = FORM.CALC_UNIT (NIH_SUPPLEMENT_DATA)
	RETURN ["form"]["quantity"] = FORM.CALC_QUANTITY (NIH_SUPPLEMENT_DATA)

	RETURN ["defined"]["serving size"]["quantity"] = DEFINED_SERVING_SIZE_QUANTITY.CALC (
		NIH_SUPPLEMENT_DATA
	)
	
	RETURN ["ingredients"]["quantified"] = INGREDIENTS_QUANTIFIED.CALC (
		NIH_SUPPLEMENT_DATA,
		RETURN
	)
	
	RETURN ["ingredients"]["unquantified"] = NIH_SUPPLEMENT_DATA [
		"otheringredients"
	] [ "ingredients" ]

	return RETURN