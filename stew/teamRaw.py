## teamRaw.py ##################################################################
## Now that we have the ids for all of the teams we want, I need to save the ###
## data they contain to file. Because IMLeagues is a bit weirdly written, and ##
## time may be critical for getting some data off the web, I think this will ###
## be much easier done by saving the webpages for each team as delivered in js #
## to file, then parsing their contents afterwards #############################
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
	sports = watMuSportInfo.sportsInfoDict()
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
		##f = open(file_path, "w")
		##writer = csv.writer(f)
		
		##for row in thisLevelTeamIds:
		##writer.write(loadedHtmlContent)
		##f.close()
		
		Html_file= open(file_path,"w")
		Html_file.write(loadedHtmlContent)
		Html_file.close()

if(__name__ == "__main__"):
	sports = watMuSportInfo.sportsInfoDict()

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
		semesters = [semester]	
		
		
		#sportId = 3
		#levelId = 'beginner'
		#teamId = 'efbb7ad9fce54785bb2a71a68b2f1ace'
		#saveTeamDataInLinkToRawHtml(browser, "https://www.imleagues.com/spa/team/%s" % teamId, sportId, levelId, semester, teamId)			
		#exit()
		
		for semester in semesters:
			with open('%shooks.csv' % semester, 'rb') as f:
				reader = csv.reader(f)
				i = 0
				for row in reader:
					print row
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
