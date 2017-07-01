## statRetrieve.py #############################################################
## moving functions that collect a list of stats from an input #################
## of teams, seasons, etc. #####################################################
################################################################################


from statContainer import *




	


def getModelDiffContainer(seasons, leagueId, levelId, independentShortName, dependentShortName, debugInfo=True):
	
	independentStatCall = getTeamStatInformation(independentShortName)[0]
	dependentStatCall = getTeamStatInformation(dependentShortName)[0]
	
	if(debugInfo):
		print "Independent: %s, " % (getTeamStatLongName(independentShortName)), independentStatCall
		print "Dependent: %s, " % (getTeamStatLongName(dependentShortName)), dependentStatCall		
		
	independentContainer = teamStatContainer(independentShortName, seasons)
	dependentContainer = teamStatContainer(dependentShortName, seasons)
	if(debugInfo):
		print "Independent Container:\n"
		print independentContainer.getShortStatName()
		independentContainer.printContainer()
		print "Dependent Container:\n"
		print dependentContainer.getShortStatName()	 			
		dependentContainer.printContainer()	
	
	modelDiffsContainer = independentContainer.getModelDiffs(dependentContainer)
	if(consistencyCheck(independentContainer, dependentContainer)):
		return modelDiffsContainer	
	else:
		print "Consistency check for model diffs container %s*%s failed" % (independentContainer.getShortStatName(), dependentContainer.getShortStatName())

