

import CYTE.INTEGER.STRING_IS_INTEGER as STRING_IS_INTEGER

def CALC (NIH_SUPPLEMENT_DATA):
	assert ("netContents" in NIH_SUPPLEMENT_DATA)
	NET_CONTENTS = NIH_SUPPLEMENT_DATA ["netContents"]

	assert ("servingSizes" in NIH_SUPPLEMENT_DATA)
	SERVING_SIZES = NIH_SUPPLEMENT_DATA ["servingSizes"]

	assert ("servingsPerContainer" in NIH_SUPPLEMENT_DATA)
	SERVINGS_PER_CONTAINER = NIH_SUPPLEMENT_DATA ["servingsPerContainer"]

	if (
		len (NET_CONTENTS) == 1 and
		STRING_IS_INTEGER.CHECK (SERVINGS_PER_CONTAINER) and
		len (SERVING_SIZES) == 1 and
		SERVING_SIZES [0] ["minQuantity"] == SERVING_SIZES [0] ["maxQuantity"] and
		NET_CONTENTS [0] ["quantity"] / int (SERVINGS_PER_CONTAINER) == SERVING_SIZES [0] ["maxQuantity"]
	):
		return SERVING_SIZES [0] ["maxQuantity"]
		
	raise Exception ("The defined serving size of the supplement could not be calculated.")
		

			#
			#	This is necessary for composition calculations,
			#	but recommendations should be determined elsewhere.
			#
			#	if:
			#		len (netContents)  == 1 and
			#
			#		import CYTE.INTEGER.STRING_IS_INTEGER as STRING_IS_INTEGER
			#		STRING_IS_INTEGER.CHECK (servingsPerContainer)
			#
			#		len (servingSizes) == 1
			#
			#		servingSizes [0].minQuantity == servingSizes[0].maxQuantity
			#
			#		netContents [0].quantity / int (servingsPerContainer) == servingSizes[0].maxQuantity
			#
			#	then:
			#		"quantity" = servingSizes[0].maxQuantity
			#		"quantity" = 3
			#
			
	

	return;