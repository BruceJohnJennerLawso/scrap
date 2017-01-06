## team.py #####################################################################
## general base type for any team ##############################################
## hoping to define a specific stat type here instead of #######################
## redoing it for every different team type ####################################
################################################################################
from player import *
import csv
import seasonParts

import game
import gameNhl
import gameWatMu

import seasonParts

def getSeasonIndexList(leagueId, debugInfo=False):
	## opens up the file containing the names of every season in our data and
	## assigns an  integer to each one so that we can keep the order straight,
	## particularly with watMu seasons which run not necessarily every season,
	## and more than once a year
	output = []
	if(debugInfo):
		print './data/%s/seasonIndex.csv' % (leagueId)
	with open('./data/%s/seasonIndex.csv' % (leagueId), 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			output.append(row[0])
			## append on the list of names, with the primary one first, ie
			## [...['winter2010', 'winter2010Contact'],...]
			
			## or in NHL case,
			## [...['2002', '2003', '2004', '2006', '2007', '2008', ...], ...]
			## (notice the season skip at the lockout), so we go
			## 2002 2003 2004 2006 2007
			##   1    2    3    4    5
			
			## cause we dont care about seasons that didnt actually happen
	return output
	
def getSeasonIndexById(seasonId, indexList):
	## if we have the seasonId (ie '2016'), we can call this function to find
	## out what seasonIndex that this season had
	
	## ie what was its place in the order of seasons throughout history
	output = 0
	## default error if we cant find the proper position for the season
	for i in range(0, len(indexList)):
		if(seasonId in indexList[i]):
			output = i+1
			break
	return output	

class Team(object):
	## base class constructor
	def __init__(self, leagueId, levelId, seasonId, teamId, debugInfo):
		self.seasonId = seasonId
		## string that reliably identifies the current season, ie
		## '2016' or
		## 'fall2015'
		self.teamId = teamId
		## string that reliably identifies the team. ie
		## '12348' (intramurals) or
		## 'TOR'
		self.leagueId = leagueId
		## string that identifies the league that we currently play in, ie
		## 'watMu' or
		## 'nhl'
		self.levelId = levelId
		## the string describing the level of play 
		## (ie beginner/casual in waterloo intramurals)
		
		## for nhl, ahl, etc level, just leave this as 'null' or whatever the
		## output directory name under ./results/nhl is gonna be
		
		##self.Games = []
		## Deprecation in process...
		## init list of objects of type game, currently empty, to be filled by
		## the first loadTier call which opens the csv file and loads in the
		## base data as game objects
		
		self.seasonGames = []
		## list of objects representing season games
		self.playoffGames = []
		
		
		if((leagueId == 'nhl')or(leagueId == 'wha')):
			self.loadPath = "./data/%s/%s/%s%s.csv" % (leagueId, seasonId, teamId, seasonId)
			## shorter load path for nhl when we dont have to branch by levelId
		else:
			self.loadPath = "./data/%s/%s/%s/%s.csv" % (leagueId, levelId, seasonId, teamId)

		self.loadTierI(debugInfo)
		rows = self.getCsvRowsList()
		self.seasonParts = []
	
	def getDescriptionString(self):
		output = "%s\n" % (self.getDescriptionHeader())
		output += "Rank: %i (%i)%s, Pts %i Pct: %.3f,\n" % (self.getSeasonRank(), self.totalSeasonGames, self.getRecordString(), self.getSeasonPointsTotal(), self.getPointsPercentage()) 
		output += "AGCI: %.3f, MaAWQI %.3f, MaAPQI %.3f\n" % (self.getAGCI(), self.getMaAWQI(), self.getMaAPQI())
		output += "Defence Quality Index %.3f, Offence Quality Index %.3f\n" % (self.getDefenceQualityIndex(), self.getOffenceQualityIndex())
		output += "ADQI %.3f, AOQI %.3f, CPQI %.3f, DQM %.3f\n" % (self.getADQI(), self.getAOQI(), self.getCPQI(), self.getDQM()) 
		output += "Offense: %.3f, Defense %.3f, +/- %i\n" % (self.getSeasonGoalsForAverage(), self.getSeasonGoalsAgainstAverage(), self.getSeasonPlusMinus()) 
		output += "%i Playoff Wins, Playoff Win %% of %.3f\n" % (self.getTotalPlayoffWins(), self.getPlayoffWinPercentage())
		output += "Playoff Offence %.3f, Playoff Defence %.3f, Playoff Avg. Goal Diff %.3f\n" % (self.getPlayoffGoalsForAverage(), self.getPlayoffGoalsAgainstAverage(), self.getPlayoffAverageGoalDifferential())
		output += "CPQI %.3f, (%.3f/%.3f) front/back (%.3f FBS)\n" % (self.getSeasonPart(seasonParts.getGameSelectConditions("regularSeason")).getAverageForStat(game.Game.getCPQI), self.getSeasonPart(seasonParts.getGameSelectConditions("firstHalfRegularSeason")).getAverageForStat(game.Game.getCPQI), self.getSeasonPart(seasonParts.getGameSelectConditions("secondHalfRegularSeason")).getAverageForStat(game.Game.getCPQI), self.getFrontBackSplit())
		output += "Defence %.3f, (%.3f/%.3f)\n" % (self.getSeasonPart(seasonParts.getGameSelectConditions("regularSeason")).getAverageForStat(game.Game.getGoalsAgainst), self.getSeasonPart(seasonParts.getGameSelectConditions("firstHalfRegularSeason")).getAverageForStat(game.Game.getGoalsAgainst), self.getSeasonPart(seasonParts.getGameSelectConditions("secondHalfRegularSeason")).getAverageForStat(game.Game.getGoalsAgainst))
		output += "Offence %.3f, (%.3f/%.3f)\n" % (self.getSeasonPart(seasonParts.getGameSelectConditions("regularSeason")).getAverageForStat(game.Game.getGoalsFor), self.getSeasonPart(seasonParts.getGameSelectConditions("firstHalfRegularSeason")).getAverageForStat(game.Game.getGoalsFor), self.getSeasonPart(seasonParts.getGameSelectConditions("secondHalfRegularSeason")).getAverageForStat(game.Game.getGoalsFor))		

		output += "Rel Front: ADQI %.3f, AOQI %.3f\n" % (self.getADQI(seasonParts.getGameSelectConditions("firstHalfRegularSeason")), self.getAOQI(seasonParts.getGameSelectConditions("firstHalfRegularSeason")))				
		output += "Rel Back: ADQI %.3f, AOQI %.3f\n" % (self.getADQI(seasonParts.getGameSelectConditions("secondHalfRegularSeason")), self.getAOQI(seasonParts.getGameSelectConditions("secondHalfRegularSeason")))
		output += "Rel Total: ADQI %.3f, AOQI %.3f" % (self.getADQI(), self.getAOQI())									
		return output
		## I should really line break this so it fits into a terminal with less
		## than 850 columns nicely
	
	
	def getSeasonPart(self, gameConditions):
		for part in self.seasonParts:
			##print type(part.getGameConditions()), len(part.getGameConditions()), type(gameConditions), len(gameConditions)
			##if((part.getGameConditions()[0] == gameConditions[0])and(part.getGameConditions()[1] == gameConditions[1])):
			if(part.getGameConditions() == gameConditions):
				return part
		
	## prototypes for the functions that load each tier of data ################
	## ABSOLUTELY MUST BE CALLED IN ORDER or bad things WILL happen ############
		
	def loadTierI(self):
		print "Bad call to Team.loadTierI"
		
	## Tier II load call #######################################################	
		
	def loadTierII(self, teamsList, debugInfo=False):	
		
		
		for game in self.getSeasonGames():
			game.loadTierII(teamsList, self.getSeasonIndex())

		self.seasonParts = [seasonParts.seasonPart(self.getSeasonGames(), self.getPlayoffGames(), seasonParts.gamesSelectConditions(part="everything"), seasonParts.gamesSelectConditions(part="none")),\
		seasonParts.seasonPart(self.getSeasonGames(), self.getPlayoffGames(), seasonParts.gamesSelectConditions(part="none"), seasonParts.gamesSelectConditions(part="everything")),\
		seasonParts.seasonPart(self.getSeasonGames(), self.getPlayoffGames(), seasonParts.gamesSelectConditions(part="everything"), seasonParts.gamesSelectConditions(part="everything")),\
		seasonParts.seasonPart(self.getSeasonGames(), self.getPlayoffGames(), seasonParts.gamesSelectConditions(part="firstHalf"), seasonParts.gamesSelectConditions(part="none")),\
		seasonParts.seasonPart(self.getSeasonGames(), self.getPlayoffGames(), seasonParts.gamesSelectConditions(part="secondHalf"), seasonParts.gamesSelectConditions(part="none"))]		
		
		for part in self.seasonParts:
			part.loadTierII(teamsList, self.getSeasonIndex())
		
		
		if(debugInfo):
			print "Load call watMuTeam Tier II, team %s %s, Id %s" % (self.getTeamName(), self.seasonId, self.teamId)
		
			
		## once we've calculated the total WQI & PQI, divy them over the total
		## games played in that season to get an average

	def setLeagueRank(self, teamRank):	
		self.teamRank = teamRank
		self.seasonRank = teamRank+1
		
		
	def loadTierIII(self, teamsList, madeRealPlayoffs, awqiMean, apqiMean, teamRank, debugInfo=False):	
		
		if(debugInfo):
			print "Load call watMuTeam Tier III, team %s" % self.getTeamName()
		
		self.realPlayoffs = madeRealPlayoffs
		if(debugInfo):
			print "Calculating Ma values"
		self.calculateMaValues(teamsList, awqiMean, apqiMean)
		if(debugInfo):
			print "Finished calculating Ma values"
		## send the list of team objects for this season off so we can get our
		## mean adjusted values	
		
	def loadTierIV(self, teamsList, seasonsList):
		print "Bad call to Team.loadTierIV"		
	
	
	## Tier I ##################################################################
	
	def getCsvRowsList(self):
		with open(self.loadPath, 'rb') as foo:
			rows = []
			reader = csv.reader(foo)
			for row in reader:
				rows.append(row)
			## create a list called row, which will hold all of the data in the
			## csv as a sublist for each row, ie
			
			## [[row 1...], [row 2...],...]
		return rows
	
	def getTeamName(self):
		## ie 'Toronto Maple Leafs', or 'The Mighty Dads'
		return self.teamName	
	
	def getTeamId(self):
		return self.teamId
	
	def getSeasonId(self):
		## ie '2016' or 'fall2015'
		return self.seasonId	
		
		
	def getSeasonGames(self):
		return self.seasonGames
		## gets list of game objects
		
	def getPlayoffGames(self):
		if(self.qualifiedForPlayoffs()):	
			return self.playoffGames	
		else:
			return []
		
	def getSeasonGoalsForAverage(self):
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getGoalsFor)

	def getSeasonGoalsAgainstAverage(self):
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getGoalsAgainst)
		
	def getSeasonPlusMinus(self):
		## goal differential (for - against)
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getTotalForStat(game.Game.getGoalDifferential)
	
	def getSeasonGoalDifferentialAverage(self):
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getGoalDifferential)
		
	def getSeasonPointsTotal(self):
		## (points earned)
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		try:
			return self.getSeasonPart(gameConditions).getTotalForStat(gameNhl.nhlGame.getPointsEarned)
		except AttributeError:
			return self.getSeasonPart(gameConditions).getTotalForStat(gameWatMu.watMuGame.getPointsEarned)
		except TypeError:
			return self.getSeasonPart(gameConditions).getTotalForStat(gameWatMu.watMuGame.getPointsEarned)
	def getSeasonPointsPossible(self):
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		try:
			return self.getSeasonPart(gameConditions).getTotalForStat(gameNhl.nhlGame.getMaxPointsPossible)
		except AttributeError:
			return self.getSeasonPart(gameConditions).getTotalForStat(gameWatMu.watMuGame.getMaxPointsPossible)
		except TypeError:
			return self.getSeasonPart(gameConditions).getTotalForStat(gameWatMu.watMuGame.getMaxPointsPossible)			
					
	def getPointsPercentage(self):
		## (points earned/total points available)
		return float(self.getSeasonPointsTotal())/self.getSeasonPointsPossible()			
	
	def getSeasonGamesTotal(self):
		## total number of games played in the regular season (up to this point)
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getTotalForStat(game.Game.getOne)	
		
	def getSeasonWinsTotal(self):
		## games won, regarless of the situation
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(game.Game.Won, True)	
		
	def getSeasonTiesTotal(self):
		## games that were tied at the end of regulation and any extra
		## overtime *and stayed that way*
		
		## no shootout games here, we only kicking things oldschool with true
		## ties
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(game.Game.Tied, True)	
		
	def getSeasonLossTotal(self):
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(game.Game.Lost, True)		
	
	def getAGCI(self):
		## stat that measures how close the games this team played were on
		## average
		
		## ie
		##
		## 1-1 -> 1.000
		## 2-1 -> 1.000
		## 3-1 -> 0.500
		## 4-1 -> 0.333
		## 5-1 -> 0.250
		## 6-1 -> 0.200
		## 7-1 -> 0.166
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getGameClosenessIndex)
		
	def getTotalPlayoffGames(self):
		## counts how many playoff games this team played in all (0, 4, 22, etc)
		
		gameConditions = seasonParts.getGameSelectConditions("playoffs")
		return self.getSeasonPart(gameConditions).getTotalForStat(game.Game.getOne)
		
		##return len(self.getPlayoffGames())

	def getTotalPlayoffWins(self):
		## total games won in the playoffs
		gameConditions = seasonParts.getGameSelectConditions("playoffs")
		return self.getSeasonPart(gameConditions).getTotalMatchForStat(game.Game.Won, True)
		
	def getPlayoffWinPercentage(self):
		## what percentage of any playoff games played that the team won as a
		## decimal, ie 0.782 
		if(self.getTotalPlayoffGames() > 0):
			return float(self.getTotalPlayoffWins())/self.getTotalPlayoffGames()
		else:
			return 0.000
	
	def getRealPlayoffWinPercentage(self, season):
		## the problem here is that for the watMu system, not all playoff wins
		## are created equal, for a big bracket like the intermediate, a win in
		## the second playoff bracket isnt really worth the same as one in the
		## top bracket, since a team in the second bracket plays much worse
		## teams than the team in the top bracket did
		
		## so for most analysis that we do, we only consider wins in the top
		## playoff bracket to be 'real'
		if(self.leagueId == 'watMu'):
			if(self.getSeasonRank() not in season.topPlayoffBracket):
				return 0.000
			else:
				return self.getPlayoffWinPercentage()	
		else:
			return self.getPlayoffWinPercentage()
			## if we arent dealing with a weird watMu style league, just get the
			## raw playoff win percentage
			
	def getPlayoffSuccessRating(self):
		return self.calculatePlayoffSuccessRating()	
				
	def getPlayoffGoalsForAverage(self):
		gameConditions = seasonParts.getGameSelectConditions("playoffs")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getGoalsFor)

	def getPlayoffGoalsAgainstAverage(self):
		gameConditions = seasonParts.getGameSelectConditions("playoffs")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getGoalsAgainst)
	
	def getPlayoffAverageGoalDifferential(self):
		gameConditions = seasonParts.getGameSelectConditions("playoffs")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getGoalDifferential)
	
	
	def getPlayoffOffenceTransition(self):
		output = self.getPlayoffGoalsForAverage()-self.getSeasonGoalsForAverage()
		return output
		
	def getPlayoffDefenceTransition(self):
		output = self.getPlayoffGoalsAgainstAverage()-self.getSeasonGoalsAgainstAverage()
		return output
		
	def getPlayoffGoalDifferentialTransition(self):
		output = self.getPlayoffAverageGoalDifferential() - self.getSeasonGoalDifferentialAverage()
		return output
	
		
	def getRoster(self):
		## *very important definition*
		## self.Roster is a list of strings of the full names of players on the
		## roster, ie
		
		## [..., 'Wayne Gretzky', 'Dave Semenko', 'Andy Moog', ...]
		
		## NOT the list of player objects
		return self.Roster
		
	## note that we try to squeeze down to shorter names here in order to make
	## working on the front end a bit easier than typing out
	## getAverageGameClosenessIndex() would be
	
	## Tier II #################################################################
		
	def getAWQI(self):
		## Sum of the average of win quality indexes for each game in the
		## schedule. The win quality index for a game is calculated as follows:
		## if this (self) team lost, they get 0.000. If they won, they get
		## the goal differential (always positive) * opponents points percentage
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getWinQualityIndex)
		
	def getAPQI(self):
		## exact same calculation as AWQI, with one small change:
		## the win quality index is the goal differential * opponent pts pct *
		## the game closeness index of the game
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getPlayQualityIndex)
		
	def getSeasonRank(self):
		## what position in the standings this team had after we sort by
		## whatever the league considers to be the ranking criteria
		
		## ie a first place team gets integer 1, a second place team gets
		## integer 2, and so on
		return self.seasonRank
		
		
	## very simple pair of stats, but a bit wordy to explain	
	def getOffenceQualityIndex(self):
		## basically the idea here is 'goals above expectations'.
		## The expected number of goals is the average allowed by an opponent
		## over the course of the season (total season completed up till now)
		## if we score more goals in this game than the expectation, it would
		## seem to indicate that this (self) team has a good (quality) offence
		## that can "get it done" against a good defensive team
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getTotalForStat(game.Game.getOffenceQualityIndex)
				
	def getDefenceQualityIndex(self):
		## converse to offence quality index, defence quality is the goals
		## allowed by this (self) team, **below** the expectation, based on the
		## opponents offence
		
		## this convention is changed from the original version, which had
		## good qualities as negative values, we now want it to be positive for
		## good defensive teams 
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getTotalForStat(game.Game.getDefenceQualityIndex)
		
	def getAOQI(self, gameConditions=[]):
		## self.AOQI-leagueMean.AOQI
		if(len(gameConditions) == 0):
			gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getOffenceQualityIndex)
		
	def getADQI(self, gameConditions=[]):
		## dont corsi and drive kids
		if(len(gameConditions) == 0):
			gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getDefenceQualityIndex)

	def getNetAODQISum(self):
		return (self.getAOQI()+self.getADQI())
		## Im strongly guessing that this will exactly match an average diff
		## qual index, but I dont know for sure

	## Tier III ################################################################


	def calculateMaValues(self, teamsList, awqiMean, apqiMean):
		## take our values for awqi, apqi, aoqi, adqi, and adjust them relative
		## to the mean of the league
		self.meanAdjustedAverageWinQualityIndex = self.getAWQI()
		self.meanAdjustedAveragePlayQualityIndex = self.getAPQI()
			
		self.meanAdjustedAverageWinQualityIndex -= awqiMean
		self.meanAdjustedAveragePlayQualityIndex -= apqiMean


	def getMaAWQI(self):
		## once we have calculated AWQI for this team, we sometimes like to
		## readjust it for the current seasons mean, to try and account for
		## fluctuations in the distribution of AWQI across the league for each
		## season
		
		## so basically this is just self.AQWI-leagueMean.AWQI
		return self.meanAdjustedAverageWinQualityIndex	
		
	def getMaAPQI(self):
		## self.APQI-leagueMean.AWQI
		return self.meanAdjustedAveragePlayQualityIndex


	def getODQSplit(self):
		return (self.getAOQI() - self.getADQI())

	## our two indexes now adjusted for season mean in an attempt to make easier
	## to compare across different seasons. MaAWQI appears to be the best 
	## predictor of playoff success so far
	
	## also makes for an easy way to benchmark likely contenders, contenders
	## are *usually* at least 1-2 times the league mean in AWQI, often 2x or
	## above. Only 1 team has ever won the championship with a MaAWQI below 1
	## (Winter 2014 Pucked Up) with a MaAWQI of 0.922
	
	## Its pronounced "Mah-Quee" in case you were wondering 

	def getSQI(self):
		return (self.getOldDiffQualityIndex() - self.getCPQI() )

	def getCPQI(self):
		return (self.getAOQI() + self.getADQI())

	def getDQM(self):
		gameConditions = seasonParts.getGameSelectConditions("regularSeason")
		return self.getSeasonPart(gameConditions).getAverageForStat(game.Game.getOldDiffQualityIndex)

	def getFrontBackSplit(self):
		frontCPQI = self.getSeasonPart(seasonParts.getGameSelectConditions("firstHalfRegularSeason")).getAverageForStat(game.Game.getCPQI)
		backCPQI = self.getSeasonPart(seasonParts.getGameSelectConditions("secondHalfRegularSeason")).getAverageForStat(game.Game.getCPQI)		
		
		return (backCPQI - frontCPQI)

	## Tier IV #################################################################
	
	def getPlayers(self):
		## list of player objects		
		return self.Players
