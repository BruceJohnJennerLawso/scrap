## scrapParam.py ###############################################################
## an object wrapper for all of the params that scrap needs ####################
## in order to run #############################################################
################################################################################


class scrapParams(object):
	def __init__(self, leagueId, levelId, playoffTeamsOnly=False, teamNames=[], runMode="Linear"):
		self.leagueId = leagueId
		self.levelId = levelId
		self.playoffTeamsOnly = playoffTeamsOnly
		self.teamNames = teamNames
		self.runMode = runMode
		
	def getLeagueId(self):
		return self.leagueId
		
	def getLevelId(self):
		return self.levelId
		
	def getPlayoffTeamsOnly(self):
		return self.playoffTeamsOnly
		
	def getTeamNames(self):
		return self.teamNames
		
	def getRunMode(self):
		return self.runMode
