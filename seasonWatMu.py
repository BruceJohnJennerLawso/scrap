## seasonWatMu.py ##############################################################
## base type for Waterloo Intramurals Hockey ###################################
## seasons (Individual semesters teams) ########################################
################################################################################
from teamWatMu import *
from season import *

def getSeedsInBracket(currentTeam, season, alreadyInBracket, count=0):
	## given an initial team that is in the playoff bracket we are
	## looking for, crawl the full extent of the playoff bracket and
	## output a list containing the standings positions (seeding nos)
	## of every team in the playoff bracket
	
	## its just a really annoying issue due to watMu having
	thisTeamSeed = currentTeam.getSeasonRank()
	## find the seed of the current team we are looking for
	if(thisTeamSeed not in alreadyInBracket):
		alreadyInBracket.append(thisTeamSeed)
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
	def __init__(self, leagueId, levelId, seasonId, teamIdList, sortTeams):
		super(watMuSeason, self).__init__(leagueId, levelId, seasonId, teamIdList)
		
		self.playoffBrackets = []
		
		for teamId in teamIdList:
			self.Teams.append(watMuTeam(leagueId, levelId, seasonId, teamId))
		
		for team in self.Teams:
			team.loadTierI()

		if(sortTeams == True):
			## all of the criteria used to determine standings position can
			## be calculated from first tier data
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonGoalsForAverage(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getSeasonAverageSOC(), reverse=True)
			self.Teams = sorted(self.Teams, key=lambda watMuTeam: watMuTeam.getPointsPercentage(), reverse=True)
			## highest priority at the end
			

		for team in self.Teams:
			team.loadTierII(self.Teams, self.Teams.index(team))
		
		self.topTeam = self.getTeamByPosition(1)
		## next work through the teams this one played and add their position
		## numbers to the top playoff bracket, then look through their
		## opponents and so on
		
		## maybe a recursive function here that takes the teams list and the
		## bracket list as arguments and returns lists of seeding positions
		
		self.topPlayoffBracket = getSeedsInBracket(self.topTeam, self, [])
		lastPlayoffBracket = self.topPlayoffBracket
		
		print "top playoff bracket: ", self.topPlayoffBracket
		
		self.playoffBrackets.append(self.topPlayoffBracket)
		
		teamsSoFar = len(self.topPlayoffBracket)
		while(True):
			totalTeams = self.getTotalPlayoffTeams()
			print "total teams for %s: %i" % (self.seasonId, totalTeams)
			print "teams so far: %i" % teamsSoFar
			if(totalTeams > teamsSoFar):
				lastSeed = max(lastPlayoffBracket)
				topOfNewBracket = self.getTeamByPosition(lastSeed+1)
				lastPlayoffBracket = getSeedsInBracket(topOfNewBracket, self, [])
				
				self.playoffBrackets.append(lastPlayoffBracket)
				teamsSoFar += len(lastPlayoffBracket)
			else:
				break
				## we reached the bottom of the league, no more brackets to crawl
			
		
		for team in self.Teams:
			team.loadTierIII(self.Teams)
	
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

