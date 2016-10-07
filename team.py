## team.py #####################################################################
## general base type for any team ##############################################
## hoping to define a specific stat type here instead of #######################
## redoing it for every different team type ####################################
################################################################################
from player import *
import csv


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
	def __init__(self, leagueId, levelId, seasonId, teamId):
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
		
		self.Games = []
		## init list of objects of type game, currently empty, to be filled by
		## the first loadTier call which opens the csv file and loads in the
		## base data as game objects
		if(leagueId == 'nhl'):
			self.loadPath = "./data/%s/%s/%s%s.csv" % (leagueId, seasonId, teamId, seasonId)
			## shorter load path for nhl when we dont have to branch by levelId
		else:
			self.loadPath = "./data/%s/%s/%s/%s.csv" % (leagueId, levelId, seasonId, teamId)

		self.loadTierI()
		
		
		
		
	## prototypes for the functions that load each tier of data ################
	## ABSOLUTELY MUST BE CALLED IN ORDER or bad things WILL happen ############
		
	def loadTierI(self):
		print "Bad call to Team.loadTierI"
		
	def loadTierII(self, teamsList):
		print "Bad call to Team.loadTierII"
		
	def loadTierIII(self, teamsList, madeRealPlayoffs):
		print "Bad call to Team.loadTierIII"
		
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
		
	def getSeasonGoalsForAverage(self):
		return float(self.seasonTotalGoalsFor)/float(self.totalSeasonGames)

	def getSeasonGoalsAgainstAverage(self):
		return float(self.seasonTotalGoalsAgainst)/float(self.totalSeasonGames)
		
	def getSeasonPlusMinus(self):
		## goal differential (for - against)
		return self.seasonPlusMinus
	
	def getSeasonGoalDifferentialAverage(self):
		return self.getSeasonPlusMinus()/float(self.getSeasonGamesTotal())
		
	def getSeasonPointsTotal(self):
		## (points earned)
		return self.seasonPointsTotal		
		
	def getPointsPercentage(self):
		## (points earned/total points available)
		return self.seasonPointsTotal/float(self.totalSeasonGames*2)			
	
	def getSeasonGamesTotal(self):
		## total games played in the regular season (up to this point)
		return self.totalSeasonGames	
		
	def getSeasonWinsTotal(self):
		## games won, regarless of the situation
		return self.seasonWins
		
	def getSeasonTiesTotal(self):
		## games that were tied at the end of regulation and any extra
		## overtime *and stayed that way*
		
		## no shootout games here, we only kicking things oldschool with true
		## ties
		return self.seasonTies	

	def getSeasonLossTotal(self):
		return self.seasonLosses		
	
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
		return self.averageGameClosenessIndex
		
	def getTotalPlayoffGames(self):
		## counts how many playoff games this team played in all (0, 4, 22, etc)
		return len(self.getPlayoffGames())

	def getTotalPlayoffWins(self):
		## total games won in the playoffs
		return self.playoffWins
		
	def getPlayoffWinPercentage(self):
		## what percentage of any playoff games played that the team won as a
		## decimal, ie 0.782 
		return self.playoffWinPercentage
	
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
		output = 0.000
		if(self.getTotalPlayoffGames() > 0):
			output = float(self.playoffGoalsFor)/float(self.getTotalPlayoffGames())
		return output

	def getPlayoffGoalsAgainstAverage(self):
		output = 0.000
		if(self.getTotalPlayoffGames() > 0):
			output = float(self.playoffGoalsAgainst)/float(self.getTotalPlayoffGames())
		return output
	
	def getPlayoffAverageGoalDifferential(self):
		return self.playoffAverageGoalDifferential
		
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
		return self.averageWinQualityIndex
		
	def getAPQI(self):
		## exact same calculation as AWQI, with one small change:
		## the win quality index is the goal differential * opponent pts pct *
		## the game closeness index of the game
		return self.averagePlayQualityIndex
		
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
		return self.offenceQualityIndex
	
	def getAOQI(self):
		return self.getOffenceQualityIndex()/float(self.getSeasonGamesTotal())
		## been meaning to do this, allows for comparison between teams that
		## played seasons of different lengths
		
		## in other words, this is "Average goals above expectations per game"
		
	def getDefenceQualityIndex(self):
		## converse to offence quality index, defence quality is the goals
		## allowed by this (self) team, **below** the expectation, based on the
		## opponents offence
		
		## this convention is changed from the original version, which had
		## good qualities as negative values, we now want it to be positive for
		## good defensive teams 
		return self.defenceQualityIndex

	def getADQI(self):
		return self.getDefenceQualityIndex()/float(self.getSeasonGamesTotal())
		## ie "Average goals below expectations per game"
		
	def getDiffQualityIndex(self):
		return self.diffQualityIndex
		
	def getADiffQI(self):
		return self.getDiffQualityIndex()/float(self.getSeasonGamesTotal())

	def getMaAQualAboveDiff(self):
		return (self.getADiffQI()-(self.getSeasonPlusMinus()/float(self.getSeasonGamesTotal())))

	def getNetAODQISum(self):
		return (self.getAOQI()+self.getADQI())
		## Im strongly guessing that this will exactly match an average diff
		## qual index, but I dont know for sure

	## Tier III ################################################################


	def calculateMaValues(self, teamsList):
		## take our values for awqi, apqi, aoqi, adqi, and adjust them relative
		## to the mean of the league
		self.meanAdjustedAverageWinQualityIndex = self.averageWinQualityIndex
		self.meanAdjustedAveragePlayQualityIndex = self.averagePlayQualityIndex
		
		self.meanAdjustedAverageOffenceQualityIndex = self.getAOQI()
		self.meanAdjustedAverageDefenceQualityIndex = self.getADQI()
		
		self.meanAdjustedAverageDiffQualityIndex = self.getADiffQI()
		
		awqiMean = 0.000
		apqiMean = 0.000
		aoqiMean = 0.000
		adqiMean = 0.000
		adiffqiMean = 0.000
		
		for team in teamsList:
			awqiMean += team.getAWQI()
			apqiMean += team.getAPQI()
			aoqiMean += team.getAOQI()
			adqiMean += team.getADQI()
			adiffqiMean += team.getADiffQI()
			
		awqiMean /= float(len(teamsList))
		apqiMean /= float(len(teamsList))
		aoqiMean /= float(len(teamsList))
		adqiMean /= float(len(teamsList))
		adiffqiMean /= float(len(teamsList))		
		
		self.meanAdjustedAverageWinQualityIndex -= awqiMean
		self.meanAdjustedAveragePlayQualityIndex -= apqiMean
		self.meanAdjustedAverageOffenceQualityIndex -= aoqiMean
		self.meanAdjustedAverageDefenceQualityIndex -= adqiMean
		self.meanAdjustedAverageDiffQualityIndex -= adiffqiMean


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

	def getMaAOQI(self):
		## self.AOQI-leagueMean.AOQI
		return self.meanAdjustedAverageOffenceQualityIndex
		
	def getMaADQI(self):
		## dont corsi and drive kids
		
		## self.ADQI-leagueMean.ADQI
		return self.meanAdjustedAverageDefenceQualityIndex

	def getMaADiffQI(self):
		return self.meanAdjustedAverageDiffQualityIndex

	def getSQI(self):
		return (self.getMaADiffQI() - (self.getMaAOQI() + self.getMaADQI()))
	## our two indexes now adjusted for season mean in an attempt to make easier
	## to compare across different seasons. MaAWQI appears to be the best 
	## predictor of playoff success so far
	
	## also makes for an easy way to benchmark likely contenders, contenders
	## are *usually* at least 1-2 times the league mean in AWQI, often 2x or
	## above. Only 1 team has ever won the championship with a MaAWQI below 1
	## (Winter 2014 Pucked Up) with a MaAWQI of 0.922
	
	## Its pronounced "Mah-Quee" in case you were wondering 

	## Tier IV #################################################################
	
	def getPlayers(self):
		## list of player objects		
		return self.Players
