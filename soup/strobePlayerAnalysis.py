## strobePlayerAnalysis.py #####################################################
## open up all of those manifest files we generated with the strobe scraper ####
## and start looking for inconsistencies, anything odd #########################
################################################################################
import csv

from obfuscant import getObfuscatedString	
from obfuscant import getMasks	
		
from random_words import RandomWords		
		
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

	playerInfoDict = {}

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
								##print teamId, seasonId, levelId, sportId, sportName
								rosterData_file_path = "./data/%s/%s/watMu/%s/%s/%i_RosterData.csv" % (sports[sportId][0], rulesPath, levelId, seasonId, int(teamId))	
								print rosterData_file_path
								
								rosterSection = False
								passedRosterHeaderRow = False
								
								with open(rosterData_file_path, 'rb') as bar:
									reader = csv.reader(bar)
									for row in reader:
										print row, rosterSection, passedRosterHeaderRow
										if(rosterSection and (not passedRosterHeaderRow) ):
											passedRosterHeaderRow = True
										if(len(row) > 0):
											if(row[0] == 'ROSTER_DATA:'):
												rosterSection = True
											elif(row[0] == 'END_ROSTERDATA'):
												rosterSection = False	
										if(rosterSection and passedRosterHeaderRow):
											fullName = row[0] + " " + row[1]
											if(row[2] == 'True'):
												email = row[3]
												print repr(fullName), repr(email), " -> ", repr(getObfuscatedString(email, getMasks(), RandomWords()))
											else:
												print repr(fullName), teamId, " -> ", repr("%s_%s" % (getObfuscatedString(fullName, getMasks(), RandomWords()), teamId))												
								##scrapeStrobeTeam(int(teamId), levelId, sportId, seasonId)
							print "\n" 
					except IOError:
						pass
						##print 'not_found: ', file_path
						##print file_path, " Does not exist"
					
