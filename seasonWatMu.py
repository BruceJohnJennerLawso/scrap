## seasonWatMu.py ##############################################################
## base type for Waterloo Intramurals Hockey ###################################
## seasons (Individual semesters teams) ########################################
################################################################################
from teamWatMu import *
from season import *

def getSeedsInBracket(currentTeam, season, alreadyInBracket, count=0):
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
	def __init__(self):
		self.bracketNumbers = []
		
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
		
		self.playoffBrackets.append(playoffBracket())
		self.topTeam = self.getTeamByPosition(1)
		## next work through the teams this one played and add their position
		## numbers to the top playoff bracket, then look through their
		## opponents and so on
		
		## maybe a recursive function here that takes the teams list and the
		## bracket list as arguments and returns lists of seeding positions
		
		self.topPlayoffBracket = getSeedsInBracket(self.topTeam, self, [])
		print "top playoff bracket: ", self.topPlayoffBracket
			
		
		for team in self.Teams:
			team.loadTierIII(self.Teams)
						
