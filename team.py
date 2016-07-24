## team.py #####################################################################
## general base type for any team ##############################################
## hoping to define a specific stat type here instead of #######################
## redoing it for every different team type ####################################
################################################################################
##from game import *
from player import *
import csv

def getSeasonIndexList(leagueId):
	## returns a list of every season
	output = []
	with open('./data/%s/seasonIndex.csv' % (leagueId), 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			output.append(row)
			## append on the list of names, with the primary one first, ie
			## [...['winter2010', 'winter2010Contact'],...]
	return output
	
def getSeasonIndexById(seasonId, indexList):
	output = 0
	## default error if we cant find the proper position for the season
	for i in range(0, len(indexList)):
		if(seasonId in indexList[i]):
			output = i
	return output	

class Team(object):
	## constructor
	def __init__(self, leagueId, levelId, seasonId, teamId):
		self.seasonId = seasonId
		self.teamId = teamId
		self.leagueId = leagueId
		self.levelId = levelId
		## the string describing the level of play 
		## (ie beginner/casual in waterloo intramurals)
		
		self.Games = []
		## list of objects of type game
		
		self.loadPath = "./data/%s/%s/%s/%s.csv" % (leagueId, levelId, seasonId, teamId)
		
	## prototypes for the functions that load each tier of data ################
	## ABSOLUTELY MUST BE CALLED IN ORDER or bad things WILL happen ############
		
	def loadTierI(self):
		print "Bad call to Team.loadTierI"
		
	def loadTierII(self, teamsList):
		print "Bad call to Team.loadTierII"
		
	def loadTierIII(self, teamsList):
		print "Bad call to Team.loadTierIII"
		
	def loadTierIV(self, teamsList, seasonsList):
		print "Bad call to Team.loadTierIV"		
	
	
	## Tier I ##################################################################
	
	def getTeamName(self):
		return self.teamName	
	
	def getSeasonId(self):
		return self.seasonId	
		
	def getSeasonGoalsForAverage(self):
		return float(self.seasonTotalGoalsFor)/float(self.totalSeasonGames)

	def getSeasonGoalsAgainstAverage(self):
		return float(self.seasonTotalGoalsAgainst)/float(self.totalSeasonGames)
		
	def getSeasonPlusMinus(self):
		return self.seasonPlusMinus
		
	def getSeasonAverageSOC(self):
		return self.averageSOC
	
	def getRecordString(self):
		return "(%s-%s-%s)" % (self.seasonWins, self.seasonLosses, self.seasonTies)
		
	def getPointsPercentage(self):
		return self.seasonPointsTotal/float(self.totalSeasonGames*2)			
	
	def getSeasonPointsTotal(self):
		return self.seasonPointsTotal
		
	def getSeasonWinsTotal(self):
		return self.seasonWins
		
	def getSeasonTiesTotal(self):
		return self.seasonTies	

	def getSeasonLossTotal(self):
		return self.seasonLosses		
	
	def getAGCI(self):
		return self.averageGameClosenessIndex
		
	def getTotalPlayoffGames(self):
		return self.playoffGames

	def getTotalPlayoffWins(self):
		return self.playoffWins
		
	def getPlayoffWinPercentage(self):
		return self.playoffWinPercentage
	
	def getRealPlayoffWinPercentage(self, season):
		if(self.getSeasonRank() not in season.topPlayoffBracket):
			return 0.000
		else:
			return self.getPlayoffWinPercentage()	
			
	def getPlayoffGoalsForAverage(self):
		output = 0.000
		if(self.playoffGames > 0):
			output = float(self.playoffGoalsFor)/float(self.playoffGames)
		return output

	def getPlayoffGoalsAgainstAverage(self):
		output = 0.000
		if(self.playoffGames > 0):
			output = float(self.playoffGoalsAgainst)/float(self.playoffGames)
		return output
		
	def getRoster(self):
		return self.Roster
		
	## note that we try to squeeze down to shorter names here in order to make
	## working on the front end a bit easier than typing out
	## getAverageGameClosenessIndex() would be
	
	## Tier II #################################################################
		
	def getAWQI(self):
		return self.averageWinQualityIndex
		
	def getAPQI(self):
		return self.averagePlayQualityIndex
		
	def getSeasonRank(self):
		return self.seasonRank
		
	def getOffenceQualityIndex(self):
		return self.offenceQualityIndex
		
	def getDefenceQualityIndex(self):
		return self.defenceQualityIndex

	## Tier III ################################################################

	def getMaAWQI(self):
		return self.meanAdjustedAverageWinQualityIndex	
		
	def getMaAPQI(self):
		return self.meanAdjustedAveragePlayQualityIndex
		
	def getMaOQI(self):
		return self.meanAdjustedOffenceQualityIndex
		
	def getMaDQI(self):
		return self.meanAdjustedDefenceQualityIndex

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
		return self.Players
