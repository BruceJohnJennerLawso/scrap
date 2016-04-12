## readata.py ##################################################################
## lets try loading the data from file again ###################################
## and make sure everything is there and comprehensible ########################
################################################################################
import csv
from seasonWatMu import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

if(__name__ == "__main__"):
	seasons = []

	leagueId = 'watMu'
	levelId = 'beginner'

	with open('./data/watMu/beginner/seasons.csv', 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			seasonId = row[0]
			idPath = "./data/watMu/beginner/%s/teamId.csv" % seasonId
			
			teamIdList = []
			with open(idPath, 'rb') as bar:
				reading = csv.reader(bar)
				for teamId in reading:
					teamIdList.append(teamId[0])
					## no idea why the ids are stored one deep
			seasons.append(watMuSeason(leagueId, levelId, seasonId, teamIdList))
	
	mawquees = []
	for season in seasons:
		print season.seasonId
		for team in season.Teams:
			print "%s (%i)%s, Pts %i Pct: %.3f, AGCI: %.3f, MaAWQI %.3f, MaAPQI %.3f" % (team.teamName, team.totalSeasonGames, team.getRecordString(), team.getSeasonPointsTotal(), team.getPointsPercentage(), team.getAGCI(), team.getMaAWQI(), team.getMaAPQI())
			print "Offense: %.3f, Defense %.3f, +/- %i, Average SOC of %.3f" % (team.getSeasonGoalsForAverage(), team.getSeasonGoalsAgainstAverage(), team.seasonPlusMinus, team.getSeasonAverageSOC())			
			mawquees.append(team.getMaAWQI())
	n, bins, patches = plt.hist(mawquees, 16, normed=0, facecolor='blue', alpha = 0.65)
	##y = mlab.normpdf(bins, 0.25, 0.75)
	##l = plt.plot(bins, y, 'g', linewidth=1)
	## cant really fit anything very well until we have much more data
	## also looks like bimodal, if not trimodal, distribution
	plt.xlabel('MaAWQI')
	plt.ylabel('frequency')
	plt.title('Histogram of Mean Adjusted AWQI values')
	float(int(max(mawquees)))	
	plt.axis([0.0, float(int(max(mawquees))), 0.0, 20.0])
	plt.grid(True)
	plt.show()


