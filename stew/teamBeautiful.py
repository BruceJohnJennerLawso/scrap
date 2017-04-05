## teamBeautiful.py ############################################################
## now that the team data is (hopefully) saved to html file in raw form, it
## needs to be broken down into the kilobyte or two of relevant data about the
## team that gets saved to csv. Sooo, I need to load up the data in beautiful
## soup and process the important data out of it
################################################################################
#!/usr/bin/env python

from gameProcessing import *

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
import codecs

def convertShortLinkHrefUrlToFull(shortLink):
	output = string.replace(shortLink, "https://www.imleagues.com", "")
	return "https://www.imleagues.com%s" % output

def getLinksFromSoup(soup):
	output = []
	gameRows = soup.find_all(lambda tag: tag.name=='tr' and tag.has_attr('rowgameid'))
	i = 0
	for row in gameRows:
		i += 1
		for link in row.find_all(lambda tag: tag.name=='a'and (not tag.has_attr('class'))):
			##print i, link, "\n",  link['href'], "\n\n"
			if link['href'] not in output:
				output.append(link['href'])
	return output

def getLinkedPagesFromUrl(browser, url, alreadyLookedAt=[], depth=0):
	print " "*depth, string.replace(url, "https://www.imleagues.com", ""), depth, len(alreadyLookedAt)
	driver = browser
	
	browser.get(url)
	##driver.manage().timeouts().pageLoadTimeout(20, TimeUnit.SECONDS);
	time.sleep(10)
	##print driver.find_element_by_tag_name('html'), driver.find_element_by_tag_name('html').text, driver.find_element_by_tag_name('html').get_attribute('innerHTML')
		
		
	loadedHtmlContent = driver.find_element_by_tag_name('html').get_attribute('innerHTML').encode('utf8')
	
	
	totalList = []
				
	##soup = BeautifulSoup("%s" % loadedHtmlContent, "lxml")
	soup = BeautifulSoup("%s" % loadedHtmlContent, 'html.parser')
	extractedLinks = getLinksFromSoup(soup)
	extractedLinks = [convertShortLinkHrefUrlToFull(li) for li in extractedLinks]
	##print "extractedLinks, ", extractedLinks
	extractedLinks = [links for links in extractedLinks if links not in alreadyLookedAt]
	extractedLinks = [links for links in extractedLinks if links not in [convertShortLinkHrefUrlToFull("/spa/team//home")]]
	##print "extractedLinks, ", extractedLinks
	for link in extractedLinks:
		if((link not in [convertShortLinkHrefUrlToFull(url)])and(link not in alreadyLookedAt)):
			linkedPagesOutput = getLinkedPagesFromUrl(browser, link, alreadyLookedAt+extractedLinks+[convertShortLinkHrefUrlToFull(url)], depth+1)
			alreadyLookedAt += linkedPagesOutput
			totalList += linkedPagesOutput
			##print linkedPagesOutput, len(linkedPagesOutput)
	return totalList+[convertShortLinkHrefUrlToFull(url)]


def getTextInput(prompt):
	output = ""
	while(output == ""):
		print prompt,
		output = raw_input()
	return output


def goToLink(browser, url):
	browser.get(url)
	##driver.manage().timeouts().pageLoadTimeout(20, TimeUnit.SECONDS);
	time.sleep(10)
	
	
def saveLinkToHtmlFileWithJsContent(browser, url, output_path):
	browser.get(url)
	##driver.manage().timeouts().pageLoadTimeout(20, TimeUnit.SECONDS);
	time.sleep(10)	
	loadedHtmlContent = browser.find_element_by_tag_name('html').get_attribute('innerHTML').encode('utf8')
	
	
