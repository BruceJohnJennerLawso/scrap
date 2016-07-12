## readata.py ##################################################################
## lets try loading the data from file again ###################################
## and make sure everything is there and comprehensible ########################
################################################################################

import csv
from seasonWatMu import *
from graphtools import *

## I cant remember exactly what this was needed for, its some very specific
## aspect of graphing with matplotlib or something


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
	
	offquees = []
	defquees = []
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
			##mawqueePctRel.append(team.getMaAWQI()/team.getPointsPercentage())			
			offence.append(team.getSeasonGoalsForAverage())
			defence.append(team.getSeasonGoalsAgainstAverage())
			gci.append(team.getAGCI())
			mapquees.append(team.getMaAPQI())
			pointsPct.append(team.getPointsPercentage())
			plusMinuses.append(team.getSeasonPlusMinus())
			
			offquees.append(team.getOffenceQualityIndex())
			defquees.append(team.getDefenceQualityIndex())
			## appending all of those values into one big list for each measure
			## so we can make a histogram of all of the values and display it
	plotHistogram('MaAWQI', 'Count', 'Histogram of Mean Adjusted AWQI values', mawquees, './results/histograms', 'MaAWQI', 'MaAWQI_Total_histogram.png')
	plotHistogram('MaAPQI', 'Count', 'Histogram of Mean Adjusted PWQI values', mapquees, './results/histograms', 'MaAPQI', 'MaAPQI_Total_histogram.png')
	plotHistogram('Points Percentage', 'Count', 'Histogram of Points Percentages', pointsPct, './results/histograms', 'PtsPct', 'PtsPct_Total_histogram.png', 0.0, 1.0, 12)		
	plotHistogram('Offence', 'Count', 'Histogram of Offence Averages', offence, './results/histograms', 'Offence', 'Offence_Total_histogram.png', 0.0, 8.0)
	plotHistogram('Defence', 'Count', 'Histogram of Defence Averages', defence, './results/histograms/', 'Defence', 'Defence_Total_histogram.png', 0.0, 8.0)	
	plotHistogram('AGCI', 'Count', 'Histogram of AGCI', gci,'./results/histograms', 'AGCI', 'AGCI_Total_histogram.png', 0.0, 1.0)	
	plotHistogram('+/-', 'Count', 'Histogram of +/-', plusMinuses,'./results/histograms', 'PlusMinus', 'PlusMinus_Total_histogram.png', -40, 40)	
	
	plotHistogram('Offence Quality Index', 'Count', 'Histogram of Offence Quality Index values', offquees,'./results/histograms', 'OQI', 'OQI_Total_histogram.png')	
	plotHistogram('Defence Quality Index', 'Count', 'Histogram of Of Defence Quality Index values', defquees,'./results/histograms', 'DQI', 'DQI_Total_histogram.png')
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

	offquees = []
	defquees = []
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

				offquees.append(team.getOffenceQualityIndex())
				defquees.append(team.getDefenceQualityIndex())
				## appending all of those values into one big list for each measure
				## so we can make a histogram of all of the values and display it
	plotHistogram('MaAWQI', 'Count', 'Histogram of Mean Adjusted AWQI values', mawquees, './results/histograms', 'MaAWQI', 'MaAWQI_PlayoffTeam_histogram.png')
	plotScatterplot('MaAWQI', 'Playoff Win %', 'Playoff Win % by Mean Adjusted AWQI values', mawquees, playoffPercentages, './results/playoffWinBy', 'MaAWQI', 'PlayoffWinPct_by_MaAWQI.png')	
	plotHistogram('MaAPQI', 'Count', 'Histogram of Mean Adjusted APQI values', mapquees, './results/histograms', 'MaAPQI', 'MaAPQI_PlayoffTeam_histogram.png')
	plotScatterplot('MaAPQI', 'Playoff Win %', 'Playoff Win % by Mean Adjusted APQI values', mapquees, playoffPercentages, './results/playoffWinBy', 'MaAPQI', 'PlayoffWinPct_by_MaAPQI.png')
	plotHistogram('Points Percentage', 'Count', 'Histogram of Points Percentages', pointsPct, './results/histograms', 'PtsPct', 'PtsPct_PlayoffTeam_histogram.png', 0.0, 1.0, 12)		
	plotScatterplot('Points Percentage', 'Playoff Win %', 'Playoff Win % by Points Percentage values', pointsPct, playoffPercentages, './results/playoffWinBy', 'PtsPct', 'PlayoffWinPct_by_PtsPct.png', 0.0, 1.0)
	plotHistogram('Offence', 'Count', 'Histogram of Offence Averages', offence, './results/histograms', 'Offence', 'Offence_PlayoffTeam_histogram.png', 0.0, 8.0)
	plotScatterplot('Average Goals For', 'Playoff Win %', 'Playoff Win % by Average Goals For', offence, playoffPercentages, './results/playoffWinBy', 'Offence', 'PlayoffWinPct_by_Offence.png', 0.0, 8.0)	
	plotHistogram('Defence', 'Count', 'Histogram of Defence Averages', defence, './results/histograms', 'Defence', 'Defence_PlayoffTeam_histogram.png', 0.0, 8.0)	
	plotScatterplot('Average Goals Against', 'Playoff Win %', 'Playoff Win % by Average Goals Against', defence, playoffPercentages, './results/playoffWinBy', 'Defence', 'PlayoffWinPct_by_Defence.png', 0.0, 8.0)
	plotHistogram('AGCI', 'Count', 'Histogram of AGCI', gci,'./results/histograms', 'AGCI', 'AGCI_PlayoffTeam_histogram.png', 0.0, 1.0)	
	plotScatterplot('AGCI', 'Playoff Win %', 'Playoff Win % by AGCI', gci, playoffPercentages, './results/playoffWinBy', 'AGCI', 'PlayoffWinPct_by_AGCI.png', 0.0, 1.0)	
	plotHistogram('+/-', 'Count', 'Histogram of +/-', plusMinuses,'./results/histograms', 'PlusMinus', 'PlusMinus_PlayoffTeam_histogram.png', -40, 40)	
	plotScatterplot('+/-', 'Playoff Win %', 'Playoff Win % by +/-', plusMinuses, playoffPercentages, './results/playoffWinBy', 'PlusMinus', 'PlayoffWinPct_by_PlusMinus.png', -40, 40)

	plotScatterplot('Offence Quality Index', 'Playoff Win %', 'Playoff Win % by Offence Quality Index', offquees, playoffPercentages, './results/playoffWinBy', 'OQI', 'PlayoffWinPct_by_OQI.png', -30, 30)
	plotScatterplot('Defence Quality Index', 'Playoff Win %', 'Playoff Win % by Defence Quality Index', defquees, playoffPercentages, './results/playoffWinBy', 'DQI', 'PlayoffWinPct_by_DQI.png', -30, 30)	
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
	print "Season Leaders #################################################################"
	print "################################################################################\n"	
	
	for season in seasons:
		print season.seasonId
		print season.getTeamByPosition(1).getDescriptionString()
		##print "Top Playoff Bracket: ", season.topPlayoffBracket, " %i" % len(season.topPlayoffBracket), "\n"
		season.printPlayoffBrackets()

