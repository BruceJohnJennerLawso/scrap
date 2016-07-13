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

	mawqueeDeltas = getLinearModelDeltas(mawquees, playoffPercentages)
	plotScatterplot('MaAWQI Model Deltas', 'AGCI', 'AGCI by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, gci, './results/playoffWinBy', 'MaAWQI/modelDeltas', 'AGCI_by_MaAWQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAWQI Model Deltas', 'MaAPQI', 'MaAPQI by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, mapquees, './results/playoffWinBy', 'MaAWQI/modelDeltas', 'MaAPQI_by_MaAWQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAWQI Model Deltas', 'Offence', 'Offence by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, offence, './results/playoffWinBy', 'MaAWQI/modelDeltas', 'Offence_by_MaAWQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAWQI Model Deltas', 'Defence', 'Defence by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, defence, './results/playoffWinBy', 'MaAWQI/modelDeltas', 'Defence_by_MaAWQI_Deltas.png', -1.0, 1.0)				
	plotScatterplot('MaAWQI Model Deltas', 'OQI', 'OQI by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, offquees, './results/playoffWinBy', 'MaAWQI/modelDeltas', 'OQI_by_MaAWQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('MaAWQI Model Deltas', 'DQI', 'DQI by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, defquees, './results/playoffWinBy', 'MaAWQI/modelDeltas', 'DQI_by_MaAWQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('MaAWQI Model Deltas', '+/-', '+/- by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, plusMinuses, './results/playoffWinBy', 'MaAWQI/modelDeltas', 'PlusMinus_by_MaAWQI_Deltas.png', -1.0, 1.0)	
	
	mapqueeDeltas = getLinearModelDeltas(mapquees, playoffPercentages)
	plotScatterplot('MaAPQI Model Deltas', 'AGCI', 'AGCI by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, gci, './results/playoffWinBy', 'MaAPQI/modelDeltas', 'AGCI_by_MaAPQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAPQI Model Deltas', 'MaAWQI', 'MaAWQI by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, mawquees, './results/playoffWinBy', 'MaAPQI/modelDeltas', 'MaAPQI_by_MaAPQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAPQI Model Deltas', 'Offence', 'Offence by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, offence, './results/playoffWinBy', 'MaAPQI/modelDeltas', 'Offence_by_MaAPQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAPQI Model Deltas', 'Defence', 'Defence by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, defence, './results/playoffWinBy', 'MaAPQI/modelDeltas', 'Defence_by_MaAPQI_Deltas.png', -1.0, 1.0)				
	plotScatterplot('MaAPQI Model Deltas', 'OQI', 'OQI by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, offquees, './results/playoffWinBy', 'MaAPQI/modelDeltas', 'OQI_by_MaAPQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('MaAPQI Model Deltas', 'DQI', 'DQI by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, defquees, './results/playoffWinBy', 'MaAPQI/modelDeltas', 'DQI_by_MaAPQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('MaAPQI Model Deltas', '+/-', '+/- by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, plusMinuses, './results/playoffWinBy', 'MaAPQI/modelDeltas', 'PlusMinus_by_MaAPQI_Deltas.png', -1.0, 1.0)	

	offqueeDeltas = getLinearModelDeltas(offquees, playoffPercentages)
	plotScatterplot('OQI Model Deltas', 'AGCI', 'AGCI by OQI Deltas from the model', offqueeDeltas, gci, './results/playoffWinBy', 'OQI/modelDeltas', 'AGCI_by_OQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('OQI Model Deltas', 'MaAWQI', 'MaAWQI by OQI Deltas from the model', offqueeDeltas, mawquees, './results/playoffWinBy', 'OQI/modelDeltas', 'MaAWQI_by_OQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('OQI Model Deltas', 'Offence', 'Offence by OQI Deltas from the model', offqueeDeltas, offence, './results/playoffWinBy', 'OQI/modelDeltas', 'Offence_by_OQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('OQI Model Deltas', 'Defence', 'Defence by OQI Deltas from the model', offqueeDeltas, defence, './results/playoffWinBy', 'OQI/modelDeltas', 'Defence_by_OQI_Deltas.png', -1.0, 1.0)				
	plotScatterplot('OQI Model Deltas', 'MaAPQI', 'MaAPQI by OQI Deltas from the model', offqueeDeltas, mapquees, './results/playoffWinBy', 'OQI/modelDeltas', 'MaAPQI_by_OQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('OQI Model Deltas', 'DQI', 'DQI by OQI Deltas from the model', offqueeDeltas, defquees, './results/playoffWinBy', 'OQI/modelDeltas', 'DQI_by_OQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('OQI Model Deltas', '+/-', '+/- by OQI Deltas from the model', offqueeDeltas, plusMinuses, './results/playoffWinBy', 'OQI/modelDeltas', 'PlusMinus_by_OQI_Deltas.png', -1.0, 1.0)	

	defqueeDeltas = getLinearModelDeltas(defquees, playoffPercentages)
	plotScatterplot('DQI Model Deltas', 'AGCI', 'AGCI by DQI Deltas from the model', defqueeDeltas, gci, './results/playoffWinBy', 'DQI/modelDeltas', 'AGCI_by_DQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('DQI Model Deltas', 'MaAWQI', 'MaAWQI by DQI Deltas from the model', defqueeDeltas, mawquees, './results/playoffWinBy', 'DQI/modelDeltas', 'MaAWQI_by_DQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('DQI Model Deltas', 'Offence', 'Offence by DQI Deltas from the model', defqueeDeltas, offence, './results/playoffWinBy', 'DQI/modelDeltas', 'Offence_by_DQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('DQI Model Deltas', 'Defence', 'Defence by DQI Deltas from the model', defqueeDeltas, defence, './results/playoffWinBy', 'DQI/modelDeltas', 'Defence_by_DQI_Deltas.png', -1.0, 1.0)				
	plotScatterplot('DQI Model Deltas', 'MaAPQI', 'MaAPQI by DQI Deltas from the model', defqueeDeltas, mapquees, './results/playoffWinBy', 'DQI/modelDeltas', 'MaAPQI_by_DQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('DQI Model Deltas', 'OQI', 'OQI by DQI Deltas from the model', defqueeDeltas, offquees, './results/playoffWinBy', 'DQI/modelDeltas', 'OQI_by_DQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('DQI Model Deltas', '+/-', '+/- by DQI Deltas from the model', defqueeDeltas, plusMinuses, './results/playoffWinBy', 'DQI/modelDeltas', 'PlusMinus_by_DQI_Deltas.png', -1.0, 1.0)	

if(__name__ == "__main__"):
	
	leagueId = 'watMu'
	levelId = 'beginner'
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	plotAllTeams(seasons)
	plotAllTopPlayoffTeams(seasons)
	

	##print "################################################################################"
	##print "Season Leaders #################################################################"
	##print "################################################################################\n"	
	
	##for season in seasons:
	##	print season.seasonId
	##	print season.getTeamByPosition(1).getDescriptionString()
		##print "Top Playoff Bracket: ", season.topPlayoffBracket, " %i" % len(season.topPlayoffBracket), "\n"
	##	season.printPlayoffBrackets()

