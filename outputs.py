## outputs.py ###############################################################
## the entire stack takes way too long to run as it ############################
## grows, so Im gonna break it up into little bits so we can ###################
## generate smaller subsets of the graphs at once ##############################
################################################################################

from seasonWatMu import *
from graphtools import *

import sys  




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


def getFranchiseList(leagueId, levelId):
	## returns a list of every season
	output = []
	with open('./data/%s/%s/franchises.csv' % (leagueId, levelId), 'rb') as foo:
		## open the manifest csv file for this particular league & level
		## which lists the franchises on each row
		reader = csv.reader(foo)
		for row in reader:
			output.append(row)
			## append on the list of names, with the primary one first, ie
			## [...['Pucked Up', 'Pucked UP'],...]
	return output

def plotAllTeams(seasons, leagueId, levelId):
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
	plotHistogram('MaAWQI', 'Count', 'Histogram of Mean Adjusted AWQI values', mawquees, './results/%s/%s/histograms' % (leagueId, levelId), 'MaAWQI', 'MaAWQI_Total_histogram.png')
	plotHistogram('MaAPQI', 'Count', 'Histogram of Mean Adjusted PWQI values', mapquees, './results/%s/%s/histograms' % (leagueId, levelId), 'MaAPQI', 'MaAPQI_Total_histogram.png')
	plotHistogram('Points Percentage', 'Count', 'Histogram of Points Percentages', pointsPct, './results/%s/%s/histograms' % (leagueId, levelId), 'PtsPct', 'PtsPct_Total_histogram.png', 0.0, 1.0, 12)		
	plotHistogram('Offence', 'Count', 'Histogram of Offence Averages', offence, './results/%s/%s/histograms' % (leagueId, levelId), 'Offence', 'Offence_Total_histogram.png', 0.0, 8.0)
	plotHistogram('Defence', 'Count', 'Histogram of Defence Averages', defence, './results/%s/%s/histograms' % (leagueId, levelId), 'Defence', 'Defence_Total_histogram.png', 0.0, 8.0)	
	plotHistogram('AGCI', 'Count', 'Histogram of AGCI', gci,'./results/%s/%s/histograms' % (leagueId, levelId), 'AGCI', 'AGCI_Total_histogram.png', 0.0, 1.0)	
	plotHistogram('+/-', 'Count', 'Histogram of +/-', plusMinuses,'./results/%s/%s/histograms' % (leagueId, levelId), 'PlusMinus', 'PlusMinus_Total_histogram.png', -40, 40)	
	
	plotHistogram('Offence Quality Index', 'Count', 'Histogram of Offence Quality Index values', offquees,'./results/%s/%s/histograms' % (leagueId, levelId), 'OQI', 'OQI_Total_histogram.png')	
	plotHistogram('Defence Quality Index', 'Count', 'Histogram of Of Defence Quality Index values', defquees,'./results/%s/%s/histograms' % (leagueId, levelId), 'DQI', 'DQI_Total_histogram.png')
	## plot all of the measures that we wanted as histograms


