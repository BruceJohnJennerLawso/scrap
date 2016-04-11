## seasonWatMu.py ##############################################################
## base type for Waterloo Intramurals Hockey ###################################
## seasons (Individual semesters teams) ########################################
################################################################################
from teamWatMu import *
from season import *


class watMuSeason(Season):
	def __init__(self, seasonId, teamIdList):
		super(watMuSeason, self).__init__(seasonId, teamIdList)
		
		for teamId in teamIdList:
			self.Teams.append(watMuTeam(seasonId, teamId))
		
		for team in self.Teams:
			team.loadTierI()
		for team in self.Teams:
			team.loadTierII(self.Teams)
		for team in self.Teams:
			team.loadTierIII(self.Teams)						
