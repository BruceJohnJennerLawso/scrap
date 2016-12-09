## seasonParts.py ##############################################################
## object of type seasonPart which represents a list of games in the parent ####
## season, and the stats that can be associated with those games ###############
################################################################################
import distStats

class gamesSelectConditions(object):
	def __init__(self, part="regularSeason", fractionOfWhole=-1, startGameNumber=-1, endGameNumber=-1):
		self.Conditions = []
		## list of conditions always starting with a part string which describes
		## how the condition should work, then 
		if(part == "regularSeason"):
			self.Conditions.append(part)
		elif(part == "firstHalfRegularSeason"):
			self.Conditions.append(part)
		elif(part == "secondHalfRegularSeason"):
			self.Conditions.append(part)
		elif(part == "none"):
			self.Conditions.append(part)						
		else:
			print "Unrecognized condition %s supplied to seasonSelectConditions() object" % part
		##self.comparisonCondition = gamesSelectConditions(comparison, comparison)
	
	
	def __eq__(self, other):
		if(self.Conditions == other.Conditions):
			return True
		else:
			return False	
			
	def getGamesList(self, inputGames):
		if(self.Conditions[0] == "regularSeason"):
			return inputGames
		elif((self.Conditions[0] == "firstHalfRegularSeason")or(self.Conditions[0] == "secondHalfRegularSeason")):
			if(distStats.isOdd(len(inputGames))):
				## we have to make a decision here, so we will place the game in
				## the middle in the back half by convention
				halfIndex = float(len(inputGames))/2.0
				halfIndexRounded = int(halfIndex)
				if(halfIndexRounded > halfIndex):
					halfIndex = halfIndexRounded - 1
				else:
					halfIndex = halfIndexRounded
					
			else:
				halfIndex = int(len(inputGames)/2.0)
				
			if(self.Conditions[0] == "firstHalfRegularSeason"):
				return inputGames[0:halfIndex]
			elif(self.Conditions[0] == "secondHalfRegularSeason"):
				return inputGames[halfIndex:len(inputGames)]
		elif(self.Conditions[0] == "none"):
			return []		
		## if we have an unrecognized condition this is going to crash hard
	


class seasonPart(object):
	## base class constructor
	def __init__(self, seasonGames, playoffGames, seasonGameConditions=gamesSelectConditions(), playoffGameConditions=gamesSelectConditions()):
		self.seasonGameConditions = seasonGameConditions
		self.playoffGameConditions = playoffGameConditions
		self.seasonGames = self.seasonGameConditions.getGamesList(seasonGames)
		self.playoffGames = self.playoffGameConditions.getGamesList(playoffGames)
		## take the original list of games for this season and run it through
		## the seasonSelectConditions object

	def getGameConditions(self):
		return [self.seasonGameConditions, self.playoffGameConditions]
		
	def loadTierII(self, teamsList, thisTeamRank):	
		## I believe this function should be where the comparison game select
		## condition is passed in.
		
		## the comparison condition is then used to get the appropriate game
		## part from opponent teams inside of game.loadTierII(...)
		for game in (self.seasonGames):
			game.loadTierII(teamsList, thisTeamRank)
		for game in (self.playoffGames):
			game.loadTierII(teamsList, thisTeamRank)			
		## I believe this should overwrite tierII stats for this season parts
		## games when a different season game condition is used...
		
	def getAverageForStat(self, statName, playoffGames=False):
		output = 0.0
		
		if(not playoffGames):
			for game in self.seasonGames:
				output += statName(game)
			output /= float(len(self.seasonGames))
		return output
		
	def getTotalForStat(self, statName, playoffGames=False):
		output = 0.0
		
		if(not playoffGames):
			for game in self.seasonGames:
				output += statName(game)
		
		return output
