## playerSummary.py ############################################################
## show a players career summary ###############################################
################################################################################

from sys import argv
from scrapParam import *

from collections import Counter

def moduleId():
	return "playerSummary"

def description():
	output = "The playerSummary module is used to print the team description string\n"
	output += "to console for every team that the player provided can be found on the\n"
	output += "roster, along with an average of the players teams stats over his/her\n"
	output += "career\n"
	return output

def exampleCommand():
	output = "python playerSummary.py pro 'Jacques Plante'\n"
	output += "python playerSummary.py watMu 'Evan Brotherston'"
	return output

def task(seasons, parameters):
	
	##seasons = filterSeasonsByParams(seasons, parameters)
	## NOT going to filter here, because we want complete data about a player
	for playerName in parameters.getPlayerNames():
		if(parameters.getLeagueId() == 'watMu'):
			playah = watMuPlayer(playerName, seasons)
		else:
			playah = nhlPlayer(playerName, seasons)		
	
		print playah.getStatsLine(), '\n\n'
	
		for team in reversed(playah.playedFor):
			print team.getDescriptionString(), '\n'

if(__name__ == "__main__"):
	
	
	try:	
		leagueId = argv[1]
		## ie 'watMu'
	
		playerName = argv[2]
		## ie 'Jim Brooks'
	except IndexError:
		print "Arguments %s failing due to index error, see example commands for %s:\n" % (tuple(argv[1:]), argv[0])		
		print exampleCommand()
		exit()
	
	
	if(leagueId == 'watMu'):
		seasons = getAllSeasons(leagueId, 'beginner') + getAllSeasons(leagueId, 'intermediate') + getAllSeasons(leagueId, 'advanced') + getAllSeasons(leagueId, 'allstar')		
	elif(leagueId == 'all'):
		seasons = getAllSeasons(leagueId, 'beginner') + getAllSeasons(leagueId, 'intermediate') + getAllSeasons(leagueId, 'advanced') + getAllSeasons(leagueId, 'allstar') +getAllSeasons('wha', 'everything') + getAllSeasons('nhl', 'everything')			
		## uber experimental, cannot reccomend trying this just yet
	else:
		##seasons = getAllSeasons(leagueId, 'everything')
		seasons = getAllSeasons('wha', 'everything') + getAllSeasons('nhl', 'everything')
	
	parameters = scrapParams(leagueId, 'everything', False, [], [playerName])
	task(seasons, parameters)
	
