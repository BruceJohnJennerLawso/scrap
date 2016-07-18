## leaders.py ##################################################################
## output for top teams each season ############################################
################################################################################

from sys import argv
from outputs import *


if(__name__ == "__main__"):
		
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	
	print "################################################################################"
	print "Season Leaders #################################################################"
	print "################################################################################\n"	
	
	for season in seasons:
		print season.seasonId
		print season.getTeamByPosition(1).getDescriptionString()
		print "Top Playoff Bracket: ", season.topPlayoffBracket, " %i" % len(season.topPlayoffBracket), "\n"
		season.printPlayoffBrackets()
