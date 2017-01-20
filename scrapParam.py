## scrapParam.py ###############################################################
## an object wrapper for all of the params that scrap needs ####################
## in order to run #############################################################
################################################################################
from outputs import *

class scrapParams(object):
	def __init__(self, leagueId, levelId, playoffTeamsOnly=False, teamNames=[], runMode="Linear", targetStatName="CPQI", independentStatName="GDA", sortOrder='desc'):
		self.leagueId = leagueId
		self.levelId = levelId
		self.playoffTeamsOnly = playoffTeamsOnly
		self.teamNames = teamNames
		self.runMode = runMode
		self.targetStatName = targetStatName
		self.independentStatName = independentStatName
		self.sortOrder = sortOrder
	
	def info(self):
		print "scrapParams object:"
		print "leagueId = %s" % (self.getLeagueId())
		print "levelId = %s" % (self.getLevelId())
		print "playoffTeamsOnly = %r" % (self.getPlayoffTeamsOnly())
		print "teamNames = ", self.getTeamNames()
		print "runMode = %s" % (self.getRunMode())
		print "targetStatName = %s" % (self.getTargetStatName())
		print "sortOrder = %s" % (self.getSortOrder())
		
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
	
	def getSortOrder(self):
		return self.sortOrder
		
	def setSortOrder(self, newSortOrder):
		self.sortOrder = newSortOrder

		
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

def watMuLevels():
	return ['beginner', 'intermediate', 'advanced', 'allstar']

def filterSeasonsByParams(seasons, parameters):
	output = []
	
	if(parameters.getLeagueId() == "watMu"):
		if(parameters.getLevelId() in watMuLevels()):
			for season in seasons:
				if(season.getLeagueId() == "watMu"):
					if(season.getLevelId() == parameters.getLevelId()):
						outputs += [season]
						## if the level is correct, and the league is right
						## (remember watMu seasons will be mixed with nhl & wha)
						## append it to our output
			if(len(output) > 0):
				return output
		else:
			for season in seasons:
				if(season.getLeagueId() == "watMu"):
					if(season.getSeasonId() == parameters.getLevelId()):
						outputs += [season]
			if(len(output) > 0):
				return output
	else:
		## nhl, wha, what have you
		
		seasonIdList = []
		
		try:
			with open('./data/%s/%s/seasons.csv' % (parameters.getLeagueId(), parameters.getLevelId()), 'rb') as foo:
				seasonIdList += [f.rstrip() for f in foo]
			for season in seasons:
				if(season.getLeagueId() == parameters.getLeagueId()):
					if(season.getSeasonId() in seasonIdList):
						output += [season]
			if(len(output) > 0):
				return output
		except IOError:
			## couldnt find a seasons manifest for what was supplied, so next we
			## check to see if the levelId supplied can be matched to a seasonId
			## in the index list
			levelIdIsSeason = False
			with open('./data/%s/seasonIndex.csv' % (leagueId), 'rb') as foo:
				if(parameters.getLevelId() in [f.rstrip() for f in foo]):
					levelIdIsSeason = True
			
			if(levelIdIsSeason):
				for season in seasons:
					if(season.getLeagueId() == parameters.getLeagueId()):
						if(season.getSeasonId() == parameters.getLevelId()):
							output += [season]
				if(len(output) > 0):
					return output
			else:
				print "Unable to make parameter set work with seasons, params:"
				params.info()
