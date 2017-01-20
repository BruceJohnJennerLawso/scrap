## teamSummary.py ##############################################################
## give a team name and summarize data about it, and its #######################
## players #####################################################################
################################################################################

from sys import argv
from scrapParam import *

def moduleId():
	return "teamSummary"

def task(seasons, parameters):

	print parameters.getOutputType()

	for season in seasons:
		if(parameters.getTeamNames() == []):	
			
			title = season.seasonId
			if(season.getLeagueId() == "watMu"):
				title += ", " + season.levelId
			printTitleBox(title)
			for team in season.Teams:
				print team.getDescriptionString(), "\n"
		
		elif(parameters.getTeamNames() != []):
			for teamName in teamNames:
				for team in season.Teams:
					if(team.getTeamName() == teamName):
						print team.getDescriptionString(), "\n"			
						
						##if(parameters.getOutputType() == "detailed"):
						if(False):							
							i = 1
							print team.getSeasonGames()
							for gm in team.getSeasonGames():
								##print "game no %i," % i, gm.Layers[0], "\nOQI %.3f, DQI %.3f, DiffQI %.3f, True Diff %.3f, DiffQualOverDiff %.3f" % (gm.offenceQualityIndex, gm.defenceQualityIndex, gm.diffQualityIndex, gm.getGoalDifferential(), gm.getDiffQualMargin())
								print gm.getGameDescription()
								print gm.getGameResult()
								i += 1
						

if(__name__ == "__main__"):
		
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	
	
	teamNames = []
	if(len(argv) > 3):
		teamNames = argv[3:len(argv)]
	
	parameters = scrapParams(leagueId, levelId, False, teamNames)
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	franchises = False

	seasonIndexList = getSeasonIndexList(leagueId)
	
	task(seasons, parameters)
