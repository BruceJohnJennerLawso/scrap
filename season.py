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
