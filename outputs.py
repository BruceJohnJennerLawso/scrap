## outputs.py ###############################################################
## the entire stack takes way too long to run as it ############################
## grows, so Im gonna break it up into little bits so we can ###################
## generate smaller subsets of the graphs at once ##############################
################################################################################

from seasonWatMu import *
from seasonNhl import *
from graphtools import *

from statRetrieve import *

import sys  


	##reload(sys)  
	##sys.setdefaultencoding('utf8')

	## this was useful at some point

def getAllSeasons(leagueId, levelId='null'):
	## returns a list of every season listed in our manifest file
	## loaded completely with team Objects
	seasons = []
	
	if(leagueId != 'watMu'):
		with open('./data/%s/seasons.csv' % (leagueId), 'rb') as foo:
			## open the manifest csv file for this particular league
			## (nhl)
			reader = csv.reader(foo)
			for row in reader:
				## open the first season id in a row (formatted like termYYYY)
				seasonId = row[0]
				idPath = "./data/%s/%s/teamId.csv" % (leagueId, seasonId)
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
				seasons.append(nhlSeason(leagueId, seasonId, teamIdList, True))
				## this should create a season from this data, and by extension
				## constructs all of the teams that played in those seasons by
				## extension
		for season in seasons:
			season.loadTierIV(seasons)
		return seasons
	else:
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
		for season in seasons:
			season.loadTierIV(seasons)
		return seasons



if(__name__ == "__main__"):
	seasons = getAllSeasons('watMu', 'beginner')
	demoStatContainer(seasons, 'watMu', 'beginner') 
	foo = getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, 'watMu', 'allstar')

def getFranchiseList(leagueId, levelId):
	## returns a list of every season
	output = []
	
	
	if(leagueId != 'watMu'):
		with open('./data/%s/franchises.csv' % (leagueId), 'rb') as foo:
			## open the manifest csv file for this particular league & level
			## which lists the franchises on each row
			reader = csv.reader(foo)
			for row in reader:
				output.append(row)
				## append on the list of names, with the primary one
				## first, ie
				## [...['Chicago Blackhawks', 'Chicago Black Hawks'],...]

	else:
		with open('./data/%s/%s/franchises.csv' % (leagueId, levelId), 'rb') as foo:
			## open the manifest csv file for this particular league & level
			## which lists the franchises on each row
			reader = csv.reader(foo)
			for row in reader:
				output.append(row)
				## append on the list of names, with the primary one
				## first, ie
				## [...['Pucked Up', 'Pucked UP'],...]
	return output


def graphTeams(leagueId, levelId, playoffTeamsOnly, dependent, *independents):
	for indie in independents:
		plotScatterplot(indie.getShortStatName(), dependent.getShortStatName(), '%s by %s for %s %s' % (dependent.getLongStatName(), indie.getLongStatName(), leagueId, levelId), indie.getStat(playoffTeamsOnly), dependent.getStat(playoffTeamsOnly), './results/%s/%s/%sBy' % (leagueId, levelId, dependent.getShortStatName()), '%s' % indie.getShortStatName(), '%s_by_%s.png' % (dependent.getShortStatName(), indie.getShortStatName()))		
		## wow, that was quick

def graphTeamsAgainstDeltas(leagueId, levelId, playoffTeamsOnly, dependent, *independents):
	for indie in independents:
		
		thisIndieDeltas = getLinearModelDeltas(indie.getStat(playoffTeamsOnly), dependent.getStat(playoffTeamsOnly))
		
		print dependent.getShortStatName(), " ", indie.getShortStatName(), " Model Deltas min ", min(thisIndieDeltas), " max ", max(thisIndieDeltas)
		for indiana in independents:
			plotScatterplot(indiana.getShortStatName(), "%s_ModelDeltas" % indie.getShortStatName(), 'Deltas from the %s Model for %s by %s for %s %s' % (indie.getLongStatName(), dependent.getLongStatName(), indiana.getLongStatName(), leagueId, levelId), indiana.getStat(playoffTeamsOnly), thisIndieDeltas, './results/%s/%s/%sBy' % (leagueId, levelId, dependent.getShortStatName()), '%s/ModelDeltas/%s' % (indie.getShortStatName(), indiana.getShortStatName()), '%s_ModelDeltas_by_%s.png' % (indie.getShortStatName(), indiana.getShortStatName()))		
		## wow, that was quick



def graphTeamsHistogram(leagueId, levelId, playoffTeamsOnly, *variables):
	
	if(playoffTeamsOnly):
		thing = 'PlayoffTeam'
	else:
		thing = 'Total'
		
	for var in variables:
		plotHistogram(var.getShortStatName(), 'Count', 'Histogram of %s' % var.getLongStatName(), var.getStat(playoffTeamsOnly),'./results/%s/%s/histograms' % (leagueId, levelId), '%s' % var.getShortStatName(), '%s_%s_histogram.png' % (var.getShortStatName(), thing))			
		## wow, that was quick



def plotVariablesHeatmap(leagueId, levelId, playoffTeamsOnly, *variables):				
	
	data = []
	headings = []
	
	for var in variables:
		data.append(var.getStat(playoffTeamsOnly))
		headings.append(var.getShortStatName())
		
	data = map(list, zip(*data))
	## converts the data from rows of individual stat data to columns
	## of individual teams, where each list contains a list of stats
	## about that team

	
	dataPanda = pd.DataFrame(data, columns=headings)
	
	print "\n\nData means"
	print dataPanda.apply(np.mean), '\n'
	print "Data standard deviations"
	print dataPanda.apply(np.std)
	
	##pd.printMeanAndSdByGroup(dataTruong, 'Franchise') 

	plotScatterMatrix(dataPanda,  './results', '/%s/%s' % (leagueId, levelId), 'AllPlayoffTeams_MatrixScatterplot.png')
	seabornHeatmap(dataPanda, './results', '/%s/%s' % (leagueId, levelId), 'AllPlayoffTeams_Heatmap.png')

