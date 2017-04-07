## teamSpider.py ###############################################################
## trying to yank js delivered content from a webpage, need an external ########
## lib to do it ################################################################
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
	
	
def saveIdsInLinkedLeague(browser, initialTeamUrl, sportId, levelId, seasonId):
	sports = watMuSportInfo.sportsInfoDict()
	sportIds = [28, 4, 3, 5, 11, 7, 1, 31, 10, 6, 2, 8, 17, 26, 18, 16]


	linkedTeamPages = getLinkedPagesFromUrl(browser, initialTeamUrl)
	print linkedTeamPages, len(linkedTeamPages)
	
	thisLevelTeamIds = [string.replace(string.replace(li, "/home", ""), "https://www.imleagues.com/spa/team/", "") for li in linkedTeamPages]
	
	if(sports[sportId][4] == "tournament"):
		rulesPath = "%s-%s-%s_tournament" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
	else:
		rulesPath = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
		
	file_path = "./data/%s/%s/watMu/%s/%s/teamId.csv" % (sports[sportId][0], rulesPath, levelId, seasonId)	
	directory = os.path.dirname(file_path)
	try:
		os.stat(directory)
	except:
		os.makedirs(directory)	
	f = open(file_path, "wb")
	writer = csv.writer(f)
	
	for row in thisLevelTeamIds:
		writer.writerow(["%s" % row])
	f.close()

if(__name__ == "__main__"):
	

	## add this line
	
	if(len(argv) >= 3):
		username = argv[1]
		password = argv[2]
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
		semesters = ['winter2017']
		
		nextUp = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17.18,19,20,21,22,23,24,25,26,27,28,29]
		for semester in semesters:
			
			with open('%shooks.csv' % semester, 'rb') as f:
				reader = csv.reader(f)
				i = 0
				for row in reader:
					i+=1
					if(i in nextUp):
						print row
						teamId = row[0]
						sportId = int(row[1])
						levelId = row[2]
						saveIdsInLinkedLeague(browser, "https://www.imleagues.com/spa/team/%s/home" % teamId, sportId, levelId, semester)
		##saveIdsInLinkedLeague(browser, "https://www.imleagues.com/spa/team/b966903aff5a400fbea28c27b77f08a9/home", 7, "advanced", "fall2016")
		
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
