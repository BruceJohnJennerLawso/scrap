## readata.py ##################################################################
## lets try loading the data from file again ###################################
## and make sure everything is there and comprehensible ########################
################################################################################

from sys import argv
from outputs import *
from multiprocessing import Process

## I cant remember exactly what this was needed for, its some very specific
## aspect of graphing with matplotlib or something


def graphPlayoffSuccessRelations(seasons, leagueId, levelId):
	graphTeams(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffSuccessRating, 'playoffSuccess', 'Playoff Success', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	
	 
	
	graphTeamsAgainstDeltas(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffSuccessRating, 'playoffSuccess', 'Playoff Success', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	


def graphPlayoffOffenceRelations(seasons, leagueId, levelId):
	graphTeams(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffGoalsForAverage, 'playoffOffence', 'Playoff Goals For Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	
	 
	
	graphTeamsAgainstDeltas(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffGoalsForAverage, 'playoffOffence', 'Playoff Goals For Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	


def graphPlayoffDefenceRelations(seasons, leagueId, levelId):
	graphTeams(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffDefence', 'Playoff Goals Against Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	
	 
	
	graphTeamsAgainstDeltas(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffDefence', 'Playoff Goals Against Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	

	


if(__name__ == "__main__"):
	
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	
	print "Running readata with argv ", argv, '\n'
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	
	
	p1 = Process(target = graphPlayoffSuccessRelations, args=(seasons, leagueId, levelId))
	##p1.start()
	p2 = Process(target = graphPlayoffOffenceRelations, args=(seasons, leagueId, levelId))
	##p2.start()
	p3 = Process(target = graphPlayoffDefenceRelations, args=(seasons, leagueId, levelId))
	##p3.start()    	
	
	##graphPlayoffSuccessRelations(seasons, leagueId, levelId)
	##graphPlayoffOffenceRelations(seasons, leagueId, levelId)
	##graphPlayoffDefenceRelations(seasons, leagueId, levelId)












	graphTeamsHistogram(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffSuccessRating, 'playoffSuccess', 'Playoff Success', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffOffence', 'Playoff Goals For Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffDefence', 'Playoff Goals Against Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	

	graphTeamsHistogram(leagueId, levelId, False,\
	getStatContainer(Team.getPlayoffSuccessRating, 'playoffSuccess', 'Playoff Success', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffOffence', 'Playoff Goals For Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffDefence', 'Playoff Goals Against Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	

	plotVariablesHeatmap(leagueId, levelId, False,\
	getStatContainer(Team.getPlayoffSuccessRating, 'playoffSuccess', 'Playoff Success', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsForAverage, 'playoffOffence', 'Playoff Goals For Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffDefence', 'Playoff Goals Against Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	

