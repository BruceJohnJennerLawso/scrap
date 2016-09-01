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
	
	print "Running readata with argv ", argv, '\n'
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	
	
	print 'Fuck'
	print getPlayoffSuccessStatContainer(seasons, leagueId, levelId).getStat(True)
	print 'Bar'
	
	graphTeams(leagueId, levelId, True, getPlayoffSuccessStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId))
	graphTeamsAgainstDeltas(leagueId, levelId, True, getPlayoffSuccessStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId))	
	graphTeamsHistogram(leagueId, levelId, True, getPlayoffSuccessStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId))
	graphTeamsHistogram(leagueId, levelId, False, getPlayoffSuccessStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId))

	
	exit()
	
	plotAllTeams(seasons, leagueId, levelId)
	plotAllTopPlayoffTeams(seasons, leagueId, levelId)
	plotAllTopPlayoffTeamsDeltas(seasons, leagueId, levelId)	
	plotAllTopPlayoffTeamsVariables(seasons, leagueId, levelId)

