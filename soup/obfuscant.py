## obfuscant.py ################################################################
## demoing a consistent way of mapping strings to other unique strings that ####
## consist of words ############################################################
################################################################################
from collections import defaultdict
import collections
from string import ascii_lowercase
import random
from random import choice

from random_words import RandomWords
from random_words import RandomNicknames


import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import watMuSportInfo
import csv

random_strings = set()


def random_string():
    while True:
        result = ''.join(choice(ascii_lowercase) for _ in range(6))
        if(result not in random_strings):
            random_strings.add(result)
            return result
			

previouslyGeneratedMaps = {}

def getObfuscatedString(inputString, masks, rw, debugInfo=False):
	if(inputString in previouslyGeneratedMaps):
		return previouslyGeneratedMaps[inputString]
	else:
		currentMaskString = ""
		i = 0
		for character in masks[inputString]:
			if(i == 0):
					
				if(character in "qwertyuiopasdfghjklzcvbnm"):
					wordCharacterMap = rw.random_word(character)
				else:
					wordCharacterMap = character		
				if(debugInfo):
					print character, wordCharacterMap
			else:
				if(character in "qwertyuiopasdfghjklzcvbnm"):
					wordCharacterMap = rw.random_word(character).capitalize()
				else:
					wordCharacterMap = character.capitalize()
				if(debugInfo):
					print character, wordCharacterMap
			i += 1
			currentMaskString += wordCharacterMap
		previouslyGeneratedMaps[inputString] = currentMaskString
		return currentMaskString

def basicTest(masks, rw):	
	names = ["Jim Brooks", "John Lawson", "Jean-Christophe Robertson"]
	
	rawMasks = {}
	
	for name in names:
		rawMasks[name] = masks[name]
	
	rw = RandomWords()
	
	outputMasks = {}
	
	for name in names:
		print(rawMasks[name])	
		
		outputMasks[masks[name]] = getObfuscatedString(name, masks, rw)
		
	for name in names:
		print repr(name), " -> ", repr(rawMasks[name]), " -> ", repr(outputMasks[rawMasks[name]])
	outputs = [outputMasks[rawMasks[name]] for name in names]	
	print len(set(names)), len(set(outputs))
	
	

	# the histogram of the data
	##n, bins, patches = plt.hist([len(name) for name in names], 50, normed=1, facecolor='green', alpha=0.75)

	##plt.xlabel('Name Length (Characters)')
	##plt.ylabel('Probability')
	##plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
	##plt.axis([40, 160, 0, 0.03])
	##plt.grid(True)
	
	##plt.show()
	




def randomizedTest(masks, rw):
	fullNames = []
	
	rn = RandomNicknames()
	
	for i in range(400000):
		##print i,
		fNameGender=choice(['f', 'm', 'u'])
		##print fNameGender
		firstNm = rn.random_nick(gender=fNameGender)
		lNameGender=choice(['m', 'u'])
		lastNm = rn.random_nick(gender=lNameGender)
		while([firstNm, lastNm] in fullNames):
			fNameGender=choice(['f', 'm', 'u'])
			firstNm = rn.random_nick(gender=fNameGender)
			lNameGender=choice(['m', 'u'])
			lastNm = rn.random_nick(gender=lNameGender)		
		fullNames.append([firstNm, lastNm])
	rawMasks = {}
	
	names = ["%s %s" % (nm[0], nm[1]) for nm in fullNames]
	
	for name in names:
		rawMasks[name] = masks[name]
	
	rw = RandomWords()
	
	outputMasks = {}
	
	for name in names:
		##print(rawMasks[name])	
		
		outputMasks[masks[name]] = getObfuscatedString(name, masks, rw)
		
	for name in names:
		print repr(name), " -> ", repr(rawMasks[name]), " -> ", repr(outputMasks[rawMasks[name]])

	raws = [rawMasks[name] for name in names]			
	outputs = [outputMasks[rawMasks[name]] for name in names]	
	print len(set(names)), len(set(outputs))
	print [item for item, count in collections.Counter(outputs).items() if count > 1], len([item for item, count in collections.Counter(outputs).items() if count > 1])
	print [item for item, count in collections.Counter(raws).items() if count > 1], len([item for item, count in collections.Counter(raws).items() if count > 1])

	outputDuplicates = [item for item, count in collections.Counter(outputs).items() if count > 1]

	for name in names:
		if(outputMasks[rawMasks[name]] in outputDuplicates):
			print repr(name), " -> ", repr(rawMasks[name]), " -> ", repr(outputMasks[rawMasks[name]])

	# the histogram of the data
	n, bins, patches = plt.hist([len(name) for name in names], 50, normed=1, facecolor='green', alpha=0.75)

	plt.xlabel('Name Length (Characters)')
	plt.ylabel('Probability')
	plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
	plt.axis([0, 30, 0, 0.75])
	plt.grid(True)
	
	plt.show()

