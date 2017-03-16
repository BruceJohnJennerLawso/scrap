## scoutEmOut.py ###############################################################
## start with some link to a web page, look at everything it links to in a #####
## specific part of the page, list what they link to, and so on ################
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests


if(__name__ == "__main__"):

	url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11256"
	url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=7627"
	page = requests.get(url)
	
	soup = BeautifulSoup(page.content, "lxml")
	##table = soup.find(lambda tag: tag.name=='table' and tag.has_key('class') and tag['class']=="refpays") 
	##table = table.find(lambda tag: tag.name=='tbody') 	
	table = soup.find(lambda tag: tag.name=='table', class_ ="refpays") 
	rows = table.findAll(lambda tag: tag.name=='tr')
	
	
			
	##for link in soup.find_all('a'):
	##	print(link.get('href'))
