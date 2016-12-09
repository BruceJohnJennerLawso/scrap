## game.py #####################################################################
## object representing all of the data known about a given game ################
################################################################################


class Game(object):
	def __init__(self):
		self.Layers = []
		## list of lists, with each list containing stats computed for that
		## layer
		self.layerCount = 0
		
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
		
		
	## TierII statistics per game ##############################################
	
	def loadTierII(self, teamsList, thisTeamRank):
		self.winQualityIndex = 0.000
		self.playQualityIndex = 0.000
		
		self.defenceQualityIndex = 0.000
		self.offenceQualityIndex = 0.000		
		
		self.diffQualityIndex = 0.000
		
		self.seasonRank = thisTeamRank+1
		## team rank is the index of this team after sorting based on the watMu
		## standings criteria
		
		opponentFound = False			
		## start off by looking for our opponents object in the list of
		## teams that we were given to search
		for team in teamsList:
			if(team.getTeamName() == self.getOpponentName()):
				opponent = team
				opponentFound = True
				break
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

		self.offenceQualityIndex = (self.getGoalsFor()-opponent.getSeasonGoalsAgainstAverage())
		## for each game the OQI is goals scored above expectations, so we
		## add that value to the total OQI
		self.defenceQualityIndex = (opponent.getSeasonGoalsForAverage()-self.getGoalsAgainst())
		## and for each game, the DQI is goals allowed below expectations,
		self.diffQualityIndex = (self.getGoalDifferential()-(-opponent.getSeasonGoalDifferentialAverage()))
		self.oldDiffQualityIndex = (self.getGoalDifferential()-(opponent.getSeasonGoalDifferentialAverage()))		
		## so we add that value to the total DQI
		if(self.Lost() != True):	
			## so long as we didnt lose the game, we will get a nonzero
			## value for WQI and PQI, varying depending on the game stats
			## and whether the game was a win or a tie
			if(self.Won()):
				self.winQualityIndex = (self.getGoalDifferential()*opponent.getSeasonPointsTotal()) 
				self.playQualityIndex = (self.getGoalDifferential()*opponent.getSeasonPointsTotal()*self.getGameClosenessIndex()) 					
			elif(self.Tied()):
				self.winQualityIndex = (opponent.getSeasonPointsTotal())
				self.playQualityIndex = (opponent.getSeasonPointsTotal()*self.getGameClosenessIndex())						
		## once we've calculated the total WQI & PQI, divy them over the total
		## games played in that season to get an average
	
	def getWinQualityIndex(self):
		return self.winQualityIndex
	
	def getPlayQualityIndex(self):
		return self.playQualityIndex
		
	def getOffenceQualityIndex(self):
		return self.offenceQualityIndex
		
	def getDefenceQualityIndex(self):
		return self.defenceQualityIndex
	
	def getCPQI(self):
		return (self.offenceQualityIndex + self.defenceQualityIndex)
		
	def getDiffQualityIndex(self):
		return self.diffQualityIndex

	def getDiffQualMargin(self):
		return (self.getDiffQualityIndex()-self.getGoalDifferential())
