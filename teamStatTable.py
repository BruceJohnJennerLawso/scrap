## teamStatTable.py ############################################################
## Get a simple list with the year and the value of a ##########################
## given stat for that year in the terminal ####################################
################################################################################


from sys import argv
from outputs import *




if(__name__ == "__main__"):
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	teamName = argv[3]
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	franchises = False

	seasonIndexList = getSeasonIndexList(leagueId)

	for season in seasons:
		for team in season.Teams:
			if(team.getTeamName() == teamName):
				print "%i,%.3f" % (int(season.seasonId),team.getCPQI())