def plotAllTopPlayoffTeams(seasons, leagueId, levelId):
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
	
	offqual = []
	
	megaThing = []
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
				
				offqual.append((team.getOffenceQualityIndex())/(team.getSeasonGoalsForAverage()+0.001))
				
				## appending all of those values into one big list for each measure
				## so we can make a histogram of all of the values and display it
	plotHistogram('MaAWQI', 'Count', 'Histogram of Mean Adjusted AWQI values', mawquees, './results/%s/%s/histograms' % (leagueId, levelId), 'MaAWQI', 'MaAWQI_PlayoffTeam_histogram.png')
	plotScatterplot('MaAWQI', 'Playoff Win %', 'Playoff Win % by Mean Adjusted AWQI values', mawquees, playoffPercentages, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAWQI', 'PlayoffWinPct_by_MaAWQI.png')	
	plotHistogram('MaAPQI', 'Count', 'Histogram of Mean Adjusted APQI values', mapquees, './results/%s/%s/histograms' % (leagueId, levelId), 'MaAPQI', 'MaAPQI_PlayoffTeam_histogram.png')
	plotScatterplot('MaAPQI', 'Playoff Win %', 'Playoff Win % by Mean Adjusted APQI values', mapquees, playoffPercentages, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAPQI', 'PlayoffWinPct_by_MaAPQI.png')
	plotHistogram('Points Percentage', 'Count', 'Histogram of Points Percentages', pointsPct, './results/%s/%s/histograms' % (leagueId, levelId), 'PtsPct', 'PtsPct_PlayoffTeam_histogram.png', 0.0, 1.0, 12)		
	plotScatterplot('Points Percentage', 'Playoff Win %', 'Playoff Win % by Points Percentage values', pointsPct, playoffPercentages, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'PtsPct', 'PlayoffWinPct_by_PtsPct.png', 0.0, 1.0)
	plotHistogram('Offence', 'Count', 'Histogram of Offence Averages', offence, './results/%s/%s/histograms' % (leagueId, levelId), 'Offence', 'Offence_PlayoffTeam_histogram.png', 0.0, 8.0)
	plotScatterplot('Average Goals For', 'Playoff Win %', 'Playoff Win % by Average Goals For', offence, playoffPercentages, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'Offence', 'PlayoffWinPct_by_Offence.png', 0.0, 8.0)	
	plotHistogram('Defence', 'Count', 'Histogram of Defence Averages', defence, './results/%s/%s/histograms' % (leagueId, levelId), 'Defence', 'Defence_PlayoffTeam_histogram.png', 0.0, 8.0)	
	plotScatterplot('Average Goals Against', 'Playoff Win %', 'Playoff Win % by Average Goals Against', defence, playoffPercentages, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'Defence', 'PlayoffWinPct_by_Defence.png', 0.0, 8.0)
	plotHistogram('AGCI', 'Count', 'Histogram of AGCI', gci,'./results/%s/%s/histograms' % (leagueId, levelId), 'AGCI', 'AGCI_PlayoffTeam_histogram.png', 0.0, 1.0)	
	plotScatterplot('AGCI', 'Playoff Win %', 'Playoff Win % by AGCI', gci, playoffPercentages, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'AGCI', 'PlayoffWinPct_by_AGCI.png', 0.0, 1.0)	
	plotHistogram('+/-', 'Count', 'Histogram of +/-', plusMinuses,'./results/%s/%s/histograms' % (leagueId, levelId), 'PlusMinus', 'PlusMinus_PlayoffTeam_histogram.png', -40, 40)	
	plotScatterplot('+/-', 'Playoff Win %', 'Playoff Win % by +/-', plusMinuses, playoffPercentages, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'PlusMinus', 'PlayoffWinPct_by_PlusMinus.png', -40, 40)

	plotHistogram('Offence Quality Margin', 'Count', 'Histogram of OQM', offqual,'./results/%s/%s/histograms' % (leagueId, levelId), 'experimental', 'OQM_PlayoffTeam_histogram.png', -180, 10)	
	plotScatterplot('Offence Quality Margin', 'Playoff Win %', 'Playoff Win % by OQM', offqual, playoffPercentages, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'experimental', 'PlayoffWinPct_by_OQM.png', -180, 10)

	plotScatterplot('Offence Quality Index', 'Playoff Win %', 'Playoff Win % by Offence Quality Index', offquees, playoffPercentages, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'OQI', 'PlayoffWinPct_by_OQI.png', -30, 30)
	plotScatterplot('Defence Quality Index', 'Playoff Win %', 'Playoff Win % by Defence Quality Index', defquees, playoffPercentages, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'DQI', 'PlayoffWinPct_by_DQI.png', -30, 30)	
	
def plotAllTopPlayoffTeamsDeltas(seasons, leagueId, levelId):
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
	offqual = []
	
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
				
				offqual.append((team.getOffenceQualityIndex())/(team.getSeasonGoalsForAverage()+0.001))
				
				## appending all of those values into one big list for each measure
				## so we can make a histogram of all of the values and display it
	mawqueeDeltas = getLinearModelDeltas(mawquees, playoffPercentages)
	plotScatterplot('MaAWQI Model Deltas', 'AGCI', 'AGCI by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, gci, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAWQI/modelDeltas', 'AGCI_by_MaAWQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAWQI Model Deltas', 'MaAPQI', 'MaAPQI by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, mapquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAWQI/modelDeltas', 'MaAPQI_by_MaAWQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAWQI Model Deltas', 'Offence', 'Offence by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, offence, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAWQI/modelDeltas', 'Offence_by_MaAWQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAWQI Model Deltas', 'Defence', 'Defence by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, defence, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAWQI/modelDeltas', 'Defence_by_MaAWQI_Deltas.png', -1.0, 1.0)				
	plotScatterplot('MaAWQI Model Deltas', 'OQI', 'OQI by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, offquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAWQI/modelDeltas', 'OQI_by_MaAWQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('MaAWQI Model Deltas', 'DQI', 'DQI by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, defquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAWQI/modelDeltas', 'DQI_by_MaAWQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('MaAWQI Model Deltas', '+/-', '+/- by Mean Adjusted AWQI Deltas from the model', mawqueeDeltas, plusMinuses, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAWQI/modelDeltas', 'PlusMinus_by_MaAWQI_Deltas.png', -1.0, 1.0)	
	
	mapqueeDeltas = getLinearModelDeltas(mapquees, playoffPercentages)
	plotScatterplot('MaAPQI Model Deltas', 'AGCI', 'AGCI by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, gci, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAPQI/modelDeltas', 'AGCI_by_MaAPQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAPQI Model Deltas', 'MaAWQI', 'MaAWQI by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, mawquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAPQI/modelDeltas', 'MaAWQI_by_MaAPQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAPQI Model Deltas', 'Offence', 'Offence by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, offence, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAPQI/modelDeltas', 'Offence_by_MaAPQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('MaAPQI Model Deltas', 'Defence', 'Defence by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, defence, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAPQI/modelDeltas', 'Defence_by_MaAPQI_Deltas.png', -1.0, 1.0)				
	plotScatterplot('MaAPQI Model Deltas', 'OQI', 'OQI by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, offquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAPQI/modelDeltas', 'OQI_by_MaAPQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('MaAPQI Model Deltas', 'DQI', 'DQI by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, defquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAPQI/modelDeltas', 'DQI_by_MaAPQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('MaAPQI Model Deltas', '+/-', '+/- by Mean Adjusted APQI Deltas from the model', mapqueeDeltas, plusMinuses, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'MaAPQI/modelDeltas', 'PlusMinus_by_MaAPQI_Deltas.png', -1.0, 1.0)	

	offqueeDeltas = getLinearModelDeltas(offquees, playoffPercentages)
	plotScatterplot('OQI Model Deltas', 'AGCI', 'AGCI by OQI Deltas from the model', offqueeDeltas, gci, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'OQI/modelDeltas', 'AGCI_by_OQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('OQI Model Deltas', 'MaAWQI', 'MaAWQI by OQI Deltas from the model', offqueeDeltas, mawquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'OQI/modelDeltas', 'MaAWQI_by_OQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('OQI Model Deltas', 'Offence', 'Offence by OQI Deltas from the model', offqueeDeltas, offence, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'OQI/modelDeltas', 'Offence_by_OQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('OQI Model Deltas', 'Defence', 'Defence by OQI Deltas from the model', offqueeDeltas, defence, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'OQI/modelDeltas', 'Defence_by_OQI_Deltas.png', -1.0, 1.0)				
	plotScatterplot('OQI Model Deltas', 'MaAPQI', 'MaAPQI by OQI Deltas from the model', offqueeDeltas, mapquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'OQI/modelDeltas', 'MaAPQI_by_OQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('OQI Model Deltas', 'DQI', 'DQI by OQI Deltas from the model', offqueeDeltas, defquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'OQI/modelDeltas', 'DQI_by_OQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('OQI Model Deltas', '+/-', '+/- by OQI Deltas from the model', offqueeDeltas, plusMinuses, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'OQI/modelDeltas', 'PlusMinus_by_OQI_Deltas.png', -1.0, 1.0)	

	defqueeDeltas = getLinearModelDeltas(defquees, playoffPercentages)
	plotScatterplot('DQI Model Deltas', 'AGCI', 'AGCI by DQI Deltas from the model', defqueeDeltas, gci, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'DQI/modelDeltas', 'AGCI_by_DQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('DQI Model Deltas', 'MaAWQI', 'MaAWQI by DQI Deltas from the model', defqueeDeltas, mawquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'DQI/modelDeltas', 'MaAWQI_by_DQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('DQI Model Deltas', 'Offence', 'Offence by DQI Deltas from the model', defqueeDeltas, offence, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'DQI/modelDeltas', 'Offence_by_DQI_Deltas.png', -1.0, 1.0)
	plotScatterplot('DQI Model Deltas', 'Defence', 'Defence by DQI Deltas from the model', defqueeDeltas, defence, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'DQI/modelDeltas', 'Defence_by_DQI_Deltas.png', -1.0, 1.0)				
	plotScatterplot('DQI Model Deltas', 'MaAPQI', 'MaAPQI by DQI Deltas from the model', defqueeDeltas, mapquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'DQI/modelDeltas', 'MaAPQI_by_DQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('DQI Model Deltas', 'OQI', 'OQI by DQI Deltas from the model', defqueeDeltas, offquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'DQI/modelDeltas', 'OQI_by_DQI_Deltas.png', -1.0, 1.0)	
	plotScatterplot('DQI Model Deltas', '+/-', '+/- by DQI Deltas from the model', defqueeDeltas, plusMinuses, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'DQI/modelDeltas', 'PlusMinus_by_DQI_Deltas.png', -1.0, 1.0)	
	
	plusminusDeltas = getLinearModelDeltas(plusMinuses, playoffPercentages)
	plotScatterplot('+/- Model Deltas', 'AGCI', 'AGCI by +/- Deltas from the model', plusminusDeltas, gci, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'PlusMinus/modelDeltas', 'AGCI_by_PlusMinus_Deltas.png', -1.0, 1.0)
	plotScatterplot('+/- Model Deltas', 'MaAWQI', 'MaAWQI by +/- Deltas from the model', plusminusDeltas, mawquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'PlusMinus/modelDeltas', 'MaAWQI_by_PlusMinus_Deltas.png', -1.0, 1.0)
	plotScatterplot('+/- Model Deltas', 'Offence', 'Offence by +/- Deltas from the model', plusminusDeltas, offence, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'PlusMinus/modelDeltas', 'Offence_by_PlusMinus_Deltas.png', -1.0, 1.0)
	plotScatterplot('+/- Model Deltas', 'Defence', 'Defence by +/- Deltas from the model', plusminusDeltas, defence, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'PlusMinus/modelDeltas', 'Defence_by_PlusMinus_Deltas.png', -1.0, 1.0)				
	plotScatterplot('+/- Model Deltas', 'MaAPQI', 'MaAPQI by +/- Deltas from the model', plusminusDeltas, mapquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'PlusMinus/modelDeltas', 'MaAPQI_by_PlusMinus_Deltas.png', -1.0, 1.0)	
	plotScatterplot('+/- Model Deltas', 'OQI', 'OQI by +/- Deltas from the model', plusminusDeltas, offquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'PlusMinus/modelDeltas', 'OQI_by_PlusMinus_Deltas.png', -1.0, 1.0)	
	plotScatterplot('+/- Model Deltas', 'DQI', 'DQI by +/- Deltas from the model', plusminusDeltas, defquees, './results/%s/%s/playoffWinBy' % (leagueId, levelId), 'PlusMinus/modelDeltas', 'DQI_by_PlusMinus_Deltas.png', -1.0, 1.0)			



def plotAllTopPlayoffTeamsVariables(seasons, leagueId, levelId, franchises):
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
	offqual = []
	
	data = []
	daterd = []
	## ermagherd, daterd
	
	reload(sys)  
	sys.setdefaultencoding('utf8')
	
	for season in seasons:
		print "################################################################################"
		print season.seasonId
		print "################################################################################\n"		
		## loop through all of the seasons available and print the id of the
		## season
		for team in season.Teams:
			## loop through all of the teams that played in that season
			if(team.getSeasonRank() in season.topPlayoffBracket):
				##print team.getDescriptionString(), "\n"
				
				data.append([team.getRealPlayoffWinPercentage(season), team.getPlayoffGoalsForAverage(), team.getPlayoffGoalsAgainstAverage(), team.getSeasonGoalsForAverage(), team.getSeasonGoalsAgainstAverage(), team.getMaAWQI(), team.getMaAPQI(), team.getAGCI(), team.getDefenceQualityIndex(), team.getOffenceQualityIndex(), team.getPointsPercentage()])
				##teamFran = unicode(team.getFranchise(franchises)).replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "")
				teamFran = str(team.getFranchise(franchises).decode('utf-8'))
				print teamFran
				
				daterd.append([teamFran.encode('utf-8'), team.getSeasonGoalsForAverage(), team.getSeasonGoalsAgainstAverage(), team.getMaAWQI(), team.getMaAPQI(), team.getAGCI(), team.getDefenceQualityIndex(), team.getOffenceQualityIndex(), team.getPointsPercentage()])
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
				
				offqual.append((team.getOffenceQualityIndex())/(team.getSeasonGoalsForAverage()+0.001))
				
				## appending all of those values into one big list for each measure
				## so we can make a histogram of all of the values and display it

	dataPanda = pd.DataFrame(data, columns=['Playoff Win Pct', 'Playoff Offence', 'Playoff Defence','GFA', 'GAA', 'MaAWQI', 'MaAPQI', 'AGCI', 'DQI', 'OQI', 'Points Pct'])
	dataTruong = pd.DataFrame(daterd, columns=['Franchise' , 'GFA', 'GAA', 'MaAWQI', 'MaAPQI', 'AGCI', 'DQI', 'OQI', 'Points Pct'])
	## Hi Ryan
	print "Data means"
	print dataPanda.apply(np.mean)
	print "Data standard deviations"
	print dataPanda.apply(np.std)
	
	##pd.printMeanAndSdByGroup(dataTruong, 'Franchise') 

	plotScatterMatrix(dataPanda, './results/%s/%s' % (leagueId, levelId), 'matrixScatterplot', 'AllPlayoffTeams_MatrixScatterplot.png')
	##plotScatterLabelled(dataTruong, 'GAA', 'GFA', 'Franchise', './results', '/%s/%s' % (leagueId, levelId), 'AllPlayoffTeams_LabelledScatterplot_GAA_GFA.png')

	seabornHeatmap(dataPanda, './results', '/%s/%s' % (leagueId, levelId), 'AllPlayoffTeams_Heatmap.png')
