## helloSoup.py ################################################################
## just mucking around with beautiful soup to get ##############################
## a feel for it ###############################################################
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests
import numpy as np
import string


def convertShortLinkHrefUrlToFull(linkHref):
	if(linkHref[0] == '/'):
		linkHref = "https://strobe.uwaterloo.ca" + linkHref
	return linkHref

def getLinkedPagesFromUrl(url, alreadyLookedAt=[], depth=0):
	##print " "*depth, string.replace(url, "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=", "")
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

def getTableInRows(url, tableTarget, debugInfo=False):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "lxml")
	##{"id": tableId}
	table = soup.find(lambda tag: tag.name=='table', tableTarget) 
	rows = table.findAll(lambda tag: tag.name=='tr')
	
	
	for row in rows:
		print row
	print "\n\nFlattening to csv\n"

	headerRows = []
	outputRows = []

	for row in rows:
		##print row, row.find_all('tr')
		headerRows.append([val.text.encode('utf8') for val in row.find_all('th')])	
		##outputRows.append([val.text.encode('utf8') for val in row.find_all('th')+row.find_all('td')])
		outputRows.append([val.text.encode('utf8') for val in row.find_all(['td', 'th'])])		
		## important note here, some evil
		## tables such as hockey reference like to make data in the first column
		## (ie game number) a <th> element, like its another header but vertical
		## because they hate me
	for row in outputRows:
		print row

				
	tableWidth = max([len(row) for row in headerRows])
	## this is to single out that blasted "meta header" row thats often present
	## but not always in a teams hockey reference page
	##headerRows = [row for row in headerRows if (len(row)==tableWidth)]
	outputRows = [row for row in outputRows if row not in headerRows]
	headerRows = [row for row in headerRows if (len(row)==tableWidth)]
	headerRows = map(list, set(map(tuple,headerRows)))
	## remove duplicate header rows (in list form) from the list of lists
	
	print "## Header Rows ##"
	for row in headerRows:
		print row, len(row)
	i = 0

	print "## Output Rows ##"	
	for row in outputRows:
		print i, outputRows.index(row), row, len(row), (len(row) == tableWidth)	, "\n"
		if(len(row) != tableWidth):
			print "Bad row does not match widths of the others"
		i+=1	
	return (headerRows, outputRows)

if(__name__ == "__main__"):


	sportIds = [28, 4, 3, 5, 11, 7, 1, 31, 10, 6, 2, 8, 17, 22, 26, 18, 16]
	## logic not included
	years = range(2007, 2017)
	
	def getTermById(termId):
		if(termId == 1):
			return "Winter"
		elif(termId == 2):
			return "Spring"
		if(termId == 4):
			return "Fall"						
	
	terms = [1,2,4]
	## it goes winter, spring, fall
	## makes no sense to me either how they picked the term numbers
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11256"
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=7627"
	
	for year in years:

		for term in terms:
			print "\n\n"
			print year, getTermById(term)
			for sport in sportIds:
				
				url = "https://strobe.uwaterloo.ca/athletics/intramurals/leagues.php?sport=%i&champions&year=%i&term=%i" % (sport, year, term)
				page = requests.get(url)
	
				soup = BeautifulSoup(page.content, "lxml") 	
				content = soup.find(lambda tag: tag.name=='div' and tag.has_key('id') and tag['id']=="primarycontent") 
				
				print content.find(lambda tag: tag.name=='h1').getText()
				
				if(content.find('strong')):
					print content.find(lambda tag: tag.name=='strong').getText(), "\n"
				else:	
					levels = content.findAll(lambda tag: tag.name=='h2')
	
					def convertShortLinkToTeamId(shortLink):
						if(shortLink[0:15] == 'teams.php?team='):
							shortLink = shortLink[15:]
						return shortLink
	
					for lev in levels:
		
						linksAfterLev = []
						nextLev = lev
						while(True):
							if(nextLev.next_sibling.name == "a"):
								linksAfterLev.append(nextLev.next_sibling)
								nextLev = nextLev.next_sibling
							else:
								break
								
						print lev.getText(), lev.name
						for teamId in [convertShortLinkToTeamId(l.get('href')) for l in linksAfterLev]:
							teamIdList = [string.replace(url, "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=", "") for url in getLinkedPagesFromUrl("https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=%i" % int(teamId))]
							
							print teamId, teamIdList, len(teamIdList), "\n"
			
	##for elem in levels(text=re.compile(r' #\S{11}')):
	##	print elem.parent
	#for row in rows:
		#print row
	#print "\n\nFlattening to csv\n"
	#outputRows = []
	#for row in rows:
		###print row, row.find_all('tr')
		#outputRows.append([val.text.encode('utf8') for val in row.find_all('td') + row.find_all('th')])		

	#for row in outputRows:
		#print row, len(row)
			
	##for link in soup.find_all('a'):
	##	print(link.get('href'))
