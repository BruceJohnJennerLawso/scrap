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


def printTitleBox(text, debugInfo=False):
	
	textLength = len(text)
	trailingLength = 80 - (3 + textLength + 1)
	
	if(debugInfo):
		for i in range(0, len(text)):
			print i, text[i]
	
	print "#"*80
	print "##", text, "#"*trailingLength
	print "#"*80, "\n"

def clearTerminal():
	## Clears the screen
	##if(x>0):
	##	for i in range(0, (x-1)):
	##		print "\n",
	sys.stdout.write("\x1b[2J\x1b[H");

def printProgressBar(x, outOf, outputWidthCap=80):
	outputLines = 1
	
	lastLineWidth = outOf
	if(lastLineWidth > (outputWidthCap -2)):
		##print "output range %i exceeds one line, going bigger" % lastLineWidth
		while(lastLineWidth > (outputWidthCap -2)):
			lastLineWidth -= (outputWidthCap -2)
			outputLines += 1
	
	lineWidths = []
	for i in range(1, outputLines+1):
		if(i == outputLines):
			## we hit our last line, so it might be slightly shorter
			## than the previous ones
			lineWidths.append(lastLineWidth)
		else:
			lineWidths.append(outputWidthCap -2)
	lines = []
		
	count = x	
		
	for line in lineWidths:
		lineString = "["
		for i in range(line):
			if(count > 0):
				lineString += "*"
				count -= 1
			else:
				lineString += "#"
		lineString += "]"
		lines.append(lineString)
	for line in lines:
		print line
	##print outputLines			




	
def getAllSeasons(leagueId, levelId='null'):
	## returns a list of every season listed in our manifest file
	## loaded completely with team Objects
	seasons = []
	
	if(leagueId != 'watMu'):
		
		try:
			total = 0
			currentlyLoaded = 0
			with open('./data/%s/%s/seasons.csv' % (leagueId, levelId), 'rb') as foo:
				## open the manifest csv file for this particular league
				## (nhl)
				earlyReader = csv.reader(foo)
				for row in earlyReader:
					total += 1
				print "total ", total
			
			with open('./data/%s/%s/seasons.csv' % (leagueId, levelId), 'rb') as foo:
				## open the manifest csv file for this particular league
				## (nhl)
				reader = csv.reader(foo)
				for row in reader:
					clearTerminal()
					printProgressBar(currentlyLoaded, total)
					
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
					
					currentlyLoaded = len(seasons)
					print "currentlyLoaded, ", currentlyLoaded
					## this should create a season from this data, and by extension
					## constructs all of the teams that played in those seasons by
					## extension
				clearTerminal()
				printProgressBar(currentlyLoaded, total)	
		except IOError:
			print "Catching unusual argument %s" % levelId
			## a year was passed as argument instead of a season spread
			## list name
			try:
				seasonId = levelId
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
			except IOError:
				print "Unable to make levelId argument %s work, failing" % levelId
			
	else:
		## our league is watMu here
		try:
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
		except IOError:
			if(True):
				seasonId = levelId
				for lev in ['beginner', 'intermediate', 'advanced', 'allstar']:
					try:
						idPath = "./data/%s/%s/%s/teamId.csv" % (leagueId, lev, seasonId)
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
						seasons.append(watMuSeason(leagueId, lev, seasonId, teamIdList, True))
					except IOError:
						print "Unable to find level %s for %s, skipping" % (lev, seasonId)
			##except IOError:
			##	print "Unable to make levelId argument %s work, failing" % levelId
			##	return seasons
	for season in seasons:
		season.loadTierIV(seasons)
	return seasons



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


def graphTeams(leagueId, levelId, playoffTeamsOnly, dependents, independents):
	for depie in dependents:
		## SHUT UP YOURE A TERRIBLE VARIABLE NAME
		for indie in independents:
			plotScatterplot(indie.getShortStatName(), depie.getShortStatName(), '%s\nby %s\nfor %s, %s' % (depie.getLongStatName(), indie.getLongStatName(), leagueId, levelId), indie.getStat(playoffTeamsOnly), depie.getStat(playoffTeamsOnly), './results/%s/%s/%sBy' % (leagueId, levelId, depie.getShortStatName()), '%s' % indie.getShortStatName(), '%s_by_%s.png' % (depie.getShortStatName(), indie.getShortStatName()))		
			## wow, that was quick

