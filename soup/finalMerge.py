## finalMerge.py ###############################################################
## now that the raw data files are downloaded, player emails are available in ##
## a spreadsheet for each team, and a map of players to hashes #################
## has been built, a sequence of changes need to be made to generate a final  ##
## 'good copy' of the data which has:                                         ##
## -The email field for each player is populated where available from the     ##
## [teamId]_RosterData.csv                                                    ##
## -Names and emails scrubbed out and replaced by the appropriate hash from   ##
## the csv that maps emails (hopefully unique) to an anonymous id made up of  ##
## randomly selected words, unique to that player (at least in theory)        ##
## -The 'Date/Time' field for games in the csv converted from one string with ##
## the data appended all together, something like 'Sat Sep 24 @ 5:00 pm', to  ##
## a series of individual fields, ie 'Year', 'Month', 'Day', 'Hour', 'Minute' ##
##								      2011,     09,    24,     5,       00    ##
## (note that the year is not available in the csv file, but can be inferred  ##
## from the seasonId value used in the team lookup chain)                     ##
## -do the same for the 'Score' string field, ie take a value 'won 0 - 4' and ##
## convert it to                     'result',   'goalsFor', 'goalsAgainst'   ##
##                                     'W'   ,       4     ,       0          ##
## -the seasonId, year, and term should be noted in the info section of the   ##
## csv as additional parameters for convenience                               ##
## -additionally use this run of the script to populate all of those          ##
## parameters that the original page scraper created but was unable to fill,  ##
## ie sportId, sportName, sportRules, levelId, seasonName, seasonId           ##
##                                                                            ##
## the order of operations here will look like this:                          ##
## open up all of the teamIds one by one, and for each do the following:      ##
## 		-load both files [teamId]_RosterData.csv and [teamId].csv and convert ##
##		contents to a dictionary to make them easier to work with             ##
##		-merge over the dictionary with the emails from the strobe panel to   ##
##		the main one so players that didnt have an email available before are ##
##		properly populated. Note that this may be a tricky step because of    ##
##		the possibility of two players with the same name on the same team,   ##
##		but the only way that could matter is if one was a captain and one was##
##		not...                                                                ##
##		for the strobe dataset it will all be much simpler if the dictionary  ##
##		of players starts with the emails as a key, then builds up the rest   ##
##		the data from there before saving                                     ##
##		-populate new fields in each game dict from the 
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests
import os
import csv

import ast

import numpy as np

from sys import argv

##from obfuscant import convertTeamFileToDictionaries



def convertRosterFileToDictionaries(rosterFileContent):
	
	
	infoStartIndex = rosterFileContent.index(['INFO:'])
	infoEndIndex = rosterFileContent.index(['END_INFO'])
	
	infoDictionary = {}
	
	infoContent = rosterFileContent[infoStartIndex+1:infoEndIndex]
	
	for row in infoContent:
		if(len(row) > 2):
			infoDictionary[row[0]] = row[1:]
		else:
			infoDictionary[row[0]] = row[1]


	rosterStartIndex = rosterFileContent.index(['ROSTER_DATA:'])
	rosterEndIndex = rosterFileContent.index(['END_ROSTERDATA'])			


	
	rosterContent = rosterFileContent[rosterStartIndex+1:rosterEndIndex]
	
	rosterHeader = rosterContent[0]
	
	rosterContent = rosterContent[1:]
	
	rosterEmailFound = rosterHeader.index('emailFound')
	rosterEmailListed = rosterHeader.index('emailListed')
	
	rosterDictionary = {}
	
	for row in rosterContent:
		rosterFirstName = rosterHeader.index('playerNameFirst')
		rosterLastName = rosterHeader.index('playerNameLast')
		if(row[rosterEmailFound] == 'True'):
			## thisPlayerKey = row[rosterEmailListed]
			## the raw email of the player
			
			firstName = row[rosterFirstName]
			lastName = row[rosterLastName]

						
			thisPlayerEmail = row[rosterEmailListed]	

			thisPlayerKey = lastName+"_"+firstName+"_"+thisPlayerEmail			
	
		else:
			## a unique email was not listed for the player in question, so 
			## i will need to fabricate a new one from a mishmash of data
			## specific to the player
			rosterFirstName = rosterHeader.index('playerNameFirst')
			rosterLastName = rosterHeader.index('playerNameLast')
			
			firstName = row[rosterFirstName]
			lastName = row[rosterLastName]
			teamId = infoDictionary['teamId']
			
			tempPlayerId = 	lastName+'_'+firstName+'_'+teamId
			
			
			thisPlayerKey = tempPlayerId

		rosterDictionary[thisPlayerKey] = {}
		for heading in rosterHeader:
			headingIndex = rosterHeader.index(heading)
			rosterDictionary[thisPlayerKey][heading] = row[headingIndex]
		rosterDictionary[thisPlayerKey]['playerId'] = thisPlayerKey
			
	return infoDictionary, rosterDictionary















