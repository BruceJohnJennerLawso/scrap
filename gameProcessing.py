## gameProcessing.py ###########################################################
## functions that break down the raw data strings ##############################
## from the intramurals site into more useful forms ############################
################################################################################


def getTeamName(teamString):
	if('(Casual)' in teamString):
		return teamString[12:len(teamString)-(len('Casual') + 1)]		
	elif('(Beginner)' in teamString):
		return teamString[12:len(teamString)-(len('(Beginner)') + 1)]
	elif('(Semi-Competitive)' in teamString):
		return teamString[12:len(teamString)-(len('(Semi-Competitive)') + 1)]
	elif('(Intermediate)' in teamString):
		return teamString[12:len(teamString)-(len('(Intermediate)') + 1)]	
	elif('(Competitive)' in teamString):
		return teamString[12:len(teamString)-(len('(Competitive)') + 1)]		
	elif('(Advanced)' in teamString):
		return teamString[12:len(teamString)-(len('(Advanced)') + 1)]		
	elif('(Elite)' in teamString):
		return teamString[12:len(teamString)-(len('(Elite)') + 1)]
	elif('(All Star)' in teamString):
		return teamString[12:len(teamString)-(len('(All Star)') + 1)]
	elif('(All Star Non-Contact)' in teamString):
		return teamString[12:len(teamString)-(len('(All Star Non-Contact)') + 1)]
	elif('(All Star Contact)' in teamString):
		return teamString[12:len(teamString)-(len('(All Star Contact)') + 1)]		
	## This is actually kind of important, cause any extra spaces at the end of
	## the team name will screw up compares in the schedule
	
	## ie 'The Mighty Dads' and 'The Mighty Dads '
	## will not compare as the same thing
	
	
def seasonLength(val):
	## wtf does this actually do...?
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
	## pretty simple stuff
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

## ^ helpful functions for handling scores

		
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
	gf =  processGoalsFor('won 100 - 9', 'won')
	ga = processGoalsAgainst('won 100 - 9', 'won')
	print "gf %i, ga %i" % (gf, ga)
	## quickly testing the goals processing function, which now can handle
	## scores above 10 with ease!!! Such resiliency!!! <3<3<3
