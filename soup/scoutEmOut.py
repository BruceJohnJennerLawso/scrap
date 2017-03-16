## scoutEmOut.py ###############################################################
## start with some link to a web page, look at everything it links to in a #####
## specific part of the page, list what they link to, and so on ################
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests
import string

def getLinkedPagesFromUrl(url, alreadyLookedAt=[]):
	print "currently on %s, already looked at" % url
	print alreadyLookedAt
	page = requests.get(url)
	
	soup = BeautifulSoup(page.content, "lxml")
	##table = soup.find(lambda tag: tag.name=='table' and tag.has_key('class') and tag['class']=="refpays") 
	##table = table.find(lambda tag: tag.name=='tbody') 	
	scheduleTable = soup.find(lambda tag: tag.name=='table', class_ ="refpays") 
	##rows = table.findAll(lambda tag: tag.name=='tr')
	
	totalList = []
	totalList.append(url)
	for link in scheduleTable.find_all('a'):
		##print(link.get('href'))
		linkHref = link.get('href')
		if(linkHref[0] == '/'):
			linkHref = "https://strobe.uwaterloo.ca" + linkHref
		
		if((linkHref not in totalList)and(linkHref not in [url])and(linkHref not in alreadyLookedAt)):
			totalList += getLinkedPagesFromUrl(linkHref, alreadyLookedAt+totalList)
	return totalList

if(__name__ == "__main__"):

	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11256"
	url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11452"
	teamUrlList = getLinkedPagesFromUrl(url)
	teamIdList = [string.replace(url, "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=", "") for url in teamUrlList]
	print teamIdList, len(teamIdList)
