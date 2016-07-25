## gameProcessing.py ###########################################################
## functions that break down the raw data strings ##############################
## from the intramurals site into more useful forms ############################
################################################################################


def getTeamName(teamString):
	if('(Casual)' in teamString):
		return teamString[12:len(teamString)-9]
	elif('(Beginner)' in teamString):
		return teamString[12:len(teamString)-11]		
	elif('(Elite)' in teamString):
		return teamString[12:len(teamString)-8]	
	elif('(All Star)' in teamString):
		return teamString[12:len(teamString)-11]	
	elif('(All Star Non-Contact)' in teamString):
		return teamString[12:len(teamString)-23]
	elif('(All Star Contact)' in teamString):
		return teamString[12:len(teamString)-19]							
	## This is actually kind of important, cause any extra spaces at the end of
	## the team name will screw up compares in the schedule
	
	
def seasonLength(val):
	if(val >= 37):
		output = (val - 9.0)/4.0
		## if the team made it to the playoffs, we need to step back one
		## more on the index to avoid the 'PLAYOFFS heading'
	else:
		output = (val-8.0)/4.0
		## rare case where a team doesnt advance to playoffs, usually bad SOC
		## only seen this once so far
	return output
	
def getGameResult(rawDataString):
	if('tie' in rawDataString):
		return 'tie'
	elif('won' in rawDataString):	
		return 'won'
	elif('lost' in rawDataString):
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


		
def processGoalsFor(rawDataString):
	## take the raw score string that waterloo intramurals uses and then extract
	## how many goals *this team* scored, made harder because the system does
	## things like 'won 0-6' for some stupid reason
	gameResult = getGameResult(rawDataString)
	
	data = rawDataString
	if(gameResult == 'tie'):
		data = rawDataString[4:len(rawDataString)]
	else:
		if(gameResult == 'won'):
			data = rawDataString[4:len(rawDataString)]
		elif(gameResult == 'lost'):
			data = rawDataString[5:len(rawDataString)]
	## depending on what the result of this game was, we start by snipping off
	## the part of the string that listed the gameResult, ie
	## 'tie 2 - 2' --> '2 - 2'
	dashIndex = data.index('-')
	## find where the dash is in this string so we can start properly placing
	## the scores
	score1 = int(data[0:(dashIndex-1)])
	score2 = int(data[(dashIndex+1):len(data)])
	if(gameResult == 'tie'):
		return score1
		## easy here cause both scores are the same here
	else:
		if(gameResult == 'won'):
			return biggerOne(score1, score2)
		elif(gameResult == 'lost'):
			return smallerOne(score1, score2)
	## a bit more complex than the original, but much easier to read, and much
	## more reliable in getting the right values	
	

def processGoalsAgainst(rawDataString):
	## take the raw score string that waterloo intramurals uses and then extract
	## how many goals *this team* allowed, made harder because the system does
	## things like 'won 0-6' for some stupid reason
	gameResult = getGameResult(rawDataString)

	data = rawDataString
	if(gameResult == 'tie'):
		data = rawDataString[4:len(rawDataString)]
	else:
		if(gameResult == 'won'):
			data = rawDataString[4:len(rawDataString)]
		elif(gameResult == 'lost'):
			data = rawDataString[5:len(rawDataString)]
	## depending on what the result of this game was, we start by snipping off
	## the part of the string that listed the gameResult, ie
	## 'tie 2 - 2' --> '2 - 2'
	dashIndex = data.index('-')
	## find where the dash is in this string so we can start properly placing
	## the scores
	score1 = int(data[0:(dashIndex-1)])
	score2 = int(data[(dashIndex+1):len(data)])
	if(gameResult == 'tie'):
		return score1
		## easy here cause both scores are the same here
	else:
		if(gameResult == 'won'):
			return smallerOne(score1, score2)
		elif(gameResult == 'lost'):
			return biggerOne(score1, score2)
	

		
	
def processSOC(rawDataString):
	if(rawDataString == 'avg.'):
		return rawDataString
		## nothing we can do about this at this step of the process
		
		## this is gonna be a clusterfuck to handle this at the end
	else:
		return int(rawDataString)
		## force it out as an integer so it can be summed a bit more easily


if(__name__ == "__main__"):
	gf =  processGoalsFor('won 100 - 9', 'won')
	ga = processGoalsAgainst('won 100 - 9', 'won')
	print "gf %i, ga %i" % (gf, ga)
