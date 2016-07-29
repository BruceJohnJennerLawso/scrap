## gameWatMu.py ################################################################
## game object specifically representing a waterloo intramurals ################
## game, since the nhl game will need to work a bit differently ################
################################################################################

from game import *

class watMuGame(Game):
	def __init__(self, dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName):
		super(watMuGame, self).__init__()
		self.addLayer([dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName])
		self.layerCount += 1

	def getSOC(self):
		return float(self.Layers[0][5])
		## must remember this can be float if the game is being listed as
		## the team average SOC
		
	def setSOC(self, newValue):
		self.Layers[0][5] = newValue

	def Won(self):
		if(self.Layers[0][2] == 'won'):
			return True
		else:
			return False
			
	def Tied(self):
		if(self.Layers[0][2] == 'tie'):
			return True
		else:
			return False	
			
	def Lost(self):
		if(self.Layers[0][2] == 'lost'):
			return True
		else:
			return False
		
	def getPointsEarned(self):
		## this needs to be defined on a league by league basis, since not all
		## leagues actually score points the same way, ie Euro leagues with
		## 3 point system
		if(self.Won()):
			return 2
		elif(self.Tied()):
			return 1
		else:
			return 0
			## regardless of whether we lost or the game hasnt been played yet,
			## no points are earned
	
	def getOpponentName(self):
		return self.Layers[0][6]
