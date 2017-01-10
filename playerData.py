## playerData.py ###############################################################
################################################################################

from sys import argv
from outputs import *

from collections import Counter

def moduleId():
	return "playerData"

if(__name__ == "__main__"):
		
	leagueId = argv[1]
	## ie 'watMu'
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, 'beginner') + getAllSeasons(leagueId, 'intermediate') + getAllSeasons(leagueId, 'advanced') + getAllSeasons(leagueId, 'allstar')		
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	franchises = False
	
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
					
