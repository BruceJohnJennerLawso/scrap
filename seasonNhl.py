## seasonWatMu.py ##############################################################
## base type for Waterloo Intramurals Hockey ###################################
## seasons (Individual semesters teams) ########################################
################################################################################
from teamNhl import *
from season import *

def debugInfoSwitch():
	return False


class nhlSeason(Season):
	def __init__(self, leagueId, seasonId, teamIdList, sortTeams, debugInfo=False):
		super(nhlSeason, self).__init__(leagueId, 'null', seasonId, teamIdList)
		## call parent constructor
		
		## note how levelId is a default argument, since the nhl doesnt
		## have different leagues within it
		self.topPlayoffBracket = []
		## always the teams that played in the highest playoff tier
		self.playoffBrackets = []
		## the top playoff bracket and all additional ones as lists
		## of seeding numbers inside of a list
		if(debugInfo):
			print "Starting Tier I for nhl season %s" % seasonId
		for teamId in teamIdList:
			## work through the team ids list and construct nhlTeam
			## objects using each teamId in the list, and append it into
			## the list of teams
			self.Teams.append(nhlTeam(leagueId, seasonId, teamId, debugInfo))
		
		if(debugInfo):
			print "Starting Tier II for nhl season %s" % seasonId
		for team in self.Teams:
			team.loadTierII(self.Teams, debugInfo)
		if(debugInfo):
			print "Sorting teams for nhl season %s" % seasonId
	
		if(sortTeams == True):
			## all of the criteria used to determine standings position can
			## be calculated from first tier data
			self.Teams = sorted(self.Teams, key=lambda nhlTeam: nhlTeam.getSeasonPlusMinus(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda nhlTeam: nhlTeam.getSeasonWinsTotal(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda nhlTeam: nhlTeam.getSeasonPointsTotal(), reverse=True)
			## highest priority at the end
			
			## I need to look up what the actual sorting criteria for
			## the nhl is
			
			## it also probably varies depending on era, but tiebreakers
			## are probably rare
		
		for team in self.Teams:			
			team.setLeagueRank(self.Teams.index(team))
		
		if(debugInfo):	
			print "Starting Tier III calculations for nhl season %s" % seasonId		
			
		##awqiMean = 	self.getTeamStatAverage(Team.getAWQI)
		##apqiMean = self.getTeamStatAverage(Team.getAPQI)
		##adiffqiMean = self.getTeamStatAverage(Team.getADiffQI)
		## this is a bit slow for modern era seasons, but acceptable
		## enough given the benefits

		

		awqiMean = 	0.0
		apqiMean = 0.0
		for team in self.Teams:
			awqiMean += team.getAWQI()
			apqiMean += team.getAPQI()
		if(debugInfo):
			print "awqiMean %.3f, apqiMean %.3f" % (awqiMean, apqiMean)

			print "Starting Tier III for nhl season %s" % seasonId	
			
		for team in self.Teams:
			team.loadTierIII(self.Teams, team.qualifiedForPlayoffs(), awqiMean, apqiMean, self.Teams.index(team), debugInfo=False)
	
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

