
'''
import CYTE.INTEGER.STRING_IS_INTEGER as STRING_IS_INTEGER
STRING_IS_INTEGER.CHECK ("1234")
'''

def CHECK (STRING):
	if (len (STRING) == 0):
		return False;
		
	INTEGER_CHARACTERS = [ 
		"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
	]
	for CHARACTER in STRING:
		if (CHARACTER not in INTEGER_CHARACTERS):
			return False;

	return True