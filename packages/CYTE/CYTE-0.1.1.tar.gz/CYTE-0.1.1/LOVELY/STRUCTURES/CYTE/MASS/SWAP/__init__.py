

'''
	https://www.wolframalpha.com/input?i=gram+to+pound
'''

'''
	GOAL:
		MASS ([ 432, "GRAMS" ], "POUNDS")
'''

'''
	import CYTE.MASS.SWAP as MASS_SWAP
	MASS_SWAP.START ([ 432, "GRAMS" ], "POUNDS")
'''

from fractions import Fraction 


GRAMS_TO_POUNDS = Fraction (1, Fraction (453.59237))
POUNDS_TO_OUNCES = 16

CONVERSIONS = {
	"grams": {
		"pounds": GRAMS_TO_POUNDS,
		"ounces": Fraction (GRAMS_TO_POUNDS, POUNDS_TO_OUNCES),
		
		"milligrams": Fraction (1000, 1),
		"micrograms": Fraction (1000000, 1)
	},
	"milligrams": {		
		"micrograms": Fraction (1000, 1),
		"grams": Fraction (1, 1000)
	},
	"micrograms": {
		"grams": Fraction (1, 1000000),
		"milligrams": Fraction (1, 1000)
	},
	
	"pounds": {
		"ounces": 16,
		"grams": Fraction (453.59237)
	},
	"ounces": {
		"pounds": Fraction (1, 16),
		"grams": Fraction (28.349523125)
	}
}


GROUPS = [
	[ "grams", "gram", "g" ],
	[ "milligrams", "milligram", "mg" ],
	[ "micrograms", "microgram", "mcg" ],

	[ "pounds", "pound", "lbs", "lb" ],
	[ "ounces", "ounce", "oz", "ozs" ],
]


def FIND_UNIT (TO_FIND):
	for GROUP in GROUPS:		
		for UNIT in GROUP:
			if (UNIT == TO_FIND):
				return GROUP [0]
	
	print ("unit to find:", TO_FIND)
	raise Exception ("Unit was not found.")



def START (FROM, TO_UNIT):
	[ FROM_AMOUNT, FROM_UNIT ] = FROM;

	FROM_UNIT = FIND_UNIT (FROM_UNIT.lower ())
	TO_UNIT = FIND_UNIT (TO_UNIT.lower ())

	assert (FROM_UNIT in CONVERSIONS)
	assert (TO_UNIT in CONVERSIONS [ FROM_UNIT ])

	return CONVERSIONS [ FROM_UNIT ] [ TO_UNIT ] * Fraction (FROM_AMOUNT);