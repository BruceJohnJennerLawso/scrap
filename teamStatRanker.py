## teamStatRanker.py ###########################################################
## Rank all teams in a given sample based on a given stat ######################
################################################################################


from sys import argv
from outputs import *

import statSelect


if(__name__ == "__main__"):
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	sortOrder = argv[3]
	if(sortOrder not in ['asc', 'desc']):
		print "Bad sort order argument %s supplied, must be either asc or desc" % sortOrder
	
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
	franchises = False

	seasonIndexList = getSeasonIndexList(leagueId)

	stat = statSelect.getTargetStatContainer(targetStatName, seasons, leagueId, levelId)
	if(sortOrder == 'asc'):
		stat.printSortedContainer(playoffTeamsOnly)
	elif(sortOrder == 'desc'):
		stat.printReverseSortedContainer(playoffTeamsOnly)
	stat.printStatBounds(playoffTeamsOnly)
