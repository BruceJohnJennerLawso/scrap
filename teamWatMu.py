## teamWatMu.py ################################################################
## object representing a team playing in waterloo ##############################
## intramural hockey ###########################################################
################################################################################
from team import *
from gameWatMu import *
from playerWatMu import *
import seasonParts





class watMuTeam(Team):
	def __init__(self, leagueId, levelId, seasonId, teamId, debugInfo=False):
		super(watMuTeam, self).__init__(leagueId, levelId, seasonId, teamId, debugInfo)
		## call the super parent constructor, which does a few basic assignments
		## of the IDs provided, then creates the Games list, and sets the load
		## path for the csv. Finally, the base constructor kicks off
		## loadTierI(...) automatically so the base data from the csv gets
		## loaded
		
	
		
	## Tier I load call ########################################################	
	
	def calculateTierIStats(self, debugInfo=False):
		
		self.averageSOC = 0	
		for game in self.getSeasonGames():
			self.averageSOC += game.getSOC()
			
		if(debugInfo):	
			print "Total season games %i" % self.totalSeasonGames
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
		
		
	
	def loadSeasonGames(self, rows, debugInfo=False):
		seasonGames = []
		
		startOfSeasonRows = 2
		endOfSeasonRows = startOfSeasonRows + self.totalSeasonGamesPlayed
		seasonData = rows[startOfSeasonRows:(endOfSeasonRows)]
		## slice out only the rows that contain games data and ignore games that
		## have not yet been played
		for game in seasonData:
			seasonGames.append(watMuGame(str(game[0]), str(game[1]), str(game[2]), int(game[3]), int(game[4]), str(game[5]), str(game[6]), seasonParts.gamesSelectConditions(part="regularSeason"), self.getSeasonIndex()))
			## set up each game as an object in memory
		if(debugInfo):
			print "seasonData: "
			for row in seasonData:
				print row	
	
		return seasonGames
	
	def calculateSocValues(self, debugInfo=False):
		self.averageSOC = 0.000
		averageSOCGames = 0
		
		for game in self.getSeasonGames():
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
		
		SOC = float(self.averageSOC)/float(self.totalSeasonGamesPlayed-averageSOCGames) 
		## start off by getting our average for the games that had an SOC number
		## available
		
		if(averageSOCGames > 0):
			## loop through the games again, if the value fails we overwrite it
			## with the average of the games that were defined
			for game in self.seasonGames:
				
				if(debugInfo):
					print game.Layers[0]
				
				try:
					game.getSOC()
				except ValueError:
					if(debugInfo):
						print "Failed int() cast due to ValueError"
					game.setSOC(SOC)
					if(debugInfo):
						print game.Layers[0]
	
	def loadPlayoffGames(self, rows, debugInfo=False):
		playoffGames = []
		
		startOfPlayoffRows = 2+self.totalSeasonGames
		endOfPlayoffRows = startOfPlayoffRows + self.totalPlayoffGamesPlayed
		
		playoffData = rows[(startOfPlayoffRows):(endOfPlayoffRows)]
		## slice out only the rows that contain games data and ignore games that
		## have not yet been played
		for game in playoffData:
			playoffGames.append(watMuGame(str(game[0]), str(game[1]), str(game[2]), int(game[3]), int(game[4]), str(game[5]), str(game[6]), seasonParts.gamesSelectConditions(part="none"), self.getSeasonIndex()))
			## set up each game as an object in memory

		if(debugInfo):
			print "\nplayoffData: "
			for row in playoffData:
				print row
		return playoffGames
		
	def loadTierI(self, debugInfo=False):
		##debugInfo = True
		rows = self.getCsvRowsList()
		
		self.teamName = rows[0][0]
		self.seasonId = rows[0][1]
		
		if(debugInfo):
			print "Load call watMuTeam Tier I, team %s %s, Id %s" % (self.getTeamName(), self.seasonId, self.teamId)
		
		self.seasonLength = int(rows[1][0])
		## everything in the schedule, including playoff games
		
		self.totalSeasonGames = int(rows[1][1])
		## this is going to be the total length of the season schedule,
		## including games that have not yet been played
		self.totalSeasonGamesPlayed = int(rows[1][2])
		## only the total of games in the season schedule that have been played
		self.totalPlayoffGames = int(rows[1][3])
		## total playoff games listed, including the TBDs
		self.totalPlayoffGamesPlayed = int(rows[1][4])
		## total playoff games actually played
		
		if(debugInfo):
			print "total season length %i games" % self.seasonLength
			print "total season games in schedule %i" % self.totalSeasonGames
			print "total season games played so far %i games" % self.totalSeasonGamesPlayed
			print "total playoff games scheduled %i games" % self.totalPlayoffGames
			print "total playoff games played so far %i games" % self.totalPlayoffGamesPlayed
		
		self.seasonGames = self.loadSeasonGames(rows, debugInfo)
		self.calculateSocValues(debugInfo)
		self.playoffGames = self.loadPlayoffGames(rows, debugInfo)
		
		## rosters...
		self.Roster = rows[ (self.seasonLength + 3) ]
		
		if(debugInfo):
			print "\nRoster:"
			for r in self.Roster:
				print r
		
		self.calculateTierIStats(debugInfo)

		
	## Tier IV load call ######################################################

	
	def loadTierIV(self, teamsList, seasonsList):
		self.Players = []
		## list containing player objects 
		for playerName in self.Roster:
			self.Players.append(watMuPlayer(playerName, seasonsList))
			## roll through the names of all the players on the roster and set
			## up their player type object based on all of the season objects
			## available in this dataset
		
	def getSeasonAverageSOC(self):
		return self.averageSOC	
		## the only value that needs to be defined here (instead of in the
		## parent team type), since SOC only applies in waterloo intramurals
		
	def getDescriptionString(self):
		output = "%s, %s (season %i) (%s)\n" % (self.getTeamName(), self.getSeasonId(), self.getSeasonIndex(), self.levelId)
		output += "Rank: %i (%i)%s, Pts %i Pct: %.3f,\n" % (self.getSeasonRank(), self.totalSeasonGames, self.getRecordString(), self.getSeasonPointsTotal(), self.getPointsPercentage()) 
		output += "AGCI: %.3f, MaAWQI %.3f, MaAPQI %.3f\n" % (self.getAGCI(), self.getMaAWQI(), self.getMaAPQI())
		output += "Defence Quality Index %.3f, Offence Quality Index %.3f Diff Quality Index %.3f\n" % (self.getDefenceQualityIndex(), self.getOffenceQualityIndex(), self.getDiffQualityIndex())
		output += "ADQI %.3f, AOQI %.3f, MaADiffQI %.3f, SQI %.3f, CPQI %.3f, DQM %.3f\n" % (self.getADQI(), self.getAOQI(), self.getMaADiffQI(), self.getSQI(), self.getCPQI(), self.getDQM()) 
		output += "Offense: %.3f, Defense %.3f, +/- %i, Average SOC of %.3f\n" % (self.getSeasonGoalsForAverage(), self.getSeasonGoalsAgainstAverage(), self.getSeasonPlusMinus(), self.getSeasonAverageSOC()) 
		output += "Playoff Win %% of %.3f\n" % self.getPlayoffWinPercentage()
		output += "Playoff Offence %.3f, Playoff Defence %.3f, Playoff Avg. Goal Diff %.3f\n" % (self.getPlayoffGoalsForAverage(), self.getPlayoffGoalsAgainstAverage(), self.getPlayoffAverageGoalDifferential())
		output += "CPQI %.3f, (%.3f/%.3f) front/back (%.3f FBS)\n" % (self.getSeasonPart(seasonParts.getGameSelectConditions("regularSeason")).getAverageForStat(Game.getCPQI), self.getSeasonPart(seasonParts.getGameSelectConditions("firstHalfRegularSeason")).getAverageForStat(Game.getCPQI), self.getSeasonPart(seasonParts.getGameSelectConditions("secondHalfRegularSeason")).getAverageForStat(Game.getCPQI), self.getFrontBackSplit())
		output += "Defence %.3f, (%.3f/%.3f)\n" % (self.getSeasonPart(seasonParts.getGameSelectConditions("regularSeason")).getAverageForStat(Game.getGoalsAgainst), self.getSeasonPart(seasonParts.getGameSelectConditions("firstHalfRegularSeason")).getAverageForStat(Game.getGoalsAgainst), self.getSeasonPart(seasonParts.getGameSelectConditions("secondHalfRegularSeason")).getAverageForStat(Game.getGoalsAgainst))
		output += "Offence %.3f, (%.3f/%.3f)\n" % (self.getSeasonPart(seasonParts.getGameSelectConditions("regularSeason")).getAverageForStat(Game.getGoalsFor), self.getSeasonPart(seasonParts.getGameSelectConditions("firstHalfRegularSeason")).getAverageForStat(Game.getGoalsFor), self.getSeasonPart(seasonParts.getGameSelectConditions("secondHalfRegularSeason")).getAverageForStat(Game.getGoalsFor))		

		output += "Rel Front: ADQI %.3f, AOQI %.3f\n" % (self.getADQI(seasonParts.getGameSelectConditions("firstHalfRegularSeason")), self.getAOQI(seasonParts.getGameSelectConditions("firstHalfRegularSeason")))				
		output += "Rel Back: ADQI %.3f, AOQI %.3f\n" % (self.getADQI(seasonParts.getGameSelectConditions("secondHalfRegularSeason")), self.getAOQI(seasonParts.getGameSelectConditions("secondHalfRegularSeason")))
		output += "Rel Total: ADQI %.3f, AOQI %.3f" % (self.getADQI(), self.getAOQI())									
		return output
		## I should really line break this so it fits into a terminal with less
		## than 850 columns nicely
	
	
	def getSeasonIndex(self):
		return getSeasonIndexById(self.getSeasonId(), getSeasonIndexList('watMu'))
		## given that we know this team is a watMu team, we can retrieve a list
		## of season indexes, which allow us to pin down the correct order that
		## seasons should go in by assigning an integer to each season
		
		## its just a really complicated way of placing things in order right
	
	def __repr__(self):
		return "<%s>" % (self.getDescriptionString())
		## this actually isnt a great choice for this, the desc string is super
		## long

	def qualifiedForPlayoffs(self):
		## note that this specifically refers to whether the team played any
		## playoff games, not whether they made the top "real" playoff bracket
		
		## the only team thats going to miss on this one is a team that got
		## DQed from the playoffs
		if(self.totalPlayoffGames > 0):
			return True
		else:
			return False


			
			
	def getPlayoffOpponentTeamNames(self):
		## helper function for the code that retrieves playoff brackets
		output = []
		for playoffGame in self.getPlayoffGames():
			output.append(playoffGame.getOpponentName())
		return output
		
	def getPlayoffOpponentTeamSeeds(self, season):
		## helper function for the code that retrieves playoff brackets
		output = []
		for playoffGame in self.getPlayoffGames():
			opponentTeam = season.getTeamByTeamName(playoffGame.getOpponentName())
			output.append(opponentTeam.getSeasonRank())
		return output	

	def getFranchise(self, franchiseList):
		output = 'None'
		for franchise in franchiseList:
			## loop through the list of franchises that are available, ie
			## ['Seekers', 'SEEKZERS']
			if(self.getTeamName().decode('utf-8') in franchise):
				output = franchise[0].decode('utf-8')
				## if the name of this current team was found in the possible
				## names for the team as listed in the franchises csv
				## set the franchise name for this team as the first
				## (most appropriate) name for this teams franchise, ie
				## SEEKZERS.getFranchise(franchiseList) -> 'Seekers'
				break
		return output

	def getRecordString(self):
		return "(%s-%s-%s)" % (self.getSeasonWinsTotal(), self.getSeasonLossTotal(), self.getSeasonTiesTotal())
		## typical hockey stat used for decades

	def calculatePlayoffSuccessRating(self):
		if(self.realPlayoffs):
			return self.getPlayoffWinPercentage()
		else:
			return 0.000
			## if its not the top playoff bracket, it doesnt count as the 'real'
			## playoffs

	def madeRealPlayoffs(self):
		return self.realPlayoffs

if(__name__ == "__main__"):
	daDads = watMuTeam('watMu', 'beginner', 'fall2015', 12348, True)
	## quick test using the one and only Mighty Dads fall 2015
