## helloSoup.py ################################################################
## just mucking around with beautiful soup to get ##############################
## a feel for it ###############################################################
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests


if(__name__ == "__main__"):

	url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11256"
	url = "http://www.hockey-reference.com/teams/TOR/2017_games.html"
	##url = "http://www.hockey-reference.com/teams/MTW/1918_games.html"
	page = requests.get(url)
	
	soup = BeautifulSoup(page.content, "lxml")
	##table = soup.find(lambda tag: tag.name=='table' and tag.has_key('class') and tag['class']=="refpays") 
	##table = table.find(lambda tag: tag.name=='tbody') 	
	table = soup.find(lambda tag: tag.name=='table', {"id": "games"}) 
	rows = table.findAll(lambda tag: tag.name=='tr')
	
	
	for row in rows:
		print row
	print "\n\nFlattening to csv\n"

	headerRows = []
	outputRows = []

	for row in rows:
		##print row, row.find_all('tr')
		headerRows.append([val.text.encode('utf8') for val in row.find_all('th')])	
		outputRows.append([val.text.encode('utf8') for val in row.find_all('th')+row.find_all('td')])		
	tableWidth = max([len(row) for row in headerRows])
	## this is to single out that blasted "meta header" row thats often present
	## but not always in a teams hockey reference page
	##headerRows = [row for row in headerRows if (len(row)==tableWidth)]
	outputRows = [row for row in outputRows if row not in headerRows]
	headerRows = [row for row in headerRows if (len(row)==tableWidth)]
	headerRows = map(list, set(map(tuple,headerRows)))
	
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
	##for link in soup.find_all('a'):
	##	print(link.get('href'))
