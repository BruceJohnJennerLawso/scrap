## seasonSummary.py ############################################################
## summarize average stats for seasons over time ###############################
################################################################################

from sys import argv
from outputs import *
import team


if(__name__ == "__main__"):
		
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	
	
	##teamNames = 0
	##if(len(argv) > 3):
	##	teamNames = argv[3:len(argv)]
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	franchises = False

	seasonIndexList = getSeasonIndexList(leagueId)

	print "################################################################################"
	print "%s#############################################################" % levelId
	print "################################################################################\n"		
	for season in seasons:	
		print "%s %i teams, league average AWQI, APQI,  AGCI, AOQI,  ADQI, CPQI, Points, Points Pct \nAverages:                    %2.2f, %2.2f, %2.2f, %2.2f, %2.2f, %2.2f, %2.2f,  %2.2f" % (season.getSeasonId(),  season.getTotalNumberOfTeams(), season.getTeamStatAverage(team.Team.getAWQI), season.getTeamStatAverage(team.Team.getAPQI), season.getTeamStatAverage(team.Team.getAGCI), season.getTeamStatAverage(team.Team.getAOQI), season.getTeamStatAverage(team.Team.getADQI), season.getTeamStatAverage(team.Team.getCPQI), season.getTeamStatAverage(team.Team.getSeasonPointsTotal), season.getTeamStatAverage(team.Team.getPointsPercentage))
						