def convertTeamFileToDictionaries(teamFileContent):
	
	
	infoStartIndex = teamFileContent.index(['INFO:'])
	infoEndIndex = teamFileContent.index(['END_INFO'])
	
	infoDictionary = {}
	
	infoContent = teamFileContent[infoStartIndex+1:infoEndIndex]
	
	for row in infoContent:
		row = [con for con in row if con != ""]
		
		if(len(row) > 2):
			infoDictionary[row[0]] = row[1:]
		else:
			infoDictionary[row[0]] = row[1]

	seasonStartIndex = teamFileContent.index(['SEASON:'])
	seasonEndIndex = teamFileContent.index(['END_SEASON'])
	
	seasonDictionary = {}
	
	seasonContent = teamFileContent[seasonStartIndex+1:seasonEndIndex]
	
	seasonHeader = seasonContent[0]
	seasonContent = seasonContent[1:]
	
	
	for row in seasonContent:
		seasonDictionary[row[0]] = {}
		for col in row[1:]:
			colHeading = seasonHeader[row.index(col)]
			
			seasonDictionary[row[0]][colHeading] = col
##
	playoffsStartIndex = teamFileContent.index(['PLAYOFFS:'])
	playoffsEndIndex = teamFileContent.index(['END_PLAYOFFS'])
	
	playoffsDictionary = {}
	
	playoffsContent = teamFileContent[playoffsStartIndex+1:playoffsEndIndex]
	
	playoffsHeader = playoffsContent[0]
	playoffsContent = playoffsContent[1:]
	
	
	for row in playoffsContent:
		playoffsDictionary[row[0]] = {}
		for col in row[1:]:
			colHeading = playoffsHeader[row.index(col)]
			
			playoffsDictionary[row[0]][colHeading] = col

##

	rosterStartIndex = teamFileContent.index(['ROSTER:'])
	rosterEndIndex = teamFileContent.index(['END_ROSTER'])			


	
	rosterContent = teamFileContent[rosterStartIndex+1:rosterEndIndex]
	
	rosterHeader = rosterContent[0]
	
	rosterContent = rosterContent[1:]
	

	
	rosterDictionary = {}
	
	i = 0
	
	for row in rosterContent:
		i += 1
		
		playerIndex = i
		
		playerId = row[0]+"%i" % playerIndex
		
		rosterDictionary[playerId] = {}
		for col in row:
			colHeading = rosterHeader[row.index(col)]
			
			rosterDictionary[playerId][colHeading] = col
			
	return infoDictionary, seasonDictionary, playoffsDictionary, rosterDictionary



