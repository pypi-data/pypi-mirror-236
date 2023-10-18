
'''
	python3 STATUS.py "STRUCTS/SCAN/NAMES_CONTAIN/STATUS_1.py"
'''

from CYTE.STRUCTS.SCAN.NAMES_CONTAIN import STRUCTS_NAMES_CONTAIN

def CHECK_1 ():	
	STRUCTS = STRUCTS_NAMES_CONTAIN ("VITAMIN B")
	STRUCTS_VAR_CAPS = STRUCTS_NAMES_CONTAIN ("VItAmIn B")
	STRUCTS_LOWER = STRUCTS_NAMES_CONTAIN ("vitamin b")

	for STRUCT in STRUCTS:
		print (STRUCT)

	assert (len (STRUCTS) >= 6);

	assert (len (STRUCTS) == len (STRUCTS_VAR_CAPS))
	assert (len (STRUCTS) == len (STRUCTS_LOWER))

	return;
	
def CHECK_1 ():	
	STRUCTS = STRUCTS_NAMES_CONTAIN ("Magnesium")
	
	REGIONS = []
	for STRUCT in STRUCTS:
		print (STRUCT)
		REGIONS.append (STRUCT ["REGION"])

	assert (len (STRUCTS) >= 1);
	assert (30 in REGIONS);


	return;
	
CHECKS = {
	"The struct has a name that contains 'vitamin b'": CHECK_1
}