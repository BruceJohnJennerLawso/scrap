## seasonWatMu.py ##############################################################
## base type for Waterloo Intramurals Hockey ###################################
## seasons (Individual semesters teams) ########################################
################################################################################
from teamWatMu import *
from season import *


class watMuSeason(Season):
	def __init__(self, leagueId, levelId, seasonId, teamIdList, sortTeams):
		super(watMuSeason, self).__init__(leagueId, levelId, seasonId, teamIdList)
		
		for teamId in teamIdList:
			self.Teams.append(watMuTeam(leagueId, levelId, seasonId, teamId))
		
		for team in self.Teams:
			team.loadTierI()
		for team in self.Teams:
			team.loadTierII(self.Teams)
		for team in self.Teams:
			team.loadTierIII(self.Teams)
		if(sortTeams == True):
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonGoalsForAverage(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonAverageSOC(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getPointsPercentage(), reverse=True)						