def mergeRosterDictionaries(teamId, seasonId, levelId, sportId, sportName, rosterEmailDict, rosterDict, hashMapDict, debugInfo=False):
	
	
	
	
	
	captainsCount = 0
		
		
	captainsCountForThisTeam = 0
	
	captainsAlreadyAssigned = []
	
	
	playerAlreadyLookedAt = []
	## we want to count the total number of captains in the teamData roster, but
	## avoid double counting them if the captain has a duplicate entry
	for player in rosterDict:
		
		
		if(rosterDict[player]['Captaincy'] != ''):
			if(rosterDict[player]['Player'] not in playerAlreadyLookedAt):
				captainsCountForThisTeam += 1 						
		playerAlreadyLookedAt.append(rosterDict[player]['Player'])
		
		
	for player in rosterEmailDict:
		
		playerName = rosterEmailDict[player]['playerNameFirst']+" "+rosterEmailDict[player]['playerNameLast']
		
		if(playerName in [rosterDict[playerId]['Player'] for playerId in rosterDict]):
			thisPlayerMatches = []
			for playerId in rosterDict:
				if(rosterDict[playerId]['Player'] == playerName):
					thisPlayerMatches.append(playerId)
			
			if(len(thisPlayerMatches) > 1):
				## multiple instances of a given player with the same name were
				## found in the teamData roster
				if('(C)' in [rosterDict[playerMatchId]['Captaincy'] for playerMatchId in thisPlayerMatches]):
						
					print "Captain with multi-name issue incoming..."
					
				else:
					print "No Captains for duplicate name '%s', should be safe to continue" % playerName
			
			playerInstanceToLookAt = len([thisPlayerName for thisPlayerName in captainsAlreadyAssigned if thisPlayerName == playerName])
			## the idea here is really hacky, basically just assume that the
			## order that players appear in each player list (and from that also
			## the matchesList for this players name), so from that we can infer
			## exactly which one we are looking at
			## the list above is the count of players with the same name as this
			## player that have been looked at, so the index bumps up to 1
			## (the second player with that name), if a captain with that name
			## has already been found
			## that way, in the most aggravating example of this issue,
			## ./data/basketball/indoor-floor-4-5vs_0GK/watMu/intermediate/fall2010/4742
			## the first instance of J.F., is the captain, and the second one is
			## the non captain with the same name J.F., and they all get
			## assigned their captaincies correctly
			rosterEmailDict[player]['Captaincy'] = rosterDict[thisPlayerMatches[playerInstanceToLookAt]]['Captaincy']
			if(rosterEmailDict[player]['Captaincy'] == '(C)'):
				captainsAlreadyAssigned.append(playerName)

		else:
			rosterEmailDict[player]['Captaincy'] = 'n/a'

	for player in rosterEmailDict:
		if(rosterEmailDict[player]['Captaincy'] == '(C)'):
			captainsCount += 1
	
	
		
	if((captainsCount > 1)or(captainsCount != captainsCountForThisTeam)):
	
		print "RAW: ", rosterDict, "\n\n", rosterEmailDict	
		
		for player in rosterDict:
			print player, '\n\n', rosterDict[player], '\n'
					
		for player in rosterEmailDict:
			playerName = rosterEmailDict[player]['playerNameFirst']+" "+rosterEmailDict[player]['playerNameLast']
			
		print player, '\n', repr(playerName), '\n', rosterEmailDict[player], '\n\n'	
		
		
		print "Captains count at %i, possible error" % captainsCount
			
		exit()

	if(debugInfo):

		print "\n\n"	
	
		for player in rosterDict:
			print player, '\n\n', rosterDict[player], '\n'
	
		print "\n\n"
	
			
		for player in rosterEmailDict:
			playerName = rosterEmailDict[player]['playerNameFirst']+" "+rosterEmailDict[player]['playerNameLast']
			
			print player, '\n', repr(playerName), '\n', rosterEmailDict[player], '\n\n'										
	
		print "Email Roster Count: ",len(rosterEmailDict)
		print "teamData Roster Count", len(rosterDict)	
	
	if(len(rosterEmailDict) != len(rosterDict)):
		print "rosterEmail list and teamData roster lists inconsistent, possible error"	
		if('Free Agent' not in str([rosterEmailDict[player]['playerNameLast'] for player in rosterEmailDict])):	
			
			teamsWithDuplicatePlayers = []
			## these all appear to be cases where a player shows up twice in both the team
			## roster and the email panel roster, but the email is the same both times
			
			setForTeamDataRoster = sorted(list(set([rosterDict[player]['Player'] for player in rosterDict])))

			setForEmailRoster = sorted([rosterEmailDict[player]['playerNameFirst']+" "+rosterEmailDict[player]['playerNameLast'] for player in rosterEmailDict])
			
			
			
			
			if(teamId not in teamsWithDuplicatePlayers):
				print "Hahaha"
				print "teamData Roster ", setForTeamDataRoster, "\n"
				print "email Roster ", setForEmailRoster	
				if(setForTeamDataRoster == setForEmailRoster):
					print "Error appears to be a duplicate player record, name sets are matching\n, readjusting...\n\n"
					newRosterDict = {}
					
					
					availableNamesToAdd = [rosterEmailDict[player]['playerNameFirst']+" "+rosterEmailDict[player]['playerNameLast'] for player in rosterEmailDict]
					originalEmailRosterNameList = [playerName for playerName in availableNamesToAdd]
					## this is the set names for all of the players considered unique in the email
					## panel roster (those with a unique email, first name, last name combination)
					## so in at least one case, there is a team out there that has two players with
					## the exact same full name, but their emails listed in the email panel are
					## different, so they can be distinguished as two different people
					
					## in the case where
					
					## so for some cases where there is actually
					
					for player in rosterDict:
						playerName = rosterDict[player]['Player']
						
						
						if(playerName in setForEmailRoster):
							if(playerName in availableNamesToAdd):
								newRosterDict[player] = rosterDict[player]
								##currentListOfUniquePlayers.append(playerName)
								availableNamesToAdd.remove(playerName)
								## rebuild the teamData Roster player by player, avoiding including a distinct
								## player twice
							else:
								## this is the case where the player being looked at by name is not available
								## as an option to add. This could be due to a more fundamental mismatch
								## between the rosters listed under the email panel and the teamData, or it
								## could just be that the player has a duplicate record which has already been
								## added to the new roster once
								if(playerName not in originalEmailRosterNameList):
									print "Player name '%s' not found in the emailRosterList,\n teamData and email roster lists do not match"
									exit()
								else:
									print "Skipping over player name '%s', this name already added to roster" % playerName
									
						else:
							## this is the case where player looked at in the teamData roster doesnt exist
							## in the email panel one, I have not yet encountered this error yet
							print "Player name '%s' not found in the emailRosterList,\n teamData and email roster lists do not match"
							exit()
						
					## once finished looping, reset the player dict to new one that was built here
					rosterDict = newRosterDict	
						
				else:		
					## the set of names listed in the email panel roster does not match the one in
					## the teamData Roster, so something is really not right here, and it is
					## important to stop and check to figure out what the hell is going on
					
					if('Individuals' in [rosterEmailDict[player]['playerNameFirst'] for player in rosterEmailDict]):
						placeHolderFreeAgentCaptain = ""
						for player in rosterEmailDict:
							if(rosterEmailDict[player]['playerNameFirst'] == 'Individuals'):
								placeHolderFreeAgentCaptain = player
								break
						del rosterEmailDict[player]
					else:
						print "teamData Roster set and email Panel Roster set do not match"
						exit()
		else:
			print "appears to be special free agent captain"	
		## at least one team now has two players indistinguishable
		## (Ball hockey 2009 winter 2442), because they listed the
		## exact same email	
		
		## this was 'fixed' by adjusting the player key to include
		## both the player email *and* the players first/last names
		## that way someEmail@gmail.com becomes 
		## someEmail@gmail.com_John_Doe
		## and
		## someEmail@gmail.com_Jane_Doe,
		## which then gets fed into the whole hashing process and
		## become unique ids
		
	mergedRosterDict = {}
	
	for player in rosterEmailDict:
		hashedPlayerKey = hashMapDict[player]['hashedPlayerId']
		##hashedPlayerKey = player
		
		mergedRosterDict[hashedPlayerKey] = {}
		
		mergedRosterDict[hashedPlayerKey]['playerKey'] = player
		
		for fieldKey in rosterEmailDict[player]:
			mergedRosterDict[hashedPlayerKey][fieldKey] = rosterEmailDict[player][fieldKey]
		
		
	return mergedRosterDict




