## teamNhl.py ##################################################################
## object representing a team playing in the NHL ###############################
################################################################################
from team import *
from gameNhl import *		
from playerNhl import *




class nhlTeam(Team):
	def __init__(self, leagueId, seasonId, teamId, levelId = ''):
		super(nhlTeam, self).__init__(leagueId, levelId, seasonId, teamId)
		## call upstairs to set basic parameters
		
		## note that the levelId is an optional parameter
		## since the issue of nhl levelIds is kinda a mess
		self.loadTierI(True)
		## and lets kick this thing off by starting the load process
		## automatically
	
		
		
	## Tier I load call ########################################################	
		
	def loadTierI(self, debugInfo=False):		
		rows = self.getCsvRowsList()
		## use our utility function to retrieve the csv file for this team
		## as a rectangular list (2 deep)
		self.teamName = rows[0][0]
		## set this teams name from the raw data
		##print "%s: %s, Id: %s" % (self.teamName, rows[1][0], self.teamId)
		
		self.seasonName = rows[1][0]
		
		print "Load call nhlTeam Tier I, team %s %s, Id %s" % (self.getTeamName(), self.seasonName, self.teamId)
		##if((debugInfo)and(rawDataView)):
		##	print "\n\nraw file\n\n"
		
		
		
		self.totalSeasonGames = int(rows[3][0])
		print "Total season games %i" % self.totalSeasonGames
		## set the length of the regular season from the csv data
		self.totalPlayoffGames = 0
		## by default we assume no playoff games
		self.playoffSeriesLengths = rows[4]
		for l in self.playoffSeriesLengths:
			self.totalPlayoffGames += int(l)
			## total up the length of all playoff series from the list that
			## the scraper made sure to save
			
		scheduleHeader = rows[5]
		## our scheduleHeader looks something like
		## [GP,Date,Time,Location,Opponent,GF,GA,Result,Game Ended In,W,L,OL,Streak,S,PIM,PPG,PPO,SHG,S,PIM,PPG,PPO,SHG,Att.,LOG,Notes]
		
		## which we then use to locate the right column for each stat in the
		## rest of the data
		scheduleData = rows[6:(self.totalSeasonGames+6)]
		## next, we slice out the data for games played in the regular season
		## and dump it into a temporary variable scheduleData
		if(debugInfo):
			print scheduleHeader, '\n\n'
			for i in scheduleData:
				print i, '\n'
		
		if(self.totalPlayoffGames > 0):
			self.playoffDataHeader = rows[(self.totalSeasonGames+7)]
			## if we have playoff data, locate the playoff header in the csv
			## (offsetting for different season lengths)
			if(debugInfo):
				print 'playoff data header\n', self.playoffDataHeader, ' ', len(self.playoffDataHeader)
			
			self.playoffData = rows[(self.totalSeasonGames+8):(self.totalSeasonGames+8+self.totalPlayoffGames)]
			## and find the data of the playoff games themselves
			if(debugInfo):
				print 'playoff data[0]\n', self.playoffData[0], ' ', len(self.playoffData[0])
		
		else:
			self.playoffDataHeader = []
			self.playoffData = []
			## if there wasnt any available data for the playoffs, just create
			## empty lists
		
		
		self.playoffGames = []
		self.Games = []
		
		## ok, so now we need to construct a game object with the data that we
		## loaded 
		
		## Im thinking that we just construct the objects in place here as usual
		## then if we want summaries we can loop through everything
		## and ignore duplicates 
		
		## slice out only the rows that contain games data
		
		dateIndex = -1
		locationIndex = -1
		resultIndex = -1
		goalsForIndex = -1
		goalsAgainstIndex = -1
		opponentNameIndex = -1
		gameEndedInIndex = -1
		## define the column number for each of the basic stats we will be
		## loading for each game in the regular season schedule
		
		for i in range(0, len(scheduleHeader)):
			## roll through the header of the regular season data
			
			colStat = scheduleHeader[i]
			## for each column, set a variable for what its heading is so we
			## can try to match it
			if(colStat == 'Date'):
				dateIndex = i
				continue
			elif(colStat == 'Location'):
				locationIndex = i
				continue
			elif(colStat == 'Result'):
				resultIndex = i
				continue
			elif(colStat == 'GF'):
				goalsForIndex = i
				continue
				## check if the current column is the stat we are looking for
				## (goals for).
				## If it is, set the goalsForIndex 
				## (the column number of this stat) to the current column number
				## then jump back to the next run of the loop so we dont waste 
				## quite as much time checking for things we already found
			elif(colStat == 'GA'):
				goalsAgainstIndex = i
				continue
			elif(colStat == 'Opponent'):
				opponentNameIndex = i
				continue
			elif(colStat == 'Game Ended In'):
				gameEndedInIndex = i
				continue
			
		if(debugInfo):
			print "dateIndex %i\nlocationIndex %i\nresultIndex %i\ngoalsForIndex %i\n goalsAgainstIndex %i\nopponentNameIndex %i\ngameEndedInIndex %i\n" % (dateIndex, locationIndex, resultIndex, goalsForIndex, goalsAgainstIndex, opponentNameIndex, gameEndedInIndex)
		
		
		for game in scheduleData:
			## once we have the index of the data columns that we want, we can
			## now feed that data into a game object for each game in the
			## regular season
			
			## this really should have some protection like raising a proper
			## exception if one of the indexes is still -1 (we never found it)
			## but it gonna crash hard in that case anyways
			
			self.Games.append(nhlGame(game[dateIndex], game[locationIndex], game[resultIndex], game[goalsForIndex], game[goalsAgainstIndex],  game[opponentNameIndex], self.teamName, game[gameEndedInIndex]))
			## set up each game as an object in memory
		
		
		if(self.totalPlayoffGames > 0):
			print "Total Playoff Games ", self.totalPlayoffGames
			
			playoffDateIndex = -1
			playoffLocationIndex = -1
			playoffResultIndex = -1
			playoffGoalsForIndex = -1
			playoffGoalsAgainstIndex = -1
			playoffOpponentNameIndex = -1
			playoffGameEndedInIndex = -1
		
			if(debugInfo):
				print self.playoffDataHeader
		
			for i in range(0, len(self.playoffDataHeader)):
				## roll through the header of the playoffs data
				colStat = self.playoffDataHeader[i]
				## for each column, set a variable for what its heading is so we
				## can try to match it
				if(colStat == 'Date'):
					playoffDateIndex = i
					continue
				elif(colStat == 'Location'):
					playoffLocationIndex = i
					continue
				elif(colStat == 'Result'):
					playoffResultIndex = i
					continue
				elif(colStat == 'GF'):
					playoffGoalsForIndex = i
					continue
					## check if the current column is the stat we are looking for
					## (goals for).
					## If it is, set the goalsForIndex 
					## (the column number of this stat) to the current column number
					## then jump back to the next run of the loop so we dont waste 
					## quite as much time checking for things we already found
				elif(colStat == 'GA'):
					playoffGoalsAgainstIndex = i
					continue
				elif(colStat == 'Opponent'):
					playoffOpponentNameIndex = i
					continue
				elif(colStat == 'Game Ended In'):
					playoffGameEndedInIndex = i
					continue
			
			if(debugInfo):
				print "dateIndex %i\nlocationIndex %i\nresultIndex %i\ngoalsForIndex %i\n goalsAgainstIndex %i\nopponentNameIndex %i\ngameEndedInIndex %i\n" % (playoffDateIndex, playoffLocationIndex, playoffResultIndex, playoffGoalsForIndex, playoffGoalsAgainstIndex, playoffOpponentNameIndex, playoffGameEndedInIndex)
				for p in self.playoffData:
					print p
		
			for game in self.playoffData:
				## need to define who the home team was here based on whether there
				## was an @ or an H
			
				self.playoffGames.append(nhlGame(game[playoffDateIndex], game[playoffLocationIndex], game[playoffResultIndex], game[playoffGoalsForIndex], game[playoffGoalsAgainstIndex],  game[playoffOpponentNameIndex], self.teamName, game[playoffGameEndedInIndex]))
				## set up each game as a nhlGame object in memory
		
		
		rosterSize = int(rows[2][0])
		## look up the number of players on the roster from the csv
		
		## future note: this really needs to account for how big the changes
		## in roster composition can be over the course of an NHL season.
		## At least a openingNight roster and a deadline roster would be a start
		## if I can find the data
		self.RosterData = rows[(self.totalSeasonGames+11+self.totalPlayoffGames):(self.totalSeasonGames+11+self.totalPlayoffGames+rosterSize)]
		## slice out the rows of data (one player per row) with our ever more
		## complex system for determining the start and end indexes :s
		
		## note that RosterData is all of the data for the players that was
		## available 
		self.Roster = []
		## JUST the names of players on the roster
		for rostDat in self.RosterData:
			self.Roster.append(rostDat[0])
			## hence the 0 index
		
		## this section is very rudimentary at the moment, but it will get more
		## complex and useful eventually with column indexes and things like
		## that
		
		if(debugInfo):	
			print 'Roster:\n'
			if(debugInfo):
				for p in self.Roster:
					print p, '\n'
		
		self.seasonPlusMinus = 0
		## goal differential for the team overall
		self.seasonTotalGoalsFor = 0
		self.seasonTotalGoalsAgainst = 0	
		## pretty self explanatory
		self.seasonPointsTotal = 0
		## 2 for a win, 1 for a tie/(ot/so) loss, 0 for a regulation loss
		## (depending on whether the game was before or after 2002)
		
		## Thanks Bettman	
		self.seasonWins = 0
		self.seasonTies = 0
		self.seasonRegulationLosses = 0
		self.seasonExtraTimeLosses = 0
		self.averageGameClosenessIndex = 0
		
		
		## now that we have the season and playoff games loaded, we can make
		## our totals/averages/what have you for tier I stats
		for game in self.getSeasonGames():
			
			self.seasonTotalGoalsFor += game.getGoalsFor()
			self.seasonTotalGoalsAgainst += game.getGoalsAgainst()
			
			self.seasonPlusMinus += game.getGoalDifferential()
			self.seasonPointsTotal += game.getPointsEarned(self.getSeasonIndex())
			
			if(game.Won()):
				self.seasonWins += 1
			elif(game.Tied()):
				self.seasonTies += 1
			elif(game.Lost()):
				if(game.decidedInExtraTime()):
					self.seasonExtraTimeLosses += 1
				else:
					self.seasonRegulationLosses += 1
			## this is such a mess, especially trying to print out a record
			## string that makes sense across eras with this steaming pile of
			## crap
			
			## again, really, thanks Bettman
			self.averageGameClosenessIndex += game.getGameClosenessIndex()	
			## see game module for more on this	

		self.averageGameClosenessIndex /= float(self.totalSeasonGames)
		## divy the GCI total over the games played for our average

		
		## now, we can quickly tally some stats for the playoffs, so we can
		## do some graphing
		self.playoffWins = 0
		self.totalPlayoffGames = 0
		
		self.playoffWinPercentage = 0.000
		## not nearly as useful as it is for watMu (you can at least lose one
		## game in the NHL playoffs without going home right away), but why not
		## hang on to it
		
		self.playoffGoalsFor = 0
		self.playoffGoalsAgainst = 0
		self.playoffPlusMinus = 0
		self.playoffAverageGoalDifferential = 0.000		
		
		if(self.qualifiedForPlayoffs()):
			self.totalPlayoffGames = len(self.getPlayoffGames())
			for game in self.getPlayoffGames():		
				if(game.Won()):
					self.playoffWins += 1
				
				self.playoffGoalsFor += game.getGoalsFor()
				self.playoffGoalsAgainst += game.getGoalsAgainst()				
				self.playoffPlusMinus += (game.getGoalsFor() - game.getGoalsAgainst())
			
			self.playoffWinPercentage = float(self.playoffWins)/float(self.getTotalPlayoffGames())
			self.playoffAverageGoalDifferential = self.playoffPlusMinus/float(self.getTotalPlayoffGames())
			
			self.playoffOffence = self.playoffGoalsFor/float(self.totalPlayoffGames)
			self.playoffDefence = self.playoffGoalsAgainst/float(self.totalPlayoffGames)
		
	## Tier II load call #######################################################	
		
	def loadTierII(self, teamsList, teamRank):	
		print "Load call nhlTeam Tier II, team %s %s, Id %s" % (self.getTeamName(), self.seasonName, self.teamId)
		
		self.averageWinQualityIndex = 0
		self.averagePlayQualityIndex = 0
		
		self.defenceQualityIndex = 0.0
		self.offenceQualityIndex = 0.0		
		
		self.diffQualityIndex = 0.000
		
		self.seasonRank = teamRank+1
		## team rank is the index of this team after sorting
		
		for game in self.getSeasonGames():
			## we dont need to reload the data, cause it was already loaded by
			## the loadTierI(...) call as game objects
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
				raise NameError('Team %s Unable to find scheduled opponent %s as team object' % (self.getTeamName(), game.getOpponentName()))

			self.offenceQualityIndex += (game.getGoalsFor()-opponent.getSeasonGoalsAgainstAverage())
			self.defenceQualityIndex += (opponent.getSeasonGoalsForAverage()-game.getGoalsAgainst())
			self.diffQualityIndex += (game.getGoalDifferential()-opponent.getSeasonGoalDifferentialAverage())
			
			if(game.Lost() != True):	
				if(game.Won()):
					self.averageWinQualityIndex += (game.getGoalDifferential()*opponent.getSeasonPointsTotal()) 
					self.averagePlayQualityIndex += (game.getGoalDifferential()*opponent.getSeasonPointsTotal()*game.getGameClosenessIndex()) 					
				elif((game.Tied()) or ((game.Lost()) and (game.decidedInExtraTime()))):
					self.averageWinQualityIndex += (opponent.getSeasonPointsTotal())
					self.averagePlayQualityIndex += (opponent.getSeasonPointsTotal()*game.getGameClosenessIndex())						
		
		self.averageWinQualityIndex /= float(self.totalSeasonGames)
		self.averagePlayQualityIndex /= float(self.totalSeasonGames)	

	## Tier III load call ######################################################

	def loadTierIII(self, teamsList, madeRealPlayoffs):	
		print "Load call watMuTeam Tier III, team %s" % self.getTeamName()
		self.calculateMaValues(teamsList)
	
	def loadTierIV(self, teamsList, seasonsList):
		self.Players = []
		## list containing player objects 
		##for playerName in self.Roster:
		##	self.Players.append(watMuPlayer(playerName, seasonsList))

		## gonna leave this offline for the moment, not too eager to dive into
		## the fustercluck of writing an NHL player object just right now
	
	def getDescriptionString(self):
		return "%s, %s (season %i)\nRank: %i (%i)%s, Pts %i Pct: %.3f,\nAGCI: %.3f, MaAWQI %.3f, MaAPQI %.3f\nDefence Quality Index %.3f, Offence Quality Index %.3f, Diff Quality Index %.3f\nMaADQI %.3f, MaAOQI %.3f MaADiffQI %.3f\nOffense: %.3f, Defense %.3f, +/- %i\n%i Playoff Wins, Playoff Win %% of %.3f, Playoff Offence %.3f, Playoff Defence %.3f, Playoff Avg. Goal Diff %.3f" % (self.getTeamName(), self.getSeasonId(), self.getSeasonIndex(), self.getSeasonRank(), self.totalSeasonGames, self.getRecordString(), self.getSeasonPointsTotal(), self.getPointsPercentage(), self.getAGCI(), self.getMaAWQI(), self.getMaAPQI(), self.getDefenceQualityIndex(), self.getOffenceQualityIndex(), self.getDiffQualityIndex(), self.getMaADQI(), self.getMaAOQI(), self.getMaADiffQI(), self.getSeasonGoalsForAverage(), self.getSeasonGoalsAgainstAverage(), self.seasonPlusMinus, self.playoffWins, self.getPlayoffWinPercentage(), self.getPlayoffGoalsForAverage(), self.getPlayoffGoalsAgainstAverage(), self.getPlayoffAverageGoalDifferential())		
		## I need to make a list of differences between this desc string and
		## the watMu version
	
	def getSeasonIndex(self):
		
		return getSeasonIndexById(self.getSeasonId(), getSeasonIndexList('nhl'))
		## not really that important for NHL, but the indexes might be kinda
		## handy for graphing
	
	def __repr__(self):
		return "<%s>" % (self.getDescriptionString())

	def qualifiedForPlayoffs(self):
		## in the case of the NHL (and most leagues) it is totally possible to
		## miss the playoffs, so
		if(len(self.playoffGames) > 0):
			return True
		else:
			return False

	def getSeasonGames(self):
		## old relic of copied hasty code here
		## just want to test this first
		##return self.Games[0:self.totalSeasonGames]
		return self.Games
		
	def getPlayoffGames(self):
			return self.playoffGames
			
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
			## loop through the franchises available, ie
			## ['The Mighty Ducks of Anaheim', 'Anaheim Ducks']
			
			## screw you Burkie
			if(self.getTeamName().decode('utf-8') in franchise):
				output = franchise[0].decode('utf-8')
				## if we had a match, output the first (most appropriate) name
				## in that franchises list of names
		return output

	def getRecordString(self):
		return "(%s-%s-%s)" % (self.seasonWins, self.seasonRegulationLosses, self.seasonExtraTimeLosses)
		## I dont have the patience to do this right now, so this is only
		## applicable for post 2005 lockout, with the shootout and loser point

		## have I mentioned all of the horrible things I would like to do to
		## our friend Gary???

	def calculatePlayoffSuccessRating(self):
		return self.playoffWins
		
	def madeRealPlayoffs(self):	
		return self.qualifiedForPlayoffs()


if(__name__ == "__main__"):
	
	##daBuds = nhlTeam('nhl', '2016', 'TOR')
	##daSharks = nhlTeam('nhl', '2016', 'SJS')
	
	fuckTampa = nhlTeam('nhl', '2015', 'TBL')
	## quick test to make sure everything is loading correctly
	print fuckTampa.getTotalPlayoffGames()
	print fuckTampa.getTotalPlayoffWins()
	
	for game in fuckTampa.getPlayoffGames():
		print game.getGameDescription()
	
	## San Jose 2015-16 used as an example here cause they made the playoffs
	## and went to the finals, so there shouldnt be anything turned off
	##print getSeasonIndexList('nhl')
