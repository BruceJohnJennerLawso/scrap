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


seasons = []
##seasons += getAllSeasons('watMu', 'beginner') + getAllSeasons('watMu', 'intermediate') + getAllSeasons('watMu', 'advanced') + getAllSeasons('watMu', 'allstar')		
##seasons += getAllSeasons('wha', 'everything')
seasons += getAllSeasons('nhl', 'postLockout')

params = scrapParams('nhl', 'everything')

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
