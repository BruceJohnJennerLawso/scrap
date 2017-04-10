## gameBeautiful.py ############################################################
## similar to how the teamBeautiful module takes the raw html page content and #
## distills it to the desired information saved in a csv file, gameBeautiful ###
## takes the raw game page content and saves it to a game csv ##################
## unfortunately, for the game page, theres quite a bit of variation in the ####
## exact layout of the game pages, such as the individual set scores for #######
## volleyball, so Im gonna break this down into separate functions per sport ###
## and handle each different case seperately ###################################
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

import watMuSportInfo

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
	

def stripGameIdFromLink(url):
	firstCrop = url.index('?')
	output = url[firstCrop+8:]
	gameType = output[len(output)-1]
	secondCrop = output.index('&')
	output = output[:secondCrop]
	if(gameType == '0'):
		return "R%s" % output
	elif(gameType == '1'):
		return "P%s" % output		

def saveGameDataInLinkToRawHtml(browser, initialGameUrl, sportId, levelId, seasonId):
	sports = watMuSportInfo.sportsInfoDict()
	sportIds = [28, 4, 3, 5, 11, 7, 1, 31, 10, 6, 2, 8, 17, 26, 18, 16]

	

	browser.get("https://www.imleagues.com%s" % initialGameUrl)
	time.sleep(20)
	
	loadedHtmlContent = browser.find_element_by_tag_name('html').get_attribute('innerHTML').encode('utf8')

	if(sports[sportId][4] == "tournament"):
		rulesPath = "%s-%s-%s_tournament" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
	else:
		rulesPath = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
	gameId = stripGameIdFromLink(initialGameUrl)
	file_path = "./data/%s/%s/watMu/%s/%s/games/%s/gameData.html" % (sports[sportId][0], rulesPath, levelId, seasonId, gameId)	
	directory = os.path.dirname(file_path)
	try:
		os.stat(directory)
	except:
		os.makedirs(directory)	
		##f = open(file_path, "w")
		##writer = csv.writer(f)
		
		##for row in thisLevelTeamIds:
		##writer.write(loadedHtmlContent)
		##f.close()
		
	Html_file= open(file_path,"w")
	Html_file.write(loadedHtmlContent)
	Html_file.close()


	
def getGameIds(sportId, levelId, seasonId, teamId, subsection):
	sports = watMuSportInfo.sportsInfoDict()

	if(sports[sportId][4] == "tournament"):
		rulesPath = "%s-%s-%s_tournament" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
	else:
		rulesPath = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
			
	file_path = "./data/%s/%s/watMu/%s/%s/%s.csv" % (sports[sportId][0], rulesPath, levelId, seasonId, teamId)	
	
	csvRows = []
	
	with open(file_path, 'rb') as ff:
		teamCsv_reader = csv.reader(ff)
		for row in teamCsv_reader:
			csvRows.append(row)
	
	
	
	def getSubsectionByTag(csvRows, tag):
		startex = csvRows.index(['%s:' % tag])
		endex = csvRows.index(['END_%s' % tag])	
	
		subsectionRows = csvRows[startex+1:endex]		
		return subsectionRows
	
	
	
	for row in getSubsectionByTag(csvRows, subsection):
		##print row
		pass
		
	subsectionRowData = getSubsectionByTag(csvRows, subsection)
		
	colInd = subsectionRowData[0].index('Game Name')	
	output = [row[colInd] for row in subsectionRowData[1:]]
	return output
		

def getPlayerStatsTableFromSoup(soup):
	headerRow = ['imlPlayerId']
	outputRows = []
	headerRowSoup = soup.find('thead').find('tr')
	for heading in headerRowSoup.findAll('th'):
		headerRow.append(heading.getText().encode('utf-8'))
	
	playerDataRowSoup = soup.find('tbody')
	for row in playerDataRowSoup.findAll('tr'):
		rowData = []
		
		rowPlayerId = stripStringOfPieces(row.find('td').find('a')['href'], ['/Members/player_card.aspx?player=']).encode('utf-8')
		rowData.append(rowPlayerId)
		print repr(rowPlayerId)
		for col in row.findAll('td'):
			if(col.getText().encode('utf-8') == '\xc2\xa0'):
				rowData.append('')
			else:	
				rowData.append(col.getText().encode('utf-8'))
		outputRows.append(rowData)
	return (headerRow, outputRows)


