

'''
import CYTE.STRUCTS.SCAN.TREES.SORT as SORT_TREES
SORT_TREES.START (TREES)
'''

def START (TREES):
	TREES.sort (key = lambda STRUCT : STRUCT ["names"][0])

	return