def updateTeamInfoDictWithLoopParameters(teamId, seasonId, levelId, sportId, sportName, rulesPath, teamInfoDict):
	if(teamInfoDict['seasonId'] == 'n/a'):
		teamInfoDict['seasonId'] = seasonId

	if(teamInfoDict['sportName'] == 'n/a'):
		teamInfoDict['sportName'] = sportName
		
	if(teamInfoDict['levelId'] == 'n/a'):
		teamInfoDict['levelId'] = levelId

	if(teamInfoDict['sportId'] == 'n/a'):
		teamInfoDict['sportId'] = sportId
		
	if(teamInfoDict['sportRules'] == 'n/a'):
		teamInfoDict['sportRules'] = rulesPath										

	teamInfoDict['seasonId'] = seasonId																			
	teamInfoDict['teamId'] = teamId
	
	## populate any blank team info fields and
	## add in any useful ones that are available
	## from the loop
	
	return teamInfoDict
	## I know this is a mutation so the return isnt really needed, but I find it
	## easier to think about it this way

def reformatSeasonAndPlayoffsDictionaries(teamInfoDict, seasonDict, playoffsDict, gamesDict):
	
	
	newSeasonDict = {}
	
	##... now how to build a gameId...
	
	for game in seasonDict:
		try:
			teamsPlaying = sorted([seasonDict[game]['Opposing Team'], teamInfoDict['teamName']])
			## sorted so that the names of the two teams always appear in the same
			## order
			
			gameId = "[%s,%s,%s,%s]" % (repr(game), repr(seasonDict[game]['Location']), repr(teamsPlaying[0]), repr(teamsPlaying[1]))
			print "gameId: ", repr(gameId), "\n reformatted to list: ", repr(ast.literal_eval(gameId))
			
			if(gameId not in gamesDict):
				gamesDict[gameId] = {}
			
			teamId = teamInfoDict['teamId']
			
			gamesDict[gameId][teamId] = seasonDict[game]
			gamesDict[gameId][teamId]['dateTimeString'] = game
			
		except KeyError:
			print game, seasonDict[game]
			exit()
			##continue
			## just going to skip right past those broken games in the fall2008
			## advanced ball hockey league
		##"".replace('', '_')
	
	
	return seasonDict, playoffsDict









