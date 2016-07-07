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
	
	
def plotScatterplot(xlabel, ylabel, title, x_values, y_values, output_filename, minShow='foo', maxShow='bar', binCount=39):
	## TLDR, takes a set of values and histograms them, whoop whop
	if(minShow == 'foo'):
		## if we dont get anything for a manual max min, just set our max and
		## min values for the graph range from the data
		minShow = float(int(min(x_values)))	
		maxShow = float(int(max(x_values)))			
	
	plt.plot(x_values, y_values)
	## histogram construction step
	## I forget, I think this was copy paste
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	## label our axes like good students
	plt.title(title)
	## an' title it
	plt.axis([minShow, maxShow, 0.0, 1.2])
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
			seasons.append(watMuSeason(leagueId, levelId, seasonId, teamIdList, True))
			## this should create a season from this data, and by extension
			## constructs all of the teams that played in those seasons by
			## extension
	return seasons


def plotAllTeams(seasons):
	mawquees = []
	mapquees = []
	offence = []
	defence = []
	gci = []
	pointsPct = []
	plusMinuses = []
	## lists of values I want to plot in a histogram
	
	for season in seasons:
		print "################################################################################"
		print season.seasonId
		print "################################################################################\n"		
		## loop through all of the seasons available and print the id of the
		## season
		for team in season.Teams:
			## loop through all of the teams that played in that season
			print team.getDescriptionString(), "\n"
			mawquees.append(team.getMaAWQI())
			offence.append(team.getSeasonGoalsForAverage())
			defence.append(team.getSeasonGoalsAgainstAverage())
			gci.append(team.getAGCI())
			mapquees.append(team.getMaAPQI())
			pointsPct.append(team.getPointsPercentage())
			plusMinuses.append(team.getSeasonPlusMinus())
			## appending all of those values into one big list for each measure
			## so we can make a histogram of all of the values and display it
	plotHistogram('MaAWQI', 'Count', 'Histogram of Mean Adjusted AWQI values', mawquees, 'MaAWQI_Total_histogram.png')
	plotHistogram('MaAPQI', 'Count', 'Histogram of Mean Adjusted PWQI values', mapquees, 'MaAPQI_Total_histogram.png')
	plotHistogram('Points Percentage', 'Count', 'Histogram of Points Percentages', pointsPct, 'PtsPct_Total_histogram.png', 0.0, 1.0, 12)		
	plotHistogram('Offence', 'Count', 'Histogram of Offence Averages', offence, 'Offence_Total_histogram.png', 0.0, 8.0)
	plotHistogram('Defence', 'Count', 'Histogram of Defence Averages', defence, 'Defence_Total_histogram.png', 0.0, 8.0)	
	plotHistogram('AGCI', 'Count', 'Histogram of AGCI', gci,'AGCI_Total_histogram.png', 0.0, 1.0)	
	plotHistogram('+/-', 'Count', 'Histogram of +/-', plusMinuses,'PlusMinus_Total_histogram.png', -40, 40)	
	## plot all of the measures that we wanted as histograms


def plotAllTopPlayoffTeams(seasons):
	mawquees = []
	mapquees = []
	offence = []
	defence = []
	gci = []
	pointsPct = []
	plusMinuses = []
	playoffPercentages = []
	## lists of values I want to plot in a histogram
	
	for season in seasons:
		print "################################################################################"
		print season.seasonId
		print "################################################################################\n"		
		## loop through all of the seasons available and print the id of the
		## season
		for team in season.Teams:
			## loop through all of the teams that played in that season
			if(team.getSeasonRank() in season.topPlayoffBracket):
				print team.getDescriptionString(), "\n"
				mawquees.append(team.getMaAWQI())
				offence.append(team.getSeasonGoalsForAverage())
				defence.append(team.getSeasonGoalsAgainstAverage())
				gci.append(team.getAGCI())
				mapquees.append(team.getMaAPQI())
				pointsPct.append(team.getPointsPercentage())
				plusMinuses.append(team.getSeasonPlusMinus())
				playoffPercentages.append(team.getRealPlayoffWinPercentage(season))
				## appending all of those values into one big list for each measure
				## so we can make a histogram of all of the values and display it
	plotHistogram('MaAWQI', 'Count', 'Histogram of Mean Adjusted AWQI values', mawquees, 'MaAWQI_PlayoffTeam_histogram.png')
	plotScatterplot('MaAWQI', 'Playoff Win %', 'Playoff Win % by Mean Adjusted AWQI values', mawquees, playoffPercentages, 'PlayoffWinPct_by_MaAWQI.png')	
	plotHistogram('MaAPQI', 'Count', 'Histogram of Mean Adjusted PWQI values', mapquees, 'MaAPQI_PlayoffTeam_histogram.png')
	plotHistogram('Points Percentage', 'Count', 'Histogram of Points Percentages', pointsPct, 'PtsPct_PlayoffTeam_histogram.png', 0.0, 1.0, 12)		
	plotHistogram('Offence', 'Count', 'Histogram of Offence Averages', offence, 'Offence_PlayoffTeam_histogram.png', 0.0, 8.0)
	plotHistogram('Defence', 'Count', 'Histogram of Defence Averages', defence, 'Defence_PlayoffTeam_histogram.png', 0.0, 8.0)	
	plotHistogram('AGCI', 'Count', 'Histogram of AGCI', gci,'AGCI_PlayoffTeam_histogram.png', 0.0, 1.0)	
	plotHistogram('+/-', 'Count', 'Histogram of +/-', plusMinuses,'PlusMinus_PlayoffTeam_histogram.png', -40, 40)	
	## plot all of the measures that we wanted as histograms


if(__name__ == "__main__"):
	
	leagueId = 'watMu'
	levelId = 'beginner'
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	plotAllTeams(seasons)
	plotAllTopPlayoffTeams(seasons)
	

	print "################################################################################"
	print "Season Leaders"
	print "################################################################################\n"	
	
	for season in seasons:
		print season.seasonId
		print season.getTeamByPosition(1).getDescriptionString()
		##print "Top Playoff Bracket: ", season.topPlayoffBracket, " %i" % len(season.topPlayoffBracket), "\n"
		season.printPlayoffBrackets()

