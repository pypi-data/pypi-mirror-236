



def CALC_UNIT (NIH_SUPPLEMENT_DATA):

	assert ("netContents" in NIH_SUPPLEMENT_DATA)
	NET_CONTENTS = NIH_SUPPLEMENT_DATA ["netContents"]

	assert ("physicalState" in NIH_SUPPLEMENT_DATA)
	PHYSICAL_STATE = NIH_SUPPLEMENT_DATA ["physicalState"]

	assert ("servingSizes" in NIH_SUPPLEMENT_DATA)
	SERVING_SIZES = NIH_SUPPLEMENT_DATA ["servingSizes"]

	if (
		len (NET_CONTENTS) == 1 and
		NET_CONTENTS [0] ["unit"] == "Tablet(s)" and 
		PHYSICAL_STATE ["langualCodeDescription"] == "Tablet or Pill" and
		len (SERVING_SIZES) == 1 and
		SERVING_SIZES [0] ["unit"] == "Tablet(s)"
	):
		return "Tablet"
		
	if (
		len (NET_CONTENTS) == 1 and
		NET_CONTENTS [0] ["unit"] == "Coated Tablet(s)" and 
		PHYSICAL_STATE ["langualCodeDescription"] == "Tablet or Pill" and
		len (SERVING_SIZES) == 1 and
		SERVING_SIZES [0] ["unit"] == "Tablet(s)"
	):
		return "Coated Tablet"
		
	raise Exception ("The form unit of the supplement could not be calculated.")


def CALC_QUANTITY (NIH_SUPPLEMENT_DATA):
	assert ("netContents" in NIH_SUPPLEMENT_DATA)
	NET_CONTENTS = NIH_SUPPLEMENT_DATA ["netContents"]
	
	if (
		len (NET_CONTENTS) == 1
	):
		return NET_CONTENTS [0] ["quantity"]
		
	raise Exception ("The form quantity of the supplement could not be calculated.")