def graphTeamsAgainstDeltas(leagueId, levelId, playoffTeamsOnly, dependents, independents):
	
	for depie in dependents:
		for indie in independents:
			
			thisIndieDeltas = getLinearModelDeltas(indie.getStat(playoffTeamsOnly), depie.getStat(playoffTeamsOnly))
			

			thisDeltasContainer = statContainer("%s_ModelDeltaFor_%s" % (indie.getShortStatName(), depie.getShortStatName()), "Model Deltas for the %s model for %s" % (indie.getLongStatName(), depie.getLongStatName()),  thisIndieDeltas, indie.getTeamIds(playoffTeamsOnly), indie.getTeamNames(playoffTeamsOnly), indie.getYears(playoffTeamsOnly), indie.getMadePlayoffsList(playoffTeamsOnly))
			plotVariablesDeltasHeatmap(leagueId, levelId, playoffTeamsOnly, depie.getShortStatName(), *[thisDeltasContainer]+[ind for ind in independents])
			
			print depie.getShortStatName(), " ", indie.getShortStatName(), " Model Deltas min ", min(thisIndieDeltas), " max ", max(thisIndieDeltas)
			for indiana in independents:
				plotScatterplot(indiana.getShortStatName(), "%s_ModelDeltas" % indie.getShortStatName(), 'Deltas from the %s Model for %s\nby %s\nfor %s %s' % (indie.getLongStatName(), depie.getLongStatName(), indiana.getLongStatName(), leagueId, levelId), indiana.getStat(playoffTeamsOnly), thisIndieDeltas, './results/%s/%s/%sBy' % (leagueId, levelId, depie.getShortStatName()), '%s/ModelDeltas/%s' % (indie.getShortStatName(), indiana.getShortStatName()), '%s_ModelDeltas_by_%s.png' % (indie.getShortStatName(), indiana.getShortStatName()))		

			## wow, that was quick


def graphTeamsHistogram(leagueId, levelId, playoffTeamsOnly, *variables):
	
	print type(variables)
	
	if(playoffTeamsOnly):
		thing = 'PlayoffTeam'
	else:
		thing = 'Total'
		
	for var in variables[0]:
		print type(var)
		plotHistogram(var.getShortStatName(), 'Count', 'Histogram of %s' % var.getLongStatName(), var.getStat(playoffTeamsOnly),'./results/%s/%s/histograms' % (leagueId, levelId), '%s' % var.getShortStatName(), '%s_%s_histogram.png' % (var.getShortStatName(), thing))			
		## wow, that was quick



def plotVariablesHeatmap(leagueId, levelId, playoffTeamsOnly, *variables):				
	
	print variables
	
	data = []
	headings = []
	
	for var in variables[0]:
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
	plotScatterMatrix(dataPanda, './results/%s/%s' % (leagueId, levelId), 'matrixScatterplot', 'AllPlayoffTeams_MatrixScatterplot.png')
	##plotScatterLabelled(dataTruong, 'GAA', 'GFA', 'Franchise', './results', '/%s/%s' % (leagueId, levelId), 'AllPlayoffTeams_LabelledScatterplot_GAA_GFA.png')

	seabornHeatmap(dataPanda, './results', '/%s/%s' % (leagueId, levelId), 'AllPlayoffTeams_Heatmap_%s_%s.png' % (leagueId, levelId))


def plotVariablesDeltasHeatmap(leagueId, levelId, playoffTeamsOnly, variableToPredict, *variables):				
	
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
	
	seabornHeatmap(dataPanda, './results', '%s/%s/%sBy' % (leagueId, levelId, variableToPredict), 'AllPlayoffTeams_%s_ModelDelta_Heatmap_%s_%s.png' % (variables[0].getShortStatName(), leagueId, levelId))



if(__name__ == "__main__"):
	##for i in range(192):
	##	printProgressBar(i, 192)
	
	seasons = getAllSeasons('nhl', 'everything')
	##demoStatContainer(seasons, 'watMu', 'beginner') 
	foo = getStatContainer(Team.getMaAWQI, 'MaAWQI', 'Mean Adjusted Average Win Quality Index', seasons, 'watMu', 'allstar')
