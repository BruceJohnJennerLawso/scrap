## helloSoup.py ################################################################
## just mucking around with beautiful soup to get ##############################
## a feel for it ###############################################################
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests


if(__name__ == "__main__"):

	url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11256"

	page = requests.get(url)
	
	soup = BeautifulSoup(page.content, "lxml")
	##table = soup.find(lambda tag: tag.name=='table' and tag.has_key('class') and tag['class']=="refpays") 
	##table = table.find(lambda tag: tag.name=='tbody') 	
	table = soup.find(lambda tag: tag.name=='table', class_ ="refpays") 
	rows = table.findAll(lambda tag: tag.name=='tr')
	
	
	for row in rows:
		print row
	print "\n\nFlattening to csv\n"
	outputRows = []
	for row in rows:
		print row, row.find_all('tr')
		outputRows.append([val.text.encode('utf8') for val in row.find_all('td') + row.find_all('th')])		

	for row in outputRows:
		print row, len(row)	
	##for link in soup.find_all('a'):
	##	print(link.get('href'))
