## scoutEmOut.py ###############################################################
## start with some link to a web page, look at everything it links to in a #####
## specific part of the page, list what they link to, and so on ################
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests
import string

def convertShortLinkHrefUrlToFull(linkHref):
	if(linkHref[0] == '/'):
		linkHref = "https://strobe.uwaterloo.ca" + linkHref
	return linkHref

def getLinkedPagesFromUrl(url, alreadyLookedAt=[], depth=0):
	print " "*depth, string.replace(url, "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=", "")
	page = requests.get(url)
	
	soup = BeautifulSoup(page.content, "lxml")	
	scheduleTable = soup.find(lambda tag: tag.name=='table', class_="refpays") 
	
	totalList = []
	totalList.append(url)
	for link in scheduleTable.find_all('a'):
		linkHref = link.get('href')
		linkHref = convertShortLinkHrefUrlToFull(linkHref)
		
		if((linkHref not in totalList)and(linkHref not in [url])and(linkHref not in alreadyLookedAt)):
			totalList += getLinkedPagesFromUrl(linkHref, alreadyLookedAt+totalList, depth+1)
	return totalList

if(__name__ == "__main__"):

	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11256"
	url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11452"
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=13089"
	teamUrlList = getLinkedPagesFromUrl(url)
	teamIdList = [string.replace(url, "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=", "") for url in teamUrlList]
	print teamIdList, len(teamIdList)
