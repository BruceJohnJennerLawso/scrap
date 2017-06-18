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
	container = teamStatContainer(shortName, longName, statValues, teamIds, teamNames, years, madePlayoffs)
	if(debugInfo):
		container.printContainer() 	
	return container
	

def getModelDiffContainer(seasons, leagueId, levelId, independentStatCall, independentShortName, independentLongName, dependentStatCall, dependentShortName, dependentLongName, debugInfo=False):
	
	if(debugInfo):
		print "Independent: %s, " % (independentLongName), independentStatCall
		print "Dependent: %s, " % (dependentLongName), dependentStatCall		
		
	
	independentStatValues = []
	dependentStatValues = []	
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			independentStatValues.append(independentStatCall(team))
			dependentStatValues.append(dependentStatCall(team))	
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	independentContainer = teamStatContainer(independentShortName, independentLongName, independentStatValues, teamIds, teamNames, years, madePlayoffs)
	dependentContainer = teamStatContainer(dependentShortName, dependentLongName, dependentStatValues, teamIds, teamNames, years, madePlayoffs)	
	if(debugInfo):
		independentContainer.printContainer()
		dependentContainer.printContainer()		 	
	
	modelDiffsContainer = independentContainer.getModelDiffs(dependentContainer)
	if(consistencyCheck(independentContainer, dependentContainer)):
		return modelDiffsContainer	
	else:
		print "Consistency check for model diffs container %s*%s failed" % (independentContainer.getShortStatName(), dependentContainer.getShortStatName())

