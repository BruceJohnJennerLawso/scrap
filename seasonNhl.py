## seasonWatMu.py ##############################################################
## base type for Waterloo Intramurals Hockey ###################################
## seasons (Individual semesters teams) ########################################
################################################################################
from teamNhl import *
from season import *




class nhlSeason(Season):
	def __init__(self, leagueId, seasonId, teamIdList, sortTeams):
		super(nhlSeason, self).__init__(leagueId, 'null', seasonId, teamIdList)
		## call parent constructor
		
		## note how levelId is a default argument, since the nhl doesnt
		## have different leagues within it
		self.topPlayoffBracket = []
		## always the teams that played in the highest playoff tier
		self.playoffBrackets = []
		## the top playoff bracket and all additional ones as lists
		## of seeding numbers inside of a list
		
		for teamId in teamIdList:
			## work through the team ids list and construct nhlTeam
			## objects using each teamId in the list, and append it into
			## the list of teams
			self.Teams.append(nhlTeam(leagueId, seasonId, teamId))
		

		if(sortTeams == True):
			## all of the criteria used to determine standings position can
			## be calculated from first tier data
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonPlusMinus(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonWinsTotal(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonPointsTotal(), reverse=True)
			## highest priority at the end
			
			## I need to look up what the actual sorting criteria for
			## the nhl is
			
			## it also probably varies depending on era, but tiebreakers
			## are probably rare

		for team in self.Teams:
			team.loadTierII(self.Teams, self.Teams.index(team))
			
		for team in self.Teams:
			team.loadTierIII(self.Teams, team.qualifiedForPlayoffs())
	
	def loadTierIV(self, seasonsList):
		for team in self.Teams:
			team.loadTierIV(self.Teams, seasonsList)
			
	def getTotalPlayoffTeams(self):
		output = 0
		for team in self.Teams:
			if(team.qualifiedForPlayoffs() == True):
				output += 1
		return output
		## I have no idea where this gets used... ?

