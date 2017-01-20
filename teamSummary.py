## teamSummary.py ##############################################################
## give a team name and summarize data about it, and its #######################
## players #####################################################################
################################################################################

from sys import argv
from scrapParam import *

def moduleId():
	return "teamSummary"

def description():
	output = "The teamSummary module is used to print the team description string\n"
	output += "to console for the spread of teams defined. The most common uses are\n"
	output += "to display the team description for all teams in a given season, or to\n"
	output += "display a teams description string over multiple seasons\n"
	return output

def exampleCommand():
	output = "python teamSummary.py nhl everything\n"
	output += "python teamSummary.py nhl 2016\n"
	output += "python teamSummary.py nhl originalSix 'Montreal Canadiens' 'Toronto Maple Leafs'\n"
	return output
	
	
def task(seasons, parameters):

	print parameters.getOutputType()

	seasons = filterSeasonsByParams(seasons, parameters)

	for season in seasons:
		if(parameters.getTeamNames() == []):	
			
			title = season.seasonId
			if(season.getLeagueId() == "watMu"):
				title += ", " + season.levelId
			printTitleBox(title)
			for team in season.Teams:
				print team.getDescriptionString(), "\n"
		
		elif(parameters.getTeamNames() != []):
			for teamName in parameters.getTeamNames():
				for team in season.Teams:
					if(team.getTeamName() == teamName):
						print team.getDescriptionString(), "\n"			
						
						if(parameters.getOutputType() == "detailed"):
							i = 1
							print team.getSeasonGames()
							for gm in team.getSeasonGames():
								##print "game no %i," % i, gm.Layers[0], "\nOQI %.3f, DQI %.3f, DiffQI %.3f, True Diff %.3f, DiffQualOverDiff %.3f" % (gm.offenceQualityIndex, gm.defenceQualityIndex, gm.diffQualityIndex, gm.getGoalDifferential(), gm.getDiffQualMargin())
								print gm.getGameDescription()
								print gm.getGameResult()
								i += 1
						

if(__name__ == "__main__"):
	
	try:	
		leagueId = argv[1]
		## ie 'watMu'
		levelId = argv[2]
		## ie 'beginner'
		teamNames = []
		if(len(argv) > 3):
			teamNames = argv[3:len(argv)]
	
	except IndexError:
		print "Arguments %s failing due to index error, see example commands for %s:\n" % (tuple(argv[1:]), argv[0])		
		print exampleCommand()
		exit()
	
	
	parameters = scrapParams(leagueId, levelId, False, teamNames)
	seasons = getAllSeasons(leagueId, levelId)
	task(seasons, parameters)
