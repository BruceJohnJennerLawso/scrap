## seasonSummary.py ############################################################
## summarize average stats for seasons over time ###############################
################################################################################

from sys import argv
from outputs import *
import team
from distStats import *
from scipy.stats import norm
import math

def moduleId():
	return "seasonSummary"

if(__name__ == "__main__"):
		
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	
	
	##teamNames = 0
	##if(len(argv) > 3):
	##	teamNames = argv[3:len(argv)]
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	##franchises = getFranchiseList(leagueId, levelId)
	franchises = False

	seasonIndexList = getSeasonIndexList(leagueId)

	print "################################################################################"
	print "%s#############################################################" % levelId
	print "################################################################################\n"		
	
	predictedTotal = 0
	actualTotal = 0
	for season in seasons:	
		print "%s %i teams," % (season.getSeasonId(), season.getTotalNumberOfTeams())
		print "           AWQI, APQI,  AGCI, AOQI,  ADQI, CPQI, Points, Points Pct \nAverages:         %2.2f, %2.2f, %2.2f, %2.2f, %2.2f, %2.2f,  %2.2f, %2.2f\nSigmas:    %2.2f, %2.2f, %2.2f,  %2.2f, %2.2f,  %2.2f,  %2.2f,  %2.2f" % (season.getTeamStatAverage(team.Team.getAWQI), season.getTeamStatAverage(team.Team.getAPQI), season.getTeamStatAverage(team.Team.getAGCI), season.getTeamStatAverage(team.Team.getAOQI), season.getTeamStatAverage(team.Team.getADQI), season.getTeamStatAverage(team.Team.getCPQI), season.getTeamStatAverage(team.Team.getSeasonPointsTotal), season.getTeamStatAverage(team.Team.getPointsPercentage), standardDeviation(season.getTeamStatList(team.Team.getAWQI)), standardDeviation(season.getTeamStatList(team.Team.getAPQI)), standardDeviation(season.getTeamStatList(team.Team.getAGCI)), standardDeviation(season.getTeamStatList(team.Team.getAOQI)), standardDeviation(season.getTeamStatList(team.Team.getADQI)), standardDeviation(season.getTeamStatList(team.Team.getCPQI)), standardDeviation(season.getTeamStatList(team.Team.getSeasonPointsTotal)), standardDeviation(season.getTeamStatList(team.Team.getPointsPercentage)))
		oneSigma = standardDeviation(season.getTeamStatList(team.Team.getCPQI))
		
		oneGoalSigma = 0.987/oneSigma
		prediction = (1.000-norm.cdf(oneGoalSigma))*season.getTotalNumberOfTeams()
		actual = season.getTeamsAboveOneGoalCutoff()
		print "One goal cutoff: %f sigma, above teams predicted, %.3f, actual %i\n"	% (norm.cdf(oneGoalSigma), prediction, actual)			
		predictedTotal += prediction
		actualTotal += actual
		
	print "%s oneGoal Team totals: predicted %i, actual %i" % (levelId, predictedTotal, actualTotal)
