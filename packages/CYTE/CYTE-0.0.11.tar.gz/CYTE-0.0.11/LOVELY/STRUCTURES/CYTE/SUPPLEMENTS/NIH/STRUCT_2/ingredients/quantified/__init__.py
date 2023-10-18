


from fractions import Fraction

import CYTE.MASS.SWAP as MASS_SWAP

def CALC_INGREDIENT (INGREDIENT, RETURN):
	DEFINED = RETURN ["defined"];
	FORM = RETURN ["form"];

	assert ("name" in INGREDIENT)
	NAME = INGREDIENT ["name"]

	AMOUNT = ""
	if (
		len (INGREDIENT ["quantity"]) == 1 and
		INGREDIENT ["quantity"][0]["servingSizeQuantity"] == DEFINED ["serving size"]["quantity"] and
		Fraction (
			FORM ["quantity"], 
			INGREDIENT ["quantity"][0]["servingSizeQuantity"]
		).denominator == 1
	):
		AMOUNT = Fraction (
			INGREDIENT ["quantity"][0]["quantity"],
			DEFINED ["serving size"]["quantity"]
		)
		
	else:
		raise Exception ("Ingredient amount could not be calculated.")


	UNIT = INGREDIENT ["quantity"][0]["unit"]

	
	

	return {
		"name": NAME,
		"quantity per form": {
			"form": FORM ["unit"],
			"amount": str (AMOUNT),
			"unit": UNIT
		},
		"quantity per form, in grams": {
			"form": FORM ["unit"],
			"amount": str (MASS_SWAP.START ([ AMOUNT, UNIT ], "grams")),
			"unit": "g"
		}
	}


def CALC (
	NIH_SUPPLEMENT_DATA,
	RETURN
):
	assert ("ingredientRows" in NIH_SUPPLEMENT_DATA)
	
	INGREDIENTS = []
	
	INGREDIENT_ROWS = NIH_SUPPLEMENT_DATA ["ingredientRows"]
	for INGREDIENT in INGREDIENT_ROWS:
		INGREDIENTS.append (CALC_INGREDIENT (INGREDIENT, RETURN))

	return INGREDIENTS