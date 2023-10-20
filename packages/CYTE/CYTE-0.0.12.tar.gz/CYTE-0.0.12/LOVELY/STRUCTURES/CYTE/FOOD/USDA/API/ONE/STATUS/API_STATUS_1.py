

from BOTANY.IMPORT import IMPORT

import json

import CYTE.FOOD.USDA.API.ONE as USDA_FOOD_API

def CHECK_BRANDED_1 ():
	KEYS = IMPORT ("/ONLINE_KEYS/USDA/__init__.py").KEYS ()
	
	FOOD = USDA_FOOD_API.FIND (
		2642759,
		API_KEY = KEYS ["API"]
	)
	
	#print (json.dumps (FOOD ['DATA'], indent = 4))

	
def CHECK_FOUNDATIONAL_1 ():
	KEYS = IMPORT ("/ONLINE_KEYS/USDA/__init__.py").KEYS ()
	
	FOOD = USDA_FOOD_API.FIND (
		2346404,
		API_KEY = KEYS ["API"],
		KIND = "FOUNDATIONAL"
	)
	
	#print (json.dumps (FOOD ['DATA'], indent = 4))
	



	
CHECKS = {
	"CHECK BRANDED 1": CHECK_BRANDED_1,
	"CHECK FOUNDATIONAL 1": CHECK_FOUNDATIONAL_1
}