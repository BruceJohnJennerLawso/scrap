## playerSummary.py ############################################################
## show a players career summary ###############################################
################################################################################

from sys import argv
from outputs import *

from collections import Counter


if(__name__ == "__main__"):
		
	leagueId = argv[1]
	## ie 'watMu'
	
	playerName = argv[2]
	## ie 'Jim Brooks'
	
	## ids needed to open the proper folders and csv files contained within
	##seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	
	
	franchises = False
	
	seasonIndexList = getSeasonIndexList(leagueId)
	
	
	if(leagueId == 'watMu'):
		seasons = getAllSeasons(leagueId, 'beginner') + getAllSeasons(leagueId, 'intermediate') + getAllSeasons(leagueId, 'advanced') + getAllSeasons(leagueId, 'allstar')		
		playah = watMuPlayer(playerName, seasons)
	else:
		##seasons = getAllSeasons(leagueId, 'everything')
		seasons = getAllSeasons('wha', 'everything') + getAllSeasons('nhl', 'everything')
		playah = nhlPlayer(playerName, seasons)		
	
	print playah.getStatsLine(), '\n\n'
	
	for team in reversed(playah.playedFor):
		print team.getDescriptionString(), '\n'
	
