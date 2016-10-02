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
	return output


if(__name__ == "__main__"):
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	sortOrder = argv[3]
	if(sortOrder not in ['asc', 'desc']):
		print "Bad sort order argument %s supplied, must be either asc or desc" % sortOrder
	
	targetStatName = argv[4]
	
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	franchises = False

	seasonIndexList = getSeasonIndexList(leagueId)

	stat = getTargetStatContainer(targetStatName, seasons, leagueId, levelId)
	if(sortOrder == 'asc'):
		stat.printSortedContainer()
	elif(sortOrder == 'desc'):
		stat.printReverseSortedContainer()
