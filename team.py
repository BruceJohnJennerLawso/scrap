## team.py #####################################################################
## general base type for any team ##############################################
## hoping to define a specific stat type here instead of #######################
## redoing it for every different team type ####################################
################################################################################
from game import *
import csv

class Team(object):
	## constructor
	def __init__(self, seasonId, teamId):
		self.seasonId = seasonId
		self.teamId = teamId
		
		self.Games = []
		## list of objects of type game
		
		self.loadPath = "./data/%s/%s.csv" % (seasonId, teamId)
		
	## prototypes for the functions that load each tier of data ################
	## ABSOLUTELY MUST BE CALLED IN ORDER or bad things will happen ############
		
	def loadTierI(self):
		print "Bad call to Team.loadTierI"
		
	def loadTierII(self, teamsList):
		print "Bad call to Team.loadTierII"
		
	def loadTierIII(self, teamsList):
		print "Bad call to Team.loadTierIII"		
	
	
	## Tier I ##################################################################
	
	def getTeamName(self):
		return self.teamName	
		
	def getSeasonGoalsForAverage(self):
		return float(self.seasonTotalGoalsFor)/float(self.totalSeasonGames)

	def getSeasonGoalsAgainstAverage(self):
		return float(self.seasonTotalGoalsAgainst)/float(self.totalSeasonGames)
		
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
		
	## note that we try to squeeze down to shorter names here in order to make
	## working on the front end a bit easier than typing out
	## getAverageGameClosenessIndex() would be
	
	## Tier II #################################################################
		
	def getAWQI(self):
		return self.averageWinQualityIndex
		
	def getAPQI(self):
		return self.averagePlayQualityIndex

	## Tier III ################################################################

	def getMaAWQI(self):
		return self.meanAdjustedAverageWinQualityIndex	
		
	def getMaAPQI(self):
		return self.meanAdjustedAveragePlayQualityIndex

	## our two indexes now adjusted for season mean in an attempt to make easier
	## to compare across different seasons. MaAWQI appears to be the best 
	## predictor of playoff success so far
	
	## also makes for an easy way to benchmark likely contenders, contenders
	## are *usually* at least 1-2 times the league mean in AWQI, often 2x or
	## above. Only 1 team has ever won the championship with a MaAWQI below 1
	## (Winter 2014 Pucked Up) with a MaAWQI of 0.922
	
	## Maybe pronounced "Mah-Quee" 
