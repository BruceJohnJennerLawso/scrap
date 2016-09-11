## nhlScraper.py ###############################################################
## scraper to grab season data from hockey-reference.com, which has NHL and ####
## WHA data going back to 1918, and possibly even more #########################
################################################################################

# -*- coding: utf-8 -*-

from lxml import html
import requests

import csv

from gameProcessing import *

from multiprocessing import Process


def saveScrapedTeamData(teamName, teamId, seasonName, seasonId, leagueId, regularSeasonLength, seasonGames, playoffRoundLengths, playoffGames, rosterSize, rosterRows):
	## once we have the data about the team in question, usually in string form,
	## we should save it in string format so its more convenient to access
	## elsewhere without connecting to the internet
	outputPath = ("./data/%s/%s/%s%s.csv" % (leagueId, seasonId, teamId, seasonId))
	## in the case of nhl games, we can usually drop the level id, as it isnt
	## really relevant
	print "current output path: %s" % outputPath
	## useful info to see when the scraper is running
	with open(outputPath, 'wb') as foo:
		bar = csv.writer(foo)
		## get set up to write a csv file under the current output path
		bar.writerows([[teamName, teamId, leagueId],\
		 [seasonName, seasonId],\
		  [rosterSize],\
		  [regularSeasonLength], playoffRoundLengths])
		## write the teams name, Id, then leagueId on the first line, ie
		## ['Toronto Maple Leafs', 'TOR', 'nhl']
		## next, write the season name and Id on the second line
		## ['2015-16', '2016']
		## next, the number of players on the roster, ie
		## [46]
		## and finally the number of games played in the regular season,
		## followed by the number of games in each playoff round
		## (we'll use San Jose here to demonstrate)
		## [82]
		## [5,7,6,6] 
		bar.writerows(seasonGames)
		## write out the regular season schedule, line by line for each game
		bar.writerows([''])
		## add in a blank row to separate the season from the playoffs
		bar.writerows(playoffGames)
		## write out playoff games (if any) just like we did with the regular
		## season
		bar.writerows([''])
		## add in another blank row before the Roster
		try:
			bar.writerows(rosterRows)		
			## write out all of the player names and stats, one line per player
		except UnicodeEncodeError:
			print rosterRows
			bar.writerows(rosterRows)


def overtimeIds():
	return ['OT', '2OT', '3OT', '4OT', '5OT', '6OT']

