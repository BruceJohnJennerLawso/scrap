## nhlScraper.py ###############################################################
## scraper to grab season data from hockey-reference.com, which has NHL and ####
## WHA data going back to 1918, and possibly even more #########################
################################################################################

# -*- coding: utf-8 -*-

from lxml import html
import requests

import csv

from gameProcessing import *



def saveScrapedTeamData(teamName, teamId, seasonName, seasonId, leagueId, regularSeasonLength, seasonGames, playoffRoundLengths, playoffGames, rosterSize, rosterRows):
	outputPath = ("./data/%s/%s/%s%s.csv" % (leagueId, seasonId, teamId, seasonId))
	print "current output path: %s" % outputPath
	with open(outputPath, 'wb') as foo:
		bar = csv.writer(foo)
		bar.writerows([[teamName, teamId, leagueId], [seasonName, seasonId], [rosterSize], [regularSeasonLength], playoffRoundLengths])
		bar.writerows(seasonGames)
		bar.writerows([''])
		bar.writerows(playoffGames)
		bar.writerows([''])
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
	
	print "%s %s" % (seasonName, teamName)
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
			if(debugInfo):
				print i, ' ', gameRow, ' ', gameRow2, ' ', len(gameRow), '\n'
			gamesLists.append(gameRow)
	regularSeasonLength = len(gamesLists)
	
	print 'Season length: %i games' % regularSeasonLength, '\n'

	print "Playoffs"

	playoffGameLists = []
	
	playoffRound = 0
	## index of the current playoff round
	playoffRoundLengths = [0]
	## a list of the number of games in each playoff round
	for i in (range(1, 33)):
		gameRow = tree.xpath('//div[@id="all_games_playoffs"]/*/*/table/tbody/tr[%i]/*/text()' % i)
		if(len(gameRow) == 0):
			print "No Playoff Games (assuming DNQ)"
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
				gameRow.insert(2, 'H')
				## maybe 'H' here for host?
			
			if(gameRow[6] not in overtimeIds()):
				## a little bit weird, but I think it works
				gameRow.insert(6, '')
			gameRow.insert(1, gameRow2[0])
			gameRow.insert(4, gameRow2[1])
		
		if(len(gameRow) > 0):
			if(debugInfo):
				print i, ' ', gameRow, ' ', gameRow2, ' ', len(gameRow), '\n'
			playoffGameLists.append(gameRow)
			playoffRoundLengths[playoffRound] += 1
	print 'playoffLength ', len(playoffGameLists), ' games'
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
		if(len(playerRow) == 0):
			continue
		else:
			if(playerRow2[1] == '(C)'):
				## the case where the player in this row is the team captain,
				## which throws a small monkeywrench into the proceedings
				playerRow = playerRow[0:1]+playerRow[2:len(playerRow)]
				## the first thing we need to do is get rid of this weird
				## (C) character that gets placed in the row by splitting and
				## reattaching the list
				playerRow.insert(0, playerRow2[0])
				## place the players name at the start of the list
				playerRow.insert(9, playerRow2[2])
				## put their country of birth right after their birthdate
				playerRow.insert(1, '(C)')
				## make a note of that captains C right after the name
			else:
				playerRow.insert(0, playerRow2[0])
				## player name at start
				playerRow.insert(9, playerRow2[1])
				## player country after birthdate. Note the different offset
				## in playerRow2 here		
				playerRow.insert(1, '')
				## put a blank where the captains C would go, since this player
				## is not a captain
			playerRows.append(playerRow)
					
		if(debugInfo):
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
	
	saveScrapedTeamData(teamName, teamId, seasonName, seasonId, leagueId, regularSeasonLength, gamesLists, playoffRoundLengths, playoffGameLists, numberOfPlayers, playerRows)
	

if(__name__ == "__main__"):
	scrapeTeamData('TOR', False, '2016', False, 'nhl')
