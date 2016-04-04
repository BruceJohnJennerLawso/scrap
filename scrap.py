################################################################################
from sys import argv

import csv

from scraper import *

if(__name__=="__main__"):
	with open('./data/seasons.csv', 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			print row
	
	
	##teamIdList = [12313, 12348]
	
	##for Id in teamIdList:
	##	scrapeTeamData(Id, False, "fall2015")
	##scrapeTeamData(8481, False, "winter2013")
