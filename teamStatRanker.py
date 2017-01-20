## teamStatRanker.py ###########################################################
## Rank all teams in a given sample based on a given stat ######################
################################################################################


from sys import argv
from scrapParam import *

import statSelect

def moduleId():
	return "teamStatRanker"

def description():
	output = "The teamStatRanker module is used to obtain a list of the team stat values\n"
	output += "for a given stat, sort the list by stat value, and print the list in\n"
	output += "a prettified form to the console\n"
	return output

def exampleCommand():
	output = "python teamStatRanker.py nhl everything desc False CPQI\n"
	output += "python teamStatRanker.py nhl everything desc True POT\n"
	return output

def task(seasons, parameters):
	seasons = filterSeasonsByParams(seasons, parameters)
	
	stat = statSelect.getTargetStatContainer(parameters.getTargetStatName(), seasons, parameters.getLeagueId(), parameters.getLevelId())
	if(parameters.getSortOrder() == 'asc'):
		stat.printSortedContainer(parameters.getPlayoffTeamsOnly())
	elif(parameters.getSortOrder() == 'desc'):
		stat.printReverseSortedContainer(parameters.getPlayoffTeamsOnly())
	stat.printStatBounds(parameters.getPlayoffTeamsOnly())


if(__name__ == "__main__"):
	
	try:
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
	except IndexError:
		print "Arguments %s failing due to index error, see example commands for %s:\n" % (tuple(argv[1:]), argv[0])		
		print exampleCommand()
		exit()
	
	seasons = getAllSeasons(leagueId, levelId)
	parameters = scrapParams(leagueId, levelId, playoffTeamsOnly, [], [], "Linear", targetStatName, independentStatName="None", sortOrder=_sortOrder)
	task(seasons, parameters)
	
		
