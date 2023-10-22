
'''
	import CYTE._interpret.unit_kind as UNIT_KIND
	KIND = UNIT_KIND.CALC ("ml")
	
	# KIND == "volume"

'''

VOLUME_UNIT_GROUPS = [
	[ "liters", "litres", "l" ],
	[ "milliliters", "millilitres", "ml" ],

	[ "fluid ounces", "fl oz" ]
]

MASS_UNIT_GROUPS = [
	[ "grams", "gram", "g" ],
	[ "milligrams", "milligram", "mg" ],
	[ "micrograms", "microgram", "mcg" ],

	[ "pounds", "pound", "lbs", "lb" ],
	[ "ounces", "ounce", "oz", "ozs" ],
]

def CALC (UNIT):
	for GROUP in VOLUME_UNIT_GROUPS:
		for GROUP_UNIT in GROUP:
			if (UNIT.lower () == GROUP_UNIT):
				return "volume"

	for GROUP in MASS_UNIT_GROUPS:
		for GROUP_UNIT in GROUP:
			if (UNIT.lower () == GROUP_UNIT):
				return "mass"
	
	return "?"