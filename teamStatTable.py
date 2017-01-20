## teamStatTable.py ############################################################
## Get a simple list with the year and the value of a ##########################
## given stat for that year in the terminal ####################################
################################################################################


from sys import argv
from scrapParam import *


def moduleId():
	return "teamStatTable"

def description():
	output = "The teamStatTable module is used to print a list of the team stat values\n"
	output += "for a given stat to the console along with the year in a form that is\n"
	output += "convenient for copying to a csv file\n"
	return output

def exampleCommand():
	output = "python teamStatTable.py nhl everything 'Montreal Canadiens' 'Boston Bruins'\n"
	return output

def task(seasons, parameters):
	for season in seasons:
		for team in season.Teams:
			if(team.getTeamName() in parameters.getTeamNames()):
				print "%i,%s,%.3f" % (int(season.seasonId), team.getTeamId(),team.getCPQI())

if(__name__ == "__main__"):
	try:
		leagueId = argv[1]
		## ie 'watMu'
		levelId = argv[2]
		## ie 'beginner'
		teamNames = argv[3:]
	except IndexError:
		print exampleCommand()
		exit()
	seasons = getAllSeasons(leagueId, levelId)

	parameters = scrapParams(leagueId, levelId, False, teamNames, [])
	task(seasons, parameters)
