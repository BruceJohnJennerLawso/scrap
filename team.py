## team.py #####################################################################
## general base type for any team ##############################################
## hoping to define a specific stat type here instead of #######################
## redoing it for every different team type ####################################
################################################################################
from game import *
import csv

class Team(object):
	def __init__(self, seasonId, teamId):
		self.seasonId = seasonId
		self.teamId = teamId
		
		self.seasonGames = []
		## list of objects of type game
		
		self.loadPath = "./data/%s/%s.csv" % (seasonId, teamId)
		
		
		
	def loadTierI(self):
		print "Bad call to Team.loadTierI"
		
	def loadTierII(self, teamsList):
		print "Bad call to Team.loadTierII"
		
	def loadTierIII(self, teamsList):
		print "Bad call to Team.loadTierIII"		
	
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
		
	def getAWQI(self):
		return self.averageWinQualityIndex
		
	def getAPQI(self):
		return self.averagePlayQualityIndex
