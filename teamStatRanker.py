## teamStatRanker.py ###########################################################
## Rank all teams in a given sample based on a given stat ######################
################################################################################


from sys import argv
from outputs import *


def getTargetStatContainer(targetStatName, seasons, leagueId, levelId):
	if(targetStatName == "PlusMinus"):
		output = getStatContainer(Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential', seasons, leagueId, levelId)
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
	sortOrder = argv[3]
	if(sortOrder not in ['asc', 'desc']):
		print "Bad sort order argument %s supplied, must be either asc or desc" % sortOrder
	
	playoffTeamsOnly = argv[4]
	if(playoffTeamsOnly == "True"):
		playoffTeamsOnly = True
	elif(playoffTeamsOnly == "False"):
		playoffTeamsOnly = False
	else:
		print "Unable to parse option 'playoffTeamsOnly' as %s" % playoffTeamsOnly	
	
	targetStatName = argv[5]
	
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	franchises = False

	seasonIndexList = getSeasonIndexList(leagueId)

	stat = getTargetStatContainer(targetStatName, seasons, leagueId, levelId)
	if(sortOrder == 'asc'):
		stat.printSortedContainer(playoffTeamsOnly)
	elif(sortOrder == 'desc'):
		stat.printReverseSortedContainer(playoffTeamsOnly)
