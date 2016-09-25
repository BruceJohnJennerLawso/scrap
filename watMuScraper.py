## watMuScraper.py #############################################################
## utilities to scrape a teams data out of the intramurals system ##############
## may need to someday scrape the playoff brackets as well, ####################
## but not going to worry about that yet #######################################
################################################################################

# -*- coding: utf-8 -*-

from lxml import html
import requests

import csv

from gameProcessing import *



def saveScrapedTeamData(teamId, teamString, seasonString, teamName, players, numberOfGames, totalSeasonGames, totalSeasonGamesPlayed, totalPlayoffGames, totalPlayoffGamesPlayed, schedule, leagueId, levelId):
	## once we have the data about the team in question, usually in string form,
	## we should save it in string format so its more convenient to access
	## elsewhere without connecting to the internet
	outputPath = ("./data/%s/%s/%s/%i.csv" % (leagueId, levelId,seasonString, teamId))
	
	print "current output path: %s" % outputPath
	## this is useful enough that we wont make it debugInfo conditional
	with open(outputPath, 'wb') as foo:
		bar = csv.writer(foo)
		## get set to write our csv to file
		bar.writerows([[teamName, seasonString, teamString], [numberOfGames, totalSeasonGames, totalSeasonGamesPlayed, totalPlayoffGames, totalPlayoffGamesPlayed]])
		## write very general info about the team on line 1[0], the total number
		## of games played that season (reg and playoffs) on line 2[1]
		bar.writerows(schedule)
		## write each game in the schedule as its own line in the csv
		bar.writerows([''])
		## put in an extra blank line, before we record the roster
		bar.writerows([players])
		## write out the names of all of the players listed on the roster in one
		## line, ie
		
		## wayne, mark, dave
		
		## ahahahaha my life




