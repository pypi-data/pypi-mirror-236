
'''
	python3 STATUS.py "STRUCTS/SCAN/NAMES/CONTAIN/STATUS_1.py"
'''

from CYTE.STRUCTS.SCAN.NAMES.CONTAIN import STRUCTS_NAMES_CONTAIN
import CYTE.STRUCTS.DB.ACCESS as ACCESS

def CHECK_1 ():	
	STRUCTS = STRUCTS_NAMES_CONTAIN (
		ACCESS.DB (),
		"VITAMIN B"
	)
	STRUCTS_VAR_CAPS = STRUCTS_NAMES_CONTAIN (
		ACCESS.DB (),
		"VItAmIn B"
	)
	STRUCTS_LOWER = STRUCTS_NAMES_CONTAIN (
		ACCESS.DB (),
		"vitamin b"
	)

	for STRUCT in STRUCTS:
		print (STRUCT)

	assert (len (STRUCTS) >= 6);

	assert (len (STRUCTS) == len (STRUCTS_VAR_CAPS))
	assert (len (STRUCTS) == len (STRUCTS_LOWER))

	return;
	
def CHECK_2 ():	
	STRUCTS = STRUCTS_NAMES_CONTAIN (ACCESS.DB (), "Magnesium")
	
	REGIONS = []
	for STRUCT in STRUCTS:
		print (STRUCT)
		REGIONS.append (STRUCT ["REGION"])

	assert (len (STRUCTS) >= 1);
	assert (30 in REGIONS);


	return;
	
CHECKS = {
	"Structs have a name that contains 'vitamin b'": CHECK_1,
	"Struct has a name that contains 'Magnesium'": CHECK_2
}