## statRetrieve.py #############################################################
## moving functions that collect a list of stats from an input #################
## of teams, seasons, etc. #####################################################
################################################################################


from statContainer import *


def getMawquees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaAWQI())
	return output

def getMapquees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaAPQI())
	return output

def getMaoquees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaAOQI())
	return output

def getMadquees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaADQI())
	return output

def getOffences(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getSeasonGoalsForAverage())
	return output

def getDefences(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getSeasonGoalsAgainstAverage())
	return output

def getAgcees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getAGCI())
	return output

def getAgcees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getAGCI())
	return output


def demoStatContainer(seasons, leagueId, levelId):
	mawquees = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			mawquees.append(team.getMaAWQI())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.qualifiedForPlayoffs())
	container = statContainer(mawquees, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	
	
	
