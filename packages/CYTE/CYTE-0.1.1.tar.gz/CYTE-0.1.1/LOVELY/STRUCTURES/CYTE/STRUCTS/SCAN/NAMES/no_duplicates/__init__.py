
'''
raises an exception is a duplicate is found.
'''

'''
import CYTE.STRUCTS.DB.ACCESS as ACCESS
from CYTE.STRUCTS.SCAN.NAMES.no_duplicates import STRUCTS_NAMES_NO_DUPLICATES
STRUCTS_NAMES_NO_DUPLICATES (
	ACCESS.DB ()
)
'''

import CYTE.STRUCTS.SCAN as STRUCT_SCAN

def STRUCTS_NAMES_NO_DUPLICATES (
	STRUCTS_DB
):
	NAMES = []

	def FOR_EACH (STRUCT):
		STRUCT_NAMES = STRUCT ["names"]
			
		for STRUCT_NAME in STRUCT_NAMES:
			STRUCT_NAME = STRUCT_NAME.lower ()
		
			if (STRUCT_NAME in NAMES):
				raise Exception (f"duplicate found: { STRUCT_NAME }")
		

	STRUCTS = STRUCT_SCAN.START (
		FOR_EACH = FOR_EACH
	)

