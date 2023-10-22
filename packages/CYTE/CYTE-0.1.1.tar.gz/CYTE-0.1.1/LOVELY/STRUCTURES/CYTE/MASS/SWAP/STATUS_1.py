
'''
	python3 STATUS.py "MASS/SWAP/STATUS_1.py"
'''

import CYTE.MASS.SWAP as MASS_SWAP

from fractions import Fraction

def CHECK_1 ():
	assert (float (MASS_SWAP.START ([ 453.59237, "GRAMS" ], "POUNDS")) == 1.0)
	assert (float (MASS_SWAP.START ([ 453.59237, "grams" ], "pounds")) == 1.0)	
	
	assert (float (MASS_SWAP.START ([ 10, "OUNCES" ], "POUNDS")) == 0.625)
	assert (float (MASS_SWAP.START ([ 10, "OUNCES" ], "GRAMS")) == 283.49523125)	

	


	return;
	
def CHECK_2 ():
	assert (
		MASS_SWAP.START ([ 10, "mcg" ], "g") == 
		Fraction (1, 100000)
	)	
	assert (
		MASS_SWAP.START ([ 10, "mcg" ], "mg") == 
		Fraction (1, 100)
	)	
	
	assert (
		MASS_SWAP.START ([ 10, "mg" ], "g") == 
		Fraction (1, 100)
	)
	
	assert (
		MASS_SWAP.START ([ 10, "g" ], "mg") == 
		Fraction (10000, 1)
	)
	assert (
		MASS_SWAP.START ([ 10, "g" ], "mcg") == 
		Fraction (10000000, 1)
	)
	
CHECKS = {
	"CHECK 1": CHECK_1,
	"CHECK 2": CHECK_2
}