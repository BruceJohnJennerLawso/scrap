################################################################################
from sys import argv

import csv

from scraper import *


def scrapeListedTeams(debugInfo):
	with open('./data/watMu/beginner/seasons.csv', 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			idPath = "./data/watMu/beginner/%s/teamId.csv" % row[0]
			with open(idPath, 'rb') as bar:
				reading = csv.reader(bar)
				for teamId in reading:
					scrapeTeamData(int(teamId[0]), debugInfo, row[0], False)
					##if(int(teamId[0]) == 8481):
					##	return 0
						## force a crash here so I can inspect this particular team


if(__name__=="__main__"):
	
	
	scrapeListedTeams(False)
	
	
	##teamIdList = [12313, 12348]
	
	##for Id in teamIdList:
	##	scrapeTeamData(Id, False, "fall2015")
	##scrapeTeamData(12340, True, "fall2015")
