## unlimitedData.py ############################################################
## 
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests
import os
import csv

def getTeamName(teamString):
	levelStrings = [' (Casual)', ' (Beginner)',' (Semi-Competitive)',\
	' (Intermediate)', ' (Competitive)', ' (Advanced)', ' (Elite)', ' (All Star)',\
	' (All Star Non-Contact)', ' (All Star Contact)', ' (Maradona)', ' (Beckham)',\
	' (Figo)', ' (District 1)', ' (The Capitol)', ' (Pele)', ' (Ronaldinho)',\
	' (All Skill Levels)', ' (Jordan)', ' (Kobe Bryant)', ' (LeBron James)']
	
	sportStrings = ['Tournament: 3-on-3 Indoor Soccer: ',\
	 'Tournament: March Madness: 3-on-3 Basketball: ',\
	 'Tournament: Hunger Games Residence Dodgeball: ', '7 vs 7 Soccer: ',\
	 'Ball Hockey: ', 'Basketball: ', 'Dodgeball: ', 'Flag Football: ',\
	 'Futsal: ', 'Ice Hockey: ', 'Indoor Ultimate: ', 'Slo Pitch: ',\
	 'Soccer: ', 'Ultimate: ', 'Volleyball: ']

	
	for levString in levelStrings:
		for sportString in sportStrings:
			##print teamString
			##print levString, levString in teamString
			##print sportString, sportString in teamString, '\n'
			##print levString, (levString in teamString), sportString, (sportString in teamString)
			if((levString in teamString)and(sportString in teamString)):
				

				##print len(sportString)
				return teamString[len(sportString): (len(teamString)-(len(levString)))]	
	print '\n\n'		


def getTableInRows(soup, tableTarget, tableDataOnlyUnder="", debugInfo=False):

	##{"id": tableId}
	table = soup.find(lambda tag: tag.name=='table', tableTarget) 
	rows = table.findAll(lambda tag: tag.name=='tr')
	
	
	##for row in rows:
	##	print row
	##print "\n\nFlattening to csv\n"

	headerRows = []
	outputRows = []


	foundTargetHeadingUnder = False
	for row in rows:
		##print row, row.find_all('tr')
		headerRows.append([val.text.encode('utf8') for val in row.find_all('th')])	
		##outputRows.append([val.text.encode('utf8') for val in row.find_all('th')+row.find_all('td')])
		if(tableDataOnlyUnder == ""):
			outputRows.append([val.text.encode('utf8') for val in row.find_all(['td', 'th'])])		
		else:
			if(row.find(lambda tag: tag.name=='th' and tag.has_attr('colspan'))):
				if(row.getText() == tableDataOnlyUnder):
					foundTargetHeadingUnder = True
					continue
					## keep going and ignore this particular break in the table	
				else:
					if(foundTargetHeadingUnder):
						break	
					else:
						continue
			else:
				if(foundTargetHeadingUnder):
					outputRows.append([val.text.encode('utf8') for val in row.find_all(['td', 'th'])])				
		## important note here, some evil
		## tables such as hockey reference like to make data in the first column
		## (ie game number) a <th> element, like its another header but vertical
		## because they hate me
	##for row in outputRows:
	##	print row

				
	tableWidth = max([len(row) for row in headerRows])
	## this is to single out that blasted "meta header" row thats often present
	## but not always in a teams hockey reference page
	##headerRows = [row for row in headerRows if (len(row)==tableWidth)]
	outputRows = [row for row in outputRows if row not in headerRows]
	headerRows = [row for row in headerRows if (len(row)==tableWidth)]
	headerRows = map(list, set(map(tuple,headerRows)))
	## remove duplicate header rows (in list form) from the list of lists
	
	##print "## Header Rows ##"
	##for row in headerRows:
	##	print row, len(row)
	##i = 0

	##print "## Output Rows ##"	
	##for row in outputRows:
	##	print i, outputRows.index(row), row, len(row), (len(row) == tableWidth)	, "\n"
	##	if(len(row) != tableWidth):
	##		print "Bad row does not match widths of the others"
	##	i+=1	
	return (headerRows, outputRows)

def getTableOfStrobePlayers(soup):
	content = soup.find(lambda tag: tag.name=='div', {"id": "primarycontent"}) 
	
		
	if(content.find(lambda tag: tag.name=='ul')):
		roster = content.find(lambda tag: tag.name=='ul') 
		players = roster.findAll(lambda tag: tag.name=='li')
		headerRow = [["Player", "Captaincy", "uwaterloo_email"]]
		outputRows = []
		for player in players:
			##print player, player.getText(),
			if(player.find(lambda tag: tag.name=='a')):
				outputRows.append([player.getText().encode('utf8')[9:], "(C)", player.find(lambda tag: tag.name=='a').get('href')[7:]])
				##print "Captain", player.find(lambda tag: tag.name=='a').get('href')[7:]
			else:
				outputRows.append([player.getText().encode('utf8'), "", ""])
				##print ""
		return (headerRow, outputRows)	
	else:
		return ([['Roster Unavailable']], [[]])
	## pretty sure this should be the only ul in the page, but this makes me
	## nervous
	
	



	
