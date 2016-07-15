## readata.py ##################################################################
## lets try loading the data from file again ###################################
## and make sure everything is there and comprehensible ########################
################################################################################

##import csv

from outputs import *

## I cant remember exactly what this was needed for, its some very specific
## aspect of graphing with matplotlib or something

if(__name__ == "__main__"):
	
	leagueId = 'watMu'
	levelId = 'beginner'
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	plotAllTeams(seasons, leagueId, levelId)
	plotAllTopPlayoffTeams(seasons, leagueId, levelId)
	plotAllTopPlayoffTeamsDeltas(seasons, leagueId, levelId)	

	##print "################################################################################"
	##print "Season Leaders #################################################################"
	##print "################################################################################\n"	
	
	##for season in seasons:
	##	print season.seasonId
	##	print season.getTeamByPosition(1).getDescriptionString()
		##print "Top Playoff Bracket: ", season.topPlayoffBracket, " %i" % len(season.topPlayoffBracket), "\n"
	##	season.printPlayoffBrackets()

