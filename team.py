## team.py #####################################################################
## general base type for any team ##############################################
## hoping to define a specific stat type here instead of #######################
## redoing it for every different team type ####################################
################################################################################
from player import *
import csv


def getSeasonIndexList(leagueId):
	## opens up the file containing the names of every season in our data and
	## assigns an  integer to each one so that we can keep the order straight,
	## particularly with watMu seasons which run not necessarily every season,
	## and more than once a year
	output = []
	with open('./data/%s/seasonIndex.csv' % (leagueId), 'rb') as foo:
		reader = csv.reader(foo)
		for row in reader:
			output.append(row)
			## append on the list of names, with the primary one first, ie
			## [...['winter2010', 'winter2010Contact'],...]
			
			## or in NHL case,
			## [...['2002', '2003', '2004', '2006', '2007', '2008', ...], ...]
			## (notice the season skip at the lockout), so we go
			## 2002 2003 2004 2006 2007
			##   1    2    3    4    5
			
			## cause we dont care about seasons that didnt actually happen
	return output
	
def getSeasonIndexById(seasonId, indexList):
	## if we have the seasonId (ie '2016'), we can call this function to find
	## out what seasonIndex that this season had
	
	## ie what was its place in the order of seasons throughout history
	output = 0
	## default error if we cant find the proper position for the season
	for i in range(0, len(indexList)):
		if(seasonId in indexList[i]):
			output = i
			break
	return output	

