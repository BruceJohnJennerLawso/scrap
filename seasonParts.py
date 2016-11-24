## seasonParts.py ##############################################################
## object of type seasonPart which represents a list of games in the parent ####
## season, and the stats that can be associated with those games ###############
################################################################################


class gamesSelectConditions(object)
	def __init__(self, part="completeSeason", fractionOfWhole=-1, startGameNumber=-1, endGameNumber=-1):
		self.Conditions = []
		## list of conditions always starting with a part string which describes
		## how the condition should work, then 
		if(part == "completeSeason"):
			self.Conditions.append(part)
		else:
			print "Unrecognized condition %s supplied to seasonSelectConditions() object" % part
			
			
	def getGamesList(self, inputGames):
		if(self.Conditions[0] == "completeSeason"):
			return inputGames
		## if we have an unrecognized condition this is going to crash hard
	


class seasonPart(object):
	## base class constructor
	def __init__(self, Games, gameConditions=gamesSelectConditions()):
		self.Games = gameConditions.getGamesList(Games)
		## take the original list of games for this season and run it through
		## the seasonSelectConditions obj
