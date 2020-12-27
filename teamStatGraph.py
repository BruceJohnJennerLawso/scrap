## teamStatGraph.py ############################################################
## create a graph of two parameters specified and save it to the results #######
## folder ######################################################################
################################################################################


from sys import argv
from scrapParam import *

import statSelect

def moduleId():
	return "teamStatGraph"

def description():
	output = "The teamStatGraph module is used to create an on-demand graph of a given\n"
	output += "pair of stats for the range of seasons &/or teams specified\n"
	return output

def exampleCommand():
	output = "python teamStatGraph.py nhl everything True PGDT CPQI*GDA\n"
	output += "(where PGDT is dependent, CPQI*GDA is independent)"
	return output

def task(seasons, parameters):
	
	seasons = filterSeasonsByParams(seasons, parameters)
	
	parameters.info()
	
	if(parameters.getPlayoffTeamsOnly()):
		thing = 'PlayoffTeam'
	else:
		thing = 'Total'
	
	independent = statSelect.getTargetStatContainer(parameters.getIndependentStatName(), seasons, parameters.getLeagueId(), parameters.getLevelId())
	print("Independent")
	independent.printStatBounds()
	dependent = statSelect.getTargetStatContainer(parameters.getTargetStatName(), seasons, parameters.getLeagueId(), parameters.getLevelId())
	print("Dependent")
	dependent.printStatBounds()
	for var in [independent, dependent]:
		plotHistogram(var.getShortStatName(), 'Count', 'Histogram of %s' % var.getLongStatName(), var.getStat(parameters.getPlayoffTeamsOnly()),'./results/%s/%s/histograms' % (parameters.getLeagueId(), parameters.getLevelId()), '%s' % var.getShortStatName(), '%s_%s_histogram.png' % (var.getShortStatName(), thing))			
	plotScatterplot(independent.getShortStatName(), dependent.getShortStatName(), '%s\nby %s\nfor %s, %s' % (dependent.getLongStatName(), independent.getLongStatName(), parameters.getLeagueId(), parameters.getLevelId()), independent.getStat(parameters.getPlayoffTeamsOnly()), dependent.getStat(parameters.getPlayoffTeamsOnly()), './results/%s/%s/%sBy' % (parameters.getLeagueId(), parameters.getLevelId(), dependent.getShortStatName()), '%s' % independent.getShortStatName(), '%s_by_%s.png' % (dependent.getShortStatName(), independent.getShortStatName()))		



if(__name__ == "__main__"):
	
	try:
		leagueId = argv[1]
		## ie 'watMu'
		levelId = argv[2]
		## ie 'beginner'
	
		dependentStat = argv[4]
	
		independentStat = argv[5]
	
		playoffTeamsOnly = argv[3]
		if(playoffTeamsOnly == "True"):
			playoffTeamsOnly = True
		elif(playoffTeamsOnly == "False"):
			playoffTeamsOnly = False
		else:
			print("Unable to parse third option 'playoffTeamsOnly' provided as %s" % playoffTeamsOnly)
			raise IndexError
	except IndexError:
		print("Arguments %s failing due to index error, see example commands for %s:\n" % (tuple(argv[1:]), argv[0]))		
		print(exampleCommand())
		exit()
		
	seasons = getAllSeasons(leagueId, levelId)

	parameters = scrapParams(leagueId, levelId, playoffTeamsOnly, [], [], "Linear", dependentStat, independentStatName=independentStat)

	task(seasons, parameters)
