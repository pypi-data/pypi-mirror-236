
'''
	python3 STATUS.py "STRUCTS/SCAN/NAMES/contains_substring/STATUS_DYNAMIC_1.py"
'''

import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.NAMES.contains_substring as STRUCTS_WHERE_NAME_CONTAINS_SUBSTRING

def CHECK_1 ():	
	STRUCTS = STRUCTS_WHERE_NAME_CONTAINS_SUBSTRING.FIND (
		ACCESS.DB (),
		"VITAMIN B"
	)
	STRUCTS_VAR_CAPS = STRUCTS_WHERE_NAME_CONTAINS_SUBSTRING.FIND (
		ACCESS.DB (),
		"VItAmIn B"
	)
	STRUCTS_LOWER = STRUCTS_WHERE_NAME_CONTAINS_SUBSTRING.FIND (
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
	STRUCTS = STRUCTS_WHERE_NAME_CONTAINS_SUBSTRING.FIND (ACCESS.DB (), "Magnesium")
	
	REGIONS = []
	for STRUCT in STRUCTS:
		print (STRUCT)
		REGIONS.append (STRUCT ["region"])

	assert (len (STRUCTS) >= 1);
	assert (30 in REGIONS);


	return;
	
CHECKS = {
	"Structs have a name that contains 'vitamin b'": CHECK_1,
	"Struct has a name that contains 'Magnesium'": CHECK_2
}