def getMasks():
	return defaultdict(random_string)





def convertTeamFileToDictionaries(teamFileContent):
	
	
	infoStartIndex = teamFileContent.index(['INFO:'])
	infoEndIndex = teamFileContent.index(['END_INFO'])
	
	infoDictionary = {}
	
	infoContent = teamFileContent[infoStartIndex+1:infoEndIndex]
	
	for row in infoContent:
		if(len(row) > 2):
			infoDictionary[row[0]] = row[1:]
		else:
			infoDictionary[row[0]] = row[1]


	rosterStartIndex = teamFileContent.index(['ROSTER_DATA:'])
	rosterEndIndex = teamFileContent.index(['END_ROSTERDATA'])			


	
	rosterContent = teamFileContent[rosterStartIndex+1:rosterEndIndex]
	
	rosterHeader = rosterContent[0]
	
	rosterContent = rosterContent[1:]
	
	rosterEmailFound = rosterHeader.index('emailFound')
	rosterEmailListed = rosterHeader.index('emailListed')
	
	rosterDictionary = {}
	
	for row in rosterContent:
		if(row[rosterEmailFound] == 'True'):
			thisPlayerKey = row[rosterEmailListed]
			## the raw email of the player
	
		else:
			## a unique email was not listed for the player in question, so 
			## i will need to fabricate a new one from a mishmash of data
			## specific to the player
			rosterFirstName = rosterHeader.index('playerNameFirst')
			rosterLastName = rosterHeader.index('playerNameLast')
			
			firstName = row[rosterFirstName]
			lastName = row[rosterLastName]
			teamId = infoDictionary['teamId']
			
			tempPlayerId = 	lastName+firstName+teamId
			
			
			thisPlayerKey = tempPlayerId

		rosterDictionary[thisPlayerKey] = {}
		for heading in rosterHeader:
			headingIndex = rosterHeader.index(heading)
			rosterDictionary[thisPlayerKey][heading] = row[headingIndex]
		rosterDictionary[thisPlayerKey]['playerId'] = thisPlayerKey
			
	return infoDictionary, rosterDictionary

