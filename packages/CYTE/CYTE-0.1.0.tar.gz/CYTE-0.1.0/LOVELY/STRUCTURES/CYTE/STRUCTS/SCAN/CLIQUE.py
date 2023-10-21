



def STRUCTS_SCAN_CLIQUE (GROUP):

	import click
	@GROUP.group ("scan")
	def GROUP ():
		pass
	
	'''
		./cyte_dev structs scan struct-find 
	'''
	import click
	@GROUP.command ("struct-find")
	def STRUCT_FIND ():	
		print ("struct find")


		return;
		

	return;