## teamStatGraph.py ############################################################
## create a graph of two parameters specified and save it to the results #######
## folder ######################################################################
################################################################################


from sys import argv
from outputs import *

import statSelect

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

	##for season in seasons:
	##	for team in season.Teams:
	##		if(team.getTeamName() == teamName):
	##			print "%i,%.3f" % (int(season.seasonId),team.getCPQI())

	independent = statSelect.getTargetStatContainer(independentStat, seasons, leagueId, levelId)
	dependent = statSelect.getTargetStatContainer(dependentStat, seasons, leagueId, levelId)
	for var in [independent, dependent]:
		plotHistogram(var.getShortStatName(), 'Count', 'Histogram of %s' % var.getLongStatName(), var.getStat(playoffTeamsOnly),'./results/%s/%s/histograms' % (leagueId, levelId), '%s' % var.getShortStatName(), '%s_%s_histogram.png' % (var.getShortStatName(), thing))			
	plotScatterplot(independent.getShortStatName(), dependent.getShortStatName(), '%s\nby %s\nfor %s, %s' % (dependent.getLongStatName(), independent.getLongStatName(), leagueId, levelId), independent.getStat(playoffTeamsOnly), dependent.getStat(playoffTeamsOnly), './results/%s/%s/%sBy' % (leagueId, levelId, dependent.getShortStatName()), '%s' % independent.getShortStatName(), '%s_by_%s.png' % (dependent.getShortStatName(), independent.getShortStatName()))		
