



'''
	import CYTE.FOOD.USDA.API.ONE as USDA_FOOD_API
	FOOD = USDA_FOOD_API.FIND (
		1960255,
		API_KEY = ""
	)
'''

'''
	curl https://api.nal.usda.gov/fdc/v1/food/1960255?api_key=DEMO_KEY
'''

import json
import requests

import CYTE.FOOD.USDA.API.ONE.ASSERTIONS.BRANDED as ASSERTIONS_BRANDED
import CYTE.FOOD.USDA.API.ONE.ASSERTIONS.FOUNDATIONAL as ASSERTIONS_FOUNDATIONAL


def FIND (
	FDC_ID,
	API_KEY = "",
	
	KIND = "BRANDED"
):
	HOST = 'https://api.nal.usda.gov'
	PATH = f'/fdc/v1/food/{ FDC_ID }'
	PARAMS = f'?api_key={ API_KEY }'
	
	ADDRESS = HOST + PATH + PARAMS
	
	print ("REQUEST IS ABOUT TO BE SENT.", json.dumps ({ "ADDRESS": ADDRESS }, indent = 2))

	r = requests.get (ADDRESS)
	# print ("GOT RESPONSE:", r.status_code)
	
	DATA = json.loads (r.text)

	if (KIND == "BRANDED"):
		ASSERTIONS_BRANDED.RUN (DATA)
		
	elif (KIND == "FOUNDATIONAL"):
		ASSERTIONS_FOUNDATIONAL.RUN (DATA)

	return {
		"DATA": DATA,
		"SOURCE": {
			"NAME": "USA USDA",
			"LINK": f"https://fdc.nal.usda.gov/fdc-app.html#/food-details/{ FDC_ID }/nutrients",
			"TEXT": "U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, 2019. fdc.nal.usda.gov."
		}
	}