def getPlayerHashMapsDictionaryFromFile(hashMapFilepath):
	
	
	hashMapContent = []
	
	with open(hashMapFilepath, 'rb') as bar:
		reader = csv.reader(bar)
		hashMapContent = [row for row in reader]	

	hashMapArray = np.array(hashMapContent)
	print hashMapArray.shape

	##print hashMapContent
	headerRow = hashMapContent[0]
	##print headerRow
	hashMapContent = hashMapContent[1:]
	
	
	##print hashMapContent
	
	playerIdIndex = headerRow.index('playerId')
	playerEmailFoundIndex = headerRow.index('playerEmailFound')
	playerNameFirstIndex = headerRow.index('playerNameFirst')
	playerNameLastIndex = headerRow.index('playerNameLast')
	hashedPlayerIdIndex = headerRow.index('hashedId')		
		
	teamIdsIndex = headerRow.index('teamIds')	
		
	hashMapDict = {}
	
	
	for row in hashMapContent:
		playerId = row[playerIdIndex]	
		playerEmailFound = row[playerEmailFoundIndex]
		playerNameFirst = row[playerNameFirstIndex]		
		playerNameLast = row[playerNameLastIndex]
		hashedPlayerId = row[hashedPlayerIdIndex]		
		

		parameters = {'playerId': playerId, 'playerEmailFound': playerEmailFound, "playerNameFirst": playerNameFirst, "playerNameLast": playerNameLast, "hashedPlayerId": hashedPlayerId}				
		
		hashMapDict[playerId] = {}
		
		for param in parameters:
			
			hashMapDict[playerId][param] = parameters[param]
		hashMapDict[playerId]['teamIds'] = row[teamIdsIndex:]
	return hashMapDict





















