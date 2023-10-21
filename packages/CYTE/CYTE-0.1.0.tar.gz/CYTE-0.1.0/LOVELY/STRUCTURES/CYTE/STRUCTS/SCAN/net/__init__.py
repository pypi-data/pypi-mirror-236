


'''
import CYTE.STRUCTS.SCAN.net as net_build
struct_net = net_build.start ()
'''

'''
{
	"names": [
		"carbohydrates",
		"carbohydrate, by difference"
	],
	"region": 2,
	"includes": [
		7
	]
}
'''

import CYTE.STRUCTS.DB.ACCESS as ACCESS
import CYTE.STRUCTS.SCAN.struct.list as STRUCTS_LIST

import json

def start (STRUCT_DB):
	LIST = STRUCTS_LIST.FIND (STRUCT_DB)

	print ("LIST:", LIST)