def saveTeamDataInLinkToRawHtml(browser, initialTeamUrl, sportId, levelId, seasonId, teamId):
	sports = {\
	 28:['soccer', 'outdoor', 'grass', '4-7vs_1GK', 'league'],\
	 4 :['hockey', 'indoor', 'floor', '3-4vs_1GK', 'league'],\
	 3 :['basketball', 'indoor', 'floor', '4-5vs_0GK', 'league'],\
	 5 :['dodgeball', 'indoor', 'floor', '6-8vs_0GK', 'league'],\
	 11:['flag_football', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 7 :['soccer', 'indoor', 'floor', '3-5vs_1GK', 'league'],\
	 1 :['hockey', 'indoor', 'ice', '6-6vs_1GK', 'league'],\
	 31:['ultimate', 'indoor', 'floor', '3-4vs_0GK', 'league'],\
	 10:['slowpitch', 'outdoor', 'grass', '8-10vs_0GK', 'league'],\
	 6 :['soccer', 'outdoor', 'grass', '7-11vs_1GK', 'league'],\
	 2 :['ultimate', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 8 :['volleyball', 'indoor', 'floor', '4-6vs_0GK', 'league'],\
	 17:['soccer', 'indoor', 'floor', '2-3vs_0GK', 'tournament'],\
	 26:['basketball', 'outdoor', 'ashphalt', '2-3vs_0GK', 'tournament'],\
	 18:['dodgeball', 'indoor', 'floor', '7-8vs_0GK_hunger_games', 'tournament'],\
	 16:['basketball', 'indoor', 'floor', '2-3vs_0GK', 'tournament']\
	 }
	sportIds = [28, 4, 3, 5, 11, 7, 1, 31, 10, 6, 2, 8, 17, 26, 18, 16]

	contentParts = {"teamData":"/home", "rosterData":"/roster"}

	for part in contentParts:
			

		browser.get("%s%s" % (initialTeamUrl, contentParts[part]))
		time.sleep(20)
		
		loadedHtmlContent = browser.find_element_by_tag_name('html').get_attribute('innerHTML').encode('utf8')

		if(sports[sportId][4] == "tournament"):
			rulesPath = "%s-%s-%s_tournament" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
		else:
			rulesPath = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
			
		file_path = "./data/%s/%s/watMu/%s/%s/%s/%s.html" % (sports[sportId][0], rulesPath, levelId, seasonId, teamId, part)	
		directory = os.path.dirname(file_path)
		try:
			os.stat(directory)
		except:
			os.makedirs(directory)	
		f = open(file_path, "wb")
		writer = csv.writer(f)
		
		##for row in thisLevelTeamIds:
		writer.writerow(["%s" % loadedHtmlContent])
		f.close()

##<span class="date-month">Sep</span><br><span class="date-day">26
def getScheduleTableFromSoup(soup):
	headerRow = ['Game Name', 'Month', 'Day', 'Result', 'Score For', 'Score Against', 'Location', 'opponent', 'opponentTeamId', 'Raw Result', 'linkToGame', 'MVP']
	outputRows = []
	gameRows = soup.find_all(lambda tag: tag.name=='tr' and tag.has_attr('rowgameid'))
	i = 0
	for row in gameRows:
		rowContent = []
		rowContent.append(row['rowgameid'].encode("utf-8"))
		## the listed value of the attribute rowgameid for this game,
		## essentially a quick marker of the game type (R-regular season, 
		## P-playoffs), followed by the imleagues id number for the game
		rowContent.append(row.find(lambda tag: tag.name=='span', {"class": "date-month"} ).getText().encode("utf-8"))
		rowContent.append(row.find(lambda tag: tag.name=='span', {"class": "date-day"} ).getText().encode("utf-8"))	
		## just like it sounds, the month of the game in short form
		## (October -> Oct, September -> Sep), and the numeric day of the month
		## Time of game is available in the game page info, but not here, which
		## is annoying, but oh well
		gameResults = [row.find(lambda tag: tag.name=='span', {"style": "color: green; font-size: large; font-weight: bold;"} )] + [row.find(lambda tag: tag.name=='span', {"style": "color: red; font-size: large; font-weight: bold;"} )] + [row.find(lambda tag: tag.name=='span', {"style": "color: black; font-size: large; font-weight: bold;"} )]
		## eggh yuck
		for res in gameResults:
			if(res != None):
				rowContent.append(res.getText().encode("utf-8"))
				try:
					goalsFor, goalsAgainst = processGoalsForAgainst(res.parent.getText().encode("utf-8"))
				except ValueError:
					goalsFor = -1
					goalsAgainst = -1
				rowContent.append(goalsFor)
				rowContent.append(goalsAgainst)
		## this part gets a bit hairy because its so tricky to positively id the
		## span thats got the game result and score, the only thing that can pin
		## it down accurately is that blasted style attribute, which is long,
		## and the colour attribute changes based on whether the game was a win,
		## loss, tie
		rowContent.append(row.find(lambda tag: tag.name=='span', {"class": "text-muted"} ).parent.getText().encode("utf-8"))	
		## Location of the game, ie 'CIFField 2', or 'CIFWarrior Field', which
		## is all messed up because of the way the location is stored across a
		## nested element, so this will definitely require post-processing to
		## properly match the 
		
		## this is just really, really bad, because theres another span right
		## after this one containing the game mvp data that fits these exact
		## parameters, the only reason this is working is because the location
		## data is always coming before the mvp data, but I shudder to think of
		## what might happen if it isnt arranged that way
		##
		## oh well, life is too short to worry about all of the ways my code
		## might faceplant
		link = row.find(lambda tag: tag.name=='a'and (not tag.has_attr('class')))
			##print i, link, "\n",  link['href'], "\n\n"
		rowContent.append(stripAnyCommasFromTeamName(link.getText().encode("utf-8"))[1:])
			
		rowContent.append(convertTeamUrlToTeamId(link['href'].encode("utf-8")))
		for res in gameResults:
			if(res != None):
				##rowContent.append(res.getText().encode("utf-8"))	
				rowContent.append(res.parent.getText().encode("utf-8"))	
		rowContent.append(row.parent.parent.parent['href'].encode("utf-8"))	
		## go upwards by 3 layers of html elements to grab the true link to this
		## particular games game page, which contains lots of useful information
		## not included here 

		rowContent.append(row.find(lambda tag: tag.name=='td', {"ng-bind-html": "trustAsHtml(item.mvps)"} ).getText().encode("utf-8"))						
					
		mvpLinks = row.find(lambda tag: tag.name=='td', {"ng-bind-html": "trustAsHtml(item.mvps)"} ).findAll(lambda tag: tag.name=='a')
		if(mvpLinks != None):
			for mvpLink in mvpLinks:
				rowContent.append(convertPlayerUrlToPlayerId(mvpLink['href'].encode("utf-8"))) 							
		

		outputRows.append(rowContent)
	maxRowWidth = max([len(row) for row in outputRows])
	print maxRowWidth
	
	
	for row in outputRows:
		if(len(row) < maxRowWidth):
			for i in range(maxRowWidth - len(row)):
				row.append('')
	if(len(headerRow) < maxRowWidth):
		for i in range(maxRowWidth - len(headerRow)):
			headerRow.append('mvpId%i' % (i+1))
	return (headerRow, outputRows)


def getTeamRosterTable(soup):
	headerRow = ['Player', 'imlPlayerId', 'Captaincy', 'Gender']
	outputRows = []
	
	rosterSoup = soup.find(lambda tag: tag.name=='ul' and tag.has_attr('ng-show'), {"class": "list-group"})
	##<ul class="list-group" ng-show=" !isDetail &amp;&amp; initData.teamRosters.length>0">
	
	for playah in rosterSoup.find_all(lambda tag: tag.name=='div', {"class":"media"}):
		playahName = playah.find(lambda tag: tag.name=='a').getText().encode("utf-8")
		playahLink = playah.find(lambda tag: tag.name=='a')['href'].encode("utf-8")
		playahGender = playah.find(lambda tag: tag.name=='div', {"class":"media-body"}).contents[-1].encode("utf-8")
		playahGender = stripStringOfPieces(playahGender, [" ", "\n"])
		##<div class="media-body">
		
		def convertImlCaptaincyToStandard(imlCaptaincyString):
			if(imlCaptaincyString == '(Captain)'):
				return '(C)'
			elif(imlCaptaincyString == '(Co-Captain)'):
				return '(A)'
			else:
				return ''
				## there could be more designations, but Im not aware of any
				## just yet	
				
				## this function takes what IMLeagues displays and makes it
				## standard with how the strobe uwaterloo dump displayed player
				## data		
		playahCaptaincy = playah.find(lambda tag: tag.name=='small').getText().encode("utf-8")
		playahCaptaincy = convertImlCaptaincyToStandard(playahCaptaincy)
		outputRow = [playahName, convertPlayerUrlToPlayerId(playahLink), playahCaptaincy, playahGender]
		for s in outputRow:
			print repr(s),
		print "\n"
		outputRows.append(outputRow)
	##<div class="media">
	
	return (headerRow, outputRows)



def scrapeImlTeam(sportId, levelId, seasonId, teamId):
	sports = {\
	 28:['soccer', 'outdoor', 'grass', '4-7vs_1GK', 'league'],\
	 4 :['hockey', 'indoor', 'floor', '3-4vs_1GK', 'league'],\
	 3 :['basketball', 'indoor', 'floor', '4-5vs_0GK', 'league'],\
	 5 :['dodgeball', 'indoor', 'floor', '6-8vs_0GK', 'league'],\
	 11:['flag_football', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 7 :['soccer', 'indoor', 'floor', '3-5vs_1GK', 'league'],\
	 1 :['hockey', 'indoor', 'ice', '6-6vs_1GK', 'league'],\
	 31:['ultimate', 'indoor', 'floor', '3-4vs_0GK', 'league'],\
	 10:['slowpitch', 'outdoor', 'grass', '8-10vs_0GK', 'league'],\
	 6 :['soccer', 'outdoor', 'grass', '7-11vs_1GK', 'league'],\
	 2 :['ultimate', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 8 :['volleyball', 'indoor', 'floor', '4-6vs_0GK', 'league'],\
	 17:['soccer', 'indoor', 'floor', '2-3vs_0GK', 'tournament'],\
	 26:['basketball', 'outdoor', 'ashphalt', '2-3vs_0GK', 'tournament'],\
	 18:['dodgeball', 'indoor', 'floor', '7-8vs_0GK_hunger_games', 'tournament'],\
	 16:['basketball', 'indoor', 'floor', '2-3vs_0GK', 'tournament']\
	 }
	
	
	
	if(sports[sportId][4] == "tournament"):
		rulesPath = "%s-%s-%s_tournament" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
	else:
		rulesPath = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
			
	file_path = "./data/%s/%s/watMu/%s/%s/%s/" % (sports[sportId][0], rulesPath, levelId, seasonId, teamId)	
	
	f=codecs.open("%s/rosterData.html" % file_path, 'r')
	##print f.read()
	peopleSoup = BeautifulSoup("%s" % f.read(), 'html.parser')
	f.close()

	f=codecs.open("%s/teamData.html" % file_path, 'r')
	teamSoup = BeautifulSoup("%s" % f.read(), 'html.parser')
	f.close()
	
	
	teamNameString = teamSoup.find(lambda tag: tag.name=='title')
	print teamNameString
	
	teamName = stripStringOfPieces(teamNameString.getText().encode("utf-8"), ["IMLeagues | ", ","])
	teamName = teamName[:teamName.index('(')]
	print teamName
	header, gameRows = getScheduleTableFromSoup(teamSoup)
	
	seasonGamesTable = [gm for gm in gameRows if (gm[0][0] == "R")]
	playoffGamesTable = [gm for gm in gameRows if (gm[0][0] == "P")]	
	
	teamRosterHeading, teamRoster = getTeamRosterTable(peopleSoup)
	
	gameLinkEx = gameRows[0][10]
	imlSeasonId = stripStringOfPieces(gameLinkEx, ["/spa/league/", "viewgame?gameId=", "&gameType=0"])
	imlSeasonId = imlSeasonId[:imlSeasonId.index('/')]
	
	print header, len(header)
	for gm in gameRows:
		print gm, len(gm)


	output_file_path = "./data/%s/%s/watMu/%s/%s/%s.csv" % (sports[sportId][0], rulesPath, levelId, seasonId, teamId)	
	print output_file_path


	directory = os.path.dirname(output_file_path)
	try:
		os.stat(directory)
	except:
		os.makedirs(directory)	
	f = open(output_file_path, "wb")
	writer = csv.writer(f)
	writer.writerow(['INFO:'])
	writer.writerow(['teamName', teamName])	
	writer.writerow(['teamAbbreviation', teamName])	
	writer.writerow(['sportId', sportId])		
	writer.writerow(['sportName', sports[sportId][0]])
	writer.writerow(['sportRules', rulesPath])		
	writer.writerow(['leagueId', 'watMu'])	
	writer.writerow(['levelId', levelId])			
	writer.writerow(['seasonName', seasonId])
	writer.writerow(['seasonId', imlSeasonId])	
	writer.writerow(['Roster Size',len(teamRoster)])	
	writer.writerow(['Season Games Played',len(seasonGamesTable)])	
	playoffRoundLengths = [1 for playoffRound in playoffGamesTable]
	if(1 not in playoffRoundLengths):
		playoffRoundLengths.append(0)
		## this is going to need to be fixed afterwards anyways, might as well
		## leave it as is I guess
	writer.writerow(['Playoff Round Lengths']+playoffRoundLengths)
	writer.writerow(['END_INFO'])
	writer.writerows([''])
	writer.writerow(['SEASON:'])
	
	writer.writerow(header)
	for row in seasonGamesTable:
		writer.writerow(row)
	writer.writerow(['END_SEASON'])
	writer.writerows([''])
	writer.writerow(['PLAYOFFS:'])
	writer.writerow(header)
	for row in playoffGamesTable:
		writer.writerow(row)
	writer.writerow(['END_PLAYOFFS'])
	writer.writerows([''])
	writer.writerow(['ROSTER:'])
	if(teamRosterHeading[0][0] != 'Roster Unavailable'):
		writer.writerow(teamRosterHeading)	
		for row in teamRoster:
			writer.writerow(row)	
	else:
		print "empty roster at %s" % teamId
		writer.writerow(['Roster Unavailable'])				
	writer.writerow(['END_ROSTER'])
	f.close()
							
	print "...Finished writing csv\n"
	
if(__name__ == "__main__"):
	##28 intermediate fall2016 0f02ca55c5ee4765bc53c72eb88a6def
	##scrapeImlTeam(28, 'intermediate', 'fall2016', '0f02ca55c5ee4765bc53c72eb88a6def')	
	##scrapeImlTeam(1, 'beginner', 'fall2016', '245ae04604684f40a40d7257467879c1')
	##exit()
	##print "\n\n"
	##scrapeImlTeam(6, 'intermediate', 'fall2016', '8a9d20afe4f240479156ad9977e60223')	
	##print "\n\n"
	##scrapeImlTeam(6, 'advanced', 'fall2016', 'c8770aa242584fc89dc1deb33c092f93')
	sports = {\
	 28:['soccer', 'outdoor', 'grass', '4-7vs_1GK', 'league'],\
	 4 :['hockey', 'indoor', 'floor', '3-4vs_1GK', 'league'],\
	 3 :['basketball', 'indoor', 'floor', '4-5vs_0GK', 'league'],\
	 5 :['dodgeball', 'indoor', 'floor', '6-8vs_0GK', 'league'],\
	 11:['flag_football', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 7 :['soccer', 'indoor', 'floor', '3-5vs_1GK', 'league'],\
	 1 :['hockey', 'indoor', 'ice', '6-6vs_1GK', 'league'],\
	 31:['ultimate', 'indoor', 'floor', '3-4vs_0GK', 'league'],\
	 10:['slowpitch', 'outdoor', 'grass', '8-10vs_0GK', 'league'],\
	 6 :['soccer', 'outdoor', 'grass', '7-11vs_1GK', 'league'],\
	 2 :['ultimate', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 8 :['volleyball', 'indoor', 'floor', '4-6vs_0GK', 'league'],\
	 17:['soccer', 'indoor', 'floor', '2-3vs_0GK', 'tournament'],\
	 26:['basketball', 'outdoor', 'ashphalt', '2-3vs_0GK', 'tournament'],\
	 18:['dodgeball', 'indoor', 'floor', '7-8vs_0GK_hunger_games', 'tournament'],\
	 16:['basketball', 'indoor', 'floor', '2-3vs_0GK', 'tournament']\
	 }


	semesters = ["fall2016"]	
	for semester in semesters:
				
		with open('%shooks.csv' % semester, 'rb') as f:
			reader = csv.reader(f)
			i = 0
			for row in reader:
				print row
				##teamId = row[0]
				sportId = int(row[1])
				levelId = row[2]
				seasonId = semester
				if(sports[sportId][4] == "tournament"):
					rulesPath = "%s-%s-%s_tournament" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
				else:
					rulesPath = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
			
				file_path = "./data/%s/%s/watMu/%s/%s/teamId.csv" % (sports[sportId][0], rulesPath, levelId, seasonId)	
				with open(file_path, 'rb') as ff:
					tm_reader = csv.reader(ff)
					for tm_row in tm_reader:
						teamId = tm_row[0]
						print sportId, levelId, seasonId, teamId
						scrapeImlTeam(sportId, levelId, seasonId, teamId)





















if(__name__ == "__grain__"):
	sports = {\
	 28:['soccer', 'outdoor', 'grass', '4-7vs_1GK', 'league'],\
	 4 :['hockey', 'indoor', 'floor', '3-4vs_1GK', 'league'],\
	 3 :['basketball', 'indoor', 'floor', '4-5vs_0GK', 'league'],\
	 5 :['dodgeball', 'indoor', 'floor', '6-8vs_0GK', 'league'],\
	 11:['flag_football', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 7 :['soccer', 'indoor', 'floor', '3-5vs_1GK', 'league'],\
	 1 :['hockey', 'indoor', 'ice', '6-6vs_1GK', 'league'],\
	 31:['ultimate', 'indoor', 'floor', '3-4vs_0GK', 'league'],\
	 10:['slowpitch', 'outdoor', 'grass', '8-10vs_0GK', 'league'],\
	 6 :['soccer', 'outdoor', 'grass', '7-11vs_1GK', 'league'],\
	 2 :['ultimate', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 8 :['volleyball', 'indoor', 'floor', '4-6vs_0GK', 'league'],\
	 17:['soccer', 'indoor', 'floor', '2-3vs_0GK', 'tournament'],\
	 26:['basketball', 'outdoor', 'ashphalt', '2-3vs_0GK', 'tournament'],\
	 18:['dodgeball', 'indoor', 'floor', '7-8vs_0GK_hunger_games', 'tournament'],\
	 16:['basketball', 'indoor', 'floor', '2-3vs_0GK', 'tournament']\
	 }

	## add this line
	
	if(len(argv) >= 3):
		username = argv[1]
		password = argv[2]
		if(len(argv) >= 4):
			semester = argv[3]
		else:
			semester = getTextInput("Please Input Desired semester: ")
	else:
		username = getTextInput("Please Input Username: ")
		password = getTextInput("Please Input Password: ")		
	
	
	url = "https://www.imleagues.com/spa/team/662222b25eb54b88b4eebb4090cb455a/home"
	
	with closing(Firefox()) as browser:

		##driver = webdriver.Firefox()

		driver = browser
	

		driver.get("https://nike.uwaterloo.ca/Login.aspx?soi=IM&ref=Intramurals")
		element = driver.find_element_by_id("ctl00_contentMain_ASPxRoundPanel2_loginMain_UserName_I")
		element.send_keys(username)
		element = driver.find_element_by_id("ctl00_contentMain_ASPxRoundPanel2_loginMain_Password_I")
		element.send_keys(password)	
		
		buttonId = 'ctl00_contentMain_ASPxRoundPanel2_loginMain_LoginButton'
		##buttonId = 'ctl00_contentMain_ASPxRoundPanel2_loginMain_LoginButton_I'		
		
		WebDriverWait(browser, timeout=10).until(
				lambda x: x.find_element_by_id(buttonId))
		button = browser.find_element_by_id(buttonId)
		##print button.tag_name, button.text
		##print browser.page_source
		button.click()
		##button.click()	
		##WebDriverWait(browser, timeout=90).until(
		##		lambda x: x.find_element_by_class_name('head-title iml-main-header-name'))
		##myNameElement = browser.find_element_by_xpath("/html/body[@class='iml-nonresponsiveness iml-body-gray im-showads']/div[@id='mainView']/div[1]/div[@id='imlHead']/div[@id='imlStickerTab-sticky-wrapper']/div[@id='imlStickerTab']/div[@class='container iml-override-container']/div[@class='row'][1]/div[@class='col-xs-12']/div[@class='media iml-header-avatar iml-head-low-height']/div[@class='media-body']/div[@id='imlDefaultMenu']/h3[@class='media-heading schoolMainNavigBack']/a[@class='head-title iml-main-header-name']")
		##print myNameElement, myNameElement.text
		while(browser.current_url != "https://www.imleagues.com/spa/member/player"):
			pass
		print "Finished signing into IMLeagues"
		##linkedTeamPages = getLinkedPagesFromUrl(browser, url)
		##print linkedTeamPages, len(linkedTeamPages)
		##goToLink(browser, "https://www.imleagues.com/spa/team/a943b71808f94437a21b123ca7c8aaaf/home")
		##saveIdsInLinkedLeague(browser, "https://www.imleagues.com/spa/team/a943b71808f94437a21b123ca7c8aaaf/home", 1, "advanced", "winter2017")

		semesters = [semester]	
		for semester in semesters:
				
			with open('%shooks.csv' % semester, 'rb') as f:
				reader = csv.reader(f)
				i = 0
				for row in reader:
					print row
					##teamId = row[0]
					sportId = int(row[1])
					levelId = row[2]
					seasonId = semester
					if(sports[sportId][4] == "tournament"):
						rulesPath = "%s-%s-%s_tournament" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
					else:
						rulesPath = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
			
					file_path = "./data/%s/%s/watMu/%s/%s/teamId.csv" % (sports[sportId][0], rulesPath, levelId, seasonId)	
					with open(file_path, 'rb') as ff:
						tm_reader = csv.reader(ff)
						for tm_row in tm_reader:
							teamId = tm_row[0]
							print sportId, levelId, seasonId, teamId
							saveTeamDataInLinkToRawHtml(browser, "https://www.imleagues.com/spa/team/%s" % teamId, sportId, levelId, semester, teamId)

		
if(__name__ == "__brain__"):
	##url = "https://www.imleagues.com/spa/team/662222b25eb54b88b4eebb4090cb455a/home"
	##url = "http://google.ca"
	##url = "http://www.quackit.com/html/html_editors/scratchpad/preview.cfm"
	url = "http://127.0.0.1/js.html"
	## use firefox to get page with javascript generated content
	with closing(Firefox()) as browser:
		##browser.get(url)
		
		
		#WebElement inputElement = driver.findElement(By.id("input_field_1"));
		#inputElement.clear();
		#inputElement.sendKeys("12");
		#//here you have to wait for javascript to finish. E.g wait for a css Class or id to appear
		#Assert.assertEquals("12", inputElement.getAttribute("value"));
		
		try:
			browser.get(url)
			button = browser.find_element_by_tag_name('button')
			button.click()
			## wait for the page to load
			##browser.refresh();
			WebDriverWait(browser, timeout=10).until(
				lambda x: x.find_element_by_id('demo'))
				##lambda x: x.find_element_by_id('mainView'))			
			## store it to string variable
		except:
			pass
		page_source = browser.page_source
	print(page_source)
