## scrapParam.py ###############################################################
## an object wrapper for all of the params that scrap needs ####################
## in order to run #############################################################
################################################################################
from outputs import *

class scrapParams(object):
	def __init__(self, leagueId, levelId, playoffTeamsOnly=False, teamNames=[], runMode="Linear", targetStatName="CPQI", independentStatName="GDA"):
		self.leagueId = leagueId
		self.levelId = levelId
		self.playoffTeamsOnly = playoffTeamsOnly
		self.teamNames = teamNames
		self.runMode = runMode
		self.targetStatName = targetStatName
		self.independentStatName = independentStatName
	
	
	def info(self):
		print "scrapParams object:"
		print "leagueId = %s" % (self.getLeagueId())
		print "levelId = %s" % (self.getLevelId())
		print "playoffTeamsOnly = %r" % (self.getPlayoffTeamsOnly())
		print "teamNames = ", self.getTeamNames()
		print "runMode = %s" % (self.getRunMode())
		print "targetStatName = %s" % (self.getTargetStatName())
		
	def getLeagueId(self):
		return self.leagueId
	
	def setLeagueId(self, newLeagueId):
		self.leagueId = newLeagueId	
		
	def getLevelId(self):
		return self.levelId
		
	def setLevelId(self, newLevelId):
		self.levelId = newLevelId
		
	def getTargetStatName(self):
		return self.targetStatName
		
	def setTargetStatName(self, newTargetStatName):
		self.targetStatName = newTargetStatName
	
	def getIndependentStatName(self):
		return self.independentStatName
		
	def setIndependentStatName(self, newIndependentStatName):
		self.independentStatName = newIndependentStatName
	
		
	def getPlayoffTeamsOnly(self):
		return self.playoffTeamsOnly
		
	def getTeamNames(self):
		return self.teamNames
		
	def getRunMode(self):
		return self.runMode

	def getOutputType(self):
		try:
			with open('./data/%s/%s/seasons.csv' % (self.leagueId, self.levelId), 'rb') as foo:
				outputType = "generic"
		except IOError:		
			outputType = "detailed"	
		return outputType
