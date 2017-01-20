## playerSummary.py ############################################################
## show a players career summary ###############################################
################################################################################

from sys import argv
from scrapParam import *

from collections import Counter

def moduleId():
	return "playerSummary"

def task(seasons, parameters):
	
	##seasons = filterSeasonsByParams(seasons, parameters)
	## NOT going to filter here, because we want complete data about a player
	
	if(parameters.getLeagueId() == 'watMu'):
		seasons = getAllSeasons(leagueId, 'beginner') + getAllSeasons(leagueId, 'intermediate') + getAllSeasons(leagueId, 'advanced') + getAllSeasons(leagueId, 'allstar')		
		playah = watMuPlayer(playerName, seasons)
	else:
		##seasons = getAllSeasons(leagueId, 'everything')
		seasons = getAllSeasons('wha', 'everything') + getAllSeasons('nhl', 'everything')
		playah = nhlPlayer(playerName, seasons)		
	
	print playah.getStatsLine(), '\n\n'
	
	for team in reversed(playah.playedFor):
		print team.getDescriptionString(), '\n'

if(__name__ == "__main__"):
		
	leagueId = argv[1]
	## ie 'watMu'
	
	playerName = argv[2]
	## ie 'Jim Brooks'
	
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

	
