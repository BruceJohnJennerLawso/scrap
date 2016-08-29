## statContainer.py ############################################################
## object that contains a specific stat and how to name ########################
## axes for it, etc., contains info for matching a given #######################
## data point to the team, year, level... ######################################
################################################################################


class statContainer:
	def __init__(self, statList, teamIdList, teamNameList, yearList, madePlayoffs):
		self.dataPoints = []
		for i in range(0, len(statList)):
			self.dataPoints.append([statList[i], teamIdList[i], teamNameList[i], yearList[i], madePlayoffs[i]])
		
	def printContainer(self):
		print "[",
		for i in self.dataPoints:
			print i
		print "]"
		
	def getStat(self, onlyPlayoffTeams=False):
		output = []
		for pt in self.dataPoints:
			if(onlyPlayoffTeams == False):
				output.append(pt[0])
			else:
				if(pt[4] == True):
					output.append(pt[0])
				else:
					continue
					## the team we were on didnt make the playoffs, so it
					## doesnt get included in the output data
		return output

	def getTeamIds(self):
		output = []
		for pt in self.dataPoints:
			if(onlyPlayoffTeams == False):
				output.append(pt[1])
			else:
				if(pt[4] == True):
					output.append(pt[1])
				else:
					continue
					## the team we were on didnt make the playoffs, so it
					## doesnt get included in the output data
		return output

	def getTeamNames(self):
		output = []
		for pt in self.dataPoints:
			if(onlyPlayoffTeams == False):
				output.append(pt[2])
			else:
				if(pt[4] == True):
					output.append(pt[2])
				else:
					continue
					## the team we were on didnt make the playoffs, so it
					## doesnt get included in the output data
		return output	

	def getYears(self):
		output = []
		for pt in self.dataPoints:
			if(onlyPlayoffTeams == False):
				output.append(pt[3])
			else:
				if(pt[4] == True):
					output.append(pt[3])
				else:
					continue
					## the team we were on didnt make the playoffs, so it
					## doesnt get included in the output data
		return output
