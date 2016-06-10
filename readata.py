## readata.py ##################################################################
## lets try loading the data from file again ###################################
## and make sure everything is there and comprehensible ########################
################################################################################

import csv
from seasonWatMu import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
## I cant remember exactly what this was needed for, its some very specific
## aspect of graphing with matplotlib or something


def plotHistogram(xlabel, ylabel, title, values, output_filename, minShow='foo', maxShow='bar', binCount=39):
	## TLDR, takes a set of values and histograms them, whoop whop
	if(minShow == 'foo'):
		## if we dont get anything for a manual max min, just set our max and
		## min values for the graph range from the data
		minShow = float(int(min(values)))	
		maxShow = float(int(max(values)))			
	
	n, bins, patches = plt.hist(values, binCount, normed=0, facecolor='blue', alpha = 0.65)
	## histogram construction step
	## I forget, I think this was copy paste
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	## label our axes like good students
	plt.title(title)
	## an' title it
	plt.axis([minShow, maxShow, 0.0, 40.0])
	## 40 here was a working value for the range of possible bin values for this
	## dataset
	
	## I need to figure out how to get a max from our plt.hist output
	plt.grid(True)
	## make sure we got a grid on
	##plt.show()
	## showit
	plt.savefig(output_filename)
	plt.close()


def getAllSeasons(leagueId, levelId):
	## returns a list of every season
	seasons = []
	with open('./data/%s/%s/seasons.csv' % (leagueId, levelId), 'rb') as foo:
		## open the manifest csv file for this particular league & level
		## (waterloo intramurals and beginner...)
		reader = csv.reader(foo)
		for row in reader:
			## open the first season id in a row (formatted like termYYYY)
			seasonId = row[0]
			idPath = "./data/%s/%s/%s/teamId.csv" % (leagueId, levelId, seasonId)
			## open the list of team ids stored for that particular season in
			## another csv file
			teamIdList = []
			with open(idPath, 'rb') as bar:
				reading = csv.reader(bar)
				for teamId in reading:
					## open up the list of teamIds for the season in question
					teamIdList.append(teamId[0])
					## stuff the ids into a list
					
					## no idea why the ids are stored one deep
			seasons.append(watMuSeason(leagueId, levelId, seasonId, teamIdList))
			## this should create a season from this data, and by extension
			## constructs all of the teams that played in those seasons by
			## extension
	return seasons

if(__name__ == "__main__"):
	
	leagueId = 'watMu'
	levelId = 'beginner'
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level

	mawquees = []
	mapquees = []
	offence = []
	defence = []
	gci = []
	pointsPct = []
	## lists of values I want to plot in a histogram
	
	for season in seasons:
		print season.seasonId
		## loop through all of the seasons available and print the id of the
		## season
		for team in season.Teams:
			## loop through all of the teams that played in that season
			print "%s (%i)%s, Pts %i Pct: %.3f, AGCI: %.3f, MaAWQI %.3f, MaAPQI %.3f" % (team.teamName, team.totalSeasonGames, team.getRecordString(), team.getSeasonPointsTotal(), team.getPointsPercentage(), team.getAGCI(), team.getMaAWQI(), team.getMaAPQI())
			print "Offense: %.3f, Defense %.3f, +/- %i, Average SOC of %.3f" % (team.getSeasonGoalsForAverage(), team.getSeasonGoalsAgainstAverage(), team.seasonPlusMinus, team.getSeasonAverageSOC())			
			mawquees.append(team.getMaAWQI())
			offence.append(team.getSeasonGoalsForAverage())
			defence.append(team.getSeasonGoalsAgainstAverage())
			gci.append(team.getAGCI())
			mapquees.append(team.getMaAPQI())
			pointsPct.append(team.getPointsPercentage())
			## appending all of those values into one big list for each measure
			## so we can make a histogram of all of the values and display it
	plotHistogram('MaAWQI', 'Count', 'Histogram of Mean Adjusted AWQI values', mawquees, 'MaAWQI_Total_histogram.png')
	plotHistogram('MaAPQI', 'Count', 'Histogram of Mean Adjusted PWQI values', mapquees, 'MaAPQI_Total_histogram.png')
	plotHistogram('Points Percentage', 'Count', 'Histogram of Points Percentages', pointsPct, 'PtsPct_Total_histogram.png', 0.0, 1.0, 12)		
	plotHistogram('Offence', 'Count', 'Histogram of Offence Averages', offence, 'Offence_Total_histogram.png')
	plotHistogram('Defence', 'Count', 'Histogram of Defence Averages', defence, 'Defence_Total_histogram.png')	
	plotHistogram('AGCI', 'Count', 'Histogram of AGCI', gci,'AGCI_Total_histogram.png', 0.0, 1.0)	
	## plot all of the measures that we wanted as histograms