def scrapeTeamData(teamId, debugInfo, seasonId, inProgressSeason, leagueId):
	
	##teamName = 'Toronto Maple Leafs'
	##teamId = 'TOR'
	##seasonName = '2015-16'
	##seasonId = '2016'
	##leagueId = 'nhl'
	##debugInfo = True
	
	page = requests.get('http://www.hockey-reference.com/teams/%s/%s_games.html' % (teamId, seasonId))
	tree = html.fromstring(page.content)

	gamesLists = []
	
	teamInfo = tree.xpath('//h1[@itemprop="name"]/*/text()')
	if(debugInfo):
		print "teamInfo ", teamInfo
	
	seasonName = teamInfo[0]
	teamName = teamInfo[1]
	
	print "\n\n%s %s" % (seasonName, teamName)
	print "Regular Season"

	headingRow = tree.xpath('//div[@id="all_games"]/*/*/table/tbody/tr[%i]/*/text()' % 21)
	if(int(seasonId) <= 2012):
		headingRow.insert(2, 'Time')
	headingRow.insert(3, 'Location')
	headingRow.insert(7, 'Result')
	headingRow.insert(8, 'Game Ended In')		
	if(debugInfo):
		print 'headingRow ', headingRow, ' ', len(headingRow)
	
	gamesLists.append(headingRow)
		
	seasonIndexes = range(1, 21)+range(22,42)+range(43,63)+range(64, 84)+ range(85, 170)	
	for i in seasonIndexes:
		gameRow = tree.xpath('//div[@id="all_games"]/*/*/table/tbody/tr[%i]/*/text()' % i)
		gameRow2 = tree.xpath('//div[@id="all_games"]/*/*/table/tbody/tr[%i]/*/*/text()' % i)		

			## this should hopefully fix the issue with the game Time column
			## messing up the offsets we were expecting
		
		if(len(gameRow) > 0):
			## so we basically have two problems here:
			## one, games only have times available for 2013 and later. Not that
			## big of a deal, but a bit of a headache because the column that it
			## was stored in is now gone, and everything is offset slightly off
			
			## second problem, the game Dates are hyperlinked to the game box
			## scores from 1988 onward, but its just plaintext for 1987 and
			## earlier
			
			## Im thinking the best way of solving these problems is to tackle
			## the overall problem in two steps.
			
			## first, I should save the header row at the start of the game data
			## and use that to index the data instead of hoping for a hard
			## layout across a century worth of data
			
			## and second, Im going to need to rewrite the section right after
			## this so that it can handle the above issues with columns
			## appearing and disappearing depending on the year
			if(int(seasonId) <= 1987):
				if(debugInfo):
					print "Season before 1988"
				if(gameRow[2] != '@'):
					gameRow.insert(2, 'H')
			
				if(gameRow[6] not in ['OT', 'SO']):
					## a little bit weird, but I think it works
					gameRow.insert(6, 'REG')
				gameRow.insert(3, gameRow2[0])
				gameRow.insert(2, 'time unavailable')
				##gameRow.insert(4, gameRow2[1])
			elif((int(seasonId) >= 1988)and(int(seasonId) <= 2012)):
				if(debugInfo):
					print "Season between 1988 and 2012"
				if(gameRow[1] != '@'):
					gameRow.insert(1, 'H')
			
				if(gameRow[5] not in ['OT', 'SO']):
					## a little bit weird, but I think it works
					gameRow.insert(5, 'REG')
				gameRow.insert(1, gameRow2[0])
				gameRow.insert(3, gameRow2[1])
				gameRow.insert(2, 'time unavailable')
			elif((int(seasonId) >= 2013)and(int(seasonId) <= 2015)):
				if(debugInfo):
					print "Season after 2013, before 2016"
				
				if((seasonId == '2014')and(teamId == 'OTT')and(i == 54)):
					continue
				## I cannot figure out why this one was rescheduled
				## most of the rest are blizzards and a medical emergency
				## in the jackets/stars game
				if((seasonId == '2014')and(teamId == 'BUF')and(i == 45)):
					continue
				if((seasonId == '2014')and(teamId == 'CAR')and(i == 46)):
					continue					
				if((seasonId == '2014')and(teamId == 'CAR')and(i == 52)):
					continue	
				if((seasonId == '2014')and(teamId == 'CAR')and(i == 55)):
					continue						
				if((seasonId == '2014')and(teamId == 'PHI')and(i == 53)):
					continue						
				if((seasonId == '2014')and(teamId == 'CBJ')and(i == 68)):
					continue						
				if((seasonId == '2014')and(teamId == 'DAL')and(i == 68)):
					continue						

					## theres a rescheduled game left in the schedule here which
					## throws a wrench into the scraper
					## gonna try jumping over it and seeing how that goes
				
				if(gameRow[2] != '@'):
					gameRow.insert(2, 'H')
				if(gameRow[6] not in ['OT', 'SO']):
					## a little bit weird, but I think it works
					gameRow.insert(6, 'REG')
				gameRow.insert(1, gameRow2[0])
				gameRow.insert(4, gameRow2[1])
			else:
				if(debugInfo):
					print "Season after 2015"
				if(gameRow[2] != '@'):
					gameRow.insert(2, 'H')
				if(gameRow[6] not in ['OT', 'SO']):
					## a little bit weird, but I think it works
					gameRow.insert(6, 'REG')
				gameRow.insert(1, gameRow2[0])
				gameRow.insert(4, gameRow2[1])
				##gameRow.insert(2, 'time unavailable')
			##if('Time' not in headingRow):
			
		
		if(len(gameRow) > 0):
			if(debugInfo):
				print i, ' ', gameRow, ' ', gameRow2, ' ', len(gameRow), '\n'
			gamesLists.append(gameRow)
	regularSeasonLength = len(gamesLists)-1
	
	print 'Season length: %i games' % regularSeasonLength, '\n'













	print "Playoffs"

	playoffGameLists = []
	if(int(seasonId) >= 2016):
		playoffHeaderRow = tree.xpath('//div[@id="all_games_playoffs"]/*/*/table/thead/tr[2]/*/text()')		
	else:
		playoffHeaderRow = tree.xpath('//div[@id="all_games_playoffs"]/*/*/table/thead/tr[1]/*/text()')
	if(int(seasonId) <= 2012):
		playoffHeaderRow.insert(2, 'Time')
	playoffHeaderRow.insert(3, 'Location')
	playoffHeaderRow.insert(7, 'Result')
	playoffHeaderRow.insert(8, 'Game Ended In')		
	
	if(debugInfo):
		print "playoff header row ", playoffHeaderRow, ' ', len(playoffHeaderRow)
	
	playoffRound = 0
	## index of the current playoff round
	playoffRoundLengths = [0]
	## a list of the number of games in each playoff round
	
	if(len(playoffHeaderRow) > 0):
		playoffGameLists.append(playoffHeaderRow)
	
		for i in (range(1, 33)):
			gameRow = tree.xpath('//div[@id="all_games_playoffs"]/*/*/table/tbody/tr[%i]/*/text()' % i)
			if(len(gameRow) == 0):
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
				if(int(seasonId) <= 1987):
					if(gameRow[2] != '@'):
						gameRow.insert(2, 'H')
			
					if(gameRow[6] not in overtimeIds()):
						## a little bit weird, but I think it works
						gameRow.insert(6, 'REG')
					gameRow.insert(3, gameRow2[0])
					gameRow.insert(2, 'time unavailable')
					##gameRow.insert(4, gameRow2[1])
				elif((int(seasonId) >= 1988)and(int(seasonId) <= 2012)):	
					if(gameRow[1] != '@'):
						gameRow.insert(1, 'H')
			
					if(gameRow[5] not in overtimeIds()):
						## a little bit weird, but I think it works
						gameRow.insert(5, 'REG')
					gameRow.insert(1, gameRow2[0])
					gameRow.insert(3, gameRow2[1])
					gameRow.insert(2, 'time unavailable')
				elif((int(seasonId) >= 2013)and(int(seasonId) <= 2015)):
					if(debugInfo):
						print "Season after 2013, before 2016"	
					if(gameRow[2] != '@'):
						gameRow.insert(2, 'H')
					if(gameRow[6] not in overtimeIds()):
						## a little bit weird, but I think it works
						gameRow.insert(6, 'REG')
					gameRow.insert(1, gameRow2[0])
					gameRow.insert(4, gameRow2[1])	
				else:
					if(debugInfo):
						print "Season after 2015"	
					if(gameRow[2] != '@'):
						gameRow.insert(2, 'H')
					if(gameRow[6] not in overtimeIds()):
						## a little bit weird, but I think it works
						gameRow.insert(6, 'REG')
					gameRow.insert(1, gameRow2[0])
					gameRow.insert(4, gameRow2[1])				
			if(len(gameRow) > 0):
				if(debugInfo):
					print i, ' ', gameRow, ' ', gameRow2, ' ', len(gameRow), '\n'
				playoffGameLists.append(gameRow)
				playoffRoundLengths[playoffRound] += 1
		print 'playoffLength ', len(playoffGameLists)-1, ' games'
		print 'playoffRoundLengths: ', playoffRoundLengths, '\n'

	##teamString = content1[0].encode('utf-8')
	
	
	##if(debugInfo):
	##	print 'teamString ', teamString
	##teamName = getTeamName(teamString).replace(',', '')
	if(debugInfo):
		print "Team Name: %s, %s" % (teamName, seasonName)
	
	
	page = requests.get('http://www.hockey-reference.com/teams/%s/%s.html' % (teamId, seasonId))
	tree = html.fromstring(page.content)	
	## lets try to reset this to get the roster info

	print "Roster"


	playerRows = []

	for i in range(0, 50):
		playerRow = tree.xpath('//table[@id="roster"]/tbody/tr[%i]/*/text()' % i)
		playerRow2 = tree.xpath('//table[@id="roster"]/tbody/tr[%i]/*/*/text()' % i)
		
		if(debugInfo):
			print "Preprocessed"
			print "playerRow ", playerRow, " %i\n" % len(playerRow)
			print "playerRow2 ", playerRow2, " %i\n" % len(playerRow2)			
		
		if(len(playerRow) == 0):
			continue
		else:
			if(len(playerRow2) < 2):
				playerRow2.append('unknown')
				## odd case where country of birth data is not available, so we
				## are going to attach a default that can be added
				
				## thank you David Dziurzynski, wherever you come from
			if(len(playerRow) < 9):
				playerRow.insert(0, 'n/a')
				
				if(playerRow2[1] == '(C)'):
					## the case where the player in this row is the team captain,
					## which throws a small monkeywrench into the proceedings
					playerRow = playerRow[0:1]+playerRow[2:len(playerRow)]
					## the first thing we need to do is get rid of this weird
					## (C) character that gets placed in the row by splitting and
					## reattaching the list around it
					playerRow.insert(0, playerRow2[0].encode('utf-8'))
					## place the players name at the start of the list
					playerRow.insert(9, playerRow2[2])
					## put their country of birth right after their birthdate
					playerRow.insert(1, '(C)')
					## make a note of that captains C right after the name
				else:
					playerRow.insert(0, playerRow2[0].encode('utf-8'))
					## player name at start
					playerRow.insert(9, playerRow2[1])
					## player country after birthdate. Note the different offset
					## in playerRow2 here		
					playerRow.insert(1, '')
					## put a blank where the captains C would go, since this player
					## is not a captain

			else:
				if(playerRow2[1] == '(C)'):
					if(playerRow[1] == u'\xa0'):
						## the case where the player in this row is the team captain,
						## which throws a small monkeywrench into the proceedings
						playerRow = playerRow[0:1]+playerRow[2:len(playerRow)]
						## the first thing we need to do is get rid of this weird
						## (C) character that gets placed in the row by splitting and
						## reattaching the list around it
						playerRow.insert(0, playerRow2[0].encode('utf-8'))
						## place the players name at the start of the list
						playerRow.insert(9, playerRow2[2])
						## put their country of birth right after their birthdate
						playerRow.insert(1, '(C)')
						## make a note of that captains C right after the name
					elif(playerRow[0] == u'\xa0'):
						## case where an old team before 1951 has a team captain
						## without his jersey number listed
						playerRow = ['n/a']+playerRow[1:len(playerRow)]
						## the first thing we need to do is get rid of this weird
						## (C) character that gets placed in the row by splitting and
						## reattaching the list around it
						playerRow.insert(0, playerRow2[0].encode('utf-8'))
						## place the players name at the start of the list
						playerRow.insert(9, playerRow2[2])
						## put their country of birth right after their birthdate
						playerRow.insert(1, '(C)')
						## make a note of that captains C right after the name						
					
				else:
					playerRow.insert(0, playerRow2[0].encode('utf-8'))
					## player name at start
					playerRow.insert(9, playerRow2[1])
					## player country after birthdate. Note the different offset
					## in playerRow2 here		
					playerRow.insert(1, '')
					## put a blank where the captains C would go, since this player
					## is not a captain
			playerRows.append(playerRow)
			
					
		if(debugInfo):
			print "Post-Processed"
			print i, ' ', playerRow, playerRow2, ' ', len(playerRow), '\n'
		## an important note about this, most of the recent data is in good
		## shape, but at least one old team (TRA 1918) has missing player height
		## and weight data for at least one player, which will fuck some of the
		## data up
		
		##if(len(playerRow) != 11):
		##	print "irregular line"
	
	numberOfPlayers = len(playerRows)
	print "%i players" % (numberOfPlayers)
		
	
	
	## now to figure out a good layout for the data in CSV...
	
	## TO BE CONTINUED DUN DUN DUN
	
	
	p1 = Process(target = saveScrapedTeamData, args=(teamName, teamId, seasonName, seasonId, leagueId, regularSeasonLength, gamesLists, playoffRoundLengths, playoffGameLists, numberOfPlayers, playerRows))
	p1.start()
	
	
	##saveScrapedTeamData(teamName, teamId, seasonName, seasonId, leagueId, regularSeasonLength, gamesLists, playoffRoundLengths, playoffGameLists, numberOfPlayers, playerRows)
	

if(__name__ == "__main__"):
	##scrapeTeamData('SJS', False, '2016', False, 'nhl')
	##scrapeTeamData('SJS', False, '2012', False, 'nhl')	
	scrapeTeamData('TOR', False, '2016', False, 'nhl')	
