## statContainer.py ############################################################
## object that contains a specific stat and how to name ########################
## axes for it, etc., contains info for matching a given #######################
## data point to the team, year, level... ######################################
################################################################################
from scipy import stats

from statSelect import *

def consistencyCheck(statCon1, statCon2):
	if(statCon1.getNumberOfDataPoints() == statCon2.getNumberOfDataPoints()):
		if(statCon1.getDataPointsWithoutData() == statCon2.getDataPointsWithoutData()):
			return True
			## the two lists have the same lengths, and are sorted in the same
			## order, so they are safe to compare
	
	return False
	## either the containers had different number of teams contained within, or
	## they arent sorted the same way (could end up producing incorrect outputs)
		












## statList, teamIdList, teamNameList, yearList, madePlayoffs

class teamStatContainer:
	def __init__(self, statNameShort, seasons, statValues=[]):
		self.statNameShort = statNameShort
		self.statNameLong = getTeamStatLongName(statNameShort)
		
		statCall = getTeamStatInformation(statNameShort)[0]
		
		
		
		##statValues = []
		teamIds = []
		teamNames = []
		years = []
		madePlayoffs = []

		for season in seasons:
			for team in season.Teams:
				teamIds.append(team.getTeamId())
				teamNames.append(team.getTeamName())
				years.append(team.seasonId)
				madePlayoffs.append(team.madeRealPlayoffs())
				
		if(statValues == []):
			for season in seasons:
				for team in season.Teams:
					statValues.append(statCall(team))
		
		self.dataPoints = []
		for i in range(0, len(statValues)):
			statRow = [statValues[i], teamIds[i], teamNames[i], years[i], madePlayoffs[i]]
			self.dataPoints.append(statRow)
		self.sortDataPointsByStandard()

	def sortDataPointsByStandard(self):
		self.dataPoints = sorted(self.dataPoints, key=lambda list: list[1])
		## first sort by the teamID, ie 'TOR', 'MTL, alphabetically'
		self.dataPoints = sorted(self.dataPoints, key=lambda list: list[2])
		## then sort by the teams full name alphabetically, ie
		## 'Toronto Maple Leafs', 'Montreal Canadiens'
		self.dataPoints = sorted(self.dataPoints, key=lambda list: list[3])
		## sort by year string (I think this should be the same as sort by
		## number, even if the year is in string form)
		self.dataPoints = sorted(self.dataPoints, key=lambda list: list[4])
		## sort by whether the team made the playoffs, Falses on top, Trues on
		## bottom
		
		## this ensuring that the teams should have the same order every
		## time, after the sort by the stat value, so even if there are two
		## teams with identical values for a given stat, they should be sorted
		## alphabetically & by year in the output
		
		## this is so that when we retrieve the data to analyze relative to a
		## different set of data about the team, data points about a particular
		## team will map one to one with the other data set


	def getModelDiffs(self, dependentContainer, playoffTeamsOnly=False):
		## so generate our model here based on the data provided in each
		## stat container, then output a new statContainer object with
		## the values of the model diffs
		
		print "Consistency check between %s and %s containers is a %r" % (self.getShortStatName(), dependentContainer.getShortStatName(), consistencyCheck(self, dependentContainer))
		
		x_values = self.getStat(playoffTeamsOnly)
		y_values = dependentContainer.getStat(playoffTeamsOnly)
		
		gradient, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
		print "fit parameters, ", gradient, intercept
		modelDiffs = []
		
		def modelValue(x, gradient, intercept):
			return (x*gradient + intercept)
		
		for i in range(0, len(x_values)):
			modelDiffs.append(y_values[i] - modelValue(x_values[i], gradient, intercept))
		
		##outputDiffContainer = teamStatContainer("%sby%s_Diffs" % (dependentContainer.getShortStatName(), self.getShortStatName()), )
		print "creating new statcontainer with diffs, ", x_values, "\n", y_values, "\n", modelDiffs, "\n", "\ngradient = %.3f\nintercept = %.3f\n\n" % (gradient, intercept)
		
		return teamStatDiffContainer(dependentContainer.getShortStatName(), self.getShortStatName(), dependentContainer, self.getLongStatName(), modelDiffs, gradient, intercept)

	def getShortStatName(self):
		return self.statNameShort
		
	def getLongStatName(self):
		return self.statNameLong

	def getNumberOfDataPoints(self):
		return len(self.dataPoints)

	def getDataPoints(self):
		return self.dataPoints

	def getDataPointsWithoutData(self):
		return [dataPt[1:] for dataPt in self.getDataPoints()]

	def printContainer(self):
		print "[",
		for i in self.getDataPoints():
			print i
		print "]"

	def printDataPoint(self, pt):
		print "%.3f " % pt[0], pt[1:]

	def printSortedContainer(self, onlyPlayoffTeams=False):
		print "[",
		for i in sorted(self.getDataPoints(), key=lambda list: list[0]):
			if(onlyPlayoffTeams == True):
				if(i[4] == True):
					self.printDataPoint(i)
			else:
				self.printDataPoint(i)
		print "]"	
		
	def printReverseSortedContainer(self, onlyPlayoffTeams=False):
		print "[",
		for i in reversed(sorted(self.dataPoints, key=lambda list: list[0])):
			if(onlyPlayoffTeams == True):
				if(i[4] == True):
					self.printDataPoint(i)
			else:
				self.printDataPoint(i)
		print "]"				
	
	def printStatBounds(self, onlyPlayoffTeams=False):
		print "[%.3f, %.3f]" % (min(self.getStat(onlyPlayoffTeams)), max(self.getStat(onlyPlayoffTeams)))
		
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
		
		
		
