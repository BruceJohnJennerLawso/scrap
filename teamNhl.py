## teamNhl.py ##################################################################
## object representing a team playing in the NHL ###############################
################################################################################
from team import *
from gameNhl import *		



class nhlTeam(Team):
	def __init__(self, leagueId, seasonId, teamId):
		super(nhlTeam, self).__init__(leagueId, '', seasonId, teamId)
		
		self.seasonId = seasonId
		
		self.loadTierI(True)
		
	
		
	## Tier I load call ########################################################	
		
	def loadTierI(self, debugInfo=False):
		with open(self.loadPath, 'rb') as foo:
			rows = []
			reader = csv.reader(foo)
			for row in reader:
				rows.append(row)
			## create a list called row, which will hold all of the data in the
			## csv as a sublist for each row, ie
			
			## [[row 1...], [row 2...],...]
		
		self.teamName = rows[0][0]
		print "%s: %s, Id: %s" % (self.teamName, rows[1][0], self.teamId)
		
		
		self.totalSeasonGames = int(rows[3][0])
		
		self.totalPlayoffGames = 0
		self.playoffSeriesLengths = rows[4]
		for l in self.playoffSeriesLengths:
			self.totalPlayoffGames += 1
			
		scheduleHeader = rows[5]
		scheduleData = rows[6:(self.totalSeasonGames+6)]
		
		if(debugInfo):
			print scheduleHeader, '\n\n'
			for i in scheduleData:
				print i, '\n'
		
		playoffLength = 0
		playoffSeriesLengths = rows[4]
		for s in playoffSeriesLengths:
			playoffLength += int(s)
		
		if(playoffLength > 0):
			self.playoffDataHeader = rows[(self.totalSeasonGames+8)]
			self.playoffData = rows[(self.totalSeasonGames+9):(self.totalSeasonGames+9+playoffLength)]
		else:
			self.playoffDataHeader = []
			self.playoffData = []
		
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
		
		
		for i in range(0, len(scheduleHeader)):
			colStat = scheduleHeader[i]
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
			## need to define who the home team was here based on whether there
			## was an @ or an H
			
			self.Games.append(nhlGame(game[dateIndex], game[locationIndex], game[resultIndex], game[goalsForIndex], game[goalsAgainstIndex],  game[opponentNameIndex], self.teamName, game[gameEndedInIndex]))
			## set up each game as an object in memory
		
		rosterSize = int(rows[2][0])
		## rosters...
		self.Roster = rows[(self.totalSeasonGames+11+playoffLength):(self.totalSeasonGames+11+playoffLength+rosterSize)]
		
		print 'Roster:\n'
		if(debugInfo):
			for p in self.Roster:
				print p, '\n'

		
		self.seasonPlusMinus = 0
		self.seasonTotalGoalsFor = 0
		self.seasonTotalGoalsAgainst = 0	
		self.seasonPointsTotal = 0	
		self.seasonWins = 0
		self.seasonTies = 0
		self.seasonRegulationLosses = 0
		self.seasonExtraTimeLosses = 0
		self.averageGameClosenessIndex = 0
		
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
				if(game.decidedInExtraTime()):
					self.seasonExtraTimeLosses += 1
				else:
					self.seasonRegulationLosses += 1
			
			self.averageGameClosenessIndex += game.getGameClosenessIndex()	
				

		print "Total season games %i" % self.totalSeasonGames
		self.averageGameClosenessIndex /= float(self.totalSeasonGames)

		
		self.playoffWins = 0
		self.playoffGames = 0
		self.playoffWinPercentage = 0.000
		
		self.playoffGoalsFor = 0
		self.playoffGoalsAgainst = 0
		if(self.qualifiedForPlayoffs() == True):
			self.playoffGames = len(self.getPlayoffGames())
		##	for game in self.getPlayoffGames():		
		##		if(game.Won()):
		##			self.playoffWins += 1
		##		self.playoffGoalsFor += game.getGoalsFor()
		##		self.playoffGoalsAgainst += game.getGoalsAgainst()				
		##		self.playoffWinPercentage = float(self.playoffWins)/float(self.playoffGames)
		
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
				elif((game.Tied()) or ((game.Lost()) and (game.decidedInExtraTime()))):
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
		##for playerName in self.Roster:
		##	self.Players.append(watMuPlayer(playerName, seasonsList))

		## gonna leave this offline for the moment
	
	def getDescriptionString(self):
		return "%s, %s (season %i)\nRank: %i (%i)%s, Pts %i Pct: %.3f,\nAGCI: %.3f, MaAWQI %.3f, MaAPQI %.3f\nDefence Quality Index %.3f, Offence Quality Index %.3f\nOffense: %.3f, Defense %.3f, +/- %i\nPlayoff Win percentage of %.3f, Playoff Offence %.3f, Playoff Defence %.3f" % (self.getTeamName(), self.getSeasonId(), self.getSeasonIndex(), self.getSeasonRank(), self.totalSeasonGames, self.getRecordString(), self.getSeasonPointsTotal(), self.getPointsPercentage(), self.getAGCI(), self.getMaAWQI(), self.getMaAPQI(), self.getDefenceQualityIndex(), self.getOffenceQualityIndex(), self.getSeasonGoalsForAverage(), self.getSeasonGoalsAgainstAverage(), self.seasonPlusMinus, self.getPlayoffWinPercentage(), self.getPlayoffGoalsForAverage(), self.getPlayoffGoalsAgainstAverage())		
	
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
			return self.playoffData
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

	def getRecordString(self):
		return "(%s-%s-%s)" % (self.seasonWins, self.seasonRegulationLosses, self.seasonExtraTimeLosses)
		## I dont have the patience for this right now, so this is only
		## applicable for post 2005 lockout, with the shootout and loser point


if(__name__ == "__main__"):
	daBuds = nhlTeam('nhl', '2016', 'TOR')
