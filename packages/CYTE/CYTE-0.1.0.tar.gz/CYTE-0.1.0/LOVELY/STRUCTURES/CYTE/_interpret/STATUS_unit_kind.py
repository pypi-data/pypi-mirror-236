



'''
	python3 STATUS.py "_interpret/STATUS_unit_kind.py"
'''

import CYTE._interpret.unit_kind as UNIT_KIND

from fractions import Fraction

def CHECK_1 ():
	assert (UNIT_KIND.CALC ("ml") == "volume")
	assert (UNIT_KIND.CALC ("fl oz") == "volume")
	
	assert (UNIT_KIND.CALC ("GRAM") == "mass")
	assert (UNIT_KIND.CALC ("gram") == "mass")
	
CHECKS = {
	"CHECK 1": CHECK_1
}
	


