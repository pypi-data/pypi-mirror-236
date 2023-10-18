


def RUN (DATA):
	assert ("description" in DATA)
	assert ("foodNutrients" in DATA)
	assert ("packageWeight" in DATA)
	
	
	
	#
	#	IF MORE THAN ONE
	#
	assert ("ingredients" in DATA)
	
	#
	#	RECOMMENDATIONS DATA
	#
	assert ("servingSize" in DATA)
	assert ("servingSizeUnit" in DATA)
	
	#
	#	SALES DATA
	#
	assert ("gtinUpc" in DATA)
	assert ("fdcId" in DATA)
	assert ("brandOwner" in DATA)
	assert ("brandName" in DATA)

	return;