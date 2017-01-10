## seasonWatMu.py ##############################################################
## base type for Waterloo Intramurals Hockey ###################################
## seasons (Individual semesters teams) ########################################
################################################################################
from teamWatMu import *
from season import *

def getSeedsInBracket(currentTeam, season, alreadyInBracket, count=0, debugInfo=False):
	## given an initial team that is in the playoff bracket we are
	## looking for, crawl the full extent of the playoff bracket and
	## output a list containing the standings positions (seeding nos)
	## of every team in the playoff bracket
	
	## its just a really annoying issue due to watMu having multiple
	## playoff brackets as we go down the standings, which makes not
	## all playoff games as meaningful
	
	## so we just ignore anything that isnt in the topmost playoff
	## bracket
	thisTeamSeed = season.Teams.index(currentTeam)+1
	## find the seed of the current team we are looking for
	if(thisTeamSeed not in alreadyInBracket):
		alreadyInBracket.append(thisTeamSeed)
		if(debugInfo):
			if(count > 0):				
				print "-"*count, thisTeamSeed
				## indent in to give us a sense of how deep the recursive calls have
				## gone
			else:
				print thisTeamSeed
		opponentSeeds = currentTeam.getPlayoffOpponentTeamSeeds(season)
		## make a list of the opponent team seed numbers
		for opponentSeed in opponentSeeds:
			opponent = season.getTeamByPosition(opponentSeed)
			if(opponentSeed not in alreadyInBracket):
				subSeeds = getSeedsInBracket(opponent, season, alreadyInBracket, count+1)
				for subSeed in subSeeds:
					if(subSeed not in alreadyInBracket):
						alreadyInBracket.append(subSeed)
	return alreadyInBracket


class playoffBracket:
	def __init__(self, bracket):
		self.bracketNumbers = []
		for pos in bracket:
			self.bracketNumbers.append(pos)
		
	def addStandingsPosition(self, position):
		self.bracketNumbers.append(position)




class watMuSeason(Season):
	def __init__(self, leagueId, levelId, seasonId, teamIdList, sortTeams, debugInfo=False):
		super(watMuSeason, self).__init__(leagueId, levelId, seasonId, teamIdList)
		## call the parents constructor
		self.playoffBrackets = []
		## list of lists
		## the lists contain the seeding numbers of teams in that
		## playoff bracket
		
		for teamId in teamIdList:
			## when the constructor was called, we got a list of the
			## team ids for each team in this season
			self.Teams.append(watMuTeam(leagueId, levelId, seasonId, teamId))
			## construct a team from each teamId, running the tierI
			## load call automatically

		for team in self.Teams:
			team.loadTierII(self.Teams)
			## calculate the stats for teams that depend on the stats of
			## other teams in the league
		
		if(sortTeams == True):
			## all of the criteria used to determine standings position can
			## be calculated from first tier data
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonGoalsForAverage(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonAverageSOC(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getPointsPercentage(), reverse=True)
			## so we sort the list of objects just like they would be in
			## the standings page
			
			## highest priority stat at the end
		
		
		for team in self.Teams:			
			team.setLeagueRank(self.Teams.index(team))
		
		
		self.topTeam = self.Teams[0]
		## next work through the teams this one played and add their position
		## numbers to the top playoff bracket, then look through their
		## opponents and so on
		
		## maybe a recursive function here that takes the teams list and the
		## bracket list as arguments and returns lists of seeding positions
		
		self.topPlayoffBracket = getSeedsInBracket(self.topTeam, self, [])
		## call the function that crawls the playoff tree and gets the
		## list of seeding numbers for the teams in the first playoff
		## bracket (the one that we care about)
		lastPlayoffBracket = self.topPlayoffBracket
		## ie the most recent playoff bracket that we handled
		
		if(debugInfo):
			print "top playoff bracket: ", self.topPlayoffBracket
			
		
		self.playoffBrackets.append(self.topPlayoffBracket)
		## add the first (top) playoff bracket to the list of playoff
		## brackets
		teamsSoFar = len(self.topPlayoffBracket)
		## the number of teams in the league that we have covered in the
		## first playoff bracket
		
		awqiMean = 	self.getTeamStatAverage(Team.getAWQI)
		apqiMean = self.getTeamStatAverage(Team.getAPQI)
		
		for team in self.Teams:
			
			if(team.getSeasonRank() in self.topPlayoffBracket):
				team.loadTierIII(self.Teams, True, awqiMean, apqiMean, team.getSeasonRank())
			else:
				team.loadTierIII(self.Teams, False, awqiMean, apqiMean, team.getSeasonRank())
			## load the stats that depend on the tier II stats of other
			## teams (usually adjusting stats for the season mean)
		
	def loadTierIV(self, seasonsList):
		for team in self.Teams:
			team.loadTierIV(self.Teams, seasonsList)
	
	def printPlayoffBrackets(self):
		for i in range(0, len(self.playoffBrackets)):
			if(i == 0):
				print "Top Playoff Bracket ", self.playoffBrackets[i]
			elif(i==1):
				print "Second Playoff Bracket ", self.playoffBrackets[i]
			elif(i==2):
				print "Third Playoff Bracket ", self.playoffBrackets[i]
			else:
				print "%th Playoff Bracket " % i, self.playoffBrackets[i]
			print len(self.playoffBrackets[i])
			
	def getTotalPlayoffTeams(self):
		output = 0
		for team in self.Teams:
			if(team.qualifiedForPlayoffs() == True):
				output += 1
		return output

