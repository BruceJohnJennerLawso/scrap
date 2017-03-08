################################################################################
## python file that takes parameters describing the league/level that we want ##
## to scrape and saves the teams in the seasons specified into csv files #######
################################################################################
from sys import argv
import csv

import watMuScraper
import nhlScraper
	
import perfectlyNormalUser
import time	
import random
	
class scrapeTeamParams(object):
	def __init__(self, leagueId, levelId, seasonId, teamId):
		self.leagueId = leagueId
		self.levelId = levelId
		self.seasonId = seasonId
		self.teamId = teamId
	
	def params(self):
		print "\n\n#########\n%s\n%s\n%s\n%s\n" % (self.leagueId, self.levelId, self.seasonId, self.teamId)
def scrapeListedTeams(debugInfo, leagueId, levelId):
	initialTime = time.time()

	teamParams = []
	
	## indicates this is the first loop of the scraper
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
							teamParams.append(scrapeTeamParams(leagueId, levelId, row[0], teamId[0]))
							##nhlScraper.scrapeTeamData(teamId[0], debugInfo, row[0], False, leagueId)		
							##deltaTime = time.time() - lastTime
							##lastTime = time.time()
							
						else:
							if(teamId[1] == 'NoScrape'):
								print "Skipping %s team %s %s" % (leagueId, teamId[0], row[0])
								continue
		random.shuffle(teamParams)
		
		lastTime = time.time()
		deltaTime = 0.0
		overflowTime = 0.0
		
		for teamScrape in teamParams:
			thisVisitLength = perfectlyNormalUser.sampleWebPageVisitLength()
			if(thisVisitLength*0.5 > overflowTime):
				thisVisitLength -= overflowTime
				overflowTime = 0.0

			nhlScraper.scrapeTeamData(teamScrape.teamId, debugInfo, teamScrape.seasonId, False, teamScrape.leagueId)
			teamScrape.params()
			print "this visit taking %.3f s" % thisVisitLength
			deltaTime = time.time() - lastTime
			lastTime = time.time()	
			if(deltaTime > thisVisitLength):
				## took too long on this visit due to the time that generating
				## a visit length/actually scraping the data being longer than
				## this visit actually had allocated, so we'll haphazardly deal
				## with it by making a future visit shorter
				
				overflowTime = deltaTime - thisVisitLength
				print "visit overflowing length by %.3f seconds, will make up elsewhere" % overflowTime
			elif(deltaTime < thisVisitLength):
				while(deltaTime < thisVisitLength):
					deltaTime = time.time() - lastTime
					##lastTime = time.time()	
	else:
		with open('./data/%s/%s/seasons.csv' % (leagueId, levelId), 'rb') as foo:
			reader = csv.reader(foo)
			for row in reader:
				idPath = "./data/%s/%s/%s/teamId.csv" % (leagueId, levelId, row[0])
				with open(idPath, 'rb') as bar:
					reading = csv.reader(bar)
					for teamId in reading:
						watMuScraper.scrapeTeamData(int(teamId[0]), debugInfo, row[0], False, leagueId, levelId, True)

	print "scrape finished in %.3f s" % (time.time()-initialTime)
	
if(__name__=="__main__"):
	
	
	print 'Arguments:\n', argv
	
	leagueId = argv[1]
	## ie 'nhl' or 'watMu'

	levelId = argv[2]
	scrapeListedTeams(True, leagueId, levelId)

	

