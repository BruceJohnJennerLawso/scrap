## teamWatMu.py ################################################################
## object representing a team playing in waterloo ##############################
## intramural hockey ###########################################################
################################################################################
from team import *


class watMuGame(Game):
	def __init__(self, dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName):
		super(watMuGame, self).__init__(dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName)
			



class watMuTeam(Team):
	def __init__(self, leagueId, levelId, seasonId, teamId):
		super(watMuTeam, self).__init__(leagueId, levelId, seasonId, teamId)
		self.loadTierI()
		
		
	def loadTierI(self):
		with open(self.loadPath, 'rb') as foo:
			rows = []
			reader = csv.reader(foo)
			for row in reader:
				rows.append(row)
		
		self.teamName = rows[0][0]
		print "%s: %s, Id: %s" % (self.teamName, rows[0][1], self.teamId)
		##print rows[1][0]
		self.seasonLength = int(rows[1][0])
		
		
		self.totalSeasonGames = 0
		self.totalPlayoffGames = 0
		if(self.seasonLength >= 6):
			self.totalSeasonGames +=6
		else:
			self.totalSeasonGames = self.seasonLength
			self.totalPlayoffGames = 0
		if((self.seasonLength-self.totalSeasonGames) > 0):
			self.totalPlayoffGames += (self.seasonLength-self.totalSeasonGames)
		
		## get the total number of games played by this team, which the
		## scraper saves on the second line for us
		scheduleData = rows[2:(self.seasonLength + 2)]
		## slice out only the rows that contain games data
		for game in scheduleData:
			self.Games.append(watMuGame(str(game[0]), str(game[1]), str(game[2]), int(game[3]), int(game[4]), str(game[5]), str(game[6])))
			## set up each game as an object in memory
		
		self.averageSOC = 0
		self.seasonPlusMinus = 0
		self.seasonTotalGoalsFor = 0
		self.seasonTotalGoalsAgainst = 0	
		self.seasonPointsTotal = 0	
		self.seasonWins = 0
		self.seasonTies = 0
		self.seasonLosses = 0
		self.averageGameClosenessIndex = 0
		
		averageSOCGames = 0
		for game in self.Games[0:6]:

			##print game.Layers[0]
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
			
			self.averageGameClosenessIndex += game.getGameClosenessIndex()	
				
			try:
				self.averageSOC += game.getSOC()
				##print self.averageSOC
			except ValueError:
				averageSOCGames += 1	
				print "Failed add due to ValueError"
				print "Adding in an average SOC game due to actual value '%s'" % game.Layers[0][5]
		print "Total season games %i" % self.totalSeasonGames
		self.averageGameClosenessIndex = self.averageGameClosenessIndex/float(self.totalSeasonGames)
		## this is fixable, just need to save game totals for each type in teh
		## csv and remember to load them
		SOC = float(self.averageSOC)/float(self.totalSeasonGames-averageSOCGames) 


		if(averageSOCGames > 0):
			## loop through the games again, if the value fails we overwrite it
			## with the average of the games that were defined
			for game in self.Games[0:6]:
				print game.Layers[0]
				try:
					game.getSOC()
				except ValueError:
					print "Failed int() cast due to ValueError"
					game.setSOC(SOC)
					print game.Layers[0]

		
		self.averageSOC = 0
		for game in self.Games[0:6]:
			## now that every game has a properly defined SOC, loop through
			## and sum again before dividing to get the average
			self.averageSOC += game.getSOC()
		self.averageSOC /= float(self.totalSeasonGames)
		
		
		
		
	def loadTierII(self, teamsList):	
		print "Load call watMuTeam Tier II, team %s, Id %s" % (self.getTeamName(), self.teamId)
		self.averageWinQualityIndex = 0
		self.averagePlayQualityIndex = 0
		
		for game in self.Games[0:6]:
			## we dont need to reload the data, cause it was already loaded by
			## the loadTierI(...) call
			opponentFound = False			
			for team in teamsList:
				if(team.getTeamName() == game.getOpponentName()):
					opponent = team
					opponentFound = True
					## shouldnt ever be two teams with the same name... I hope
					
			if(opponentFound == False):
				print "Unable to find opponent '%s' in opposition teams," % game.getOpponentName()
				for team in teamsList:
					print team.getTeamName(),
				print '\n'
					## maybe this would be better done as a truly unique string,
					## ie as teamname appended to season
			if(game.Lost() != True):	
				if(game.Won()):
					self.averageWinQualityIndex += (game.getGoalDifferential()*opponent.getSeasonPointsTotal()) 
					self.averagePlayQualityIndex += (game.getGoalDifferential()*opponent.getSeasonPointsTotal()*game.getGameClosenessIndex()) 					
				elif(game.Tied()):
					self.averageWinQualityIndex += (opponent.getSeasonPointsTotal())
					self.averagePlayQualityIndex += (opponent.getSeasonPointsTotal()*game.getGameClosenessIndex())						
			##print self.averageWinQualityIndex, game.getGoalDifferential()
			##print self.averagePlayQualityIndex
		self.averageWinQualityIndex /= float(self.totalSeasonGames)
		self.averagePlayQualityIndex /= float(self.totalSeasonGames)	


	def loadTierIII(self, teamsList):	
		print "Load call watMuTeam Tier III, team %s" % self.getTeamName()

		self.meanAdjustedAverageWinQualityIndex = self.averageWinQualityIndex
		self.meanAdjustedAveragePlayQualityIndex = self.averagePlayQualityIndex
		
		awqiMean = 0
		apqiMean = 0
		
		for team in teamsList:
			awqiMean += team.getAWQI()
			apqiMean += team.getAPQI()
			
		awqiMean /= float(len(teamsList))
		apqiMean /= float(len(teamsList))
		
		self.meanAdjustedAverageWinQualityIndex /= awqiMean
		## this matches the spreadsheet perfectly
		self.meanAdjustedAveragePlayQualityIndex /= apqiMean
		## cant find any mistakes in how this is calculated, but the values dont
		## match what the spreadsheet had		
		
		## because these values are calculated differently
		## PQI in the spreadsheet was just a product of the averages for AWQI
		## and AGCI
		
		## thats why these values are different from what the spreadsheet had
				



