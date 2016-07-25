################################################################################
from sys import argv
import csv

import watMuScraper
import nhlScraper
	
def scrapeListedTeams(debugInfo, leagueId, levelId=False):
	if(levelId == False):
		with open('./data/%s/seasons.csv' % (leagueId), 'rb') as foo:
			reader = csv.reader(foo)
			for row in reader:
				idPath = "./data/%s/%s/teamId.csv" % (leagueId, row[0])
				with open(idPath, 'rb') as bar:
					reading = csv.reader(bar)
					for teamId in reading:
						nhlScraper.scrapeTeamData(teamId[0], debugInfo, row[0], False, leagueId)		
	else:
		with open('./data/%s/%s/seasons.csv' % (leagueId, levelId), 'rb') as foo:
			reader = csv.reader(foo)
			for row in reader:
				idPath = "./data/%s/%s/%s/teamId.csv" % (leagueId, levelId, row[0])
				with open(idPath, 'rb') as bar:
					reading = csv.reader(bar)
					for teamId in reading:
						watMuScraper.scrapeTeamData(int(teamId[0]), debugInfo, row[0], False, leagueId, levelId)


if(__name__=="__main__"):
	
	print argv
	
	leagueId = argv[1]
	if(leagueId == 'nhl'):
		scrapeListedTeams(True, leagueId)
	else:
		levelId = argv[2]
		scrapeListedTeams(False, leagueId, levelId)
	##leagueId = 'watMu'
	##levelId = 'beginner'
	## ids needed to open the proper folders and csv files contained within
	

