################################################################################
from lxml import html
import requests

from sys import argv

import csv

def seasonLength(val):
	if(val >= 37):
		output = (val - 9.0)/4.0
		## if the team made it to the playoffs, we need to step back one
		## more on the index to avoid the 'PLAYOFFS heading'
	else:
		output = (val-8.0)/4.0
		## rare case where a team doesnt advance to playoffs, usually bad SOC
		## only seen this once so far
	return output
	
	

def scrapeTeamData(teamId, debugInfo):
	page = requests.get('http://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=%i&sport=1' % (teamId))
	tree = html.fromstring(page.content)

	## actually a string with the sport, team name, then play level (casual)

	content1 = tree.xpath('//div[@id="primarycontent"]/*/text()')
	## used to retrieve the team name and play level
	content2 = tree.xpath('//div[@id="primarycontent"]/*/*/text()')
	## used to grab the roster, except for the captains name, which is retrieved
	## from the next section
	content3 = tree.xpath('//div[@id="primarycontent"]/*/*/*/text()')
	## captains name at the start
	
	## then we can pull the dates, location (always CIF), results and SOC from
	## the rest
	content4 = tree.xpath('//div[@id="primarycontent"]/*/*/*/*/text()')
	## The column of opponents faced during the season, with the first round
	## byes at the end
	content5 = tree.xpath('//div[@id="primarycontent"]/*/*/*/*/*/text()')	
	## playoff data, not sure how much we care about this yet, since it can
	## be retrieved from the rest of the data that we already pulled, but it
	## might be needed to make sense of playoff seedings at some point
	
	## the sixth layer isnt needed, so we wont bother

	teamName = content1[0]
	print "Team Name: %s" % teamName
	
	players = []
	for i in range(6, len(content2)):
		players.append(content2[i])
	captainName = content3[1]
	## retrieve the captains name which got stuck a layer deeper than the rest	
	print "Captain: ", captainName
	players.append(captainName)
	## might just make the last name the captain by convention
	
	
	print "Roster: "
	for playah in players:
		print playah	

	print "end of roster\n"	
	
	numberOfGames = int(seasonLength(len(content3)))
	print "Season Length: %i games" % numberOfGames
	
	schedule = []
	
	for game in range(numberOfGames):
		if(game <= 5):
			access =((game*4)+8)
		else:
			access = ((game*4)+9)
		schedule.append([content3[access], content3[access+1], content3[access+2], content3[access + 3], content4[game]])
		## left to right, the game record reads ['date and time', 'Location', 'won/lost [score]', 'SOC Rating', 'opponent name']
	print "Schedule: "
	for game in schedule:
		print game
	
	if(debugInfo == True):
	
		print "\ncontent1", content1, "\n", len(content1)
		print "\n\ncontent2", content2, "\n", len(content2)
		print "\ncontent3", content3, "\n", len(content3)	
		print "\ncontent4", content4, "\n", len(content4)
		print "\ncontent5", content5, "\n", len(content5)			
	
		##foo = 2
		##print "content3[%i] " %	(foo), content3[foo]
	
		##print tree.xpath('//div[@id="primarycontent"]/*/*[%i]/text()' % (1))
	print '\n'

if(__name__=="__main__"):
	teamIdList = [12348, 12319, 12313]
	
	for Id in teamIdList:
		scrapeTeamData(Id, False)
	##scrapeTeamData(12348, True)