class teamStatDiffContainer(teamStatContainer):
	def __init__(self, dependentShortName, independentShortName, dependentContainer, independentLongStatName, modelDiffs, gradient, intercept):
		
		##super(teamStatDiffContainer, self).__init__(data)
		
		self.statNameShort = "%sby%s_ModelDiffs" % (dependentShortName, independentShortName)
		self.statNameLong = "Deltas from the Model for %s by %s, gradient=%.3f, intercept=%.3f" % (dependentContainer.getLongStatName(), independentLongStatName, gradient, intercept)
		
		
		

		##statValues = []
		teamIds = dependentContainer.getTeamIds()
		teamNames = dependentContainer.getTeamNames()
		years = dependentContainer.getYears()
		madePlayoffs = dependentContainer.getMadePlayoffsList()
	
		statValues = modelDiffs
		
		self.dataPoints = []
		for i in range(0, len(statValues)):
			statRow = [statValues[i], teamIds[i], teamNames[i], years[i], madePlayoffs[i]]
			self.dataPoints.append(statRow)
		self.sortDataPointsByStandard()		
		
		
		
		
		
		
		
		
		
		
		
class gameStatContainer:
	def __init__(self, statNameShort, statNameLong):
		self.statNameShort = statNameShort
		self.statNameLong = statNameLong
		
		self.dataPoints = []
		for i in range(0, len(statList)):
			statRow = [statList[i], homeTeamIdList[i], homeTeamNameList[i], awayTeamIdList[i], awayTeamNameList[i], dateList[i]]
			self.dataPoints.append(statRow)
		self.sortDataPointsByStandard()

	def sortDataPointsByStandard(self):
		self.dataPoints = sorted(self.dataPoints, key=lambda list: list[1])
		## first sort by the teamID, ie 'TOR', 'MTL, alphabetically'
		self.dataPoints = sorted(self.dataPoints, key=lambda list: list[2])
		## then sort by the teams full name alphabetically, ie
		## 'Toronto Maple Leafs', 'Montreal Canadiens'
		self.dataPoints = sorted(self.dataPoints, key=lambda list: list[3])
		## sort by year string (I think this should be the same as sort by
		## number, even if the year is in string form)
		self.dataPoints = sorted(self.dataPoints, key=lambda list: list[4])
		## sort by whether the team made the playoffs, Falses on top, Trues on
		## bottom
		
		## this ensuring that the teams should have the same order every
		## time, after the sort by the stat value, so even if there are two
		## teams with identical values for a given stat, they should be sorted
		## alphabetically & by year in the output
		
		## this is so that when we retrieve the data to analyze relative to a
		## different set of data about the team, data points about a particular
		## team will map one to one with the other data set


	def getModelDiffs(self, dependentContainer, playoffTeamsOnly=False):
		## so generate our model here based on the data provided in each
		## stat container, then output a new statContainer object with
		## the values of the model diffs
		
		print "Consistency check between %s and %s containers is a %r" % (self.getShortStatName(), dependentContainer.getShortStatName(), consistencyCheck(self, dependentContainer))
		
		x_values = self.getStat(playoffTeamsOnly)
		y_values = dependentContainer.getStat(playoffTeamsOnly)
		
		gradient, intercept, r_value, p_value, std_err = stats.linregress( x_values, y_values)
		
		modelDiffs = []
		
		def modelValue(x, gradient, intercept):
			return (x*gradient + intercept)
		
		for i in range(0, len(x_values)):
			modelDiffs.append(y_values[i] - modelValue(x_values[i], gradient, intercept))
		return teamStatContainer("%sby%s Model Diffs" % (dependentContainer.getShortStatName(), self.getShortStatName()), "Deltas from the Model for %s by %s, gradient=%.3f, intercept=%.3f" % (dependentContainer.getLongStatName, self.getShortStatName(), gradient, intercept), modelDiffs, self.getTeamIds(playoffTeamsOnly), self.getTeamNames(playoffTeamsOnly), self.getYears(playoffTeamsOnly), self.getMadePlayoffsList(playoffTeamsOnly))

	def getShortStatName(self):
		return self.statNameShort
		
	def getLongStatName(self):
		return self.statNameLong

	def getNumberOfDataPoints(self):
		return len(self.dataPoints)

	def getDataPoints(self):
		return self.dataPoints

	def getDataPointsWithoutData(self):
		return [dataPt[1:] for dataPt in self.getDataPoints()]

	def printContainer(self):
		print "[",
		for i in self.getDataPoints():
			print i
		print "]"

	def printDataPoint(self, pt):
		print "%.3f " % pt[0], pt[1:]

	def printSortedContainer(self, onlyPlayoffTeams=False):
		print "[",
		for i in sorted(self.getDataPoints(), key=lambda list: list[0]):
			if(onlyPlayoffTeams == True):
				if(i[4] == True):
					self.printDataPoint(i)
			else:
				self.printDataPoint(i)
		print "]"	
		
	def printReverseSortedContainer(self, onlyPlayoffTeams=False):
		print "[",
		for i in reversed(sorted(self.dataPoints, key=lambda list: list[0])):
			if(onlyPlayoffTeams == True):
				if(i[4] == True):
					self.printDataPoint(i)
			else:
				self.printDataPoint(i)
		print "]"				
	
	def printStatBounds(self, onlyPlayoffTeams=False):
		print "[%.3f, %.3f]" % (min(self.getStat(onlyPlayoffTeams)), max(self.getStat(onlyPlayoffTeams)))
		
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
		
		
