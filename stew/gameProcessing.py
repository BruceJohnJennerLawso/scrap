## gameProcessing.py ###########################################################
## functions that break down the raw data strings ##############################
## from the intramurals site into more useful forms ############################
################################################################################
import string

def getTeamName(teamString):
	levelStrings = ['(Casual)', '(Beginner)','(Semi-Competitive)',\
	'(Intermediate)', '(Competitive)', '(Advanced)', '(Elite)', '(All Star)',\
	'(All Star Non-Contact)', '(All Star Contact)', ' (Maradona)', '(Beckham)',\
	'(Figo)', '(District 1)', '(The Capitol)', ' (Pele)', ' (Ronaldinho)'\
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
			if((levString in teamString)and(sportString in teamString)):
				
				
				print len(sportString)
				return teamString[len(sportString): (len(teamString)-(len(levString)))]	
	print '\n\n'	
	
	

	
def getGameResult(rawDataString):
	## pretty simple stuff
	if('T' in rawDataString):
		return 'tie'
	elif('W' in rawDataString):	
		return 'won'
	elif('L' in rawDataString):
		return 'lost'
	else:
		return 'unplayed'
		
def biggerOne(val1, val2):
	if(val1 > val2):
		return val1
	else:
		return val2		

def smallerOne(val1, val2):
	if(val1 < val2):
		return val1
	else:
		return val2

## ^ helpful functions for handling scores

		
def stripStringOfPieces(inputString, pieces):
	output = string.replace(inputString, "%s" % pieces[0], "")
	if(len(pieces) > 1):
		return stripStringOfPieces(output, pieces[1:])
	else:
		return output


def convertTeamUrlToTeamId(url):
	return stripStringOfPieces(url, ["https://www.imleagues.com", "/spa/team/", "/home"])

def convertPlayerUrlToPlayerId(url):
	return stripStringOfPieces(url, ["https://www.imleagues.com", "/spa/member/", "/player"])	

def stripAnyCommasFromTeamName(name):
	return stripStringOfPieces(name, [","])	
	
def processGoalsForAgainst(rawDataString):
	## take the raw score string that waterloo intramurals uses and then extract
	## how many goals *this team* scored, made harder because the system does
	## things like 'won 0-6' for some stupid reason
	gameResult = getGameResult(rawDataString)
	

	data = rawDataString[2:len(rawDataString)]

	## depending on what the result of this game was, we start by snipping off
	## the part of the string that listed the gameResult, ie
	## 'T 2 - 2' --> '2 - 2'
	dashIndex = data.index('-')
	## find where the dash is in this string so we can start properly placing
	## the scores
	score1 = int(data[0:(dashIndex-1)])
	score2 = int(data[(dashIndex+1):len(data)])
	if(gameResult == 'tie'):
		return (score1, score1)
		## easy here cause both scores are the same here
	else:
		if(gameResult == 'won'):
			goalsFor = biggerOne(score1, score2)
			goalsAgainst = smallerOne(score1, score2)
					
		elif(gameResult == 'lost'):
			goalsAgainst = biggerOne(score1, score2)
			goalsFor = smallerOne(score1, score2)	
		return (goalsFor, goalsAgainst)	
	

		
	
def processSOC(rawDataString):
	## take whatever was in the SOC column and make sense of it as a value we
	## can use later to calculate overall SOC average
	if(rawDataString == 'avg.'):
		return rawDataString
		## nothing we can do about this at this step of the process
		
		## so we can handle this later when the team object is loading data, and
		## it will make sure this counts as weighting the average a bit more
	else:
		return int(rawDataString)
		## force it out as an integer so it can be summed easily


if(__name__ == "__main__"):
	gf, ga =  processGoalsForAgainst('W 100 - 9')
	print "gf %i, ga %i" % (gf, ga)
	## quickly testing the goals processing function, which now can handle
	## scores above 10 with ease!!! Such resiliency!!! <3<3<3

	print getTeamName('Ice Hockey: The Mighty Dads (Casual)')
	print getTeamName('Ice Hockey: David R. Ceriton School of Super Friends (Beginner)')	
