## game.py #####################################################################
## object representing all of the data known about a given game ################
################################################################################


class Game(object):
	def __init__(self, dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName):
		self.Layers = []
		self.addLayer([dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName])
		self.layerCount = 1
		
	def addLayer(self, data):
		self.Layers.append(data)
		
	def getGoalsFor(self):
		return self.Layers[0][3]
		## should hopefully already be in 
		
	def getGoalsAgainst(self):
		return self.Layers[0][4]		
		
	def getGoalDifferential(self):
		diff = self.getGoalsFor()-self.getGoalsAgainst()
		return diff		
		
	def getSOC(self):
		return float(self.Layers[0][5])
		## must remember this can be float if the game is being listed as
		## the team average SOC
		
	def setSOC(self, newValue):
		self.Layers[0][5] = newValue
		
	def getPointsEarned(self):
		if(self.Won()):
			return 2
		elif(self.Tied()):
			return 1
		else:
			return 0
			## regardless of whether we lost or the game hasnt been played yet,
			## no points are earned
			
	
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

	def getGameClosenessIndex(self):
		if(self.Tied() != True):
			return 1/float(abs(self.getGoalDifferential()))
		else:
			return 1
		
	def getOpponentName(self):
		return self.Layers[0][6]
