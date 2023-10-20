


'''
{
	"PART OF": "",
	"NAMES": [
		"TOTAL LIPID (FAT)"
	],
	"REGION": 3,
	"QUANTIFIED INGREDIENTS": [
		{
			"PART OF": 3,
			"NAMES": [
				"FATTY ACIDS, TOTAL SATURATED"
			],
			"REGION": 4
		}	
	
	]
},

FOR EXAMPLE, TRYING TO FIND "LIPIDS"
'''
def START (TO_FIND, BRANCHES):
	print ("ATTEMPTING TO ATTACH", TO_FIND ["NAMES"])

	

	for BRANCH in BRANCHES:	
		if (BRANCH ["REGION"] == TO_FIND ["PART OF"][0]):
			if ("includes" not in BRANCH):
				BRANCH ["includes"] = []
		
			BRANCH ["includes"].append (TO_FIND)
			print ("	ATTACHED:", TO_FIND ["NAMES"])
		
			return True
			
		if ("includes" in BRANCH and len (BRANCH ["includes"])):
			ATTACHED = START (TO_FIND, BRANCH ["includes"])
			if (ATTACHED == True):
				return True;

	return False