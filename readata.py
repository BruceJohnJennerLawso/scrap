## readata.py ##################################################################
## lets try loading the data from file again ###################################
## and make sure everything is there and comprehensible ########################
################################################################################

from sys import argv
from outputs import *

## I cant remember exactly what this was needed for, its some very specific
## aspect of graphing with matplotlib or something

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

	exit()
	
	
	
	plotAllTeams(seasons, leagueId, levelId)
	plotAllTopPlayoffTeams(seasons, leagueId, levelId)
	plotAllTopPlayoffTeamsDeltas(seasons, leagueId, levelId)	
	plotAllTopPlayoffTeamsVariables(seasons, leagueId, levelId)
	
	
	graphTeams(leagueId, levelId, True, getPlayoffSuccessStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId), getPlusMinusStatContainer(seasons, leagueId, levelId), getPointsPercentageStatContainer(seasons, leagueId, levelId))
	graphTeamsAgainstDeltas(leagueId, levelId, True, getPlayoffSuccessStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId), getPlusMinusStatContainer(seasons, leagueId, levelId), getPointsPercentageStatContainer(seasons, leagueId, levelId))	
	
	graphTeams(leagueId, levelId, True, getPlayoffOffenceStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId), getPlusMinusStatContainer(seasons, leagueId, levelId), getPointsPercentageStatContainer(seasons, leagueId, levelId))
	graphTeamsAgainstDeltas(leagueId, levelId, True, getPlayoffOffenceStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId), getPlusMinusStatContainer(seasons, leagueId, levelId), getPointsPercentageStatContainer(seasons, leagueId, levelId))	
	
	graphTeams(leagueId, levelId, True, getPlayoffDefenceStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId), getPlusMinusStatContainer(seasons, leagueId, levelId), getPointsPercentageStatContainer(seasons, leagueId, levelId))
	graphTeamsAgainstDeltas(leagueId, levelId, True, getPlayoffDefenceStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId), getPlusMinusStatContainer(seasons, leagueId, levelId), getPointsPercentageStatContainer(seasons, leagueId, levelId))			
	
	
	graphTeamsHistogram(leagueId, levelId, True, getPlayoffSuccessStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId), getPlusMinusStatContainer(seasons, leagueId, levelId), getPointsPercentageStatContainer(seasons, leagueId, levelId))
	graphTeamsHistogram(leagueId, levelId, False, getPlayoffSuccessStatContainer(seasons, leagueId, levelId), getPlayoffOffenceStatContainer(seasons, leagueId, levelId), getPlayoffDefenceStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId), getPlusMinusStatContainer(seasons, leagueId, levelId), getPointsPercentageStatContainer(seasons, leagueId, levelId))
	
	plotVariablesHeatmap(leagueId, levelId, True, getPlayoffSuccessStatContainer(seasons, leagueId, levelId), getPlayoffOffenceStatContainer(seasons, leagueId, levelId), getPlayoffDefenceStatContainer(seasons, leagueId, levelId), getOffenceStatContainer(seasons, leagueId, levelId), getDefenceStatContainer(seasons, leagueId, levelId), getAgciStatContainer(seasons, leagueId, levelId), getMaADQIStatContainer(seasons, leagueId, levelId), getMaAOQIStatContainer(seasons, leagueId, levelId), getMawqueeStatContainer(seasons, leagueId, levelId), getPlusMinusStatContainer(seasons, leagueId, levelId), getPointsPercentageStatContainer(seasons, leagueId, levelId))
	

