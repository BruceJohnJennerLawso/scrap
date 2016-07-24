## teamNhl.py ##################################################################
## object representing a team playing in the NHL ###############################
################################################################################
from team import *
from gameNhl import *






class nhlGame(Game):
	def __init__(self, dateString, Location, gameResult, goalsFor, goalsAgainst, opponentName):
		super(nhlGame, self).__init__(dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName)
			



class watMuTeam(Team):
	def __init__(self, leagueId, levelId, seasonId, teamId):
		super(watMuTeam, self).__init__(leagueId, levelId, seasonId, teamId)
		
		self.seasonId = seasonId
		
		self.loadTierI()
		
	
		
	## Tier I load call ########################################################	
		
	def loadTierI(self):
		with open(self.loadPath, 'rb') as foo:
			rows = []
			reader = csv.reader(foo)
			for row in reader:
				rows.append(row)
			## create a list called row, which will hold all of the data in the
			## csv as a sublist for each row, ie
			
			## [[row 1...], [row 2...],...]
		
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
		
		
		## rosters...
		self.Roster = rows[(self.seasonLength + 3)]
		
			
		
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
		for game in self.getSeasonGames():

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
			for game in self.Games[0:self.totalSeasonGames]:
				print game.Layers[0]
				try:
					game.getSOC()
				except ValueError:
					print "Failed int() cast due to ValueError"
					game.setSOC(SOC)
					print game.Layers[0]

		
		self.averageSOC = 0
		for game in self.getSeasonGames():
			## now that every game has a properly defined SOC, loop through
			## and sum again before dividing to get the average
			self.averageSOC += game.getSOC()
		self.averageSOC /= float(self.totalSeasonGames)
		
		self.playoffWins = 0
		self.playoffGames = 0
		self.playoffWinPercentage = 0.000
		
		self.playoffGoalsFor = 0
		self.playoffGoalsAgainst = 0
		if(self.qualifiedForPlayoffs() == True):
			self.playoffGames = len(self.getPlayoffGames())
			for game in self.getPlayoffGames():		
				if(game.Won()):
					self.playoffWins += 1
				self.playoffGoalsFor += game.getGoalsFor()
				self.playoffGoalsAgainst += game.getGoalsAgainst()				
				self.playoffWinPercentage = float(self.playoffWins)/float(self.playoffGames)
		
	## Tier II load call #######################################################	
		
	def loadTierII(self, teamsList, teamRank):	
		print "Load call watMuTeam Tier II, team %s, Id %s" % (self.getTeamName(), self.teamId)
		self.averageWinQualityIndex = 0
		self.averagePlayQualityIndex = 0
		
		self.defenceQualityIndex = 0.0
		self.offenceQualityIndex = 0.0		
		
		self.seasonRank = teamRank+1
		## team rank is the index of this team after sorting
		
		for game in self.getSeasonGames():
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
			self.offenceQualityIndex += (game.getGoalsFor()-opponent.getSeasonGoalsAgainstAverage())
			self.defenceQualityIndex += (game.getGoalsAgainst()-opponent.getSeasonGoalsForAverage())
			if(game.Lost() != True):	
				if(game.Won()):
					self.averageWinQualityIndex += (game.getGoalDifferential()*opponent.getSeasonPointsTotal()) 
					self.averagePlayQualityIndex += (game.getGoalDifferential()*opponent.getSeasonPointsTotal()*game.getGameClosenessIndex()) 					
				elif(game.Tied()):
					self.averageWinQualityIndex += (opponent.getSeasonPointsTotal())
					self.averagePlayQualityIndex += (opponent.getSeasonPointsTotal()*game.getGameClosenessIndex())						
		self.averageWinQualityIndex /= float(self.totalSeasonGames)
		self.averagePlayQualityIndex /= float(self.totalSeasonGames)	


	## Tier III load call ######################################################

	def loadTierIII(self, teamsList):	
		print "Load call watMuTeam Tier III, team %s" % self.getTeamName()

		self.meanAdjustedAverageWinQualityIndex = self.averageWinQualityIndex
		self.meanAdjustedAveragePlayQualityIndex = self.averagePlayQualityIndex
		
		self.meanAdjustedOffenceQualityIndex = self.getOffenceQualityIndex()
		self.meanAdjustedDefenceQualityIndex = self.getDefenceQualityIndex()
		
		awqiMean = 0.00
		apqiMean = 0.00
		oqiMean = 0.00
		dqiMean = 0.00
		
		for team in teamsList:
			awqiMean += team.getAWQI()
			apqiMean += team.getAPQI()
			oqiMean += team.getOffenceQualityIndex()
			dqiMean += team.getDefenceQualityIndex()
			
		awqiMean /= float(len(teamsList))
		apqiMean /= float(len(teamsList))
		oqiMean /= float(len(teamsList))
		dqiMean /= float(len(teamsList))		
		
		self.meanAdjustedAverageWinQualityIndex /= awqiMean
		## this matches the spreadsheet perfectly
		self.meanAdjustedAveragePlayQualityIndex /= apqiMean
		## cant find any mistakes in how this is calculated, but the values dont
		## match what the spreadsheet had		
		
		## because these values are calculated differently
		## PQI in the spreadsheet was just a product of the averages for AWQI
		## and AGCI
		
		## thats why these values are different from what the spreadsheet had
		## cause they get calculated for every game and then summed, instead of
		## being calculated at the end
		self.meanAdjustedOffenceQualityIndex -= oqiMean
		self.meanAdjustedDefenceQualityIndex -= dqiMean
	
	def loadTierIV(self, teamsList, seasonsList):
		self.Players = []
		## list containing player objects 
		for playerName in self.Roster:
			self.Players.append(watMuPlayer(playerName, seasonsList))
	
	def getDescriptionString(self):
		return "%s, %s (season %i)\nRank: %i (%i)%s, Pts %i Pct: %.3f,\nAGCI: %.3f, MaAWQI %.3f, MaAPQI %.3f Defence Quality Index %.3f, Offence Quality Index %.3f\nOffense: %.3f, Defense %.3f, +/- %i, Average SOC of %.3f\nPlayoff Win percentage of %.3f, Playoff Offence %.3f, Playoff Defence %.3f" % (self.getTeamName(), self.getSeasonId(), self.getSeasonIndex(), self.getSeasonRank(), self.totalSeasonGames, self.getRecordString(), self.getSeasonPointsTotal(), self.getPointsPercentage(), self.getAGCI(), self.getMaAWQI(), self.getMaAPQI(), self.getDefenceQualityIndex(), self.getOffenceQualityIndex(), self.getSeasonGoalsForAverage(), self.getSeasonGoalsAgainstAverage(), self.seasonPlusMinus, self.getSeasonAverageSOC(), self.getPlayoffWinPercentage(), self.getPlayoffGoalsForAverage(), self.getPlayoffGoalsAgainstAverage())		
	
	def getSeasonIndex(self):
		return getSeasonIndexById(self.getSeasonId(), getSeasonIndexList('watMu'))
	
	def __repr__(self):
		return "<%s>" % (self.getDescriptionString())

	def qualifiedForPlayoffs(self):
		## note that this specifically refers to whether the team played any
		## playoff games, not whether they made the top "real" playoff bracket
		
		## the only team thats going to miss on this one is a team that got
		## DQed from the playoffs
		if(self.totalPlayoffGames > 0):
			return True
		else:
			return False

	def getSeasonGames(self):
		return self.Games[0:self.totalSeasonGames]
		
	def getPlayoffGames(self):
		if(self.qualifiedForPlayoffs() == True):
			return self.Games[self.totalSeasonGames:self.seasonLength]
		else:
			print "Unable to return playoff games, %s did not qualify for playoffs"
			
	def getPlayoffOpponentTeamNames(self):
		output = []
		for playoffGame in self.getPlayoffGames():
			output.append(playoffGame.getOpponentName())
		return output
		
	def getPlayoffOpponentTeamSeeds(self, season):
		output = []
		for playoffGame in self.getPlayoffGames():
			opponentTeam = season.getTeamByTeamName(playoffGame.getOpponentName())
			output.append(opponentTeam.getSeasonRank())
		return output	

	def getFranchise(self, franchiseList):
		output = 'None'
		for franchise in franchiseList:
			if(self.getTeamName().decode('utf-8') in franchise):
				output = franchise[0].decode('utf-8')
		return output

