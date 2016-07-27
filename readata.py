## readata.py ##################################################################
## lets try loading the data from file again ###################################
## and make sure everything is there and comprehensible ########################
################################################################################

from sys import argv
from outputs import *

## I cant remember exactly what this was needed for, its some very specific
## aspect of graphing with matplotlib or something

if(__name__ == "__main__"):
	
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	franchises = getFranchiseList(leagueId, levelId)
	
	
	plotAllTeams(seasons, leagueId, levelId)
	plotAllTopPlayoffTeams(seasons, leagueId, levelId)
	plotAllTopPlayoffTeamsDeltas(seasons, leagueId, levelId)	
	plotAllTopPlayoffTeamsVariables(seasons, leagueId, levelId, franchises)

