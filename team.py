## team.py #####################################################################
## general base type for any team ##############################################
## hoping to define a specific stat type here instead of #######################
## redoing it for every different team type ####################################
################################################################################
from game import *

class Team(object):
	def __init__(self, seasonId, teamId):
		self.seasonId = seasonId
		self.teamId = teamId
		
		self.seasonGames = []
		## list of objects of type game
		
		
		
		loadPath = "./foooo"
		## gonna point this to the appropriate file using season and team ids
	
		