def scrapeTeamData(teamId, debugInfo, seasonString, inProgressSeason, leagueId, levelId, saveMe):
	## abandon all hope of comprehension, ye who enter here

	## gotta pass in the season, since the system doesnt display it anywhere
	## on a teams page for some stupid reason
	page = requests.get('http://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=%i&sport=1' % (teamId))
	## start off by requesting the page of the team we are looking at
	
	## each team in the waterloo intramurals system up until 2016 has a number
	## assigned to it that is used to identify what page in the intramurals
	## system it is displayed on
	
	## for example, the fall 2015 Mighty Dads are found on the page
	## https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=12348
	## so their teamId is 12348
	tree = html.fromstring(page.content)
	
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
	if(debugInfo):
		## if we are debugging, we need to see the raw data that the page is
		## spitting back at us
		print 'Raw page data for %i' % teamId
		##print 'Content Layer 1\n', content1, '\nContent Layer 2\n', content2, '\nContent Layer 3\n', content3, '\nContent Layer 4\n', content4, '\nContent Layer 5\n', content5, '\n\n'
	
		print "\ncontent1\n"
		for i in range(0, len(content1)):
			print i, " ", content1[i]		
		print "\n\ncontent2\n"
		for i in range(0, len(content2)):
			print i, " ", content2[i]
		print "\ncontent3\n"	
		for i in range(0, len(content3)):
			print i, " ", content3[i]
		print "\ncontent4\n"
		for i in range(0, len(content4)):
			print i, " ", content4[i]
		print "\ncontent5\n"
		for i in range(0, len(content5)):
			print i, " ", content5[i]			
	
	teamString = content1[0].encode('utf-8')
	## get the name and level of the team, ie 
	## 'Ice Hockey: The Mighty Dads (Casual)'
	if(debugInfo):
		print 'teamString ', teamString
		
	teamName = getTeamName(teamString).replace(',', '')
	## important note here, a bunch of jackasses have created teams with commas
	## in their names which makes me want to die
	
	## but dont worry, cause we can fix this by just removing any commas which
	## may show up in a teams name as a standard
	
	## anyways getTeamName(...) takes the teamString and extracts the teams name
	## from it, ie 
	
	## 'Ice Hockey: The Mighty Dads (Casual)' -> 'The Mighty Dads'
	
	## which should match the name in the opponent column for whatever teams
	## they played
	print teamName
	## useful even when not debugging, so we'll keep it
	indiesTeam = False
	## Indies teams are living death for me, because their pages are formatted
	## slightly differently from regular teams
	if(('Indies' in teamName)or('Inides' in teamName)):
		## learn to spell u idiots
		indiesTeam = True
		## Apparently indies teams dont have captains
		## which royally fucks this up
		## so we make a note of that for later
	
	if(debugInfo):
		print "Team String, ", teamString
	print "Team Name: %s, %s, Id: %s" % (teamName, seasonString, teamId)
	
	players = []
	## in this context, this is just a list of names in string format of all of
	## the players that were on the roster of the team
	for i in range(5, len(content2)):
		## roll through the second layer after we pass some column headings that
		## ended up in here, and add the names into our players list
		players.append(content2[i].encode('utf-8'))
	if(indiesTeam == False):
		## for everybody but indies teams, the captain gets stored in a div one
		## deeper than the rest, because reasons. So we retrieve his/her name
		## from the third layer here, make a note of 
		captainName = content3[1].encode('utf-8')
		## retrieve the captains name which got stuck a layer deeper than the rest	
		print "Captain: ", captainName
		players.append(captainName)
		## the last name in the list is the captain by convention
		
		## but there really should be a marker somewhere to indicate whether
		## there actually was a captain
	
	if(debugInfo):
		print "Roster: "
		for playah in players:
			print playah	
		print "end of roster\n"	
	
	if(indiesTeam == True):
		indiesOffset = 2
	else:
		indiesOffset = 0
		
	numberOfGames = int(seasonLength(len(content3)+indiesOffset))
	## infer the number of games from content layer 3, which needs to be offset
	## by 2 if the team had a captain, since the stupid captains name got dumped
	## into here >-<
	print "Season Length: %i games" % numberOfGames
	
	schedule = []
	
	postponedGames = [8481, 8722]
	socGamed = [8936, 8488]
	## these may not be needed anymore I think
	## they only applied to the old version of the scraper, which wasnt
	## sophisticated enough to handle problems like this without making a
	## special case in the code
	
	for con in content3:
		if(con == "REGULAR SEASON"):
			seasonIndex = content3.index(con)
			## we find the index that the regular season starts at			
	
	
	socGamesIndex = -1
	## by default we dont have any SOC games, so we set the index to a default
	## thatll trigger an error if it gets used
	socGamesFound = False
	if("S.O.C. GAMES" in content3):
		print "SOC Games found"
		socGamesFound = True 
		socGamesIndex = content3.index("S.O.C. GAMES")
		## assign its index so we know where to find soc games
	
	
	playoffGameIndex = -1
	## similar idea with playoffs, theyre not guaranteed to be there, so we dont
	## assume we can find them unles we are sure theyre there
	playoffGamesFound = False
	if("PLAYOFFS" in content3):
		print "Playoff Games found"
		playoffGamesFound = True 
		playoffGameIndex = content3.index("PLAYOFFS")
		## assign its index so we know where to find soc games	
	
	totalIndex = len(content3)-1
	## number of the last index in content3 that can be accessed
	
	## we essentially treat the totalIndex as being the last point in content3
	## that represents data about a game in the schedule (I think???) 
	
	totalSeasonGames = 0	
	totalSOCGames = 0
	totalPlayoffGames = 0
	
	if(socGamesFound):
		totalSOCGames += ((totalIndex-socGamesIndex)/4)
		totalIndex = socGamesIndex
	if(playoffGamesFound):
		totalPlayoffGames += ((totalIndex-playoffGameIndex)/4)
		totalIndex = playoffGameIndex
	totalSeasonGames += ((totalIndex-seasonIndex)/4)
	
	if(inProgressSeason):
		print "Scraping an in progress season, may be buggy"
		## so much for that ^^
		
		## no point in even doing anything with this, since strobe is going the
		## way of the dinosaur pretty soon
	else:
		print "Season Games %i, index %i" % (totalSeasonGames, seasonIndex)
		print "Playoff Games %i, index %i" % (totalPlayoffGames, playoffGameIndex)
		print "SOC Games %i, index %i" % (totalSOCGames, socGamesIndex)				
		## print information about the layout of games in schedule data seen so
		## far
		
		seasonGamesVal = totalSeasonGames
		
		if(debugInfo):
				print range(seasonGamesVal), '\n'
		
		for game in range(seasonGamesVal): 
			access = (seasonIndex+1) + (4*game)
			## access is like the first index of the game data in content3 that
			## we want to access
			
			## that way we can access everything else about the game quickly,
			## like content[access], content[access + 1], content[access + 2],
			## and so on
			if(debugInfo):
				print "access ", access, "/", (len(content3)-1)	
				## quick not to show how far along in content3 the current index
				## is relative to the highest index we can use in this list		
			gameVal = game
			rawScoreData = content3[access+2]
			## pull out the score of the game in question, ie 
			## 'lost 2 - 3'
			outcome = getGameResult(rawScoreData)
			## use a function to tell us whether they won, tied or lost the game
			## (or if the game just hasnt been played yet)
			if(('won' not in rawScoreData)and('lost' not in rawScoreData)and('tie' not in rawScoreData)):
				if(debugInfo):
					print "Found a postponed game"
				## we found a game that was replayed (or if we are in an in
				## progress season, the game hasnt been played yet)
				totalSeasonGames -= 1
				## drop this down by one, since we counted a game that was not
				## actually played in the schedule when we counted the games
				## using the length of content3
				continue
				## jump past this game, cause we dont want it in the schedule
				
				## people who write schedules with postponed games listed like
				## this are the bane of my existence
				
				## just put the original date that the game was supposed to have
				## been played on in a notes column for fucks sakes
			else:
				goalsFor = processGoalsFor(rawScoreData)
				goalsAgainst = processGoalsAgainst(rawScoreData)
				## take the raw score string (ie 'lost 2 - 3') and process it
				## in a function to get the goals scored by and against the team
				## we are looking at
				schedule.append([content3[access], content3[access+1], outcome, goalsFor, goalsAgainst, processSOC(content3[access+3])  , content4[gameVal].replace(',', '').encode('utf-8')])
				## left to right, the game record reads ['date and time', 'Location', 'won', 'SOC Rating', 'opponent name', ]			
				if(debugInfo):
					print "Added Season game # %i" % gameVal

		if(socGamesFound):
			## append the SOC games on after the season, but before the playoffs
			## this could screw up if the SOC game came mid season, but we
			## could just sort the games list by date string at the end
			for game in range(totalSOCGames): 
				access = (socGamesIndex+1) + (4*(game))
				if(debugInfo):
					print "access ", access, "/", (len(content3)-1)
				gameVal = game+totalSeasonGames+totalPlayoffGames
				## gets the sum of the season and playoff games played this
				## season, but LESS the number of soc games that are in the data
				print "gameVal ", gameVal
				## this isnt quite right, but I dont think we'll have a season
				## with both rescheduled games and SOC games
				
				## usually we only get rage OR apathy, not both
				rawScoreData = content3[access+2]
				
				outcome = getGameResult(rawScoreData)
				goalsFor = processGoalsFor(rawScoreData)				
				goalsAgainst = processGoalsAgainst(rawScoreData)
				## grab the rawScoreData
			
				##if(debugInfo == False):
				##	assert isinstance(content4[game], str)

				schedule.append([content3[access], content3[access+1], outcome, goalsFor, goalsAgainst, processSOC(content3[access+3])  , content4[gameVal].replace(',', '').encode('utf-8')])
				## sets up a 2d list, with rows representing games in the
				## schedule
				
				## left to right, the game record reads ['date and time', 'Location', 'won', 'SOC Rating', 'opponent name', ]			
				if(debugInfo):
					print "Added SOC game # %i" % gameVal

		if(playoffGamesFound):
			for game in range(totalPlayoffGames): 
				access = (playoffGameIndex+1) + (4*(game))
				gameVal = game+seasonGamesVal
				if(debugInfo):
					print "access ", access, "/", (len(content3)-1), "game ", gameVal
					print "gameVal ", gameVal
				
				rawScoreData = content3[access+2]
				
				try:
					outcome = getGameResult(rawScoreData)				
					goalsFor = processGoalsFor(rawScoreData)
					goalsAgainst = processGoalsAgainst(rawScoreData)
				except ValueError:
					## this is the shit way of dealing with this
					totalPlayoffGames -= 1
					continue

				schedule.append([content3[access], content3[access+1], outcome, goalsFor, goalsAgainst, processSOC(content3[access+3])  , content4[gameVal].replace(',', '').encode('utf-8')])
				## left to right, the game record reads ['date and time', 'Location', 'won', 'SOC Rating', 'opponent name', ]			
				if(debugInfo):
					print "Added Playoff game # %i" % gameVal


			## !!!! Important Note !!!!
			## This will NOT work with seasons in progress, because the scores for 
			## games not yet played will appear as  - - - or something like that
			## the functions that process the goals will need to adjust for this
		
			## there needs to be a precheck to verify that the game was played
			## before committing the data, TODO
		
			## I would do it now (March 2016) but I cant remember what the unplayed
			## games look like at the moment, and I wont have to worry about it
			## for a while anyways
		
			## later note:
			## overall, I am having a really hard time understanding this
			## section now (July 2016), but its working well for the moment, so
			## I wont go too nuts over figuring it out just yet
				
	numberOfGames = (totalSeasonGames + totalSOCGames + totalPlayoffGames)
	## sum up the total games in the season, then
		

					
	print "Schedule: "
	for game in schedule:
		print game
	print '\n'
	
	## now to save data in the csv
	## TO BE CONTINUED DUN DUN DUN
	if(saveMe == True):
		saveScrapedTeamData(teamId, teamString, seasonString, teamName, players, numberOfGames, (totalSeasonGames+totalSOCGames), (totalSeasonGames+totalSOCGames), totalPlayoffGames, totalPlayoffGames, schedule, leagueId, levelId)
	else:
		print "Not saving data for team %i" % (teamId)

if(__name__ == "__main__"):
	scrapeTeamData(8317, True, 'fall2012', False, 'watMu', 'advanced', True)
