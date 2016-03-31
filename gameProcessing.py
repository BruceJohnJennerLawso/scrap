## gameProcessing.py ###########################################################
## functions that break down the raw data strings ##############################
## from the intramurals site into more useful forms ############################
################################################################################


def getTeamName(teamString):
	if('(Casual)' in teamString):
		return teamString[12:len(teamString)-9]
	elif('(Beginner)' in teamString):
		return teamString[12:len(teamString)-11]		
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
	
def gameResult(rawDataString):
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


		
def processGoalsFor(rawDataString, gameResult):
	## take the raw score string that waterloo intramurals uses and then extract
	## how many goals *this team* scored, made harder because the system does
	## things like 'won 0-6' for some stupid reason
	
	if(gameResult == 'tie'):
		return int(rawDataString[4:len(rawDataString)-4])
		## easy here cause both scores are the same here
	else:
		if(gameResult == 'won'):
			score1 = int(rawDataString[4:len(rawDataString)-4])
			score2 = int(rawDataString[8:len(rawDataString)])
			return biggerOne(score1, score2)
		elif(gameResult == 'lost'):
			score1 = int(rawDataString[5:len(rawDataString)-4])
			score2 = int(rawDataString[9:len(rawDataString)])
			return smallerOne(score1, score2)
		
	

def processGoalsAgainst(rawDataString, gameResult):
	## take the raw score string that waterloo intramurals uses and then extract
	## how many goals *this team* allowed, made harder because the system does
	## things like 'won 0-6' for some stupid reason
	
	if(gameResult == 'tie'):
		return int(rawDataString[4:len(rawDataString)-4])
		## easy here cause both scores are the same here
	else:
		if(gameResult == 'won'):
			score1 = int(rawDataString[4:len(rawDataString)-4])
			score2 = int(rawDataString[8:len(rawDataString)])
			return smallerOne(score1, score2)
		elif(gameResult == 'lost'):
			score1 = int(rawDataString[5:len(rawDataString)-4])
			score2 = int(rawDataString[9:len(rawDataString)])
			return biggerOne(score1, score2)
	
