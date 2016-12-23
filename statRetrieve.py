## statRetrieve.py #############################################################
## moving functions that collect a list of stats from an input #################
## of teams, seasons, etc. #####################################################
################################################################################


from statContainer import *

	
def getStatContainer(statCall, shortName, longName, seasons, leagueId, levelId, debugInfo=False):
	
	if(debugInfo):
		print statCall
	
	statValues = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			statValues.append(statCall(team))
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer(shortName, longName, statValues, teamIds, teamNames, years, madePlayoffs)
	if(debugInfo):
		container.printContainer() 	
	return container
	

