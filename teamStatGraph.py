## teamStatGraph.py ############################################################
## create a graph of two parameters specified and save it to the results #######
## folder ######################################################################
################################################################################


from sys import argv
from scrapParam import *

import statSelect

def moduleId():
	return "teamStatGraph"


def task(seasons, parameters):
	
	if(parameters.getPlayoffTeamsOnly()):
		thing = 'PlayoffTeam'
	else:
		thing = 'Total'
	
	independent = statSelect.getTargetStatContainer(parameters.getIndependentStatName(), seasons, parameters.getLeagueId(), parameters.getLevelId())
	print "Independent"
	independent.printStatBounds()
	dependent = statSelect.getTargetStatContainer(parameters.getTargetStatName(), seasons, parameters.getLeagueId(), parameters.getLevelId())
	print "Dependent"
	dependent.printStatBounds()
	for var in [independent, dependent]:
		plotHistogram(var.getShortStatName(), 'Count', 'Histogram of %s' % var.getLongStatName(), var.getStat(parameters.getPlayoffTeamsOnly()),'./results/%s/%s/histograms' % (parameters.getLeagueId(), parameters.getLevelId()), '%s' % var.getShortStatName(), '%s_%s_histogram.png' % (var.getShortStatName(), thing))			
	plotScatterplot(independent.getShortStatName(), dependent.getShortStatName(), '%s\nby %s\nfor %s, %s' % (dependent.getLongStatName(), independent.getLongStatName(), parameters.getLeagueId(), parameters.getLevelId()), independent.getStat(parameters.getPlayoffTeamsOnly()), dependent.getStat(parameters.getPlayoffTeamsOnly()), './results/%s/%s/%sBy' % (parameters.getLeagueId(), parameters.getLevelId(), dependent.getShortStatName()), '%s' % independent.getShortStatName(), '%s_by_%s.png' % (dependent.getShortStatName(), independent.getShortStatName()))		



if(__name__ == "__main__"):
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	independentStat = argv[4]
	
	dependentStat = argv[5]
	
	playoffTeamsOnly = argv[3]
	if(playoffTeamsOnly == "True"):
		playoffTeamsOnly = True
	elif(playoffTeamsOnly == "False"):
		playoffTeamsOnly = False
	else:
		print "Unable to parse option 'playoffTeamsOnly' as %s" % playoffTeamsOnly
	
	if(playoffTeamsOnly):
		thing = 'PlayoffTeam'
	else:
		thing = 'Total'
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	franchises = False

	seasonIndexList = getSeasonIndexList(leagueId)

	parameters = scrapParams(leagueId, levelId, playoffTeamsOnly, [], dependentStat, independentStat)

	task(seasons, parameters)
