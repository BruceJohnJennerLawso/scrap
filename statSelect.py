## statSelect.py ###############################################################
## unified pipe that takes text input and responds with the ####################
## appropriate stat container object ###########################################
################################################################################


from team import *




def getTeamStatLongName(targetStatName):
	if(targetStatName == "PlusMinus"):
		return 'Season Goal Differential'
	elif(targetStatName == "Wins"):
		return 'Season Wins'		
	elif(targetStatName == "GDA"):
		return 'Season Goal Differential Average'
	elif(targetStatName == "AOQI"):
		return 'Average Offence Quality Index'
	elif(targetStatName == "ADQI"):
		return 'Average Defence Quality Index'	
	elif(targetStatName == "AGCI"):
		return 'Average Game Closeness Index'	
	elif(targetStatName == "OQI"):
		return 'Offence Quality Index'	
	elif(targetStatName == "DQI"):
		return 'Defence Quality Index'			
	elif(targetStatName == "MaAWQI"):
		return 'Mean Adjusted Average Win Quality Index'			
	elif(targetStatName == "MaAPQI"):
		return 'Mean Adjusted Average Play Quality Index'			
	elif(targetStatName == "Points"):
		return 'Season Points Total'				
	elif(targetStatName == "Offence"):
		return 'Season Goals For Average'				
	elif(targetStatName == "Defence"):
		return 'Season Goals Against Average'				
	elif(targetStatName == "CPQI"):
		return 'Complete Play Quality Index'						
	elif(targetStatName == "ODQSplit"):
		return 'OffenceDefence Quality Split'			
	elif(targetStatName == "DQM"):
		return 'DiffQualityMargin'	
	elif(targetStatName == "FBS"):
		return 'CPQI FrontBack Split'	
	elif(targetStatName == "SGP"):
		return 'Total Season Games Played'			
	## playoff stats start here
	elif(targetStatName == "PlayoffOffence"):
		return 'PlayoffOffence'	
	elif(targetStatName == "PlayoffDefence"):
		return 'PlayoffDefence'
	elif(targetStatName == "PlayoffSuccess"):
		return 'PlayoffSuccess'	
	elif(targetStatName == "POT"):
		return 'Playoffs Offence Transition'						
	elif(targetStatName == "PDT"):
		return 'Playoffs Defence Transition'	
	elif(targetStatName == "PGDT"):
		return 'Playoffs Goal Differential Transition'			
	else:
		return targetStatName




def getTeamStatInformation(targetStatName):
	if(targetStatName == "PlusMinus"):
		return (Team.getSeasonPlusMinus, targetStatName, getTeamStatLongName(targetStatName))
	elif(targetStatName == "Wins"):
		return (Team.getSeasonWinsTotal, targetStatName, getTeamStatLongName(targetStatName))		
	elif(targetStatName == "GDA"):
		return (Team.getSeasonGoalDifferentialAverage, targetStatName, getTeamStatLongName(targetStatName))
	elif(targetStatName == "AOQI"):
		return (Team.getAOQI, targetStatName, getTeamStatLongName(targetStatName))
	elif(targetStatName == "ADQI"):
		return (Team.getADQI, targetStatName, getTeamStatLongName(targetStatName))	
	elif(targetStatName == "AGCI"):
		return (Team.getAGCI, targetStatName, getTeamStatLongName(targetStatName))	
	elif(targetStatName == "OQI"):
		return (Team.getOffenceQualityIndex, targetStatName, getTeamStatLongName(targetStatName))	
	elif(targetStatName == "DQI"):
		return (Team.getDefenceQualityIndex, targetStatName, getTeamStatLongName(targetStatName))			
	elif(targetStatName == "MaAWQI"):
		return (Team.getMaAWQI, targetStatName, getTeamStatLongName(targetStatName))			
	elif(targetStatName == "MaAPQI"):
		return (Team.getMaAPQI, targetStatName, getTeamStatLongName(targetStatName))			
	elif(targetStatName == "Points"):
		return (Team.getSeasonPointsTotal, targetStatName, getTeamStatLongName(targetStatName))				
	elif(targetStatName == "Offence"):
		return (Team.getSeasonGoalsForAverage, targetStatName, getTeamStatLongName(targetStatName))				
	elif(targetStatName == "Defence"):
		return (Team.getSeasonGoalsAgainstAverage, targetStatName, getTeamStatLongName(targetStatName))				
	elif(targetStatName == "CPQI"):
		return (Team.getCPQI, targetStatName, getTeamStatLongName(targetStatName))						
	elif(targetStatName == "ODQSplit"):
		return (Team.getODQSplit, targetStatName, getTeamStatLongName(targetStatName))			
	elif(targetStatName == "DQM"):
		return (Team.getDQM, targetStatName, getTeamStatLongName(targetStatName))	
	elif(targetStatName == "FBS"):
		return (Team.getFrontBackSplit, targetStatName, getTeamStatLongName(targetStatName))	
	elif(targetStatName == "SGP"):
		return (Team.getSeasonGamesTotal, targetStatName, getTeamStatLongName(targetStatName))
	## playoff stats start here
	elif(targetStatName == "PlayoffOffence"):
		return (Team.getPlayoffGoalsForAverage, targetStatName, getTeamStatLongName(targetStatName))	
	elif(targetStatName == "PlayoffDefence"):
		return (Team.getPlayoffGoalsAgainstAverage, targetStatName, getTeamStatLongName(targetStatName))
	elif(targetStatName == "PlayoffSuccess"):
		return (Team.getPlayoffSuccessRating, targetStatName, getTeamStatLongName(targetStatName))	
	elif(targetStatName == "POT"):
		return (Team.getPlayoffOffenceTransition, targetStatName, getTeamStatLongName(targetStatName))						
	elif(targetStatName == "PDT"):
		return (Team.getPlayoffDefenceTransition, targetStatName, getTeamStatLongName(targetStatName))	
	elif(targetStatName == "PGDT"):
		return (Team.getPlayoffGoalDifferentialTransition, targetStatName, getTeamStatLongName(targetStatName))			
	else:
		raise TypeError("Unable to find stat type for name %s" % targetStatName)






def getTeamSeasonStatNames():
	seasonStats = ["PlusMinus", "Wins", "AOQI", "ADQI", "AGCI", "OQI", "DQI", "MaAWQI",\
	"MaAPQI", "Points", "Offence", "Defence", "DQM", "CPQI", "ODQSplit",\
	"FBS", "GDA", "SGP"]
	return seasonStats

def getTeamPlayoffStatNames():
	playoffStats = ["POT", "PDT", "PGDT", "PlayoffOffence", "PlayoffDefence", "PlayoffSuccess"]	
	return playoffStats

def getTeamStatNames():
	return getTeamSeasonStatNames()+getTeamPlayoffStatNames()



