## game.py #####################################################################
## object representing all of the data known about a given game ################
################################################################################


class Layer(object):
	def __init__(self, amLayer, inputData):
		self.Datas = []
		for dat in inputData:
			self.Datas.append(dat)
			## append dat shit
		self.layerNumber = amLayer
		
	def getData(layer, dataType):
		if(self.layerNumber == layer):
			
			if(layer == 1):
				## first layer is stuff assembled from the raw data set itself only,
				## only depending on data that deals with this specific team
				return getLayer1Data(dataType)
			elif(layer == 2):
				## second layer could be something more complex, like WQI, which
				## depends on the goal differential of this game, as well as the
				## point totals of the opposing team,
			
				## in other words, layer2 data cant be calculated until layer1
				## data is fully loaded, and layer3 depends on layer2, and so on
				return getLayer2Data(dataType)
			else:
				## havent gotten to this just yet		

		else:
			## asked the wrong layer for data, we fucked up
			return []







	def getLayer1Data(dataType):
		if(dataType == "dateString"):
			return self.Datas[0]
		elif(dataType == "Location"):
			return self.Datas[1]
		elif(dataType == "gameResult"):
			return self.Datas[2]
		elif(dataType == "goalsFor"):
			return self.Datas[3]
		elif(dataType == "goalsAgainst"):
			return self.Datas[4]
		elif(dataType == "SOC"):
			return self.Datas[5]
		elif(dataType == "opponentName"):
			return self.Datas[6]						
		else:
			return []	
			## some error code that should immediately grind things to a
			## halt if we ask for a piece of data that doesnt exist
	
	def getLayer2Data(dataType):
		if(dataType == "WQI"):
			return self.Datas[0]
		elif(dataType == "GCI"):
			return self.Datas[1]
		else:
			return []










class Game(object):
	def __init__(self, dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName):
		self.Layers = []
		self.Layers.append(Layer(1, [dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName]))
		
	def loadLayer(self, layerNumber, layerFunctions, parentLeague, parentTeam):
		layerData = []
		for func in layerFunctions:
			layerData.append(func(self.Layers[layerNumber - 2, parentLeague, parentTeam))
		self.Layers.append(Layer(layerNumber, layerData))	
		## whew, brain burning stuff right there
		
	def getTotalGoals(self):
		return (self.Layers[0].getData(1, "goalsFor") + self.Layers[0].getData(1, "goalsAgainst"))
	
