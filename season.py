## season.py ###################################################################
## general object representing seasons of a ####################################
## league ######################################################################
################################################################################
from team import *


class Season(Team):
	
	def __init__(self, leagueId, levelId, seasonId, teamIdList):
		self.Teams = []
		## list containing objects of type team<insert league here>
		self.seasonId = seasonId
		self.leagueId = leagueId
		self.levelId = levelId
	
	def getSeasonId(self):
		return self.seasonId
	
	def getTotalNumberOfTeams(self):
		## total teams in the league playing this season
		return len(self.Teams)
	
	def getSeasonTeams(self):
		## get a list of the team objects for this season
		return self.Teams
	
		
	## we often want to retrieve a team object from a season based
	## on a variety of information about it#
	
	def getTeamByPosition(self, position):
		## get the team object that finished at the given spot in the
		## standings, ie first overall would be position 1, second
		## overall would be position 2 and so on
		
		## this needs to raise an exception on failing to find what we
		## looking for
		for team in self.Teams:
			if((position -1) == self.Teams.index(team)):
				return team
		print "Unable to find team, position %i out of range" % position
		
	def getTeamByTeamName(self, teamName):
		## get the team object by its name in text,
		## ie 'Toronto Maple Leafs'
		
		## again, where those exceptions at
		for team in self.Teams:
			if(team.getTeamName() == teamName):
				return team
		print "Unable to find team, no team with name %s found" % teamName	

	def getTeamStatAverage(self, statName):
		output = 0.00
		
		for team in self.Teams:
			output += statName(team)
		output /= float(len(self.Teams))
		return output
		
	def getTeamStatList(self, statName):
		output = []
		
		for team in self.Teams:
			output.append(statName(team))
		return output		
		
	def getTeamsAboveOneGoalCutoff(self):
		output = 0
		for team in self.Teams:
			if(team.getCPQI() > 0.987):
			## 0.987 instead of 1.0 , since we want to ignore the possible
			## effect of one bad game (ie 1/82 lower than 1)	
				output += 1
		return output
