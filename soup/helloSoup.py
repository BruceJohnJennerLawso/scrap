## helloSoup.py ################################################################
## just mucking around with beautiful soup to get ##############################
## a feel for it ###############################################################
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests
import numpy as np





if(__name__ == "__main__"):


	sportIds = [28, 4, 3, 5, 11, 7, 1, 31, 10, 6, 2, 8, 17, 22, 26, 18, 16]
	## logic not included
	years = range(1957, 2017)
	terms = [1,2,4]
	## it goes winter, spring, fall
	## makes no sense to me either how they picked the term numbers
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11256"
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=7627"
	url = "https://strobe.uwaterloo.ca/athletics/intramurals/leagues.php?sport=1&champions&year=2010&term=1"
	page = requests.get(url)
	
	soup = BeautifulSoup(page.content, "lxml") 	
	content = soup.find(lambda tag: tag.name=='div' and tag.has_key('id') and tag['id']=="primarycontent") 
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
				
		print lev.getText(), lev.name, [convertShortLinkToTeamId(l.get('href')) for l in linksAfterLev]	
	
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
