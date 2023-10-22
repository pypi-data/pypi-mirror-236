

UNIT_LEGEND = {	
	"oz": "OUNCES",
	"lb": "POUNDS",
	
	"g": "GRAMS",
	"kg": "KILOGRAMS",
	"mg": "MICROGRAMS",
	"mcg": "MILLIGRAMS"
}


'''
	lb -> g

	oz -> g
	
	g -> g
'''

from fractions import Fraction
import CYTE.MASS.SWAP as MASS_SWAP

'''
	
'''
def INTERPRET (PARAM):
	if (type (PARAM) != str):
		return [ "?", "POUNDS" ]
		
	RETURNS = {}
		
	SPLITS = PARAM.split ("/")
	for SPLIT in SPLITS:
		[ AMOUNT, UNIT ] = SPLIT.split (" ")
		
		print (AMOUNT, UNIT)
		
		assert (UNIT in UNIT_LEGEND)
		SPRUCED_UNIT = UNIT_LEGEND [ UNIT ]
		
		RETURNS [ SPRUCED_UNIT ] = AMOUNT
	
	
	print ("RETURNS", RETURNS)
	
	#
	#	IF GRAMS IS NOT IN RETURNS,
	# 	THEN TRY TO FIND ANOTHER UNIT THAT
	#	CAN BE SWAPPED INTO GRAMS.
	#
	if ("GRAMS" not in RETURNS):
		if ("OUNCES" in RETURNS):
			AMOUNT_OF_OUNCES = RETURNS ["OUNCES"]
		
			RETURNS ["GRAMS"] = str (float (
				MASS_SWAP.START (
					[ AMOUNT, "OUNCES" ],
					"GRAMS"
				)
			))
			
		elif ("POUNDS" in RETURNS): 
			AMOUNT = RETURNS ["GRAMS"]
		
			RETURNS ["GRAMS"] = str (float (
				MASS_SWAP.START (
					[ AMOUNT, "POUNDS" ],
					"GRAMS"
				)
			))
			
		else:
			raise Exception ("COULD NOT DETERMINE PACKAGE MASS IN GRAMS.")

	assert ("GRAMS" in RETURNS)

	
	print ("RETURNS:", RETURNS)
	
	#
	#	IF POUNDS IS NOT IN RETURNS,
	# 	THEN TRY TO FIND ANOTHER UNIT THAT
	#	CAN BE SWAPPED INTO POUNDS.
	#
	if ("POUNDS" not in RETURNS):
		if ("OUNCES" in RETURNS):
			AMOUNT = RETURNS ["OUNCES"]
		
			RETURNS ["POUNDS"] = str (float (
				MASS_SWAP.START (
					[ AMOUNT, "OUNCES" ],
					"POUNDS"
				)
			))
			
		elif ("GRAMS" in RETURNS): 
			AMOUNT = RETURNS ["GRAMS"]
		
			RETURNS ["POUNDS"] = str (float (
				MASS_SWAP.START (
					[ AMOUNT, "GRAMS" ],
					"POUNDS"
				)
			))
			
		else:
			raise Exception ("COULD NOT DETERMINE PACKAGE MASS IN POUNDS.")

	assert ("POUNDS" in RETURNS)

	return RETURNS

