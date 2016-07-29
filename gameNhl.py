## gameNhl.py ##################################################################
## nhl game object #############################################################
## probably going to fragment into several different object ####################
## types depending on the era, since we may want to use more ###################
## data thats available for more recent eras ###################################
################################################################################
from game import *


class nhlGame(Game):
	def __init__(self, dateString, Location, gameResult, goalsFor, goalsAgainst, opponentName, thisTeamName, gameEndedIn):
		super(nhlGame, self).__init__()
		
		if(Location == '@'):
			gameLocation = '@%s_%s' % (opponentName, dateString)
		elif(Location == 'H'):
			gameLocation = '@%s_%s' % (thisTeamName, dateString)
		## gonna use this to track back to what barn the game
		## would have been played in
		
		self.addLayer([dateString, gameLocation, gameResult, goalsFor, goalsAgainst, thisTeamName, opponentName, gameEndedIn])
		self.layerCount += 1
	
	def getGameDescription(self):
		return "%s %s %s %s %i-%i %s %s" % (self.Layers[0][0], self.Layers[0][1], self.getThisTeamName(), self.Layers[0][2], self.getGoalsFor(), self.getGoalsAgainst(), self.getOpponentName(), self.Layers[0][7])

	def getThisTeamName(self):
		return self.Layers[0][5]
	
	def Won(self):
		if(self.Layers[0][2] == 'W'):
			return True
		else:
			return False
			
	def Tied(self):
		if(self.Layers[0][2] == 'T'):
			return True
		else:
			return False	
			
	def Lost(self):
		if(self.Layers[0][2] == 'L'):
			return True
		else:
			return False	

	def getExtraTimeString(self):
		return self.Layers[0][7]
		
	def decidedInOvertime(self):
		if(self.Layers[0][7] == 'OT'):
			return True
		else:
			return False
		
	def decidedInShootout(self):
		if(self.Layers[0][7] == 'SO'):
			return True
		else:
			return False
			
	def decidedInExtraTime(self):
		if((self.decidedInOvertime())or(self.decidedInShootout())):
			return True
		else:
			return False

		
	def getPointsEarned(self):
		if(self.Won()):
			return 2
		elif(self.Tied()):
			return 1
		elif((self.Lost())and(self.decidedInExtraTime())):
			return 1
		else:
			return 0
			## regardless of whether we lost in regulation or the game hasnt
			## been played yet, no points are earned
			
					
	def getOpponentName(self):
		return self.Layers[0][6]


