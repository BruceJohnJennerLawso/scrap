## readata.py ##################################################################
## lets try loading the data from file again ###################################
## and make sure everything is there and comprehensible ########################
################################################################################

import matplotlib
matplotlib.use('Agg')
## begone ye horrible display environment errors

from sys import argv
import time
import sys
from outputs import *
import multiprocessing as mp

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
	getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Goal Differential Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAQualAboveDiff, 'MaAQualAboveDiff', 'Mean Adjusted Average Goal Differential Offence Quality Index above Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	
	 
	
	graphTeamsAgainstDeltas(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffSuccessRating, 'playoffSuccess', 'Playoff Success', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Goal Differential Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAQualAboveDiff, 'MaAQualAboveDiff', 'Mean Adjusted Average Goal Differential Offence Quality Index above Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	

	return 0

def graphPlayoffOffenceRelations(seasons, leagueId, levelId):
	graphTeams(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffGoalsForAverage, 'playoffOffence', 'Playoff Goals For Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Goal Differential Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAQualAboveDiff, 'MaAQualAboveDiff', 'Mean Adjusted Average Goal Differential Offence Quality Index above Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	
	 
	
	graphTeamsAgainstDeltas(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffGoalsForAverage, 'playoffOffence', 'Playoff Goals For Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Goal Differential Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAQualAboveDiff, 'MaAQualAboveDiff', 'Mean Adjusted Average Goal Differential Offence Quality Index above Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	

	return 0

def graphPlayoffDefenceRelations(seasons, leagueId, levelId):
	graphTeams(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffDefence', 'Playoff Goals Against Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Goal Differential Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAQualAboveDiff, 'MaAQualAboveDiff', 'Mean Adjusted Average Goal Differential Offence Quality Index above Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	
	 
	
	graphTeamsAgainstDeltas(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffDefence', 'Playoff Goals Against Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Goal Differential Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAQualAboveDiff, 'MaAQualAboveDiff', 'Mean Adjusted Average Goal Differential Offence Quality Index above Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	

	return 0

def graphPlayoffGoalDifferentialRelations(seasons, leagueId, levelId):
	graphTeams(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffAverageGoalDifferential, 'playoffAvgPlusMinus', 'Playoff Average Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Goal Differential Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAQualAboveDiff, 'MaAQualAboveDiff', 'Mean Adjusted Average Goal Differential Offence Quality Index above Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	
	 
	
	graphTeamsAgainstDeltas(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffAverageGoalDifferential, 'playoffAvgPlusMinus', 'Playoff Average Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Goal Differential Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAQualAboveDiff, 'MaAQualAboveDiff', 'Mean Adjusted Average Goal Differential Offence Quality Index above Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	

	return 0

def plotHistograms(seasons, leagueId, levelId):
	
	graphTeamsHistogram(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffSuccessRating, 'playoffSuccess', 'Playoff Success', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffAverageGoalDifferential, 'playoffAvgPlusMinus', 'Playoff Average Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffOffence', 'Playoff Goals For Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffDefence', 'Playoff Goals Against Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Goal Differential Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAQualAboveDiff, 'MaAQualAboveDiff', 'Mean Adjusted Average Goal Differential Offence Quality Index above Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	

	graphTeamsHistogram(leagueId, levelId, False,\
	getStatContainer(Team.getPlayoffAverageGoalDifferential, 'playoffAvgPlusMinus', 'Playoff Average Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffSuccessRating, 'playoffSuccess', 'Playoff Success', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffOffence', 'Playoff Goals For Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffDefence', 'Playoff Goals Against Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Goal Differential Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAQualAboveDiff, 'MaAQualAboveDiff', 'Mean Adjusted Average Goal Differential Offence Quality Index above Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	
	
	return 0

def plotHeatmap(seasons, leagueId, levelId):
	plotVariablesHeatmap(leagueId, levelId, True,\
	getStatContainer(Team.getPlayoffAverageGoalDifferential, 'playoffAvgPlusMinus', 'Playoff Average Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffSuccessRating, 'playoffSuccess', 'Playoff Success', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsForAverage, 'playoffOffence', 'Playoff Goals For Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'playoffDefence', 'Playoff Goals Against Average', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Average Goals For Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Average Goals Against Per Game', seasons, leagueId, levelId),\
	getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Goal Differential Offence Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAQualAboveDiff, 'MaAQualAboveDiff', 'Mean Adjusted Average Goal Differential Offence Quality Index above Goal Differential', seasons, leagueId, levelId),\
	getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential (+/-)', seasons, leagueId, levelId),\
	getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId),\
	getStatContainer(Team.getPointsPercentage, 'PtsPct', 'Points Percentage', seasons, leagueId, levelId))				 	

	return 0


if(__name__ == "__main__"):
	
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	
	num_cores = int(mp.cpu_count()*0.25)
	
	print "Running readata with argv ", argv, '\non %i cores, %i available' % (mp.cpu_count(), num_cores)
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	
	
	
	
	p1 = mp.Process(target = graphPlayoffSuccessRelations, args=(seasons, leagueId, levelId), name = "Playoff Success")
	p2 = mp.Process(target = graphPlayoffOffenceRelations, args=(seasons, leagueId, levelId), name = "Playoff Offence")
	p3 = mp.Process(target = graphPlayoffDefenceRelations, args=(seasons, leagueId, levelId), name = "Playoff Defence")
	p4 = mp.Process(target = graphPlayoffGoalDifferentialRelations, args=(seasons, leagueId, levelId), name = "Playoff Goal Differential")
	p5 = mp.Process(target = plotHistograms, args=(seasons, leagueId, levelId), name = "Histograms")
	p6 = mp.Process(target = plotHeatmap, args=(seasons, leagueId, levelId), name = "Heatmap")		

	procs = [p6, p2, p3, p4, p5, p1]
	activeProcs = []
	
	while(True):
		time.sleep(1)
		
		runningProcesses = 0
		for p in activeProcs:
			if((p.exitcode != 0)and(p.is_alive())):
				runningProcesses += 1

		finishedProcesses = 0
		for p in procs:
			if(p.exitcode == 0):
				finishedProcesses += 1
		if(finishedProcesses == len(procs)):
			print "Finished all processes for readata.py, %s, %s" % (leagueId, levelId)
			break
		
		print "%i running processes, %i finished %i cores available\n" % (runningProcesses, finishedProcesses, num_cores)
		print "Total Process List\n", [[p.name, p.exitcode, p.is_alive(), p.pid] for p in procs], '\n'
		print "Active Process List\n", [[p.name, p.exitcode, p.is_alive(), p.pid] for p in activeProcs], '\n\n'
		sys.stdout.write("\x1b[2J\x1b[H");
		if(runningProcesses < num_cores):
			for p in procs:
				if p not in activeProcs:
					activeProcs.append(p)
					p.start()
					break









