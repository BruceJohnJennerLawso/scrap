################################################################################
from lxml import html
import requests

from sys import argv

import csv


def scrapeTeamData(teamId):
	page = requests.get('http://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=%i&sport=1' % (teamId))
	tree = html.fromstring(page.content)

	content1 = tree.xpath('//div[@id="primarycontent"]/*[0]/text()')


	teamName = tree.xpath('//div[@id="primarycontent"]/*/text()')

	content2 = tree.xpath('//div[@id="primarycontent"]/*/*/text()')
	
	content3 = tree.xpath('//div[@id="primarycontent"]/*/*/*/text()')
	
	print "content1", content1, "\n\n", len(content1)
	print "content2", content2, "\n\n", len(content2)
	print "content3", content3, "\n\n", len(content3)		
	
	print tree.xpath('//div[@id="primarycontent"]/*/*[%i]/text()' % (1))

if(__name__=="__main__"):
	teamIdList = [12348, 12307]
	
	for Id in teamIdList:
		scrapeTeamData(Id)
