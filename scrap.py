################################################################################
from sys import argv
import csv

from scraper import *


def scrapeListedTeams(debugInfo, leagueId, levelId):
	with open('./data/%s/%s/seasons.csv' % (leagueId, levelId), 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			idPath = "./data/%s/%s/%s/teamId.csv" % (leagueId, levelId, row[0])
			with open(idPath, 'rb') as bar:
				reading = csv.reader(bar)
				for teamId in reading:
					scrapeTeamData(int(teamId[0]), debugInfo, row[0], False)


if(__name__=="__main__"):
	
	print argv
	
	leagueId = argv[1]
	levelId = argv[2]
	
	##leagueId = 'watMu'
	##levelId = 'beginner'
	## ids needed to open the proper folders and csv files contained within
	scrapeListedTeams(False, leagueId, levelId)
