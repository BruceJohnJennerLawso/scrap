## doorBreach.py ###############################################################
## lets just start off by verifying we can get into the data on an IMLeagues ###
## page at all #################################################################
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests
import os
import csv


def getTableInRows(soup, tableTarget, tableDataOnlyUnder="", debugInfo=False):

	##{"id": tableId}
	table = soup.find(lambda tag: tag.name=='table', tableTarget) 
	rows = table.findAll(lambda tag: tag.name=='tr')
	
	
	##for row in rows:
	##	print row
	##print "\n\nFlattening to csv\n"

	headerRows = []
	outputRows = []


	foundTargetHeadingUnder = False
	for row in rows:
		##print row, row.find_all('tr')
		headerRows.append([val.text.encode('utf8') for val in row.find_all('th')])	
		##outputRows.append([val.text.encode('utf8') for val in row.find_all('th')+row.find_all('td')])
		if(tableDataOnlyUnder == ""):
			outputRows.append([val.text.encode('utf8') for val in row.find_all(['td', 'th'])])		
		else:
			if(row.find(lambda tag: tag.name=='th' and tag.has_attr('colspan'))):
				if(row.getText() == tableDataOnlyUnder):
					foundTargetHeadingUnder = True
					continue
					## keep going and ignore this particular break in the table	
				else:
					if(foundTargetHeadingUnder):
						break	
					else:
						continue
			else:
				if(foundTargetHeadingUnder):
					outputRows.append([val.text.encode('utf8') for val in row.find_all(['td', 'th'])])				
		## important note here, some evil
		## tables such as hockey reference like to make data in the first column
		## (ie game number) a <th> element, like its another header but vertical
		## because they hate me
	##for row in outputRows:
	##	print row

				
	tableWidth = max([len(row) for row in headerRows])
	## this is to single out that blasted "meta header" row thats often present
	## but not always in a teams hockey reference page
	##headerRows = [row for row in headerRows if (len(row)==tableWidth)]
	outputRows = [row for row in outputRows if row not in headerRows]
	headerRows = [row for row in headerRows if (len(row)==tableWidth)]
	headerRows = map(list, set(map(tuple,headerRows)))
	## remove duplicate header rows (in list form) from the list of lists
	
	##print "## Header Rows ##"
	##for row in headerRows:
	##	print row, len(row)
	##i = 0

	##print "## Output Rows ##"	
	##for row in outputRows:
	##	print i, outputRows.index(row), row, len(row), (len(row) == tableWidth)	, "\n"
	##	if(len(row) != tableWidth):
	##		print "Bad row does not match widths of the others"
	##	i+=1	
	return (headerRows, outputRows)

if(__name__ == "__main__"):

	url = "https://www.imleagues.com/spa/team/662222b25eb54b88b4eebb4090cb455a/home"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "lxml")	
	
	##print soup, "\n\n"
	##print soup.findAll(lambda tag: tag.name=='th')
	
	view = soup.find(lambda tag: tag.name=='div', {"id": "mainView"}) 

	print view, "\n\n"
	print view.findAll(lambda tag: tag.name=='th')
	exit()
		
	tableHeader, tableContent = getTableInRows(soup, {"class": "table-hover tablesorter stat-tab team-player"})

	for head in tableHeader:
		print head
	for row in tableContent:
		print row
