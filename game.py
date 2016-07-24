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
