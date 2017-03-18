## unlimitedData.py ############################################################
## 
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests

def getTeamName(teamString):
	levelStrings = ['(Casual)', '(Beginner)','(Semi-Competitive)',\
	'(Intermediate)', '(Competitive)', '(Advanced)', '(Elite)', '(All Star)',\
	'(All Star Non-Contact)', '(All Star Contact)', ' (Maradona)', '(Beckham)',\
	'(Figo)', '(District 1)', '(The Capitol)', ' (Pele)', ' (Ronaldinho)'\
	' (All Skill Levels)', ' (Jordan)']
	
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
			if((levString in teamString)and(sportString in teamString)):
				
				
				print len(sportString)
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
	roster = content.find(lambda tag: tag.name=='ul') 
	## pretty sure this should be the only ul in the page, but this makes me
	## nervous
	players = roster.findAll(lambda tag: tag.name=='li')
	
	headerRow = [["Player", "Captaincy", "uwaterloo_email"]]
	outputRows = []
	for player in players:
		##print player, player.getText(),
		if(player.find(lambda tag: tag.name=='a')):
			outputRows.append([player.getText().encode('utf8'), "(C)", player.find(lambda tag: tag.name=='a').get('href')[7:]])
			##print "Captain", player.find(lambda tag: tag.name=='a').get('href')[7:]
		else:
			outputRows.append([player.getText(), "", ""])
			##print ""
	return (headerRow, outputRows)
		
if(__name__ == "__main__"):

	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11256"
	
	url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11484"
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=8936"	
	##url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=8481"	
	##url = "http://www.hockey-reference.com/teams/TOR/2017_games.html"
	##url = "http://www.hockey-reference.com/teams/MTW/1918_games.html"

	url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=6887"
	url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=13245"
	##page = requests.get(url)
	##getTableInRows(url, {"class", "refpays"})
	##getTableInRows(url, {"id": "games"})
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "lxml")	
	
	content = soup.find(lambda tag: tag.name=='div', {"id": "primarycontent"}) 
	teamNameString = content.find(lambda tag: tag.name=='h1').getText()
	
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
	print "## Team ##\n%s\n%s %i" % (teamNameString, getTeamName(teamNameString), len(getTeamName(teamNameString)))
	
	
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
