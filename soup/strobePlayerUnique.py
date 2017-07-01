## strobePlayerUnique.py #######################################################
## now that strobe is pulled out of the team pages (mostly), I want to use a ###
## sort of hack in the strobe website that allows uniquely identifying a #######
## based on their uwaterloo email (ie jjlastname#@uwaterloo.ca) ################
## so our first step here is to log into the old strobe player panel ###########
## (for which selenium will be needed of course), then walk across the spread ##
## of teamIds that we have as our targets and create a csv from the available ##
## names & uwaterloo emails linked there #######################################
##
## for example, Mighty Dads fall 2015 can be found at
##
## https://strobe.uwaterloo.ca/athletics/intramurals/tools/
## /teams/index.php?roster=12348&sport=1
##
## but that url apparently can be fuzzed to cover every single team on the #####
## site, probably not how this service was originally intended to work, but ####
## it helps me get the data I need, so Ill take whatever I can get #############
################################################################################
#!/usr/bin/env python
from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
from bs4 import BeautifulSoup

import time
import sys
from sys import argv
import string
import csv
import os

import watMuSportInfo



def convertShortLinkHrefUrlToFull(shortLink):
	output = string.replace(shortLink, "https://www.imleagues.com", "")
	return "https://www.imleagues.com%s" % output


def scrapePlayerInfoFromStrobeTeamPanel(browser, teamId, levelId, sportId, seasonId):
	browser.get("https://strobe.uwaterloo.ca/athletics/intramurals/tools/teams/index.php?roster=%i&sport=%i" % (teamId, sportId))
	page_source = browser.page_source
	teamPlayersSoup = BeautifulSoup(page_source, 'html.parser')
	teamPlayersSoup = teamPlayersSoup.find(lambda tag: tag.name=='table') 
	print teamPlayersSoup
	
if(__name__ == "__main__"):
	sports = watMuSportInfo.sportsInfoDict()

	sportIds = [28, 4, 3, 5, 11, 7, 1, 31, 10, 6, 2, 8, 17, 26, 18, 16]	
	##sportIds = [ 17, 26, 18, 16]
	##sportIds = [16]	
	
	years = range(2008, 2017)
	
	def getTermById(termId):
		if(termId == 1):
			return "winter"
		elif(termId == 2):
			return "spring"
		if(termId == 4):
			return "fall"						
	
	terms = [1,2,4]
	## it goes winter, spring, fall
	## makes no sense to me either how they picked the term numbers
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11256"
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=7627"
	
	
	
	
	
	if(len(argv) >= 2):
		uwaterlooId = argv[1]
	else:
		uwaterlooId = getTextInput("Please Input Uwaterloo Id: ")
		## technically some people did change their passwords, but any access
		## will do here, so Im just going to use one of the many accounts that
		## had the same username and password (uwaterloo student number)
		##password = getTextInput("Please Input Password: ")		
	
	print uwaterlooId
	url = "https://strobe.uwaterloo.ca/athletics/intramurals/tools/"
	
	firefox_options = webdriver.FirefoxProfile()
	prefs = {"dom.webnotifications.enabled" : False}
	firefox_options.set_preference('dom.webnotifications.enabled', False)
	firefox_options.set_preference('dom.webnotifications.serviceworker.enabled', False)	
	


	with closing(Firefox(firefox_options)) as browser:	



		browser.get(url)
		element = browser.find_element_by_id("userid")
		element.send_keys(uwaterlooId)
		element = browser.find_element_by_id("password")
		element.send_keys(uwaterlooId)	
		
		buttonId = "//input[@value='Submit']"	
		WebDriverWait(browser, timeout=10).until(
				lambda x: x.find_element_by_xpath(buttonId))
		button = browser.find_element_by_xpath(buttonId)
		button.click()
		while(browser.current_url != "https://strobe.uwaterloo.ca/athletics/intramurals/tools/tools.php"):
			pass
		print "Finished signing into strobe uwaterloo player panel"
		
		
		
	
		for sport in sportIds:
					
			sportId = sport
			sportName = sports[sportId][0]
			rulesSpec = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
			##print sports[sportId][4]
			if(sports[sportId][4] == "tournament"):
				##print "tournament"
				rulesPath = "%s-%s-%s_tournament" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])			
			else:
				rulesPath = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])		
			levelIdList = ['beginner', 'intermediate', 'advanced', 'allstar', 'allstarContact', 'any']
			if(sportId in [16,17,18,26]):
				levelIdList += ['beckham', 'figo', 'maradona', 'pele', 'ronaldinho', 'jordan', 'kobeBryant', 'lebronJames']
				## when I go completely nuts, please refer to this as the reason why
			for levelId in levelIdList:
				for year in years:
					for term in [getTermById(id_) for id_ in terms]:
						seasonId = "%s%i" % (term, year)
						file_path = "./data/%s/%s/watMu/%s/%s/teamId.csv" % (sports[sportId][0], rulesPath, levelId, seasonId)	
						try:
							with open(file_path, 'rb') as foo:
								reader = csv.reader(foo)
								print file_path, " Exists"
								for row in reader:
									teamId = row[0]
									##print teamId, seasonId, levelId, sportId, sportName
									scrapePlayerInfoFromStrobeTeamPanel(browser, int(teamId), levelId, sportId, seasonId)
								print "\n" 
						except IOError:
							pass
		
		##browser.get("https://strobe.uwaterloo.ca/athletics/intramurals/tools/teams/index.php?roster=12348&sport=1")
		##page_source = browser.page_source
		