def scrapeStrobeTeam(teamId, levelId, sportId, seasonId):	
	##teamId = 12348
	url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=%i&sport=%i" % (teamId, sportId)
	
			
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "lxml")	
			
	content = soup.find(lambda tag: tag.name=='div', {"id": "primarycontent"}) 
	teamNameString = content.find(lambda tag: tag.name=='h1').getText().encode('utf8')
				
	teamRosterHeading, teamRoster = getTableOfStrobePlayers(soup)
	seasonGamesHeading, seasonGamesTable = getTableInRows(soup, {"class": "refpays"}, "REGULAR SEASON")
	playoffGamesHeading, playoffGamesTable = getTableInRows(soup, {"class": "refpays"}, "PLAYOFFS")
				
	gameHeadings = content.findAll(lambda tag: tag.name=='th' and tag.has_attr('colspan') and tag.has_attr('class'))
	for head in gameHeadings:
		print head.getText(), head.getText() in ["REGULAR SEASON", "S.O.C. GAMES", "PLAYOFFS"]

	if("S.O.C. GAMES" in [gm.getText() for gm in gameHeadings]):
		print "SOC games found"
		socGamesHeading, socGames = getTableInRows(soup, {"class": "refpays"}, "S.O.C. GAMES")
		if(len(socGames) > 0):
			seasonGamesTable += socGames
	teamName = getTeamName(teamNameString)
	print "## Team ##\n%s\n%s %i" % (teamNameString, teamName, len(teamName))
				
				
	print "\n## Roster ##"
	for roshead in teamRosterHeading:
		print roshead, len(roshead)
	for ros in teamRoster:
		print ros, len(ros)
				
	print "\n## Season ##"
	for head in seasonGamesHeading:
		print head, len(head)
	for gm in seasonGamesTable:
		print gm, len(gm)

	print "\n## Playoffs ##"
	for head in playoffGamesHeading:
		print head, len(head)
	for gm in playoffGamesTable:
		print gm, len(gm)	



	print "Saving to csv..."

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
	
	
	 
	rulesSpec = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])
	if(sports[sportId][4] == "tournament"):
		##print "tournament"
		rulesPath = "%s-%s-%s_tournament" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])			
	else:
		rulesPath = "%s-%s-%s" % (sports[sportId][1], sports[sportId][2], sports[sportId][3])	
	file_path = "./data/%s/%s/watMu/%s/%s/%i.csv" % (sports[sportId][0], rulesPath, levelId, seasonId, teamId)


	##file_path = "./outputFiles/%i.csv" % teamId

	directory = os.path.dirname(file_path)
	try:
		os.stat(directory)
	except:
		os.makedirs(directory)	
	f = open(file_path, "wb")
	writer = csv.writer(f)
	writer.writerow(['INFO:'])
	writer.writerow(['teamName', teamName])	
	writer.writerow(['teamAbbreviation', teamName])	
	writer.writerow(['sportId', 'n/a'])		
	writer.writerow(['sportName', 'n/a'])
	writer.writerow(['sportRules', 'n/a'])		
	writer.writerow(['leagueId', 'watMu'])	
	writer.writerow(['levelId', 'n/a'])			
	writer.writerow(['seasonName', 'n/a'])
	writer.writerow(['seasonId', 'n/a'])	
	writer.writerow(['Roster Size',len(teamRoster)])	
	writer.writerow(['Season Games Played',len(seasonGamesTable)])	
	playoffRoundLengths = [1 for playoffRound in playoffGamesTable]
	if(1 not in playoffRoundLengths):
		playoffRoundLengths.append(0)
	writer.writerow(['Playoff Round Lengths']+playoffRoundLengths)
	writer.writerow(['END_INFO'])
	writer.writerows([''])
	writer.writerow(['SEASON:'])
	for row in seasonGamesHeading:
		writer.writerow(row)
	for row in seasonGamesTable:
		writer.writerow(row)
	writer.writerow(['END_SEASON'])
	writer.writerows([''])
	writer.writerow(['PLAYOFFS:'])
	for row in playoffGamesHeading:
		writer.writerow(row)
	for row in playoffGamesTable:
		writer.writerow(row)
	writer.writerow(['END_PLAYOFFS'])
	writer.writerows([''])
	writer.writerow(['ROSTER:'])
	if(teamRosterHeading[0][0] != 'Roster Unavailable'):
		for row in teamRosterHeading:
			writer.writerow(row)	
		for row in teamRoster:
			writer.writerow(row)	
	else:
		writer.writerow(['Roster Unavailable'])				
	writer.writerow(['END_ROSTER'])
	f.close()
							
	print "...Finished writing csv\n"		
	

	
		
if(__name__ == "__main__"):

	##teamId = 12348
	##teamId = 7627
	##teamId = 11256
	##teamId = 6867
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=%i" % (teamId)

	#teamId = 6169
	#levelId = 'intermediate'
	#sportId = 3
	#seasonId = 'spring2011'
	#scrapeStrobeTeam(teamId, levelId, sportId, seasonId)	
	#exit()

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
	##sportIds = [28, 4, 3, 5, 11, 7, 1, 31, 10, 6, 2, 8, 17, 26, 18, 16]	
	sportIds = [ 17, 26, 18, 16]
	##sportIds = [16]	
	
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
								scrapeStrobeTeam(int(teamId), levelId, sportId, seasonId)
							print "\n" 
					except IOError:
						pass
						##print 'not_found: ', file_path
						##print file_path, " Does not exist"
		##teamId = 12348
		##levelId = 'beginner'
		##sportId = 1
		##seasonId = fall2015
		##scrapeStrobeTeam(teamId, levelId, sportId, seasonId)					

	#termName = getTermById(term)
									
	#leagueSpecifics = "%s-%s-%s" % (sports[sportId][3], sports[sportId][1], sports[sportId][2])
									
	#if(sports[sportId][4] == "league"):
		#file_path = "./data/%s/watMu/%s/%s%i_%s/teamId.csv" % (sportName, levelId, termName, year, leagueSpecifics)
	#else:
		#file_path = "./data/%s/watMu/%s/%s%i_%s_tournament/teamId.csv" % (sportName, levelId, termName, year, leagueSpecifics)				
	#directory = os.path.dirname(file_path)
	#print directory
					

