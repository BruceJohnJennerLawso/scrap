## season.py ###################################################################
## general object representing seasons of a ####################################
## league ######################################################################
################################################################################
from team import *


class Season(Team):
	def __init__(self, leagueId, levelId, seasonId, teamIdList):
		self.Teams = []
		self.seasonId = seasonId
		self.leagueId = leagueId
		self.levelId = levelId
		
	def getTeamByPosition(self, position):
		for team in self.Teams:
			if((position -1) == self.Teams.index(team)):
				return team
		print "Unable to find team, position %i out of range" % position
		
	def getTeamByTeamName(self, teamName):
		for team in self.Teams:
			if(team.getTeamName() == teamName):
				return team
		print "Unable to find team, no team with name %s found" % teamName	
