## game.py #####################################################################
## object representing all of the data known about a given game ################
################################################################################


class Game(object):
	##def __init__(self, dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName):
	def __init__(self):
		self.Layers = []
		## list of lists, with each list containing stats computed for that
		## layer
		self.layerCount = 0
		
	def addLayer(self, data):
		self.Layers.append(data)
		self.layerCount += 1

	def getDate(self):
		return self.Layers[0][0]
		
	def getLocation(self):
		return self.Layers[0][1]

	def getGoalsFor(self):
		return int(self.Layers[0][3])
		## should hopefully already be in 
		
	def getGoalsAgainst(self):
		return int(self.Layers[0][4])		
		
	def getGoalDifferential(self):
		diff = self.getGoalsFor()-self.getGoalsAgainst()
		return diff					
							

	def getGameClosenessIndex(self):
		if(self.Tied() != True):
			return 1/float(abs(self.getGoalDifferential()))
		else:
			return 1
