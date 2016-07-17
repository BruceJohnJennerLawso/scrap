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
		## this just barely handles double digit scores properly, but I could
		## swear theres a weird 10-7 or 11-10 game somewhere in the system thats
		## going to crash this
		
		## it handles the case of a first double digit score fine, which is the
		## only case I was able to find in the system (9749), but if the second
		## score or both are double digit we're fucked
	
	
def processSOC(rawDataString):
	if(rawDataString == 'avg.'):
		return rawDataString
		## nothing we can do about this at this step of the process
		
		## this is gonna be a clusterfuck to handle this at the end
	else:
		return int(rawDataString)
		## force it out as an integer so it can be summed a bit more easily
