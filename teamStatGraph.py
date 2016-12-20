## teamStatGraph.py ############################################################
## create a graph of two parameters specified and save it to the results #######
## folder ######################################################################
################################################################################


from sys import argv
from outputs import *


def getTargetStatContainer(targetStatName, seasons, leagueId, levelId):
	if(targetStatName == "PlusMinus"):
		output = getStatContainer(Team.getSeasonGoalDifferentialAverage, 'PlusMinus', 'Season Goal Differential', seasons, leagueId, levelId)
	elif(targetStatName == "MaADiffQI"):
		output = getStatContainer(Team.getMaADiffQI, 'MaADiffQI', 'Mean Adjusted Average Diff Quality Index', seasons, leagueId, levelId)
	elif(targetStatName == "MaAOQI"):
		output = getStatContainer(Team.getMaAOQI, 'MaAOQI', 'Mean Adjusted Average Offence Quality Index', seasons, leagueId, levelId)
	elif(targetStatName == "MaADQI"):
		output = getStatContainer(Team.getMaADQI, 'MaADQI', 'Mean Adjusted Average Defence Quality Index', seasons, leagueId, levelId)	
	elif(targetStatName == "AGCI"):
		output = getStatContainer(Team.getAGCI, 'AGCI', 'Average Game Closeness Index', seasons, leagueId, levelId)	
	elif(targetStatName == "OQI"):
		output = getStatContainer(Team.getOffenceQualityIndex, 'OQI', 'Offence Quality Index', seasons, leagueId, levelId)	
	elif(targetStatName == "DQI"):
		output = getStatContainer(Team.getDefenceQualityIndex, 'DQI', 'Defence Quality Index', seasons, leagueId, levelId)			
	elif(targetStatName == "MaAWQI"):
		output = getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, leagueId, levelId)			
	elif(targetStatName == "MaAPQI"):
		output = getStatContainer(Team.getMaAPQI, 'MaAPQI', 'Mean Adjusted Average Play Quality Index', seasons, leagueId, levelId)			
	elif(targetStatName == "Points"):
		output = getStatContainer(Team.getSeasonPointsTotal, 'Points', 'Season Points Total', seasons, leagueId, levelId)				
	elif(targetStatName == "Offence"):
		output = getStatContainer(Team.getSeasonGoalsForAverage, 'Offence', 'Season Goals For Average', seasons, leagueId, levelId)				
	elif(targetStatName == "Defence"):
		output = getStatContainer(Team.getSeasonGoalsAgainstAverage, 'Defence', 'Season Goals Against Average', seasons, leagueId, levelId)				
	elif(targetStatName == "SQI"):
		output = getStatContainer(Team.getSQI, 'SQI', 'Situation Quality Index', seasons, leagueId, levelId)	
	elif(targetStatName == "CPQI"):
		output = getStatContainer(Team.getCPQI, 'CPQI', 'Complete Play Quality Index', seasons, leagueId, levelId)						
	elif(targetStatName == "POT"):
		output = getStatContainer(Team.getPlayoffOffenceTransition, 'POT', 'Playoffs Offence Transition', seasons, leagueId, levelId)						
	elif(targetStatName == "PDT"):
		output = getStatContainer(Team.getPlayoffDefenceTransition, 'PDT', 'Playoffs Defence Transition', seasons, leagueId, levelId)	
	elif(targetStatName == "PGDT"):
		output = getStatContainer(Team.getPlayoffGoalDifferentialTransition, 'PGDT', 'Playoffs Goal Differential Transition', seasons, leagueId, levelId)	
	elif(targetStatName == "ODQSplit"):
		output = getStatContainer(Team.getODQSplit, 'ODQSplit', 'OffenceDefence Quality Split', seasons, leagueId, levelId)			
	elif(targetStatName == "DQM"):
		output = getStatContainer(Team.getDQM, 'DiffQualityMargin', 'DiffQualityMargin', seasons, leagueId, levelId)	
	elif(targetStatName == "FBS"):
		output = getStatContainer(Team.getFrontBackSplit, 'CPQI FrontBack Split', 'CPQI FrontBack Split', seasons, leagueId, levelId)	
	elif(targetStatName == "PlayoffOffence"):
		output = getStatContainer(Team.getPlayoffGoalsForAverage, 'PlayoffOffence', 'PlayoffOffence', seasons, leagueId, levelId)	
	elif(targetStatName == "PlayoffDefence"):
		output = getStatContainer(Team.getPlayoffGoalsAgainstAverage, 'PlayoffDefence', 'PlayoffDefence', seasons, leagueId, levelId)
	elif(targetStatName == "PlayoffSuccess"):
		output = getStatContainer(Team.getPlayoffSuccessRating, 'PlayoffSuccess', 'PlayoffSuccess', seasons, leagueId, levelId)							
	else:
		print "Stat name %s not found, available options are:\n\n" % targetStatName
		print ["PlusMinus", "MaADiffQI", "MaAOQI", "MaADQI", "AGCI", "OQI", "DQI", "MaAWQI", "MaAPQI", "Points", "Offence", "Defence", "SQI", "CPQI", "POT", "PDT", "PGDT"]
		exit
	return output


if(__name__ == "__main__"):
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	independentStat = argv[4]
	
	dependentStat = argv[5]
	
	playoffTeamsOnly = argv[3]
	if(playoffTeamsOnly == "True"):
		playoffTeamsOnly = True
	elif(playoffTeamsOnly == "False"):
		playoffTeamsOnly = False
	else:
		print "Unable to parse option 'playoffTeamsOnly' as %s" % playoffTeamsOnly
	
	if(playoffTeamsOnly):
		thing = 'PlayoffTeam'
	else:
		thing = 'Total'
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	franchises = False

	seasonIndexList = getSeasonIndexList(leagueId)

	##for season in seasons:
	##	for team in season.Teams:
	##		if(team.getTeamName() == teamName):
	##			print "%i,%.3f" % (int(season.seasonId),team.getCPQI())

	independent = getTargetStatContainer(independentStat, seasons, leagueId, levelId)
	dependent = getTargetStatContainer(dependentStat, seasons, leagueId, levelId)
	for var in [independent, dependent]:
		plotHistogram(var.getShortStatName(), 'Count', 'Histogram of %s' % var.getLongStatName(), var.getStat(playoffTeamsOnly),'./results/%s/%s/histograms' % (leagueId, levelId), '%s' % var.getShortStatName(), '%s_%s_histogram.png' % (var.getShortStatName(), thing))			
	plotScatterplot(independent.getShortStatName(), dependent.getShortStatName(), '%s\nby %s\nfor %s, %s' % (dependent.getLongStatName(), independent.getLongStatName(), leagueId, levelId), independent.getStat(playoffTeamsOnly), dependent.getStat(playoffTeamsOnly), './results/%s/%s/%sBy' % (leagueId, levelId, dependent.getShortStatName()), '%s' % independent.getShortStatName(), '%s_by_%s.png' % (dependent.getShortStatName(), independent.getShortStatName()))		
