



'''
	python3 STATUS.py "SUPPLEMENTS/NIH/STRUCT_2/STATUS_COATED_TABLETS/DEVA_MULTIVITAMIN_276336.py"
'''

import json

import CYTE.SUPPLEMENTS.NIH.EXAMPLES as NIH_EXAMPLES
import CYTE.SUPPLEMENTS.NIH.STRUCT_2 as STRUCT_2

def CHECK_1 ():
	EXAMPLE = NIH_EXAMPLES.RETRIEVE ("COATED TABLETS/MULTIVITAMIN_276336.JSON")
	RETURN = STRUCT_2.CALC (EXAMPLE)
	
	#print ("RETURN:", json.dumps (RETURN, indent = 4))

	#print (RETURN ["product"])

	assert (RETURN ["product"]["name"] == "Vegan Multivitamin & Mineral Supplement with Greens")
	assert (RETURN ["product"]["DSLD"] == "276336")
	
	assert (RETURN ["brand"]["name"] == "DEVA")
	assert (
		RETURN ["defined"] ==
		{
			"serving size": {
				"quantity": 1
			}
		}
	)
	assert (
		RETURN ["form"] ==
		{
			"unit": "Coated Tablet",
			"quantity": 90
		}
	)
	
	#print ("RETURN IQ:", len (RETURN ["ingredients"]["quantified"]))
	assert (len (RETURN ["ingredients"]["quantified"]) == 31) 

	#print ("RETURN IU:", len (RETURN ["ingredients"]["unquantified"]))
	assert (len (RETURN ["ingredients"]["unquantified"]) == 7) 


CHECKS = {
	"DEVA MULTIVITAMIN 276336": CHECK_1
}