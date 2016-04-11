## readata.py ##################################################################
## lets try loading the data from file again ###################################
## and make sure everything is there and comprehensible ########################
################################################################################
import csv
from teamWatMu import *

if(__name__ == "__main__"):
	print "Bahahaha"
	
	teams = []
	

	idPath = "./data/%s/teamId.csv" % "fall2015"
	with open(idPath, 'rb') as bar:
		reading = csv.reader(bar)
		for teamId in reading:
			teams.append(watMuTeam("fall2015", teamId[0]))
		for team in teams:
			team.loadTierII(teams)
		for team in teams:
			team.loadTierIII(teams)			
		for team in teams:
			print "%s (%i)%s, Pts %i Pct: %.3f, AGCI: %.3f, MaAWQI %.3f, MaAPQI %.3f" % (team.teamName, team.totalSeasonGames, team.getRecordString(), team.getSeasonPointsTotal(), team.getPointsPercentage(), team.getAGCI(), team.getMaAWQI(), team.getMaAPQI())
			print "Offense: %.3f, Defense %.3f, +/- %i, Average SOC of %.3f" % (team.getSeasonGoalsForAverage(), team.getSeasonGoalsAgainstAverage(), team.seasonPlusMinus, team.getSeasonAverageSOC())
			print "\n"
