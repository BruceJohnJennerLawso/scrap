## amTheStrobe.py ##############################################################
## just mucking around with beautiful soup to get ##############################
## a feel for it ###############################################################
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests
import numpy as np
import string
import collections
import os
import csv

def convertShortLinkHrefUrlToFull(linkHref):
	if(linkHref[0] == '/'):
		linkHref = "https://strobe.uwaterloo.ca" + linkHref
	return linkHref

def getLinkedPagesFromUrl(url, alreadyLookedAt=[], depth=0):
	##print " "*depth, string.replace(url, "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=", "")
	page = requests.get(url)
	
	soup = BeautifulSoup(page.content, "lxml")	
	scheduleTable = soup.find(lambda tag: tag.name=='table', class_="refpays") 
	
	totalList = []
	totalList.append(url)
	for link in scheduleTable.find_all('a'):
		linkHref = link.get('href')
		linkHref = convertShortLinkHrefUrlToFull(linkHref)
		
		if((linkHref not in totalList)and(linkHref not in [url])and(linkHref not in alreadyLookedAt)):
			totalList += getLinkedPagesFromUrl(linkHref, alreadyLookedAt+totalList, depth+1)
	return totalList

def getTableInRows(url, tableTarget, debugInfo=False):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "lxml")
	##{"id": tableId}
	table = soup.find(lambda tag: tag.name=='table', tableTarget) 
	rows = table.findAll(lambda tag: tag.name=='tr')
	
	
	for row in rows:
		print row
	print "\n\nFlattening to csv\n"

	headerRows = []
	outputRows = []

	for row in rows:
		##print row, row.find_all('tr')
		headerRows.append([val.text.encode('utf8') for val in row.find_all('th')])	
		##outputRows.append([val.text.encode('utf8') for val in row.find_all('th')+row.find_all('td')])
		outputRows.append([val.text.encode('utf8') for val in row.find_all(['td', 'th'])])		
		## important note here, some evil
		## tables such as hockey reference like to make data in the first column
		## (ie game number) a <th> element, like its another header but vertical
		## because they hate me
	for row in outputRows:
		print row

				
	tableWidth = max([len(row) for row in headerRows])
	## this is to single out that blasted "meta header" row thats often present
	## but not always in a teams hockey reference page
	##headerRows = [row for row in headerRows if (len(row)==tableWidth)]
	outputRows = [row for row in outputRows if row not in headerRows]
	headerRows = [row for row in headerRows if (len(row)==tableWidth)]
	headerRows = map(list, set(map(tuple,headerRows)))
	## remove duplicate header rows (in list form) from the list of lists
	
	print "## Header Rows ##"
	for row in headerRows:
		print row, len(row)
	i = 0

	print "## Output Rows ##"	
	for row in outputRows:
		print i, outputRows.index(row), row, len(row), (len(row) == tableWidth)	, "\n"
		if(len(row) != tableWidth):
			print "Bad row does not match widths of the others"
		i+=1	
	return (headerRows, outputRows)

if(__name__ == "__main__"):

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
	 18:['dodgeball', 'indoor', 'floor', '7-8vs_0GK_hunger_games', 'tournament'],\
	 16:['basketball', 'indoor', 'floor', '2-3vs_0GK', 'tournament']\
	 }
	sportIds = [28, 4, 3, 5, 11, 7, 1, 31, 10, 6, 2, 8, 17, 26, 18, 16]
	## logic not included
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
	
	def convertLevelsToStandard(levelName):
		newLevelNameMap = {"Casual":"beginner", "Semi-Competitive":"intermediate", "Competitive":"advanced", "Elite":"allstar"}
		if(levelName in newLevelNameMap):
			return newLevelNameMap[levelName]
		oldNamesCaseMap = {"Beginner":"beginner", "Intermediate":"intermediate", "Advanced":"advanced", "All Star":"allstar", "All Star Non-Contact":"allstar", "All Star Contact":"allstarContact"}	
		if(levelName in oldNamesCaseMap):
			return oldNamesCaseMap[levelName]
		
		randomAssDivisionNames = {'Maradona':"maradona", 'Beckham':"beckham",'Figo':"figo",\
		'District 1':'any', 'The Capitol':'any', 'Pele':'pele', 'Ronaldinho':'ronaldinho',\
		'All Skill Levels':'any', 'Jordan':'jordan', 'Kobe Bryant':'kobeBryant', 'LeBron James':'lebronJames'}
		if(levelName in randomAssDivisionNames):
			return randomAssDivisionNames[levelName]
		
		return levelName
		
		
	for year in years:

		for term in terms:
			print "\n\n"
			print year, getTermById(term)
			for sport in sportIds:
				
				url = "https://strobe.uwaterloo.ca/athletics/intramurals/leagues.php?sport=%i&champions&year=%i&term=%i" % (sport, year, term)
				page = requests.get(url)
	
				soup = BeautifulSoup(page.content, "lxml") 	
				content = soup.find(lambda tag: tag.name=='div' and tag.has_key('id') and tag['id']=="primarycontent") 
				
				print content.find(lambda tag: tag.name=='h1').getText()
				
				if(content.find('strong')):
					print content.find(lambda tag: tag.name=='strong').getText(), "\n"
				else:	
					levels = content.findAll(lambda tag: tag.name=='h2')
	
					def convertShortLinkToTeamId(shortLink):
						if(shortLink[0:15] == 'teams.php?team='):
							shortLink = shortLink[15:]
						return shortLink
	
					for lev in levels:
		
						linksAfterLev = []
						nextLev = lev
						while(True):
							if(nextLev.next_sibling.name == "a"):
								linksAfterLev.append(nextLev.next_sibling)
								nextLev = nextLev.next_sibling
							else:
								break
								
						print lev.getText(), lev.name
						thisLevelTeamIds = []
						for teamId in [convertShortLinkToTeamId(l.get('href')) for l in linksAfterLev]:
							if(teamId not in thisLevelTeamIds):
								if(len(thisLevelTeamIds)):
									print "Top bracket not fully connected to teamId %s" % teamId
								linkedTeams = getLinkedPagesFromUrl("https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=%i" % int(teamId))
								for tm in [string.replace(url, "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=", "") for url in linkedTeams]:
									thisLevelTeamIds.append(tm)
								teamIdList = [string.replace(url, "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=", "") for url in linkedTeams]
							
							print teamId
						thisLevelTeamIds = [string.replace(url, "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=", "") for url in thisLevelTeamIds]
						print thisLevelTeamIds, len(thisLevelTeamIds), len([item for item, count in collections.Counter(thisLevelTeamIds).items() if count > 1]), "\n"
						
						print "Saving to manifest csv..."
						sportId = sport
						sportName = sports[sportId][0]
						levelId = convertLevelsToStandard(lev.getText())
						termName = getTermById(term)
						
						leagueSpecifics = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
						
						if(sports[sportId][4] == "league"):
							file_path = "./data/%s/%s/watMu/%s/%s%i/teamId.csv" % (sportName, leagueSpecifics, levelId, termName, year)
							
						else:
							file_path = "./data/%s/%s_%s/watMu/%s/%s%i/teamId.csv" % (sportName, leagueSpecifics, "tournament", levelId, termName, year)
						directory = os.path.dirname(file_path)
						try:
							os.stat(directory)
						except:
							os.makedirs(directory)	
						f = open(file_path, "wb")
						writer = csv.writer(f)
						for row in thisLevelTeamIds:
							writer.writerow(["%s" % row])
						f.close()
						
						print "...Finished writing manifest csv\n"				
					print "\n\n"




