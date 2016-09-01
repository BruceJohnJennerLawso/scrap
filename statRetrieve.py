## statRetrieve.py #############################################################
## moving functions that collect a list of stats from an input #################
## of teams, seasons, etc. #####################################################
################################################################################


from statContainer import *


def getMawquees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaAWQI())
	return output

def getMapquees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaAPQI())
	return output

def getMaoquees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaAOQI())
	return output

def getMadquees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaADQI())
	return output

def getOffences(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getSeasonGoalsForAverage())
	return output

def getDefences(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getSeasonGoalsAgainstAverage())
	return output

def getAgcees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getAGCI())
	return output

def getAgcees(seasons):
	output = []
	for season in seasons:
		for team in season.Teams:
			output.append(team.getAGCI())
	return output


def demoStatContainer(seasons, leagueId, levelId):
	mawquees = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			mawquees.append(team.getMaAWQI())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('MaAWQI', 'Mean Adjusted Average Win Quality Index', mawquees, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	
	
def getStatContainer(statCall, seasons, leagueId, levelId):
	print statCall
	
	statValues = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			statValues.append(team.statCall)
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer(statValues, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 	
	
	
def getMawqueeStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaAWQI())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('MaAWQI', 'Mean Adjusted Average Win Quality Index',output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container
	
	
def getMapqueeStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaAPQI())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('MaAPQI', 'Mean Adjusted Average Play Quality Index',output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container	

def getMapqueeStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaAPQI())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('MaAPQI', 'Mean Adjusted Average Play Quality Index',output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container	
	
def getOffenceStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getSeasonGoalsForAverage())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('AGF', 'Average Goals For',output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container	
	
def getDefenceStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getSeasonGoalsAgainstAverage())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('GAA', 'Goals Against Average',output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container	
	
def getPlusMinusStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getSeasonPlusMinus())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('+/-', 'Goal Differential (+/-)',output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container		
	
def getPointsPercentageStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getPointsPercentage())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('Pts Pct', 'Points Percentage',output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container	
	
def getWinsStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getSeasonWinsTotal())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('Wins', 'Wins',output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container					
		
		
def getLossesStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getSeasonLossTotal())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('Losses', 'Losses',output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container	
	
def getMaADQIStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaADQI())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('MaADQI', 'Mean Adjusted Defence Quality Index',output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container		

def getMaAOQIStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getMaAOQI())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('MaAOQI', 'Mean Adjusted Offence Quality Index',output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container	
	
	
def getAgciStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getAGCI())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('AGCI', 'Average Game Closeness Index', output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container				


def getPlayoffSuccessStatContainer(seasons, leagueId, levelId):
	output = []
	teamIds = []
	teamNames = []
	years = []
	madePlayoffs = []

	for season in seasons:
		for team in season.Teams:
			output.append(team.getPlayoffSuccessRating())
			teamIds.append(team.getTeamId())
			teamNames.append(team.getTeamName())
			years.append(team.seasonId)
			madePlayoffs.append(team.madeRealPlayoffs())
	container = statContainer('playoffSuccess', 'Playoff Success', output, teamIds, teamNames, years, madePlayoffs)
	container.printContainer() 
	return container				

