
from CYTE.STRUCTS.CLIQUE import STRUCTS_CLIQUE

def START ():
	import click
	@click.group ()
	def GROUP ():
		pass


	import click
	@click.command ("example")
	def EXAMPLE ():	
		print ("EXAMPLE")

		return;
	GROUP.add_command (EXAMPLE)


	STRUCTS_CLIQUE (GROUP)


	GROUP ()


START ()

#
