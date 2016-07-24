## nhlScraper.py ###############################################################
## scraper to grab season data from hockey-reference.com, which has NHL and ####
## WHA data going back to 1918, and possibly even more #########################
################################################################################

# -*- coding: utf-8 -*-

from lxml import html
import requests

import csv

from gameProcessing import *



def saveScrapedTeamData(teamId, teamString, seasonString, teamName, players, numberOfGames, schedule, leagueId, levelId):
	outputPath = ("./data/%s/%s/%s/%i.csv" % (leagueId, levelId,seasonString, teamId))
	print "current output path: %s" % outputPath
	with open(outputPath, 'wb') as foo:
		bar = csv.writer(foo)
		bar.writerows([[teamName, seasonString, teamString], [numberOfGames]])
		bar.writerows(schedule)
		bar.writerows([''])
		bar.writerows([players])
		## ahahahaha my life




## abandon all hope of comprehension, ye who enter here

##def scrapeTeamData(teamId, debugInfo, seasonString, inProgressSeason, leagueId, levelId):

def scrapeTeamData():
	## gotta pass in the season, since the system doesnt display it anywhere
	## for some reason
	teamId = 'SJS'
	seasonString = '2016'
	debugInfo = True
	page = requests.get('http://www.hockey-reference.com/teams/%s/%s_games.html' % (teamId, seasonString))
	tree = html.fromstring(page.content)

	gamesLists = []
	
	teamInfo = tree.xpath('//h1[@itemprop="name"]/*/text()')
	print "teamInfo ", teamInfo
	
	seasonName = teamInfo[0]
	teamName = teamInfo[1]
	
	print "Regular Season"
	
	for i in (range(1, 21)+range(22,42)+range(43,63)+range(64, 84)+ range(85, 170)):
		gameRow = tree.xpath('//div[@id="all_games"]/*/*/table/tbody/tr[%i]/*/text()' % i)
		gameRow2 = tree.xpath('//div[@id="all_games"]/*/*/table/tbody/tr[%i]/*/*/text()' % i)		
		
		if(len(gameRow) > 0):
			if(gameRow[2] != '@'):
				gameRow.insert(2, '')
				## maybe 'H' here for host?
			
			if(gameRow[6] not in ['OT', 'SO']):
				## a little bit weird, but I think it works
				gameRow.insert(6, '')
			gameRow.insert(1, gameRow2[0])
			gameRow.insert(4, gameRow2[1])
		
		if(len(gameRow) > 0):
			print i, ' ', gameRow, ' ', gameRow2, ' ', len(gameRow), '\n'
			gamesLists.append(gameRow)
	seasonLength = len(gamesLists)
	
	print 'seasonLength %i games' % seasonLength

	print "Playoffs"

	playoffGameLists = []
	
	playoffRound = 0
	## index of the current playoff round
	playoffRoundLengths = [0]
	## a list of the number of games in each playoff round
	for i in (range(1, 33)):
		gameRow = tree.xpath('//div[@id="all_games_playoffs"]/*/*/table/tbody/tr[%i]/*/text()' % i)
		if(len(gameRow) == 0):
			print "No Playoff Games"
			break
		
		gameRow2 = tree.xpath('//div[@id="all_games_playoffs"]/*/*/table/tbody/tr[%i]/*/*/text()' % i)		
		
		
		
		if(len(gameRow) == 0):
			## we hit the end of the playoffs for this team, so the loop will
			## just keep cycling and doing this until we hit 33
			continue
			
		if(gameRow[0] == 'GP'):
			playoffRound += 1
			playoffRoundLengths.append(0)
			continue
		if(len(gameRow) > 0):
			if(gameRow[2] != '@'):
				gameRow.insert(2, '')
				## maybe 'H' here for host?
			
			if(gameRow[6] not in ['OT', 'SO']):
				## a little bit weird, but I think it works
				gameRow.insert(6, '')
			gameRow.insert(1, gameRow2[0])
			gameRow.insert(4, gameRow2[1])
		
		if(len(gameRow) > 0):
			print i, ' ', gameRow, ' ', gameRow2, ' ', len(gameRow), '\n'
			playoffGameLists.append(gameRow)
	print 'playoffLength ', len(playoffGameLists), ' games'






	##teamString = content1[0].encode('utf-8')
	
	
	##if(debugInfo):
	##	print 'teamString ', teamString
	##teamName = getTeamName(teamString).replace(',', '')
	
	print "Team Name: %s, %s" % (teamName, seasonName)
	
	
	page = requests.get('http://www.hockey-reference.com/teams/%s/%s.html' % (teamId, seasonString))
	tree = html.fromstring(page.content)	
	## lets try to reset this to get the roster info
	
	players = []
	for i in range(6, len(content2)):
		players.append(content2[i].encode('utf-8'))
	if(indiesTeam == False):
		captainName = content3[1].encode('utf-8')
		## retrieve the captains name which got stuck a layer deeper than the rest	
		print "Captain: ", captainName
		players.append(captainName)
	## might just make the last name the captain by convention
	
	
	print "Roster: "
	for playah in players:
		print playah	
	print players	

	print "end of roster\n"	
	
	
	if(indiesTeam == True):
		indiesOffset = 2
	else:
		indiesOffset = 0
		
	numberOfGames = int(seasonLength(len(content3)+indiesOffset))
	print "Season Length: %i games" % numberOfGames
	
	schedule = []
	
	postponedGames = [8481, 8722]
	
	socGamed = [8936, 8488]
	
	
	
	for con in content3:
		if(con == "REGULAR SEASON"):
			seasonIndex = content3.index(con)
			## we find the index that the regular season starts at
			
	socGamesIndex = -1
	socGamesFound = False
	## default value if we dont find any SOC games in the schedule
	if("S.O.C. GAMES" in content3):
		print "SOC Games found"
		socGamesFound = True 
		socGamesIndex = content3.index("S.O.C. GAMES")
		## assign its index so we know where to find soc games
	playoffGameIndex = -1
	playoffGamesFound = False
	if("PLAYOFFS" in content3):
		print "SOC Games found"
		playoffGamesFound = True 
		playoffGameIndex = content3.index("PLAYOFFS")
		## assign its index so we know where to find soc games	
	totalIndex = len(content3)-1
	## number of the last index
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
	else:
		print "Season Games %i, index %i" % (totalSeasonGames, seasonIndex)
		print "Playoff Games %i, index %i" % (totalPlayoffGames, playoffGameIndex)
		print "SOC Games %i, index %i" % (totalSOCGames, socGamesIndex)				
		seasonGamesVal = totalSeasonGames
		for game in range(seasonGamesVal): 
			print range(seasonGamesVal)
			access = (seasonIndex+1) + (4*game)
			print "access ", access, "/", (len(content3)-1)			
			gameVal = game
			rawScoreData = content3[access+2]
			##print rawScoreData
			outcome = gameResult(rawScoreData)
			if(('won' not in rawScoreData)and('lost' not in rawScoreData)and('tie' not in rawScoreData)):
				print "Found a postponed game"
				## we found a game that was replayed (or if we are in an in
				## progress season, the game hasnt been played yet)
				totalSeasonGames -= 1
				## drop this down by one, since we counted a game that was not
				## actually played
				continue
				## jump past this game, cause we dont want it in the schedule
			else:
				goalsFor = processGoalsFor(rawScoreData, outcome)
				goalsAgainst = processGoalsAgainst(rawScoreData, outcome)
				
				##if(debugInfo == False):
				##	assert isinstance(content4[game], str)

				schedule.append([content3[access], content3[access+1], outcome, goalsFor, goalsAgainst, processSOC(content3[access+3])  , content4[gameVal].replace(',', '').encode('utf-8')])
				## left to right, the game record reads ['date and time', 'Location', 'won', 'SOC Rating', 'opponent name', ]			
				print "Added Season game # %i" % gameVal

		if(socGamesFound):
			## append the SOC games on after the season, but before the playoffs
			## this could screw up if the SOC game came mid season, but we
			## could just sort the games list by date string at the end
			for game in range(totalSOCGames): 
				access = (socGamesIndex+1) + (4*(game))
				print "access ", access, "/", (len(content3)-1)
				gameVal = game+totalSeasonGames+totalPlayoffGames
				print "gameVal ", gameVal
				## this isnt quite right, but I dont think we'll have a season
				## with both rescheduled games and SOC games
				rawScoreData = content3[access+2]
				outcome = gameResult(rawScoreData)
				goalsFor = processGoalsFor(rawScoreData, outcome)
				goalsAgainst = processGoalsAgainst(rawScoreData, outcome)
			
				##if(debugInfo == False):
				##	assert isinstance(content4[game], str)

				schedule.append([content3[access], content3[access+1], outcome, goalsFor, goalsAgainst, processSOC(content3[access+3])  , content4[gameVal].replace(',', '').encode('utf-8')])
				## left to right, the game record reads ['date and time', 'Location', 'won', 'SOC Rating', 'opponent name', ]			
				print "Added SOC game # %i" % gameVal

		if(playoffGamesFound):
			for game in range(totalPlayoffGames): 
				access = (playoffGameIndex+1) + (4*(game))
				gameVal = game+seasonGamesVal
				print "access ", access, "/", (len(content3)-1), "game ", gameVal
				print "gameVal ", gameVal
				rawScoreData = content3[access+2]
				outcome = gameResult(rawScoreData)				
				goalsFor = processGoalsFor(rawScoreData, outcome)
				goalsAgainst = processGoalsAgainst(rawScoreData, outcome)
				##if(debugInfo == False):
				##	assert isinstance(content4[game], str)

				schedule.append([content3[access], content3[access+1], outcome, goalsFor, goalsAgainst, processSOC(content3[access+3])  , content4[gameVal].replace(',', '').encode('utf-8')])
				## left to right, the game record reads ['date and time', 'Location', 'won', 'SOC Rating', 'opponent name', ]			
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
		
				
	numberOfGames = (totalSeasonGames + totalSOCGames + totalPlayoffGames)
					
	print "Schedule: "
	for game in schedule:
		print game
	
	if(debugInfo == True):
	
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
	
		##foo = 2
		##print "content3[%i] " %	(foo), content3[foo]
	
		##print tree.xpath('//div[@id="primarycontent"]/*/*[%i]/text()' % (1))
	print '\n'
	
	
	## now to figure out a good layout for the data in CSV...
	
	## TO BE CONTINUED DUN DUN DUN
	
	## this might be a good spot to jump into a second function with the data
	##saveScrapedTeamData(teamId, teamString, seasonString, teamName, players, numberOfGames, schedule, leagueId, levelId)
	
	## cant decide whether I want to break the date strings down a bit before
	## I start on this

if(__name__ == "__main__"):
	scrapeTeamData()
