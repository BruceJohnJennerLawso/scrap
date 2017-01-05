## game.py #####################################################################
## object representing all of the data known about a given game ################
################################################################################
import seasonParts

class Game(object):
	def __init__(self, comparisonSelectCondition, seasonIndex):
		self.Layers = []
		## list of lists, with each list containing stats computed for that
		## layer
		self.layerCount = 0
		self.comparisonSelectCondition = comparisonSelectCondition
		self.seasonIndex = seasonIndex
	
	def getOne(self):
		## Just... dont worry about it ok?
		return 1
		
	def getComparisonConditions(self):
		return self.comparisonSelectCondition	
		
	def addLayer(self, data):
		self.Layers.append(data)
		## tack on a new layer
		self.layerCount += 1
		## increment the counter so we know its there

	def getDate(self):
		return self.Layers[0][0]
		## this should hopefully probably be a convention for all games levels
		
	def getLocation(self):
		return self.Layers[0][1]
		## same idea here
		
	def getGameResult(self):
		return self.Layers[0][2]

	def getGoalsFor(self):
		return int(self.Layers[0][3])
		
	def getGoalsAgainst(self):
		return int(self.Layers[0][4])		
		
	def getOpponentName(self):
		return self.Layers[0][6]		
		
	def getGoalDifferential(self):
		diff = self.getGoalsFor()-self.getGoalsAgainst()
		return diff					
		## easy mode here	

	def Won(self):
		if(self.getGameResult() in ['won', 'W']):
			return True
		else:
			return False
			
	def Tied(self):
		if(self.getGameResult() in ['tie', 'T']):
			return True
		else:
			return False	
			
	def Lost(self):
		if(self.getGameResult() in ['lost', 'L']):
			return True
		else:
			return False

	def getGameClosenessIndex(self):
		if(self.Tied() != True):
			return 1.000/float(abs(self.getGoalDifferential()))
		else:
			return 1.000
		## ie
		##
		## 1-1 -> 1.000
		## 2-1 -> 1.000
		## 3-1 -> 0.500
		## 4-1 -> 0.333
		## 5-1 -> 0.250
		## 6-1 -> 0.200
		## 7-1 -> 0.166

		## its a quick way of measuring how close a game was with a single
		## number
		
		## although now that I take a look at it, the dropoff is a little bit
		## too steep early on between a 1 to 2 to 3 goal differential
	
	def getPointsPercentage(self):
		return float(self.getPointsEarned())/self.getMaxPointsPossible()
		
		
	## TierII statistics per game ##############################################
		
	
	def loadTierII(self, teamsList, thisTeamRank, seasonIndex):
		
		self.seasonIndex = seasonIndex
		opponentFound = False			
		## start off by looking for our opponents object in the list of
		## teams that we were given to search
		for team in teamsList:
			if(team.getTeamName() == self.getOpponentName()):
				opponent = team
				opponentFound = True
				self.opponent = opponent
				## once we find our team, assign it, and break outa here
					
				## shouldnt ever be two teams with the same name... I hope
					
		if(opponentFound == False):
			## we wanna blow everything up here so that we can start
			## debugging the problem 
			if(debugInfo):
				print "Unable to find opponent '%s' in opposition teams," % game.getOpponentName()
				for team in teamsList:
					print team.getTeamName(),
				print '\n'
			raise NameError('Team %s Unable to find scheduled opponent %s as team object' % (self.getTeamName(), game.getOpponentName()))
		
		self.seasonRank = thisTeamRank+1
		## team rank is the index of this team after sorting based on the watMu
		## standings criteria
		
		
		opponent = self.getOpponent()
	
	def getOpponent(self):
		return self.opponent
		
	def getWinQualityIndex(self):
		output = 0.000
		
		opponentPointsPct = self.getOpponent().getSeasonPart([self.getComparisonConditions(),seasonParts.gamesSelectConditions(part="none")]).getAverageForStat(Game.getPointsPercentage)
		if(self.Lost() != True):	
			## so long as we didnt lose the game, we will get a nonzero
			## value for WQI and PQI, varying depending on the game stats
			## and whether the game was a win or a tie
			if(self.Won()):
				output += (self.getGoalDifferential()*opponentPointsPct) 
			elif(self.Tied()):
				output += (opponentPointsPct)	
		return output
	
	def getPlayQualityIndex(self):
		output = 0.000
		
		opponentPointsPct = self.getOpponent().getSeasonPart([self.getComparisonConditions(),seasonParts.gamesSelectConditions(part="none")]).getAverageForStat(Game.getPointsPercentage)
		if(self.Lost() != True):	
			## so long as we didnt lose the game, we will get a nonzero
			## value for WQI and PQI, varying depending on the game stats
			## and whether the game was a win or a tie
			if(self.Won()):
				output += (self.getGoalDifferential()*opponentPointsPct*self.getGameClosenessIndex()) 
			elif(self.Tied()):
				output += (opponentPointsPct*self.getGameClosenessIndex())	
		return output
	
	def getDefenceQualityIndex(self):
		output = 0.000	
		opponentOffence = self.getOpponent().getSeasonPart([self.getComparisonConditions(),seasonParts.gamesSelectConditions(part="none")]).getAverageForStat(Game.getGoalsFor)
		output += (opponentOffence - self.getGoalsAgainst())
		return output

	def getOffenceQualityIndex(self):
		output = 0.000
		
		opponentDefence = self.getOpponent().getSeasonPart([self.getComparisonConditions(),seasonParts.gamesSelectConditions(part="none")]).getAverageForStat(Game.getGoalsAgainst)
		output += (self.getGoalsFor() - opponentDefence)
		return output
		
	def getDiffQualityIndex(self):
		output = 0.000
		
		opponentGoalDiff = self.getOpponent().getSeasonPart([self.getComparisonConditions(),seasonParts.gamesSelectConditions(part="none")]).getAverageForStat(Game.getGoalDifferential)
		output += (self.getGoalsFor() - (-opponentGoalDiff))
		return output	
		
	def getOldDiffQualityIndex(self):
		output = 0.000
		
		opponentGoalDiff = self.getOpponent().getSeasonPart([self.getComparisonConditions(),seasonParts.gamesSelectConditions(part="none")]).getAverageForStat(Game.getGoalDifferential)
		output += (self.getGoalsFor() - opponentGoalDiff)
		return output			

	
	def getCPQI(self):
		return (self.getOffenceQualityIndex() + self.getDefenceQualityIndex())
		
	def getDiffQualMargin(self):
		return (self.getCPQI()-self.getGoalDifferential())	
