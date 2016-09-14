## statContainer.py ############################################################
## object that contains a specific stat and how to name ########################
## axes for it, etc., contains info for matching a given #######################
## data point to the team, year, level... ######################################
################################################################################


class statContainer:
	def __init__(self, statNameShort, statNameLong, statList, teamIdList, teamNameList, yearList, madePlayoffs):
		self.statNameShort = statNameShort
		self.statNameLong = statNameLong
		
		self.dataPoints = []
		for i in range(0, len(statList)):
			self.dataPoints.append([statList[i], teamIdList[i], teamNameList[i], yearList[i], madePlayoffs[i]])
			self.dataPoints = sorted(self.dataPoints, key=lambda list: list[1])
			self.dataPoints = sorted(self.dataPoints, key=lambda list: list[2])
			self.dataPoints = sorted(self.dataPoints, key=lambda list: list[3])
			self.dataPoints = sorted(self.dataPoints, key=lambda list: list[4])
			## this ensuring that the teams should have the same order every
			## time

	def getShortStatName(self):
		return self.statNameShort
		
	def getLongStatName(self):
		return self.statNameLong

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

	def getTeamIds(self, onlyPlayoffTeams=False):
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

	def getTeamNames(self, onlyPlayoffTeams=False):
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

	def getYears(self, onlyPlayoffTeams=False):
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
		
	def getMadePlayoffsList(self, onlyPlayoffTeams=False):
		output = []
		for pt in self.dataPoints:
			if(onlyPlayoffTeams == False):
				output.append(pt[4])
			else:
				if(pt[4] == True):
					output.append(pt[4])
				else:
					continue
					## the team we were on didnt make the playoffs, so it
					## doesnt get included in the output data
		return output
