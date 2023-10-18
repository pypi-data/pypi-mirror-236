
'''
	import CYTE.FOOD.NIH.EXAMPLES as NIH_EXAMPLES
	EXAMPLE = NIH_EXAMPLES.RETRIEVE ("TABLETS/MULTIVITAMIN_249664.JSON")
'''


def RETRIEVE (PATH):
	import pathlib
	from os.path import dirname, join, normpath

	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
	EXAMPLE = normpath (join (THIS_FOLDER, PATH))

	import json
	with open (EXAMPLE) as FP:
		DATA = json.load (FP)

	return DATA