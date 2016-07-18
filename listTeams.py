## listTeams.py ################################################################
## need just all of the teams and their info ###################################
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
	print "Season Teams ###################################################################"
	print "################################################################################\n"	
	
	for season in seasons:
		print season.seasonId, '\n'
		for team in season.Teams:
			print "		", team.getTeamName()
