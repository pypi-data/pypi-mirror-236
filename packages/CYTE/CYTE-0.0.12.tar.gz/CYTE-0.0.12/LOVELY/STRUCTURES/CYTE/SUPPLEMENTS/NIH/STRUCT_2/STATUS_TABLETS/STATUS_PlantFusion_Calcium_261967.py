



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
	
	assert (RETURN ["product"]["name"] == "Vegan Plant-Based Calcium 1,000 mg")
	assert (RETURN ["product"]["DSLD"] == "261967")

	
	assert ("brand" in RETURN)
	assert ("name" in RETURN ["brand"])
	assert (type (RETURN ["brand"]["name"]) == str)
	
	assert (
		RETURN ["defined"] ==
		{
			"serving size": {
				"quantity": 3
			}
		}
	)
	assert (
		RETURN ["form"] ==
		{
			"unit": "Tablet",
			"quantity": 90
		}
	)
	
	assert (len (RETURN ["ingredients"]["quantified"]) == 9)
	assert (
		RETURN ["ingredients"]["quantified"][0] ==
		{
			"name": "Vitamin D3",
			"quantity per form": {
				"form": "Tablet",
				"amount": "20/3",
				"unit": "mcg"
			},
			"quantity per form, in grams": {
				"form": "Tablet",
				"amount": "1/150000",
				"unit": "g"
			}
		}
	)
	
	assert (len (RETURN ["ingredients"]["unquantified"]) == 4)

	assert (
		RETURN ["mass of quantified ingredients"]["caculated per package, ignoring IU, in grams"] ==
		"580153/375000"
	)
	assert (
		RETURN ["mass of quantified ingredients"]["caculated per form, ignoring IU, in grams"] ==
		"580153/33750000"
	)

	
	
CHECKS = {
	"CALCIUM 261967": CHECK_1
}