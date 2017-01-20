## teamStatRanker.py ###########################################################
## Rank all teams in a given sample based on a given stat ######################
################################################################################


from sys import argv
from scrapParam import *

import statSelect

def moduleId():
	return "teamStatRanker"

def task(seasons, parameters):
	stat = statSelect.getTargetStatContainer(parameters.getTargetStatName(), seasons, parameters.getLeagueId(), parameters.getLevelId())
	if(parameters.getSortOrder() == 'asc'):
		stat.printSortedContainer(parameters.getPlayoffTeamsOnly())
	elif(parameters.getSortOrder() == 'desc'):
		stat.printReverseSortedContainer(parameters.getPlayoffTeamsOnly())
	stat.printStatBounds(parameters.getPlayoffTeamsOnly())


if(__name__ == "__main__"):
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	_sortOrder = argv[3]
	if(_sortOrder not in ['asc', 'desc']):
		print "Bad sort order argument %s supplied, must be either asc or desc" % _sortOrder
	
	playoffTeamsOnly = argv[4]
	if(playoffTeamsOnly == "True"):
		playoffTeamsOnly = True
	elif(playoffTeamsOnly == "False"):
		playoffTeamsOnly = False
	else:
		print "Unable to parse option 'playoffTeamsOnly' as %s" % playoffTeamsOnly	
	
	targetStatName = argv[5]
	
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	##franchises = False

	##seasonIndexList = getSeasonIndexList(leagueId)
	parameters = scrapParams(leagueId, levelId, playoffTeamsOnly, [], "Linear", targetStatName, independentStatName="None", sortOrder=_sortOrder)
	task(seasons, parameters)
	
		
