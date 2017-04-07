## gameRaw.py ##################################################################
## now that we have the team csvs scraped from the raw js delivered webpage ####
## content of the team pages of each team in the league, I want to pull the ####
## game pages data raw out of imleagues by the stored gameids in the teamcsvs ##
## and dump them into folders under each individual season, ie #################
## /data/hockey/indoor-ice-6-6vs_1GK/watMu/ ####################################
## beginner/fall2016/games/[gameId]/gameData.html ##############################
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
		
	colInd = subsectionRowData[0].index('linkToGame')	
	output = [row[colInd] for row in subsectionRowData[1:]]
	return output
		



if(__name__ == "__main__"):

	url = "/spa/league/d75eb42ff22f45baaea249ceaf0e72d5/viewgame?gameId=7836505&gameType=0"	
	print stripGameIdFromLink(url)
	exit()
	##print getGameIds(1, 'beginner', 'fall2016', '245ae04604684f40a40d7257467879c1', 'SEASON') + getGameIds(1, 'beginner', 'fall2016', '245ae04604684f40a40d7257467879c1', 'PLAYOFFS')
	##exit()
	sports = watMuSportInfo.sportsInfoDict()


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
	
	
	##url = "https://www.imleagues.com/spa/team/662222b25eb54b88b4eebb4090cb455a/home"
	
	with closing(Firefox()) as browser:

		##driver = webdriver.Firefox()

		driver = browser
	

		driver.get("https://nike.uwaterloo.ca/Login.aspx?soi=IM&ref=Intramurals")
		element = driver.find_element_by_id("ctl00_contentMain_ASPxRoundPanel2_loginMain_UserName_I")
		element.send_keys(username)
		element = driver.find_element_by_id("ctl00_contentMain_ASPxRoundPanel2_loginMain_Password_I")
		element.send_keys(password)	
		
		buttonId = 'ctl00_contentMain_ASPxRoundPanel2_loginMain_LoginButton'

		WebDriverWait(browser, timeout=10).until(
				lambda x: x.find_element_by_id(buttonId))
		button = browser.find_element_by_id(buttonId)
		button.click()
		while(browser.current_url != "https://www.imleagues.com/spa/member/player"):
			pass
		print "Finished signing into IMLeagues"

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
					
					seasonGames = []
					teamCount = 0
					with open(file_path, 'rb') as ff:
						tm_reader = csv.reader(ff)
						for tm_row in tm_reader:
							teamCount += 1
							teamId = tm_row[0]
							##print sportId, levelId, seasonId, teamId
							teamGameLinks = getGameIds(sportId, levelId, seasonId, teamId, "SEASON") + getGameIds(sportId, levelId, seasonId, teamId, "PLAYOFFS")
							seasonGames += [link for link in teamGameLinks if link not in seasonGames]
					print sportId, levelId, seasonId, len(seasonGames)
					for gmUrl in seasonGames:
						saveGameDataInLinkToRawHtml(browser, gmUrl, sportId, levelId, seasonId)
						
						print gm
					##print sportId, levelId, seasonId, teamCount, len(seasonGames)