if(__name__ == "__main__"):
	
	random.seed(3141592654)
	masks = getMasks()
	
	rw = RandomWords()
	basicTest(masks, rw)
	##randomizedTest(masks, rw)
	
	sports = watMuSportInfo.sportsInfoDict()

	sportIds = [28, 4, 3, 5, 11, 7, 1, 31, 10, 6, 2, 8, 17, 26, 18, 16]	
	years = range(2008, 2017)

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
	


	completePlayersList = []
	completePlayersDict = {}
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
							for row in reader:
								teamId = row[0]
								print teamId, seasonId, levelId, sportId, sportName
								
								rosterData_file_path = "./data/%s/%s/watMu/%s/%s/%i_RosterData.csv" % (sports[sportId][0], rulesPath, levelId, seasonId, int(teamId))	
								print rosterData_file_path
								
								
								with open(rosterData_file_path, 'rb') as bar:
									reader = csv.reader(bar)
									
									teamData = []
									for row in reader:
										##print row
										teamData += [row]
									##print teamData
									
									teamInfoDict, rosterDict = convertTeamFileToDictionaries(teamData)
									##print teamInfoDict
									##print rosterDict
									for player in rosterDict:
										completePlayersList.append({player: rosterDict[player]})
										if(player not in completePlayersDict):
											completePlayersDict[player] = []	
										rosterDict[player]['teamInfoDict'] = teamInfoDict
										completePlayersDict[player].append(rosterDict[player])
										##completePlayersDict[player].append(teamInfoDict)
								##scrapePlayerInfoFromStrobeTeamPanel(browser, int(teamId), levelId, sportId, seasonId)
							print "\n" 
					except IOError:
						pass

	
	
	
	names = [player for player in completePlayersDict]
	
	rawMasks = {}
	
	for name in names:
		rawMasks[name] = masks[name]
	
	rw = RandomWords()
	
	outputMasks = {}
	
	for name in names:
		##print(rawMasks[name])	
		
		outputMasks[masks[name]] = getObfuscatedString(name, masks, rw)
		
	for name in names:
		print repr(name), " -> ", repr(rawMasks[name]), " -> ", repr(outputMasks[rawMasks[name]])

	print "\n"*50		
	##for player in completePlayersDict:
	##	completePlayersDict[player][0]['hashedId'] = outputMasks[rawMasks[player]]
	
	completePlayersList = [[player, completePlayersDict[player]] for player in completePlayersDict]
	print "***\n\n", completePlayersList[0], "\n\n***"
	
	for playerList in completePlayersList[:5]:
		print len(playerList[1])
	
	completePlayersList = sorted(completePlayersList, key=lambda playerList: len(playerList[1]), reverse=False)

	sortedPlayersKeys = [row[0] for row in completePlayersList]

	completePlayersDict = {}
	for row in completePlayersList:
		completePlayersDict[row[0]] = row[1]
	
	
	
	##for player in sortedPlayersKeys:		
	##	print player, len(completePlayersDict[player]), "\n\n\n"
	##	for entry in completePlayersDict[player]:
	##		print entry
	##	print "\n"*2
	##print len(completePlayersList)		
	
	hashedPlayersDict = {}
	
	
	for player in sortedPlayersKeys:
		playerHash = outputMasks[rawMasks[player]]
		
		hashedPlayersDict[playerHash] = completePlayersDict[player]

	


	for hashedKey in [outputMasks[rawMasks[name]] for name in sortedPlayersKeys]:		
		print hashedKey, len(hashedPlayersDict[hashedKey]), "\n\n\n"
		for entry in hashedPlayersDict[hashedKey]:
			print entry
		print "\n"*2
	print len(hashedPlayersDict)	
	
	
	outputs = [outputMasks[rawMasks[name]] for name in names]	
	print len(set(names)), len(set(outputs))
	
	file_path = "./playerIdHashMaps.csv"
	
	f = open(file_path, "wb")
	writer = csv.writer(f)
	for hashedKey in [outputMasks[rawMasks[name]] for name in sortedPlayersKeys]:
		playerHash = hashedKey
		playerEmail = hashedPlayersDict[hashedKey][0]['playerId']
		playerNameFirst = hashedPlayersDict[hashedKey][0]['playerNameFirst']			
		playerNameLast = hashedPlayersDict[hashedKey][0]['playerNameLast']			
		
		rowToWrite = [playerHash, playerEmail, playerNameFirst, playerNameLast] + [entry['teamInfoDict']['teamId'] for entry in hashedPlayersDict[hashedKey]]
		
		writer.writerow(rowToWrite)
	f.close()	
	
	
	##print [rw.random_word('b') for i in range(100)]
