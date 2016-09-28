## playerSummary.py ############################################################
## show a players career summary ###############################################
################################################################################

from sys import argv
from outputs import *

from collections import Counter


if(__name__ == "__main__"):
		
	leagueId = argv[1]
	## ie 'watMu'
	##levelId = argv[2]
	
	playerName = argv[2]
	## ie 'Jim Brooks'
	
	## ids needed to open the proper folders and csv files contained within
	##seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	seasons = getAllSeasons(leagueId, 'beginner') + getAllSeasons(leagueId, 'intermediate') + getAllSeasons(leagueId, 'advanced') + getAllSeasons(leagueId, 'allstar')	
	
	
	franchises = False
	
	seasonIndexList = getSeasonIndexList(leagueId)
	
	playah = watMuPlayer(playerName, seasons)
	print playah.getStatsLine(), '\n\n'
	
	for team in reversed(playah.playedFor):
		print team.getDescriptionString(), '\n'
	
