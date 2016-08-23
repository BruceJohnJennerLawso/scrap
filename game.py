## game.py #####################################################################
## object representing all of the data known about a given game ################
################################################################################


class Game(object):
	def __init__(self):
		self.Layers = []
		## list of lists, with each list containing stats computed for that
		## layer
		self.layerCount = 0
		
	def addLayer(self, data):
		self.Layers.append(data)
		## tack on a new layer
		self.layerCount += 1
		## increment the counter so we know its there

	def getDate(self):
		return self.Layers[0][0]
		## this should hopefully probably be a convention for all games levels
		
	def getLocation(self):
		return self.Layers[0][1]
		## same idea here
		
	def getGameResult(self):
		return self.Layers[0][2]

	def getGoalsFor(self):
		return int(self.Layers[0][3])
		
	def getGoalsAgainst(self):
		return int(self.Layers[0][4])		
		
	def getOpponentName(self):
		return self.Layers[0][6]		
		
	def getGoalDifferential(self):
		diff = self.getGoalsFor()-self.getGoalsAgainst()
		return diff					
		## easy mode here	

	def getGameClosenessIndex(self):
		if(self.Tied() != True):
			return 1.000/float(abs(self.getGoalDifferential()))
		else:
			return 1.000
		## ie
		##
		## 1-1 -> 1.000
		## 2-1 -> 1.000
		## 3-1 -> 0.500
		## 4-1 -> 0.333
		## 5-1 -> 0.250
		## 6-1 -> 0.200
		## 7-1 -> 0.166

		## its a quick way of measuring how close a game was in a numeric
		## way
		
		## although now that I take a look at it, the dropoff is a little bit
		## too steep early on between a 1 to 2 to 3 goal differential
		
	
