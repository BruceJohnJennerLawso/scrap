################################################################################
from sys import argv

import csv

from scraper import *

if(__name__=="__main__"):
	teamIdList = [12313, 12348]
	
	for Id in teamIdList:
		scrapeTeamData(Id, False, "Fall 2015")
	scrapeTeamData(8481, True, "Winter 2013")
