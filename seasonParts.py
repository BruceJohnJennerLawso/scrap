## seasonParts.py ##############################################################
## object of type seasonPart which represents a list of games in the parent ####
## season, and the stats that can be associated with those games ###############
################################################################################


class gamesSelectConditions(object):
	def __init__(self, part="completeSeason", fractionOfWhole=-1, startGameNumber=-1, endGameNumber=-1):
		self.Conditions = []
		## list of conditions always starting with a part string which describes
		## how the condition should work, then 
		if(part == "completeSeason"):
			self.Conditions.append(part)
		else:
			print "Unrecognized condition %s supplied to seasonSelectConditions() object" % part
	
	def __eq__(self, other):
		if(self.Conditions == other.Conditions):
			return True
		else:
			return False	
			
	def getGamesList(self, inputGames):
		if(self.Conditions[0] == "completeSeason"):
			return inputGames
		## if we have an unrecognized condition this is going to crash hard
	


class seasonPart(object):
	## base class constructor
	def __init__(self, Games, seasonGameConditions=gamesSelectConditions(), playoffGameConditions=gamesSelectConditions()):
		self.gameConditions = gameConditions
		self.Games = self.seasonGameConditions.getGamesList(Games)
		## take the original list of games for this season and run it through
		## the seasonSelectConditions obj

	def getGameConditions(self):
		return self.gameConditions
		
	def loadTierI(self, rows, debugInfo=False):
		
	
		
		self.totalSeasonGames = 0
		## this will be the total games that have been played up to this point
		## even if there are more games in the schedule that have yet to be
		## played
		self.totalPlayoffGames = 0
		
		if(self.seasonLength >= 6):
			self.totalSeasonGames +=6
		else:
			self.totalSeasonGames = self.seasonLength
			self.totalPlayoffGames = 0
		## I dont like how this works, cause it wont be able to handle in
		## progress seasons properly
		
		## ideally, this needs to step through the game objects and verify that
		## they have in fact been played 
		
		if((self.seasonLength-self.totalSeasonGames) > 0):
			self.totalPlayoffGames += (self.seasonLength-self.totalSeasonGames)	
		
		
		self.averageSOC = 0
		
		self.seasonPlusMinus = 0
		self.seasonTotalGoalsFor = 0
		self.seasonTotalGoalsAgainst = 0	
		
		self.seasonPointsTotal = 0	
		self.seasonWins = 0
		self.seasonTies = 0
		self.seasonLosses = 0
		self.seasonGamesNotYetPlayed = 0
		
		self.averageGameClosenessIndex = 0
		
		averageSOCGames = 0
		
		for game in self.getSeasonGames():
			
			self.seasonTotalGoalsFor += game.getGoalsFor()
			self.seasonTotalGoalsAgainst += game.getGoalsAgainst()
			self.seasonPlusMinus += game.getGoalDifferential()
			self.seasonPointsTotal += game.getPointsEarned()
			
			if(game.Won()):
				self.seasonWins += 1
			elif(game.Tied()):
				self.seasonTies += 1
			elif(game.Lost()):
				self.seasonLosses += 1
			elif(game.notYetPlayed()):
				self.seasonGamesNotYetPlayed += 1
			
			self.averageGameClosenessIndex += game.getGameClosenessIndex()	
				
			try:
				## try to add the SOC of a given game as a float 
				self.averageSOC += game.getSOC()
			except ValueError:
				## if this fails because game.getSOC() is actually a string
				## (saying 'avg.') we tally one more SOC game in the schedule
				averageSOCGames += 1	
				if(debugInfo):
					print "Failed add due to ValueError"
					print "Adding in an average SOC game due to actual value '%s'" % game.Layers[0][5]
		
		print "Total season games %i" % self.totalSeasonGames
		self.averageGameClosenessIndex /= float(self.totalSeasonGamesPlayed)
		
		SOC = float(self.averageSOC)/float(self.totalSeasonGamesPlayed-averageSOCGames) 
		## start off by getting our average for the games that had an SOC number
		## available

		if(averageSOCGames > 0):
			## loop through the games again, if the value fails we overwrite it
			## with the average of the games that were defined
			for game in self.Games[0:self.totalSeasonGames]:
				print game.Layers[0]
				try:
					game.getSOC()
				except ValueError:
					if(debugInfo):
						print "Failed int() cast due to ValueError"
					game.setSOC(SOC)
					print game.Layers[0]

		
		self.averageSOC = 0
		for game in self.getSeasonGames():
			## now that every game has a properly defined SOC, loop through
			## and sum again before dividing to get the average
			self.averageSOC += game.getSOC()
		self.averageSOC /= float(self.totalSeasonGames)
		
		## now time to tally the stats we have available for the playoffs
		
		self.playoffWins = 0
		##self.totalPlayoffGames = 0
		self.playoffWinPercentage = 0.000
		
		self.playoffGoalsFor = 0
		self.playoffGoalsAgainst = 0
		self.playoffPlusMinus = 0
		self.playoffAverageGoalDifferential = 0.000
		
		if(self.qualifiedForPlayoffs() == True):
			self.totalPlayoffGames = len(self.getPlayoffGames())
			for game in self.getPlayoffGames():		
				if(game.Won()):
					self.playoffWins += 1
				self.playoffGoalsFor += game.getGoalsFor()
				self.playoffGoalsAgainst += game.getGoalsAgainst()	
				self.playoffPlusMinus += (game.getGoalsFor() - game.getGoalsAgainst())			
			self.playoffWinPercentage = float(self.playoffWins)/float(self.totalPlayoffGames)
			self.playoffAverageGoalDifferential = self.playoffPlusMinus/float(self.totalPlayoffGames)
		
		
			
		
