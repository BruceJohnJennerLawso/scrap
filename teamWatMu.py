## teamWatMu.py ################################################################
## object representing a team playing in waterloo ##############################
## intramural hockey ###########################################################
################################################################################
from team import *
from gameWatMu import *
from playerWatMu import *






class watMuTeam(Team):
	def __init__(self, leagueId, levelId, seasonId, teamId):
		super(watMuTeam, self).__init__(leagueId, levelId, seasonId, teamId)
		## call the super parent constructor, which does a few basic assignments
		## of the IDs provided, then creates the Games list, and sets the load
		## path for the csv. Finally, the base constructor kicks off
		## loadTierI(...) automatically so the base data from the csv gets
		## loaded
		
	
		
	## Tier I load call ########################################################	
		
	def loadTierI(self, debugInfo=False):
		
		rows = self.getCsvRowsList()
		
		self.teamName = rows[0][0]
		self.seasonId = rows[0][1]
		
		
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
		self.totalPlayoffGames = int(rows[1][4])
		## total playoff games actually played
		
		scheduleData = rows[2:(self.seasonLength + 2)]
		## slice out only the rows that contain games data
		for game in scheduleData:
			self.Games.append(watMuGame(str(game[0]), str(game[1]), str(game[2]), int(game[3]), int(game[4]), str(game[5]), str(game[6])))
			## set up each game as an object in memory
		
		
		## rosters...
		self.Roster = rows[ (self.seasonLength + 3) ]
		
		if(debugInfo):
			print "\nRoster:"
			for r in self.Roster:
				print r
		
		
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
		
		
		
		
		
		
		
		
	## Tier II load call #######################################################	
		
	def loadTierII(self, teamsList, teamRank, debugInfo=False):	
		debugInfo = True
		
		
		
		print "Load call watMuTeam Tier II, team %s %s, Id %s" % (self.getTeamName(), self.seasonId, self.teamId)
		
		
		self.averageWinQualityIndex = 0.000
		self.averagePlayQualityIndex = 0.000
		
		self.defenceQualityIndex = 0.000
		self.offenceQualityIndex = 0.000		
		
		self.diffQualityIndex = 0.000
		
		self.seasonRank = teamRank+1
		## team rank is the index of this team after sorting based on the watMu
		## standings criteria
		
		for game in self.getSeasonGames():
			## we dont need to reload the data from csv, cause it was already
			## loaded by the loadTierI(...) call and stored in objects
			
			opponentFound = False			
			## start off by looking for our opponents object in the list of
			## teams that we were given to search
			for team in teamsList:
				if(team.getTeamName() == game.getOpponentName()):
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

			self.offenceQualityIndex += (game.getGoalsFor()-opponent.getSeasonGoalsAgainstAverage())
			## for each game the OQI is goals scored above expectations, so we
			## add that value to the total OQI
			self.defenceQualityIndex += (opponent.getSeasonGoalsForAverage()-game.getGoalsAgainst())
			## and for each game, the DQI is goals allowed below expectations,
			self.diffQualityIndex += (game.getGoalDifferential()-opponent.getSeasonGoalDifferentialAverage())
			## so we add that value to the total DQI
			if(game.Lost() != True):	
				## so long as we didnt lose the game, we will get a nonzero
				## value for WQI and PQI, varying depending on the game stats
				## and whether the game was a win or a tie
				if(game.Won()):
					self.averageWinQualityIndex += (game.getGoalDifferential()*opponent.getSeasonPointsTotal()) 
					self.averagePlayQualityIndex += (game.getGoalDifferential()*opponent.getSeasonPointsTotal()*game.getGameClosenessIndex()) 					
				elif(game.Tied()):
					self.averageWinQualityIndex += (opponent.getSeasonPointsTotal())
					self.averagePlayQualityIndex += (opponent.getSeasonPointsTotal()*game.getGameClosenessIndex())						
		self.averageWinQualityIndex /= float(self.totalSeasonGames)
		self.averagePlayQualityIndex /= float(self.totalSeasonGames)	
		## once we've calculated the total WQI & PQI, divy them over the total
		## games played in that season to get an average

	## Tier III load call ######################################################

	def loadTierIII(self, teamsList, madeRealPlayoffs):	
		print "Load call watMuTeam Tier III, team %s" % self.getTeamName()
		
		self.realPlayoffs = madeRealPlayoffs
		
		self.calculateMaValues(teamsList)
		## send the list of team objects for this season off so we can get our
		## mean adjusted values
	
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
		return "%s, %s (season %i) (%s)\nRank: %i (%i)%s, Pts %i Pct: %.3f,\nAGCI: %.3f, MaAWQI %.3f, MaAPQI %.3f\nDefence Quality Index %.3f, Offence Quality Index %.3f Diff Quality Index %.3f\nMaADQI %.3f, MaAOQI %.3f, MaADiffQI %.3f, SQI %.3f, CPQI %.3f\nOffense: %.3f, Defense %.3f, +/- %i, Average SOC of %.3f\nPlayoff Win %% of %.3f\nPlayoff Offence %.3f, Playoff Defence %.3f, Playoff Avg. Goal Diff %.3f" % (self.getTeamName(), self.getSeasonId(), self.getSeasonIndex(), self.levelId, self.getSeasonRank(), self.totalSeasonGames, self.getRecordString(), self.getSeasonPointsTotal(), self.getPointsPercentage(), self.getAGCI(), self.getMaAWQI(), self.getMaAPQI(), self.getDefenceQualityIndex(), self.getOffenceQualityIndex(), self.getDiffQualityIndex(), self.getMaADQI(), self.getMaAOQI(), self.getMaADiffQI(), self.getSQI(), self.getCPQI(), self.getSeasonGoalsForAverage(), self.getSeasonGoalsAgainstAverage(), self.seasonPlusMinus, self.getSeasonAverageSOC(), self.getPlayoffWinPercentage(), self.getPlayoffGoalsForAverage(), self.getPlayoffGoalsAgainstAverage(), self.getPlayoffAverageGoalDifferential())		
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

	def getSeasonGames(self):
		## all game objects for watMu are stored in a list that has reg season
		## and playoffs inclusive
		
		## so we need to slice the list to get only season games
		return self.Games[0:self.totalSeasonGames]
		
	def getPlayoffGames(self):
		if(self.qualifiedForPlayoffs() == True):
			## quick check that there are playoff games to be had
			return self.Games[self.totalSeasonGames:self.seasonLength]
		else:
			## maybe we should throw something here?
			## this pretty much always gets checked anyways
			##print "Unable to return playoff games, %s did not qualify for playoffs"
			return []
			
			
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
		return "(%s-%s-%s)" % (self.seasonWins, self.seasonLosses, self.seasonTies)
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
	daDads = watMuTeam('watMu', 'beginner', 'fall2015', 12348)
	## quick test using the one and only Mighty Dads fall 2015
