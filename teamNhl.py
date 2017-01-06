## teamNhl.py ##################################################################
## object representing a team playing in the NHL ###############################
################################################################################
from team import *
from gameNhl import *		
from playerNhl import *
import seasonParts



class nhlTeam(Team):
	def __init__(self, leagueId, seasonId, teamId, levelId = '', debugInfo=False):
		super(nhlTeam, self).__init__(leagueId, levelId, seasonId, teamId, debugInfo)
		## call upstairs to set basic parameters
		
		## note that the levelId is an optional parameter
		## since the issue of nhl levelIds is kinda a mess
	
		
		
	## Tier I load call ########################################################	
		
		
	def calculateTierIStats(self):		
		pass
		
		
		
		
	def loadTierI(self, debugInfo=False):		
		rows = self.getCsvRowsList()
		## use our utility function to retrieve the csv file for this team
		## as a rectangular list (2 deep)
		self.teamName = rows[0][0]
		## set this teams name from the raw data
		##print "%s: %s, Id: %s" % (self.teamName, rows[1][0], self.teamId)
		
		self.seasonName = rows[1][0]
		if(debugInfo):
			print "Load call nhlTeam Tier I, team %s %s, Id %s" % (self.getTeamName(), self.seasonName, self.teamId)
		##if((debugInfo)and(rawDataView)):
		##	print "\n\nraw file\n\n"
		
		
		
		self.totalSeasonGames = int(rows[3][0])
		if(debugInfo):
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
			
			self.seasonGames.append(nhlGame(game[dateIndex], game[locationIndex], game[resultIndex], game[goalsForIndex], game[goalsAgainstIndex],  game[opponentNameIndex], self.teamName, game[gameEndedInIndex], seasonParts.getGameSelectConditions("regularSeason"), self.getSeasonIndex()))
			## set up each game as an object in memory
		
		
		if(self.totalPlayoffGames > 0):
			if(debugInfo):
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
			
				self.playoffGames.append(nhlGame(game[playoffDateIndex], game[playoffLocationIndex], game[playoffResultIndex], game[playoffGoalsForIndex], game[playoffGoalsAgainstIndex],  game[playoffOpponentNameIndex], self.teamName, game[playoffGameEndedInIndex], seasonParts.getGameSelectConditions("everything"), self.getSeasonIndex()))
				## set up each game as a nhlGame object in memory
		
		
		rosterSize = int(rows[2][0])
		## look up the number of players on the roster from the csv
		
		## future note: this really needs to account for how big the changes
		## in roster composition can be over the course of an NHL season.
		## At least a openingNight roster and a deadline roster would be a start
		## if I can find the data
		self.RosterData = rows[(self.totalSeasonGames+9+self.totalPlayoffGames):(self.totalSeasonGames+11+self.totalPlayoffGames+rosterSize)]
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
		if(debugInfo):
			print "Calculating Tier I stats"
		self.calculateTierIStats()			
		if(debugInfo):
			print "Finished calculating Tier I stats"

	## Tier IV load call ######################################################

	def loadTierIV(self, teamsList, seasonsList):
		self.Players = []
		## list containing player objects 
		##for playerName in self.Roster:
		##	self.Players.append(watMuPlayer(playerName, seasonsList))

		## gonna leave this offline for the moment, not too eager to dive into
		## the fustercluck of writing an NHL player object just right now
	
	def getDescriptionHeader(self):		
		return "%s, %s (season %i) (%s)" % (self.getTeamName(), self.getSeasonId(), self.getSeasonIndex(), self.leagueId)
	
	def getSeasonIndex(self):
		
		return getSeasonIndexById(self.getSeasonId(), getSeasonIndexList('nhl'))
		## not really that important for NHL, but the indexes might be kinda
		## handy for graphing
	
	def __repr__(self):
		return "<%s>" % (self.getDescriptionString())
		## rewrite this with less info in our angle brackets to make it easier
		## to read

	def qualifiedForPlayoffs(self):
		## in the case of the NHL (and most leagues) it is totally possible to
		## miss the playoffs, so
		if(len(self.playoffGames) > 0):
			return True
		else:
			return False


			
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

	def getRecordString(self, detailed=False):
		index = self.getSeasonIndex()
		if((index <= 26)or(67 <= index <= 81)):
			## the early nhl period, or the 84-98 period, where an OT period was
			## played, but the loser did not get a point
			if(not detailed):
				return "(%s-%s-%s)" % (self.getSeasonWinsTotal(), self.getSeasonLossTotal(), self.getSeasonTiesTotal())				
			else:
				return "(%s(%s)-%s(%s)-%s)" % (self.getSeasonWinsTotal(), self.getSeasonOvertimeWinTotal(), self.getSeasonLossTotal(), self.getSeasonOvertimeLossTotal(), self.getSeasonTiesTotal())			
		elif(82 <= index <= 87):
			## the 99-04 period where OT was played, and an OT loser got one 
			## point, but if the game ended in a tie, each team got 1 point
			if(not detailed):
				return "(%s-%s-%s-%s)" % (self.getSeasonWinsTotal(), self.getSeasonRegulationLossTotal(), self.getSeasonOvertimeLossTotal(), self.getSeasonTiesTotal())						
			else:
				return "(%s(%s/%s)-%s-%s-%s)" % (self.getSeasonWinsTotal(), self.getSeasonRegulationWinTotal(), self.getSeasonOvertimeWinTotal(), self.getSeasonLossTotal(), self.getSeasonOvertimeLossTotal(), self.getSeasonTiesTotal())										
		elif(index >= 88):
			## the bettman shootout era
			if(not detailed):
				return "(%s-%s-%s)" % (self.getSeasonWinsTotal(), self.getSeasonLossTotal(), self.getSeasonExtraTimeLossTotal())
			else:
				return "(%s(%s/%s/%s)-%s-%s(%s/%s))" % (self.getSeasonWinsTotal(),\
				self.getSeasonRegulationWinTotal(), self.getSeasonOvertimeWinTotal(),\
				self.getSeasonShootoutWinTotal(), self.getSeasonLossTotal(), self.getSeasonExtraTimeLossTotal(), self.getSeasonOvertimeLossTotal(), self.getSeasonShootoutLossTotal())				
		else:
			return "(%s-%s-%s)" % (self.getSeasonWinsTotal(), self.getSeasonRegulationLossTotal(), self.getSeasonTiesTotal())				
			## soooooo much better
		
		## have I mentioned all of the horrible things I would like to do to
		## our friend Gary???

	def calculatePlayoffSuccessRating(self):
		return self.getTotalPlayoffWins()

	def getSeasonRegulationLossTotal(self):
		## total number games lost, if the game went longer than regulation time
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(gameNhl.nhlGame.lostInRegulationTime, True)

	def getSeasonRegulationWinTotal(self):
		## total number games lost, if the game went longer than regulation time
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(gameNhl.nhlGame.wonInRegulationTime, True)


	def getSeasonExtraTimeLossTotal(self):
		## total number games lost, if the game went longer than regulation time
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(gameNhl.nhlGame.lostInExtraTime, True)

	def getSeasonExtraTimeWinTotal(self):
		## total number games lost, if the game went longer than regulation time
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(gameNhl.nhlGame.wonInExtraTime, True)		

	def getSeasonOvertimeLossTotal(self):
		## total number of games lost in overtime
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(gameNhl.nhlGame.lostInOvertime, True)	

	def getSeasonOvertimeWinTotal(self):
		## total number of games lost in overtime
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(gameNhl.nhlGame.wonInOvertime, True)	

	def getSeasonShootoutLossTotal(self):
		## total number of games lost in a shootout
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(gameNhl.nhlGame.lostInShootout, True)
		
	def getSeasonShootoutWinTotal(self):
		## total number of games lost in a shootout
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(gameNhl.nhlGame.wonInShootout, True)			
	
		
	def madeRealPlayoffs(self):	
		return self.qualifiedForPlayoffs()


if(__name__ == "__main__"):
	
	##daBuds = nhlTeam('nhl', '2016', 'TOR')
	##daSharks = nhlTeam('nhl', '2016', 'SJS')
	
	fuckTampa = nhlTeam('wha', '1978', 'SVT', True)
	## quick test to make sure everything is loading correctly
	print fuckTampa.getTotalPlayoffGames()
	print fuckTampa.getTotalPlayoffWins()
	
	for game in fuckTampa.getPlayoffGames():
		print game.getGameDescription()
	
	## San Jose 2015-16 used as an example here cause they made the playoffs
	## and went to the finals, so there shouldnt be anything turned off
	##print getSeasonIndexList('nhl')
