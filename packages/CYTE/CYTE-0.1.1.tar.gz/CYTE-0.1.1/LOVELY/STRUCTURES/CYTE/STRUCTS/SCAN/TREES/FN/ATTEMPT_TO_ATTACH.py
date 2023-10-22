


'''
{
	"PART OF": "",
	"names": [
		"TOTAL LIPID (FAT)"
	],
	"region": 3,
	"QUANTIFIED INGREDIENTS": [
		{
			"PART OF": 3,
			"names": [
				"FATTY ACIDS, TOTAL SATURATED"
			],
			"region": 4
		}	
	
	]
},

FOR EXAMPLE, TRYING TO FIND "LIPIDS"
'''
def START (TO_FIND, BRANCHES):
	print ("ATTEMPTING TO ATTACH", TO_FIND ["names"])

	

	for BRANCH in BRANCHES:	
		if (BRANCH ["region"] == TO_FIND ["PART OF"][0]):
			if ("includes" not in BRANCH):
				BRANCH ["includes"] = []
		
			BRANCH ["includes"].append (TO_FIND)
			print ("	ATTACHED:", TO_FIND ["names"])
		
			return True
			
		if ("includes" in BRANCH and len (BRANCH ["includes"])):
			ATTACHED = START (TO_FIND, BRANCH ["includes"])
			if (ATTACHED == True):
				return True;

	return False