



'''
	python3 STATUS.py "FOOD/USDA/FORM_1/CALC/PACKAGE_MASS/STATUS_1.py"
'''

import CYTE.FOOD.USDA.FORM_1.CALC.PACKAGE_MASS as PACKAGE_MASS

CHECKS = {}

def CHECK_1 ():
	MASS = PACKAGE_MASS.PROCESS (
		PACKAGE_WEIGHT = "4 oz/113 g"
	)

	assert (MASS ["REPORTED"] == "4 oz/113 g")
	assert (MASS ["SYSTEM INTERNATIONAL"][0] == "113")
	assert (MASS ["SYSTEM INTERNATIONAL"][1] == "g")

CHECKS ["oz & g -> g"] = CHECK_1
	
def CHECK_2 ():
	MASS = PACKAGE_MASS.PROCESS (
		PACKAGE_WEIGHT = "4 oz"
	)

	assert (MASS ["REPORTED"] == "4 oz")
	assert (MASS ["SYSTEM INTERNATIONAL"][0] == "113.3980925")
	assert (MASS ["SYSTEM INTERNATIONAL"][1] == "g")
	
CHECKS ["oz -> g"] = CHECK_2
	
	
def CHECK_3 ():
	MASS = PACKAGE_MASS.PROCESS (
		PACKAGE_WEIGHT = "113 g"
	)

	assert (MASS ["REPORTED"] == "113 g")
	assert (MASS ["SYSTEM INTERNATIONAL"][0] == "113")
	assert (MASS ["SYSTEM INTERNATIONAL"][1] == "g")
	
CHECKS ["g -> g"] = CHECK_3
	
