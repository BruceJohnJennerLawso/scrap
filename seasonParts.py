## seasonParts.py ##############################################################
## object of type seasonPart which represents a list of games in the parent ####
## season, and the stats that can be associated with those games ###############
################################################################################
import distStats
import gameWatMu
import gameNhl

class gamesSelectConditions(object):
	def __init__(self, part="everything", fractionOfWhole=-1, startGameNumber=-1, endGameNumber=-1):
		self.Conditions = []
		## list of conditions always starting with a part string which describes
		## how the condition should work, then 
		if(part == "everything"):
			self.Conditions.append(part)
		elif(part == "firstHalf"):
			self.Conditions.append(part)
		elif(part == "secondHalf"):
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
		if(inputGames is None):
			print "getGamesList received none type inputGames"
		if(self.Conditions[0] == "everything"):
			return inputGames
		elif((self.Conditions[0] == "firstHalf")or(self.Conditions[0] == "secondHalf")):
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
				
			if(self.Conditions[0] == "firstHalf"):
				return inputGames[0:halfIndex]
			elif(self.Conditions[0] == "secondHalf"):
				return inputGames[halfIndex:len(inputGames)]
		elif(self.Conditions[0] == "none"):
			return []		
		## if we have an unrecognized condition this is going to crash hard	
	
def getGameSelectConditions(description):
	if(description == "completeSeason"):
		return [gamesSelectConditions(part="everything"),gamesSelectConditions(part="everything")]
	elif(description == "regularSeason"):
		return [gamesSelectConditions(part="everything"),gamesSelectConditions(part="none")]	
	elif(description == "firstHalfRegularSeason"):
		return [gamesSelectConditions(part="firstHalf"),gamesSelectConditions(part="none")]		
	elif(description == "secondHalfRegularSeason"):
		return [gamesSelectConditions(part="secondHalf"),gamesSelectConditions(part="none")]
	elif(description == "playoffs"):
		return [gamesSelectConditions(part="none"),gamesSelectConditions(part="everything")]						

if(__name__ == "__main__"):
	print "Fuck"
	##print (getGameSelectConditions("regularSeason") == [gamesSelectConditions(part="everything"),gamesSelectConditions(part="none")])


class seasonPart(object):
	## base class constructor
	def __init__(self, seasonGames, playoffGames, seasonGameConditions=gamesSelectConditions(), playoffGameConditions=gamesSelectConditions()):
		
		if((seasonGames is None)or(playoffGames is None)):
			print "Season parts constructor received none type in games list"
		
		self.seasonGameConditions = seasonGameConditions
		self.playoffGameConditions = playoffGameConditions
		self.seasonGames = self.seasonGameConditions.getGamesList([gm.cloneGame(seasonGameConditions) for gm in seasonGames])
		self.playoffGames = self.playoffGameConditions.getGamesList([gm.cloneGame(playoffGameConditions) for gm in playoffGames])
		## take the original list of games for this season and run it through
		## the seasonSelectConditions object
		if((self.seasonGames is None)or(self.playoffGames is None)):
			print "Season parts constructor finished with none type in games list"


	def getGameConditions(self):
		return [self.seasonGameConditions, self.playoffGameConditions]
		
	def loadTierII(self, teamsList, thisTeamRank, seasonIndex):	
		## I believe this function should be where the comparison game select
		## condition is passed in.
		
		## the comparison condition is then used to get the appropriate game
		## part from opponent teams inside of game.loadTierII(...)
		for game in self.getGames():
			game.loadTierII(teamsList, thisTeamRank, seasonIndex)			
		## I believe this should overwrite tierII stats for this season parts
		## games when a different season game condition is used...
	
	def getGames(self, excludePlayoffGames=False):
		if(excludePlayoffGames):
			return self.seasonGames
		else:
			return self.seasonGames + self.playoffGames	
		
	def getTotalForStat(self, statName, playoffGames=True):
		output = 0.000
		games = self.getGames(not playoffGames)
		
		for game in games:
			output += statName(game)
		
		return output
		
	def getTotalMatchForStat(self, statName, valueToMatch, playoffGames=True):
		output = 0
		games = self.getGames(not playoffGames)
		
		for game in games:
			if(statName(game) == valueToMatch):
				output += 1
		return output				
		
	def getAverageForStat(self, statName, playoffGames=True):
		output = 0.000
		games = self.getGames(not playoffGames)
		
		for game in games:
			output += statName(game)
		
		if(len(games) != 0):
			output /= float(len(games))
		else:
			output = 0.000
		
		return output
			
	
	#def getPointsPercentage(self, seasonIndex, playoffGames=False):
		#output = 0.0
		#ceiling = 0.0
		#games = self.getGames(not playoffGames)
		
		
		#for game in games:
			#output += game.getPointsEarned(seasonIndex)
			#ceiling += game.getMaxPointsPossible()
		
		#if(len(games) != 0):
			#output /= float(ceiling)
		#else:
			#output = 0.000
		
		#return output
		


		

