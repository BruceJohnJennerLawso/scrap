## teamSummary.py ##############################################################
## give a team name and summarize data about it, and its #######################
## players #####################################################################
################################################################################

from sys import argv
from outputs import *

from collections import Counter


if(__name__ == "__main__"):
		
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	seasonId = argv[3]
	## ie 'fall2015'
	teamName = argv[4]
	## ie 'The Mighty Dads'
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	franchises = getFranchiseList(leagueId, levelId)
	
	seasonIndexList = getSeasonIndexList(leagueId)
	for season in seasons:
		if(season.getSeasonId() == seasonId):
			for team in season.Teams:
				if(team.getTeamName() == teamName):
					print team.getDescriptionString()
					
					teamExpectedMawquee = 0.000
					
					for player in team.getPlayers():
						player.getStatsLine(getSeasonIndexById(seasonId, getSeasonIndexList(leagueId)))
						print getSeasonIndexById(seasonId, getSeasonIndexList(leagueId))
						teamExpectedMawquee += player.getPlayerMaAWQI(getSeasonIndexById(seasonId, getSeasonIndexList(leagueId)))
					teamExpectedMawquee /= float(len(team.getPlayers()))
					print "Team expected MaAWQI %.3f, Actual %.3f, diff %.3f" % (teamExpectedMawquee, team.getMaAWQI(), (team.getMaAWQI()-teamExpectedMawquee))
	
	teamExpectedMawquees = []
	playoffPercentages = []
