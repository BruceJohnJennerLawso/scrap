## game.py #####################################################################
## object representing all of the data known about a given game ################
################################################################################


class Game(object):
	def __init__(self, dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName):
		self.Layers = []
		self.addLayer([dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName])
		self.layerCount = 1
		
	def addLayer(data):
		self.Layers.append(data)
	
