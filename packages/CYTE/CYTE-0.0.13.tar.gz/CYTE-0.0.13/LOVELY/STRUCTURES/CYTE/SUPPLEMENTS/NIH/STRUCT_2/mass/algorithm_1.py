


'''
	"mass of quantified ingredients": {
		"caculated per package, ignoring IU": {
			
		}
	}
'''

from fractions import Fraction

def CALC (NIH_SUPPLEMENT_DATA, RETURN):
	QUANTITY_OF_FORM = RETURN ["form"]["quantity"]
	QUANTIFIED_INGREDIENTS = RETURN ["ingredients"]["quantified"]
	
	QUANTITY_IN_GRAMS = 0
	
	SKIPPED = []
	
	for INGREDIENT in QUANTIFIED_INGREDIENTS:
		AMOUNT = INGREDIENT [
			"quantity per form, in grams"
		]["amount"];
		if (AMOUNT == "?"):
			SKIPPED.append (INGREDIENT ["name"])
			
		else:
			QUANTITY_IN_GRAMS += Fraction (INGREDIENT [
				"quantity per form, in grams"
			]["amount"])
		
	#print ("QUANTITY_OF_FORM:", QUANTITY_OF_FORM)	
	
	return {
		"caculated per package, ignoring IU, RAE, DFE, in grams": str (QUANTITY_IN_GRAMS),
		"caculated per form, ignoring IU, RAE, DFE in grams": str (Fraction (QUANTITY_IN_GRAMS, QUANTITY_OF_FORM)),
		"skipped": SKIPPED
	}