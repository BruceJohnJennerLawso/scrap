## teamSummary.py ##############################################################
## give a team name and summarize data about it, and its #######################
## players #####################################################################
################################################################################

from sys import argv
from outputs import *



if(__name__ == "__main__"):
		
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	
	
	teamName = 0
	if(len(argv) > 3):
		teamName = argv[3]
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	franchises = False

	seasonIndexList = getSeasonIndexList(leagueId)
	
	for season in seasons:
		if(teamName == 0):
			print "################################################################################"
			print season.seasonId, "###########################################################################"
			print "################################################################################\n"		
		
		for team in season.Teams:
			if(teamName != 0):
				if(team.getTeamName() == teamName):
					print team.getDescriptionString(), "\n"			
			else:	
				print team.getDescriptionString(), "\n"
