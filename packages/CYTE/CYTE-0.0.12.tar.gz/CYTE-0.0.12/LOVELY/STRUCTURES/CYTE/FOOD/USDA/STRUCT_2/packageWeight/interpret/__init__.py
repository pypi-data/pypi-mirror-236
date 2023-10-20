



UNIT_LEGEND = {	
	"oz": "OUNCES",
	"lb": "POUNDS",

	"kg": "KILOGRAMS",
	"g": "GRAMS",
	"mg": "MICROGRAMS",
	"mcg": "MILLIGRAMS",
	
	"fl oz": "FLUID OUNCES",
	"ml": "MILLILITERS"
}

VOLUME_UNITS = [ "fl oz", "ml" ]
MASS_UNITS = [ "oz", "lb", "g", "kg", "mg", "mcg" ]


'''
	lb -> g

	oz -> g
	
	g -> g
'''

from fractions import Fraction
import CYTE.MASS.SWAP as MASS_SWAP
import CYTE.volume.swap as VOLUME_SWAP

import json

def SPLIT_LABEL (LABEL):
	ONE = ""
	TWO = ""

	PART_2 = False
	
	SELECTOR = 0
	LAST_INDEX = len (LABEL) - 1
	while (SELECTOR <= LAST_INDEX):
		CHARACTER = LABEL [SELECTOR]
		
		print ("CHARACTER:", CHARACTER)
	
		if (CHARACTER == " "):
			SELECTOR += 1
			break;
		else:	
			ONE += CHARACTER
			
			
		SELECTOR += 1
	
		
	while (SELECTOR <= LAST_INDEX):
		CHARACTER = LABEL [SELECTOR]
		TWO += CHARACTER
		SELECTOR += 1
	
	return [ ONE.lower (), TWO.lower () ]


def INTERPRET (PARAM):
	if (type (PARAM) != str):
		return [ "?", "POUNDS" ]
		
	RETURNS = {}
		
	SPLITS = PARAM.split ("/")
	
	print ("SPLITS:", SPLITS)
	
	VOLUME_IS_KNOWN = False
	MASS_IS_KNOWN = False
	
	for SPLIT in SPLITS:
		[ AMOUNT, UNIT ] = SPLIT_LABEL (SPLIT)
		#[ AMOUNT, UNIT ] = SPLIT.split (" ")
		
		print (AMOUNT, UNIT)
		
		print (
			json.dumps (
				{
					"AMOUNT": AMOUNT, 
					"UNIT": UNIT 
				}, 
				indent = 4
			)
		)
		
		assert (UNIT in UNIT_LEGEND), f"unit: '{ UNIT }'"
		
		if (UNIT in VOLUME_UNITS):
			VOLUME_IS_KNOWN = True
		elif (UNIT in MASS_UNITS):
			MASS_IS_KNOWN = True;
		else:
			print ("unit:", UNIT)
			raise Exception ("Unit was not found in volume of mass units.")
		
		
		SPRUCED_UNIT = UNIT_LEGEND [ UNIT ]
		
		RETURNS [ SPRUCED_UNIT ] = AMOUNT
	
	
	print ("VOLUME_IS_KNOWN:", VOLUME_IS_KNOWN)
	print ("MASS_IS_KNOWN:", MASS_IS_KNOWN)
	print ("RETURNS", RETURNS)

	if (MASS_IS_KNOWN):
	
		
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
				raise Exception ("'pounds' per package could not be calculated.")

		assert ("POUNDS" in RETURNS)
		
	if (VOLUME_IS_KNOWN):
		#
		#	plan:
		#		calculate ([ "liters", "fluid ounces" ])
		#
	
		def calculate ():
			return;
		
	
		if ("LITERS" not in RETURNS):
			if ("FLUID OUNCES" in RETURNS):
				UNIT_1 = "FLUID OUNCES"
				UNIT_2 = "LITERS"

				AMOUNT = RETURNS [ UNIT_1 ]
				RETURNS [ UNIT_2 ] = str (float (
					VOLUME_SWAP.START (
						[ AMOUNT, UNIT_1 ],
						UNIT_2
					)
				))
				
			elif ("MILLILITERS" in RETURNS): 
				UNIT_1 = "MILLILITERS"
				UNIT_2 = "LITERS"

				AMOUNT = RETURNS [ UNIT_1 ]
				RETURNS [ UNIT_2 ] = str (float (
					VOLUME_SWAP.START (
						[ AMOUNT, UNIT_1 ],
						UNIT_2
					)
				))
				
			else:
				raise Exception ("'liters' per package could not be calculated.")

	return RETURNS

