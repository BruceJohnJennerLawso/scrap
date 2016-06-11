## seasonWatMu.py ##############################################################
## base type for Waterloo Intramurals Hockey ###################################
## seasons (Individual semesters teams) ########################################
################################################################################
from teamWatMu import *
from season import *

class playoffBracket:
	def __init__(self):
		self.bracketNumbers = []
		
	def addStandingsPosition(self, position):
		self.bracketNumbers.append(position)


def getSeedsInBracket(currentTeam, season):
	
	bracketTeamList = []
	

class watMuSeason(Season):
	def __init__(self, leagueId, levelId, seasonId, teamIdList, sortTeams):
		super(watMuSeason, self).__init__(leagueId, levelId, seasonId, teamIdList)
		
		self.playoffBrackets = []
		
		for teamId in teamIdList:
			self.Teams.append(watMuTeam(leagueId, levelId, seasonId, teamId))
		
		for team in self.Teams:
			team.loadTierI()

		if(sortTeams == True):
			## all of the criteria used to determine standings position can
			## be calculated from first tier data
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonGoalsForAverage(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonAverageSOC(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getPointsPercentage(), reverse=True)
			## highest priority at the end
			

		for team in self.Teams:
			team.loadTierII(self.Teams, self.Teams.index(team))
		
		self.playoffBrackets.append(playoffBracket())
		topTeam = self.getTeamByPosition(1)
		## next work through the teams this one played and add their position
		## numbers to the top playoff bracket, then look through their
		## opponents and so on
		
		## maybe a recursive function here that takes the teams list and the
		## bracket list as arguments and returns lists of seeding positions
		topPlayoffBracket = getSeedsInBracket(topTeam, self)
		print topPlayoffBracket
			
		
		for team in self.Teams:
			team.loadTierIII(self.Teams)
						
