



'''
	python3 STATUS.py "SUPPLEMENTS/NIH/STRUCT_2/STATUS_TABLETS/PlantFusion_Calcium_261967.py"
'''

import json

import CYTE.SUPPLEMENTS.NIH.EXAMPLES as NIH_EXAMPLES
import CYTE.SUPPLEMENTS.NIH.STRUCT_2 as STRUCT_2

def CHECK_1 ():
	EXAMPLE = NIH_EXAMPLES.RETRIEVE ("TABLETS/CALCIUM_261967.JSON")
	RETURN = STRUCT_2.CALC (EXAMPLE)
	
	print ("RETURN:", json.dumps (RETURN, indent = 4))
	
	assert ("product name" in RETURN)
	assert ("DSLD ID" in RETURN)
	
	assert ("brand" in RETURN)
	assert ("name" in RETURN ["brand"])
	assert (type (RETURN ["brand"]["name"]) == str)
	
	
	
	
CHECKS = {
	"CALCIUM 261967": CHECK_1
}