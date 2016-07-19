## player.py ###################################################################
## object representing an individual player in the waterloo ####################
## intramurals system ##########################################################
################################################################################

class Player(object):
	def __init__(self, name):
		self.Name = name
		
	def getName(self):
		return self.Name
