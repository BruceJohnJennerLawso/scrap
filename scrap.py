################################################################################
## python file that takes parameters describing the league/level that we want ##
## to scrape and saves the teams in the seasons specified into csv files #######
################################################################################
from sys import argv
import csv

import watMuScraper
import nhlScraper
	
def scrapeListedTeams(debugInfo, leagueId, levelId):
	if((leagueId == 'nhl')or(leagueId == 'wha')):
		## everything else besides watMu teams
		with open('./data/%s/%s/seasons.csv' % (leagueId, levelId), 'rb') as foo:
			reader = csv.reader(foo)
			## open up the seasons manifest file to get a list of all of the
			## seasons that we will be scraping for this league
			for row in reader:
				idPath = "./data/%s/%s/teamId.csv" % (leagueId, row[0])
				with open(idPath, 'rb') as bar:
					## for each season that we will be scraping, open up the
					## manifest file to get a list of teamIds that will need to
					## be scraped
					reading = csv.reader(bar)
					for teamId in reading:
						if(len(teamId) == 1):
							nhlScraper.scrapeTeamData(teamId[0], debugInfo, row[0], False, leagueId)		
						else:
							if(teamId[1] == 'NoScrape'):
								print "Skipping %s team %s %s" % (leagueId, teamId[0], row[0])
								##exit() 
								continue
							
						
	else:
		with open('./data/%s/%s/seasons.csv' % (leagueId, levelId), 'rb') as foo:
			reader = csv.reader(foo)
			for row in reader:
				idPath = "./data/%s/%s/%s/teamId.csv" % (leagueId, levelId, row[0])
				with open(idPath, 'rb') as bar:
					reading = csv.reader(bar)
					for teamId in reading:
						watMuScraper.scrapeTeamData(int(teamId[0]), debugInfo, row[0], False, leagueId, levelId, True)


if(__name__=="__main__"):
	
	
	print 'Arguments:\n', argv
	
	leagueId = argv[1]
	## ie 'nhl' or 'watMu'

	levelId = argv[2]
	scrapeListedTeams(True, leagueId, levelId)

	