if(__name__ == "__main__"):

	arguments = argv[1:]

	newFolderPrefix = arguments[0]
	## ie "FinalizeTest"
	outputStyle = arguments[1]
	## public


	newFolderPath = "./data%s" % newFolderPrefix

	print newFolderPath, " as ", outputStyle

	##exit()

	hashMapDict = getPlayerHashMapsDictionaryFromFile('./playerIdHashMaps.csv')
	##for player in hashMapDict:
	##	print player, '\n', hashMapDict[player], '\n\n'
	
	sports = {\
	 28:['soccer', 'outdoor', 'grass', '4-7vs_1GK', 'league'],\
	 4 :['hockey', 'indoor', 'floor', '3-4vs_1GK', 'league'],\
	 3 :['basketball', 'indoor', 'floor', '4-5vs_0GK', 'league'],\
	 5 :['dodgeball', 'indoor', 'floor', '6-8vs_0GK', 'league'],\
	 11:['flag_football', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 7 :['soccer', 'indoor', 'floor', '3-5vs_1GK', 'league'],\
	 1 :['hockey', 'indoor', 'ice', '6-6vs_1GK', 'league'],\
	 31:['ultimate', 'indoor', 'floor', '3-4vs_0GK', 'league'],\
	 10:['slowpitch', 'outdoor', 'grass', '8-10vs_0GK', 'league'],\
	 6 :['soccer', 'outdoor', 'grass', '7-11vs_1GK', 'league'],\
	 2 :['ultimate', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 8 :['volleyball', 'indoor', 'floor', '4-6vs_0GK', 'league'],\
	 17:['soccer', 'indoor', 'floor', '2-3vs_0GK', 'tournament'],\
	 26:['basketball', 'outdoor', 'ashphalt', '2-3vs_0GK', 'tournament'],\
	 18:['hunger_games_dodgeball', 'indoor', 'floor', '7-8vs_0GK', 'tournament'],\
	 16:['basketball', 'indoor', 'floor', '2-3vs_0GK', 'tournament']\
	 }
	sportIds = [28, 4, 3, 5, 11, 7, 1, 31, 10, 6, 2, 8, 17, 26, 18, 16]	
	##sportIds = [ 17, 26, 18, 16]
	##sportIds = [16]	
	
	years = range(2008, 2017)
	
	gamesDict = {}
	## every game played by Waterloo Intramurals from 2008 to 2016 or so
	
	def getTermById(termId):
		if(termId == 1):
			return "winter"
		elif(termId == 2):
			return "spring"
		if(termId == 4):
			return "fall"						
	
	terms = [1,2,4]
	## it goes winter, spring, fall
	## makes no sense to me either how they picked the term numbers
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11256"
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=7627"
	
	
	for sport in sportIds:
				
		sportId = sport
		sportName = sports[sportId][0]
		rulesSpec = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
		##print sports[sportId][4]
		if(sports[sportId][4] == "tournament"):
			##print "tournament"
			rulesPath = "%s-%s-%s_tournament" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])			
		else:
			rulesPath = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])		
		levelIdList = ['beginner', 'intermediate', 'advanced', 'allstar', 'allstarContact', 'any']
		if(sportId in [16,17,18,26]):
			levelIdList += ['beckham', 'figo', 'maradona', 'pele', 'ronaldinho', 'jordan', 'kobeBryant', 'lebronJames']
			## when I go completely nuts, please refer to this as the reason why
		for levelId in levelIdList:
			for year in years:
				for term in [getTermById(id_) for id_ in terms]:
					seasonId = "%s%i" % (term, year)
					file_path = "./data/%s/%s/watMu/%s/%s/teamId.csv" % (sports[sportId][0], rulesPath, levelId, seasonId)	
					try:
						with open(file_path, 'rb') as foo:
							reader = csv.reader(foo)
							print file_path, " Exists"

							teamData = []							
							for row in reader:
								teamData += [row]
								teamId = row[0]
								print "\n"*5, teamId, seasonId, levelId, sportId, sportName, "\n"*2							
								rosterEmailDict = {}
								rosterDict = {}
								
								rosterData_file_path = "./data/%s/%s/watMu/%s/%s/%i_RosterData.csv" % (sports[sportId][0], rulesPath, levelId, seasonId, int(teamId))	
								print "rosterData file path: ", rosterData_file_path, "\n"
								
								rosterEmailData = []
								with open(rosterData_file_path, 'rb') as bar:
									reader = csv.reader(bar)
									
									rosterEmailData = [row for row in reader]		
																
																	
																
									teamInfoDict, rosterEmailDict = convertRosterFileToDictionaries(rosterEmailData)
									##for player in rosterEmailDict:
									##	print player, '\n\n', rosterEmailDict[player]
										
								teamData_file_path = "./data/%s/%s/watMu/%s/%s/%i.csv" % (sports[sportId][0], rulesPath, levelId, seasonId, int(teamId))	
								print "\nteamData file path: ", teamData_file_path, "\n"		
								
								teamData = []
								with open(teamData_file_path, 'rb') as bar:
									reader = csv.reader(bar)
									
									teamData = [row for row in reader]		
																
																	
																
								teamInfoDict, seasonDict, playoffsDict, rosterDict = convertTeamFileToDictionaries(teamData)
								
								
								
								
								updateTeamInfoDictWithLoopParameters(teamId, seasonId, levelId, sportId, sportName, rulesPath, teamInfoDict)
								
								seasonDict, playoffsDict = reformatSeasonAndPlayoffsDictionaries(teamInfoDict, seasonDict, playoffsDict, gamesDict)
								
								for game in seasonDict:
									print game, seasonDict[game]
								print "\n\n"
								
								for game in playoffsDict:
									print game, playoffsDict[game]
								print "\n\n"
								
								
								
								print teamInfoDict
								for infoField in teamInfoDict:
									print infoField, ": ", repr(teamInfoDict[infoField])
									
																			
								##print "\n\n"
								##for player in rosterDict:
								##	print player, rosterDict[player]
								
								mergedRosterDict = mergeRosterDictionaries(teamId, seasonId, levelId, sportId, sportName, rosterEmailDict, rosterDict, hashMapDict, False)
								##for player in mergedRosterDict:
								##	print player, "\n", mergedRosterDict[player], "\n\n"	
							print "\n" 
					except IOError:
						pass
	gamesWithErrors = {}	
	gamesWithErrors['notEnoughTeams'] = {}
	gamesWithErrors['tooManyTeams'] = {}
	gamesWithErrors['locationsDontMatch'] = {}						
	gamesWithErrors['locationsNotListed'] = {}		
	
	gameLocationCounts = {}
						
	for game in gamesDict:
		print game, "\n", 
		
		teamIdList = [team for team in gamesDict[game]]
		listedLocations = [gamesDict[game][team]['Location'] for team in gamesDict[game]]
		
		if(len(teamIdList) < 2):
			gamesWithErrors['notEnoughTeams'][game] = teamIdList
		elif(len(teamIdList) > 2):
			gamesWithErrors['tooManyTeams'][game] = teamIdList
			## obviously unlikely, but worth checking just in case the gameIds
			## produced arent truly unique for some awful reason
		else:
			
			if(loc == listedLocations[0] for loc in listedLocations):
				gameLocation = listedLocations[0]
				if(gameLocation not in gameLocationCounts):
					gameLocationCounts[gameLocation] = 0
				gameLocationCounts[gameLocation] += 1
			else:
				gamesWithErrors['locationsDontMatch'][game] = listedLocations
		for team in gamesDict[game]:
			print team, "\n", gamesDict[game][team]					
		print "\n"
	
	for gameLoc in gameLocationCounts:
		print gameLoc, gameLocationCounts[gameLoc]
	print "\n\n"
	print gamesWithErrors
	print "\n\n\n"
	errorGameKeys = sorted([game for game in gamesWithErrors['notEnoughTeams']])
	totalGameKeys = sorted([game for game in gamesDict])	
	print len(totalGameKeys)
	for game in errorGameKeys:
		print game, gamesWithErrors['notEnoughTeams'][game]
		##for team in gamesWithErrors['notEnoughTeams'][game]
		
		## so the only legit error I see so far is 7630 'Kleats-R-Us', which has
		## a tbd game hanging off the schedule that never actually got resolved
		##
		## thats 7630 spring2012 intermediate 2 ultimate
		##
		## actually one error isnt bad for the amount of data worked over here
		##
		## my solution for this is going to be a simple manual fix of the files
		## applied like a patch as usual
