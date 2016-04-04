################################################################################
from sys import argv

import csv

from scraper import *


def scrapeListedTeams(debugInfo):
	with open('./data/seasons.csv', 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			idPath = "./data/%s/teamId.csv" % row[0]
			with open(idPath, 'rb') as bar:
				reading = csv.reader(bar)
				for teamId in reading:
					scrapeTeamData(int(teamId[0]), debugInfo, row[0])


if(__name__=="__main__"):
	
	
	scrapeListedTeams(False)
	
	
	##teamIdList = [12313, 12348]
	
	##for Id in teamIdList:
	##	scrapeTeamData(Id, False, "fall2015")
	##scrapeTeamData(12340, True, "fall2015")
