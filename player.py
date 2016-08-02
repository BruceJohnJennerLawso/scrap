## player.py ###################################################################
## object representing an individual player in the waterloo ####################
## intramurals system ##########################################################
################################################################################

class Player(object):
	def __init__(self, name):
		self.Name = name
		## whats in a name, eh?
		
		## overall, the general structure of a player in our context here is a
		## list of team objects that it has played for, which we can use to
		## pull career data about the teams that we played for
		
		## for teams that had individual player data, we can obviously use it
		## to directly return the numbers, but we might be able to do 
		## interesting things with interpolating career curves out of small
		## samples of a players individual numbers
		
		## FFUUUTUURE
		
	def getName(self):
		return self.Name
