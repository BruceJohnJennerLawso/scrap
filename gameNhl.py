## gameNhl.py ##################################################################
## nhl game object #############################################################
## probably going to fragment into several different object ####################
## types depending on the era, since we may want to use more ###################
## data thats available for more recent eras ###################################
################################################################################
from game import *


class nhlGame(Game):
	def __init__(self, dateString, Location, homeTeamName, homeTeamGoalsScored, awayTeamName, awayTeamGoalsScored, extraTimeString):
		super(nhlGame, self).__init__()
		self.addLayer([dateString, Location, homeTeamName, homeTeamGoalsScored, awayTeamName, awayTeamGoalsScored, extraTimeString])
		self.layerCount += 1
		## first layer is the absolute bare minimum, just who played, who was
		## the home team, and how many goals each team scored, along with
		## whether the game went to OT or shootout. We should have
		## access to this data for any game we are looking at
		
		## if we have access to more data, like shots, teamwise PIM, PPG, SHG,
		## attendance, time of game (if its even worth handling that)
	
	def getHomeTeam(self):
		return self.Layers[0][2]
		
	def getAwayTeam(self):
		return self.Layers[0][4]

	def getGoalsFor(self, teamName):
		if(teamName == self.getHomeTeam()):
			return self.Layers[0][3]
		elif(teamName == self.getAwayTeam())
			return self.Layers[0][5]
		## should hopefully already be in 
		
	def getGoalsAgainst(self, teamName):
		if(teamName == self.getHomeTeam()):
			return self.Layers[0][5]
		elif(teamName == self.getAwayTeam())
			return self.Layers[0][3]
		## should hopefully already be in 
		
	def getGoalDifferential(self):
		diff = self.getGoalsFor()-self.getGoalsAgainst()
		return diff		
		
	def getPointsEarned(self):
		if(self.Won()):
			return 2
		elif(self.Tied()):
			return 1
		else:
			return 0
			## regardless of whether we lost or the game hasnt been played yet,
			## no points are earned
			
	
	def Won(self, teamName):
		if(self.getGoalsFor(teamName)>self.getGoalsAgainst(teamName)):
			return True
		else:
			return False
			
	def Tied(self):
		if(self.getGoalsFor(teamName)==self.getGoalsAgainst(teamName)):
			return True
		else:
			return False	
			
	def Lost(self):
		if(self.getGoalsFor(teamName)<self.getGoalsAgainst(teamName)):
			return True
		else:
			return False						

	def getExtraTimeString(self):
		return self.Layers[0][6]

	def getGameClosenessIndex(self):
		if(self.Tied() != True):
			return 1/float(abs(self.getGoalDifferential()))
		else:
			return 1

