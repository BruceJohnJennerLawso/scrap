## scrap.py ####################################################################
## the scrap console: imported in the standard python interpreter ##############
################################################################################
from sys import argv
from outputs import *

import team

from distStats import *
from scipy.stats import norm
from scrapParam import *

import statSelect



import teamStatTable
import teamStatGraph
import teamSummary
import readata
import teamStatRanker
import playerData

def getModulesList():
	return [teamStatTable, teamStatGraph, teamSummary, readata, teamStatRanker, playerData]

def printModulesList():
	for module in getModulesList():
		print module.__name__, module
		##print module.moduleId()

def getModuleByName(moduleName):
	for module in getModulesList:
		if(module.__name__ == moduleName):
			return module
	print "Unable to find module named %s, returning empty list instead" % moduleName
	return []
	## intentional crash here

def help():
	## Oh wont you pleaaaaaase pleaaaaaaaaaaase help meeeee
	print "Scrap Version %s" % ("blah")
	
	flatTeams = [individualTeam for yearTeamList in [season.Teams for season in seasons] for individualTeam in yearTeamList]
	
	print "Currently loaded %i seasons for %i teams in %i leagues" % (len(seasons), len(flatTeams), len(set([ssn.getLeagueId() for ssn in seasons])))

if(__name__ == "scrap"):
	printTitleBox("The Scrap Project")
	seasons = []
	##seasons += getAllSeasons('watMu', 'beginner') + getAllSeasons('watMu', 'intermediate') + getAllSeasons('watMu', 'advanced') + getAllSeasons('watMu', 'allstar')		
	##seasons += getAllSeasons('wha', 'everything')
	seasons += getAllSeasons('nhl', 'the2010s')
	
	params = scrapParams('nhl', 'everything')
	clearTerminal()
	printTitleBox("The Scrap Project")
	print "type scrap.help() for information on how to use this module\n"	
	
	
elif(__name__ == "__main__"):
	printTitleBox("The Scrap Project")
	print "The scrap.py module is meant to be run inside of the python"
	print "interpreter, in order to reduce overhead time reloading resources"
	print "with the new seasonParts system\n"
	print "Please run the python interpreter in the directory where scrap is"
	print "located and import scrap to proceed"




def seasonSummary(leagueId, levelId, seasonId):
	for season in seasons:
		##print "Current season: ", season.getLeagueId(), season.getLevelId(), season.getSeasonId()
		##print "Args: ", leagueId, levelId, seasonId
		
		if(season.getLeagueId() == leagueId):
			if(season.getLeagueId() == 'watMu'):
				if(season.getLevelId() != levelId):
					continue
			if(season.getSeasonId() == seasonId):
				print "%s %i teams," % (season.getSeasonId(), season.getTotalNumberOfTeams())
				print "           AWQI, APQI,  AGCI, AOQI,  ADQI, CPQI, Points, Points Pct \nAverages:         %2.2f, %2.2f, %2.2f, %2.2f, %2.2f, %2.2f,  %2.2f, %2.2f\nSigmas:    %2.2f, %2.2f, %2.2f,  %2.2f, %2.2f,  %2.2f,  %2.2f,  %2.2f" % (season.getTeamStatAverage(team.Team.getAWQI), season.getTeamStatAverage(team.Team.getAPQI), season.getTeamStatAverage(team.Team.getAGCI), season.getTeamStatAverage(team.Team.getAOQI), season.getTeamStatAverage(team.Team.getADQI), season.getTeamStatAverage(team.Team.getCPQI), season.getTeamStatAverage(team.Team.getSeasonPointsTotal), season.getTeamStatAverage(team.Team.getPointsPercentage), standardDeviation(season.getTeamStatList(team.Team.getAWQI)), standardDeviation(season.getTeamStatList(team.Team.getAPQI)), standardDeviation(season.getTeamStatList(team.Team.getAGCI)), standardDeviation(season.getTeamStatList(team.Team.getAOQI)), standardDeviation(season.getTeamStatList(team.Team.getADQI)), standardDeviation(season.getTeamStatList(team.Team.getCPQI)), standardDeviation(season.getTeamStatList(team.Team.getSeasonPointsTotal)), standardDeviation(season.getTeamStatList(team.Team.getPointsPercentage)))
				oneSigma = standardDeviation(season.getTeamStatList(team.Team.getCPQI))
		
				oneGoalSigma = 0.987/oneSigma
				prediction = (1.000-norm.cdf(oneGoalSigma))*season.getTotalNumberOfTeams()
				actual = season.getTeamsAboveOneGoalCutoff()
				print "One goal cutoff: %f sigma, above teams predicted, %.3f, actual %i\n"	% (norm.cdf(oneGoalSigma), prediction, actual)			
					
				for seasonTeam in season.Teams:
					print seasonTeam.getDescriptionString(), '\n'
				break