def scrapeImlGame(sportId, levelId, seasonId, gameId):
	sports = watMuSportInfo.sportsInfoDict()
	
	
	
	if(sports[sportId][4] == "tournament"):
		rulesPath = "%s-%s-%s_tournament" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
	else:
		rulesPath = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
			
	file_path = "./data/%s/%s/watMu/%s/%s/games/%s/gameData.html" % (sports[sportId][0], rulesPath, levelId, seasonId, gameId)	
	

	f=codecs.open("%s" % file_path, 'r') 
	gameSoup = BeautifulSoup("%s" % f.read(), 'html.parser')
	f.close()
	
	
	gameDateString = "%s" % gameSoup.find(lambda tag: tag.name=='span', {"class": "game-date"}).getText().encode("utf-8")
	gameResultString = "%s" % gameSoup.find(lambda tag: tag.name=='div', {"class": "game-result"}).getText().encode("utf-8")
	
	
	gamePeriodSoup = gameSoup.find(lambda tag: tag.name=='table', {"id": "tbGamePeriodDetail"})
	
	print repr(gameDateString)
	print repr(gameResultString)
	##stripStringOfPieces(gameLinkEx, ["/spa/league/", "viewgame?gameId=", "&gameType=0"])
	sidesStats = {'home':{}, 'away':{}}
	## left is home, right is away
	sideConversion = {'left': 'home', 'right': 'away'}
	for side in ['left', 'right']:
		sideSoup = gameSoup.find(lambda tag: tag.name=='div', {"class": "media team-%s" % side})
		print '\n\n\n', side, '\n'
		thisSideTeam = sideSoup.find(lambda tag: tag.name=='a')
		
		teamName = thisSideTeam.getText().encode("utf-8")
		teamId = stripStringOfPieces(thisSideTeam['href'].encode("utf-8"), ['/spa/team/', '/home'])	
		
		teamSide = sideConversion[side]
		##sidesStats[teamSide]['teamName'] = teamName
		sidesStats[teamSide]['teamId'] = teamId	
		
		
	visibleDataRows = [row for row in gamePeriodSoup.findAll(lambda tag: tag.name=='tr', {}) if (row.has_attr('class')==False)]
		
		
	for row in visibleDataRows:
		rowStatName = row.find(['td', 'th'], {'class': "item-name text-center"}).getText().encode("utf-8")
		homeRowStatValue = row.find(['td', 'th']).getText().encode("utf-8")
			
		secondValue = row.find(['td'], {'class': "td-2"})
		if(secondValue == None):
			visitorRowStatValue = row.find([ 'th'], {'class': "th-1"}).getText().encode("utf-8")
		else:
			visitorRowStatValue = secondValue.getText().encode("utf-8")
		print 'rowStatName', rowStatName
		print 'home: ', homeRowStatValue
		print 'visitor: ', visitorRowStatValue
		sidesStats['home'][rowStatName] = homeRowStatValue
		sidesStats['away'][rowStatName] = homeRowStatValue
		print row
		##print sideSoup
	##print gamePeriodSoup
	
	for side in ['home', 'away']:
		teamPlayerStats = gameSoup.find('div', {'id': "divPlayerStats%s" % sidesStats[side]['teamId']})
		teamName = stripStringOfPieces(teamPlayerStats.parent.parent.parent.find('h3').getText().encode("utf-8"), [ '\n']).strip()
		print repr(teamName)
		sidesStats[side]['teamName'] = teamName
	
	print sidesStats
	
	gamePlayerStatsTable = {'home':{}, 'away':{}}
	
	for side in ['home', 'away']:
		teamPlayerStats = gameSoup.find('div', {'id': "divPlayerStats%s" % sidesStats[side]['teamId']})
		header, data = getPlayerStatsTableFromSoup(teamPlayerStats)
		gamePlayerStatsTable[side]['header'] = header
		gamePlayerStatsTable[side]['data'] = data
	print gamePlayerStatsTable
	for side in ['home', 'away']:
		print gamePlayerStatsTable[side]['header']
		playerDataRows = gamePlayerStatsTable[side]['data']
		for row in playerDataRows:
			print row, '\n'
	return
	
	
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


	sportId = 1
	levelId = "advanced"
	seasonId = "winter2017"
	##gameId = "R8442888"
	gameId = "P2087295"


	##sportId = 8
	##levelId = "beginner"
	##seasonId = "winter2017"
	##gameId = "R8442632"

	sportId = 4
	levelId = 'beginner'
	seasonId = 'winter2017'
	gameId = 'P2074877'

	scrapeImlGame(sportId, levelId, seasonId, gameId)
	exit()
	sports = watMuSportInfo.sportsInfoDict()


	if(len(argv) >= 1):
		semester = argv[1]
	else:
		semester = getTextInput("Please Input Desired semester: ")
	
	totalGamesList = []
	semesters = [semester]	
	for semester in semesters:
		incompleteTeams = []		
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
					
				seasonGames = []
				teamCount = 0
				with open(file_path, 'rb') as ff:
					tm_reader = csv.reader(ff)
					for tm_row in tm_reader:
						teamCount += 1
						teamId = tm_row[0]
						##print sportId, levelId, seasonId, teamId
						teamGameLinks = getGameIds(sportId, levelId, seasonId, teamId, "SEASON") + getGameIds(sportId, levelId, seasonId, teamId, "PLAYOFFS")
						if("" in teamGameLinks):
							incompleteTeams.append("%s_%s_%s"% (teamId, levelId, sportId))
							print teamId, " had a bad gameId"
						seasonGames += [link for link in teamGameLinks if link not in seasonGames]
				print sportId, levelId, seasonId, len(seasonGames)
				for gmUrl in seasonGames:
					totalGamesList.append(gmUrl)
					print seasonGames.index(gmUrl), gmUrl
					scrapeImlGame(sportId, levelId, seasonId, gameId)
		print incompleteTeams
	print len(totalGamesList)










