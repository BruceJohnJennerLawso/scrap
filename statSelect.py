## statSelect.py ###############################################################
## unified pipe that takes text input and responds with the ####################
## appropriate stat container object ###########################################
################################################################################

from statRetrieve import *
from team import *


def getTeamStatInformation(targetStatName):
	if(targetStatName == "PlusMinus"):
		return (Team.getSeasonPlusMinus, 'PlusMinus', 'Season Goal Differential')
	elif(targetStatName == "Wins"):
		return (Team.getSeasonWinsTotal, 'Wins', 'Season Wins')		
	elif(targetStatName == "GDA"):
		return (Team.getSeasonGoalDifferentialAverage, 'GDA', 'Season Goal Differential Average')
	elif(targetStatName == "AOQI"):
		return (Team.getAOQI, 'AOQI', 'Average Offence Quality Index')
	elif(targetStatName == "ADQI"):
		return (Team.getADQI, 'ADQI', 'Average Defence Quality Index')	
	elif(targetStatName == "AGCI"):
		return (Team.getAGCI, 'AGCI', 'Average Game Closeness Index')	
	elif(targetStatName == "OQI"):
		return (Team.getOffenceQualityIndex, 'OQI', 'Offence Quality Index')	
	elif(targetStatName == "DQI"):
		return (Team.getDefenceQualityIndex, 'DQI', 'Defence Quality Index')			
	elif(targetStatName == "MaAWQI"):
		return (Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index')			
	elif(targetStatName == "MaAPQI"):
		return (Team.getMaAPQI, 'MaAPQI', 'Mean Adjusted Average Play Quality Index')			
	elif(targetStatName == "Points"):
		return (Team.getSeasonPointsTotal, 'Points', 'Season Points Total')				
	elif(targetStatName == "Offence"):
		return (Team.getSeasonGoalsForAverage, 'Offence', 'Season Goals For Average')				
	elif(targetStatName == "Defence"):
		return (Team.getSeasonGoalsAgainstAverage, 'Defence', 'Season Goals Against Average')				
	elif(targetStatName == "CPQI"):
		return (Team.getCPQI, 'CPQI', 'Complete Play Quality Index')						
	elif(targetStatName == "ODQSplit"):
		return (Team.getODQSplit, 'ODQSplit', 'OffenceDefence Quality Split')			
	elif(targetStatName == "DQM"):
		return (Team.getDQM, 'DiffQualityMargin', 'DiffQualityMargin')	
	elif(targetStatName == "FBS"):
		return (Team.getFrontBackSplit, 'CPQI FrontBack Split', 'CPQI FrontBack Split')	
	## playoff stats start here
	elif(targetStatName == "PlayoffOffence"):
		return (Team.getPlayoffGoalsForAverage, 'PlayoffOffence', 'PlayoffOffence')	
	elif(targetStatName == "PlayoffDefence"):
		return (Team.getPlayoffGoalsAgainstAverage, 'PlayoffDefence', 'PlayoffDefence')
	elif(targetStatName == "PlayoffSuccess"):
		return (Team.getPlayoffSuccessRating, 'PlayoffSuccess', 'PlayoffSuccess')	
	elif(targetStatName == "POT"):
		return (Team.getPlayoffOffenceTransition, 'POT', 'Playoffs Offence Transition')						
	elif(targetStatName == "PDT"):
		return (Team.getPlayoffDefenceTransition, 'PDT', 'Playoffs Defence Transition')	
	elif(targetStatName == "PGDT"):
		return (Team.getPlayoffGoalDifferentialTransition, 'PGDT', 'Playoffs Goal Differential Transition')			
	else:
		raise TypeError("Unable to find stat type for name %s" % targetStatName)

def getTeamSeasonStatNames():
	seasonStats = ["PlusMinus", "Wins", "AOQI", "ADQI", "AGCI", "OQI", "DQI", "MaAWQI",\
	"MaAPQI", "Points", "Offence", "Defence", "DQM", "CPQI", "ODQSplit",\
	"FBS", "GDA"]
	return seasonStats

def getTeamPlayoffStatNames():
	playoffStats = ["POT", "PDT", "PGDT", "PlayoffOffence", "PlayoffDefence", "PlayoffSuccess"]	
	return playoffStats

def getTeamStatNames():
	return getTeamSeasonStatNames()+getTeamPlayoffStatNames()

def getTargetStatContainer(targetStatName, seasons, leagueId, levelId):
	
	statNames = getTeamStatNames()
	
	try:
		statCall, shortStatName, longStatName = getTeamStatInformation(targetStatName)
		return getStatContainer(statCall, shortStatName, longStatName, seasons, leagueId, levelId)
	except TypeError:
		print("Dependent: ", targetStatName.rsplit('*')[0], len(targetStatName.rsplit('*')[0]))
		print("Independent: ", targetStatName.rsplit('*')[1], len(targetStatName.rsplit('*')[1]))
		if(("*" in targetStatName) and (len(targetStatName.rsplit('*')) == 2) and (targetStatName.rsplit('*')[0] in statNames) and (targetStatName.rsplit('*')[1] in statNames)):
			## wordy, but its a rather specific requirement
			dependentStatCall, dependentShortStatName, dependentLongStatName = getTeamStatInformation(targetStatName.rsplit('*')[0])
			independentStatCall, independentShortStatName, independentLongStatName = getTeamStatInformation(targetStatName.rsplit('*')[1])
			return getModelDiffContainer(seasons, leagueId, levelId, independentStatCall, independentShortStatName, independentLongStatName, dependentStatCall, dependentShortStatName, dependentLongStatName)
		else:
			print("Stat name %s not found, available options are:\n\n" % targetStatName)
			print(statNames)
			return []

						
	return output

