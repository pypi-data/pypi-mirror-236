

'''
	"servingSize": 240,
	"servingSizeUnit": "ml",
'''

from fractions import Fraction

import CYTE.volume.swap as VOLUME_SWAP
	
def CALC (USDA_FOOD_DATA, USDA_FOOD_DATA_CALCULATED):
	assert ("servingSize" in USDA_FOOD_DATA)
	assert ("servingSizeUnit" in USDA_FOOD_DATA)
	
	SERVING_SIZE_UNIT = USDA_FOOD_DATA ["servingSizeUnit"]
	SERVING_SIZE = USDA_FOOD_DATA ["servingSize"]
	
	import CYTE._interpret.unit_kind as UNIT_KIND
	KIND = UNIT_KIND.CALC (SERVING_SIZE_UNIT)
	
	if (KIND == "volume"):
		if ("per package, in liters" in USDA_FOOD_DATA_CALCULATED ["volume"]):
			LITERS_PER_SERVING = VOLUME_SWAP.START ([ SERVING_SIZE, SERVING_SIZE_UNIT ], "LITER")
			
			SERVINGS_PER_PACKAGE = str (
				float (
					Fraction (USDA_FOOD_DATA_CALCULATED ["volume"] ["per package, in liters"]) /
					Fraction (LITERS_PER_SERVING)
				)
			)
		
		else:
			print (USDA_FOOD_DATA_CALCULATED)
		
			raise Exception ('serving size is in volume, but package volume is not known.')
		
		
	elif (KIND == "mass"):
		pass;
		
	else:
		raise Exception (f'Kind, received "{ KIND }", of serving size unit needs to be "volume" or "mass".')
	
	

	return SERVINGS_PER_PACKAGE