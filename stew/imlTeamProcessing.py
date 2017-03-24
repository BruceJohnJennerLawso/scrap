## imlTeamProcessing.py ########################################################
## tired of constantly handling getting into IMLeagues, just want ##############
## to consistently find the elements I need in the monster html response #######
## that the page sends me, so Im going to work on loading the html from ########
## file ########################################################################
################################################################################
from bs4 import BeautifulSoup

import time
import sys


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

if(__name__ == "__main__"):
	import codecs
	f=codecs.open("./visiblePage.html", 'r')
	##print f.read()
	soup = BeautifulSoup("%s" % f.read(), 'html.parser')
	##print soup, type(soup)
	print getLinksFromSoup(soup)