class Team(object):
	## base class constructor
	def __init__(self, leagueId, levelId, seasonId, teamId):
		self.seasonId = seasonId
		## string that reliably identifies the current season, ie
		## '2016' or
		## 'fall2015'
		self.teamId = teamId
		## string that reliably identifies the team. ie
		## '12348' (intramurals) or
		## 'TOR'
		self.leagueId = leagueId
		## string that identifies the league that we currently play in, ie
		## 'watMu' or
		## 'nhl'
		self.levelId = levelId
		## the string describing the level of play 
		## (ie beginner/casual in waterloo intramurals)
		
		## for nhl, ahl, etc level, just leave this as 'null' or whatever the
		## output directory name under ./results/nhl is gonna be
		
		self.Games = []
		## init list of objects of type game, currently empty, to be filled by
		## the first loadTier call which opens the csv file and loads in the
		## base data as game objects
		if(leagueId == 'nhl'):
			self.loadPath = "./data/%s/%s/%s%s.csv" % (leagueId, seasonId, teamId, seasonId)
			## shorter load path for nhl when we dont have to branch by levelId
		else:
			self.loadPath = "./data/%s/%s/%s/%s.csv" % (leagueId, levelId, seasonId, teamId)
		
	## prototypes for the functions that load each tier of data ################
	## ABSOLUTELY MUST BE CALLED IN ORDER or bad things WILL happen ############
		
	def loadTierI(self):
		print "Bad call to Team.loadTierI"
		
	def loadTierII(self, teamsList):
		print "Bad call to Team.loadTierII"
		
	def loadTierIII(self, teamsList):
		print "Bad call to Team.loadTierIII"
		
	def loadTierIV(self, teamsList, seasonsList):
		print "Bad call to Team.loadTierIV"		
	
	
	## Tier I ##################################################################
	
	def getTeamName(self):
		## ie 'Toronto Maple Leafs', or 'The Mighty Dads'
		return self.teamName	
	
	def getSeasonId(self):
		## ie '2016' or 'fall2015'
		return self.seasonId	
		
	def getSeasonGoalsForAverage(self):
		return float(self.seasonTotalGoalsFor)/float(self.totalSeasonGames)

	def getSeasonGoalsAgainstAverage(self):
		return float(self.seasonTotalGoalsAgainst)/float(self.totalSeasonGames)
		
	def getSeasonPlusMinus(self):
		## goal differential (for - against)
		return self.seasonPlusMinus
		
	def getSeasonPointsTotal(self):
		## (points earned)
		return self.seasonPointsTotal		
		
	def getPointsPercentage(self):
		## (points earned/total points available)
		return self.seasonPointsTotal/float(self.totalSeasonGames*2)			
		
	def getSeasonWinsTotal(self):
		## games won, regarless of the situation
		return self.seasonWins
		
	def getSeasonTiesTotal(self):
		## games that were tied at the end of regulation and any extra
		## overtime *and stayed that way*
		
		## no shootout games here, we only kicking things oldschool with true
		## ties
		return self.seasonTies	

	def getSeasonLossTotal(self):
		return self.seasonLosses		
	
	def getAGCI(self):
		## stat that measures how close the games this team played were on
		## average
		
		## ie
		##
		## 1-1 -> 1.000
		## 2-1 -> 1.000
		## 3-1 -> 0.500
		## 4-1 -> 0.333
		## 5-1 -> 0.250
		## 6-1 -> 0.200
		## 7-1 -> 0.166
		return self.averageGameClosenessIndex
		
	def getTotalPlayoffGames(self):
		## counts how many playoff games this team played in all (0, 4, 22, etc)
		return len(self.playoffGames)

	def getTotalPlayoffWins(self):
		## total games won in the playoffs
		return self.playoffWins
		
	def getPlayoffWinPercentage(self):
		## what percentage of any playoff games played that the team won as a
		## decimal, ie 0.782 
		return self.playoffWinPercentage
	
	def getRealPlayoffWinPercentage(self, season):
		## the problem here is that for the watMu system, not all playoff wins
		## are created equal, for a big bracket like the intermediate, a win in
		## the second playoff bracket isnt really worth the same as one in the
		## top bracket, since a team in the second bracket plays much worse
		## teams than the team in the top bracket did
		
		## so for most analysis that we do, we only consider wins in the top
		## playoff bracket to be 'real'
		if(self.leagueId == 'watMu'):
			if(self.getSeasonRank() not in season.topPlayoffBracket):
				return 0.000
			else:
				return self.getPlayoffWinPercentage()	
		else:
			return self.getPlayoffWinPercentage()
			## if we arent dealing with a weird watMu style league, just get the
			## raw playoff win percentage
			
				
	def getPlayoffGoalsForAverage(self):
		output = 0.000
		if(self.getTotalPlayoffGames() > 0):
			output = float(self.playoffGoalsFor)/float(self.getTotalPlayoffGames())
		return output

	def getPlayoffGoalsAgainstAverage(self):
		output = 0.000
		if(self.getTotalPlayoffGames() > 0):
			output = float(self.playoffGoalsAgainst)/float(self.getTotalPlayoffGames())
		return output
		
	def getRoster(self):
		return self.Roster
		
	## note that we try to squeeze down to shorter names here in order to make
	## working on the front end a bit easier than typing out
	## getAverageGameClosenessIndex() would be
	
	## Tier II #################################################################
		
	def getAWQI(self):
		return self.averageWinQualityIndex
		
	def getAPQI(self):
		return self.averagePlayQualityIndex
		
	def getSeasonRank(self):
		return self.seasonRank
		
	def getOffenceQualityIndex(self):
		return self.offenceQualityIndex
		
	def getDefenceQualityIndex(self):
		return self.defenceQualityIndex

	## Tier III ################################################################

	def getMaAWQI(self):
		return self.meanAdjustedAverageWinQualityIndex	
		
	def getMaAPQI(self):
		return self.meanAdjustedAveragePlayQualityIndex
		
	def getMaOQI(self):
		return self.meanAdjustedOffenceQualityIndex
		
	def getMaDQI(self):
		return self.meanAdjustedDefenceQualityIndex

	## our two indexes now adjusted for season mean in an attempt to make easier
	## to compare across different seasons. MaAWQI appears to be the best 
	## predictor of playoff success so far
	
	## also makes for an easy way to benchmark likely contenders, contenders
	## are *usually* at least 1-2 times the league mean in AWQI, often 2x or
	## above. Only 1 team has ever won the championship with a MaAWQI below 1
	## (Winter 2014 Pucked Up) with a MaAWQI of 0.922
	
	## Its pronounced "Mah-Quee" in case you were wondering 

	## Tier IV #################################################################
	
	def getPlayers(self):
		return self.Players
