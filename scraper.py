## scraper.py ##################################################################
## utilities to scrape a teams data out of the intramurals system ##############
## may need to someday scrape the playoff brackets as well, ####################
## but not going to worry about that yet #######################################
################################################################################
from lxml import html
import requests

from gameProcessing import *


def scrapeTeamData(teamId, debugInfo, seasonString):
	## gotta pass in the season, since the system doesnt display it anywhere
	## for some reason
	
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

	teamString = content1[0]
	teamName = getTeamName(teamString)
	print "Team String, ", teamString
	print "Team Name: %s, %s" % (teamName, seasonString)
	
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
		
		
		
		rawScoreData = content3[access + 2]
		outcome = gameResult(rawScoreData)
		
		if(outcome != 'unplayed'):
			goalsFor = processGoalsFor(rawScoreData, outcome)
			goalsAgainst = processGoalsAgainst(rawScoreData, outcome)
			
			schedule.append([content3[access], content3[access+1], outcome, goalsFor, goalsAgainst, processSOC(content3[access+3])  , content4[game]])
			## left to right, the game record reads ['date and time', 'Location', 'won', 'SOC Rating', 'opponent name', ]			
		else:
			if(False):
				continue
				## this fixes the problem brilliantly, maybe activate this if we
				## know the whole schedule should be played by now to avoid the
				## issue that 8481 has with the rescheduled game
			schedule.append([content3[access], content3[access+1], outcome, content3[access+2] , content3[access+3]  , content4[game]])			
			## that should fix things somewhat
		
		## !!!! Important Note !!!!
		## This will NOT work with seasons in progress, because the scores for 
		## games not yet played will appear as  - - - or something like that
		## the functions that process the goals will need to adjust for this
		
		## there needs to be a precheck to verify that the game was played
		## before committing the data, TODO
		
		## I would do it now (March 2016) but I cant remember what the unplayed
		## games look like at the moment, and I wont have to worry about it
		## for a while anyways
		
					
					
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
