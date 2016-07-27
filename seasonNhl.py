## seasonWatMu.py ##############################################################
## base type for Waterloo Intramurals Hockey ###################################
## seasons (Individual semesters teams) ########################################
################################################################################
from teamNhl import *
from season import *




class nhlSeason(Season):
	def __init__(self, leagueId, seasonId, teamIdList, sortTeams):
		super(nhlSeason, self).__init__(leagueId, 'null', seasonId, teamIdList)
		
		self.playoffBrackets = []
		
		for teamId in teamIdList:
			self.Teams.append(nhlTeam(leagueId, seasonId, teamId))
		
		for team in self.Teams:
			team.loadTierI()

		if(sortTeams == True):
			## all of the criteria used to determine standings position can
			## be calculated from first tier data
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonPointsTotal(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonWinsTotal(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonPlusMinus(), reverse=True)
			## highest priority at the end
			

		for team in self.Teams:
			team.loadTierII(self.Teams, self.Teams.index(team))
			
		for team in self.Teams:
			team.loadTierIII(self.Teams)
	
	def loadTierIV(self, seasonsList):
		for team in self.Teams:
			team.loadTierIV(self.Teams, seasonsList)
	
	##def printPlayoffBrackets(self):

			
	def getTotalPlayoffTeams(self):
		output = 0
		for team in self.Teams:
			if(team.qualifiedForPlayoffs() == True):
				output += 1
		return output

