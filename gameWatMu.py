## gameWatMu.py ################################################################
## game object specifically representing a waterloo intramurals ################
## game, since the nhl game will need to work a bit differently ################
## (storing a couple of slightly different stats in each one) ##################
################################################################################

from game import *

class watMuGame(Game):
	def __init__(self, dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName, comparisonSelectCondition, seasonIndex):
		super(watMuGame, self).__init__(comparisonSelectCondition, seasonIndex)
		self.addLayer([dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName])
		self.layerCount += 1

	def getSOC(self):
		return float(self.Layers[0][5])
		## Waterloo intramurals has basically a 'Plays Nice' rating, which
		## measures how 'sportsmanlike' a team was. During the season, a teams
		## SOC is part assigned by the refs and the other team, and playoffs is
		## all assesed by the refs
		
		## typically a negative correlation between this and everything that
		## shows a good team, because nobody usually hates on teams that suck

	def cloneGame(self, newCompSelectConditions="noChange"):
		if(type(newCompSelectConditions) == str):
			newCompSelectConditions = self.getComparisonConditions()
		return watMuGame(self.getDate(), self.getLocation(), self.getGameResult(), self.getGoalsFor(), self.getGoalsAgainst(), self.getSOC(), self.getOpponentName(), newCompSelectConditions, self.seasonIndex)

	def getGameDescription(self):
		output = "%s %s %s %i-%i %s\n" % (self.getDate(), self.getLocation(), self.getGameResult(), self.getGoalsFor(), self.getGoalsAgainst(), self.getOpponentName())
		output += "OQI %.3f, DQI %.3f, DQM %.3f, CPQI %.3f\n\n" % (self.getOffenceQualityIndex(), self.getDefenceQualityIndex(), self.getDiffQualMargin(), self.getCPQI())
		output += self.opponent.getDescriptionString()
		output += "\n\n"
		
		return output

	def wasHomeGame(self):
		return True

	def wasAwayGame(self):
		return True
		
	def setSOC(self, newValue):
		self.Layers[0][5] = newValue
		## important to have this to reset values of avg games from
		## 'avg.' -> 2.333 or whatever the teams overall average was


	def notYetPlayed(self):
		if(self.getGameResult() == '-'):
			return True
		else:
			return False
		
	def getPointsEarned(self):
		## this needs to be defined on a league by league basis, since not all
		## leagues actually score points the same way, ie Euro leagues with
		## 3 point system
		if(self.Won()):
			return 2
		elif(self.Tied()):
			return 1
		else:
			return 0
			## regardless of whether we lost or the game hasnt been played yet,
			## no points are earned
	
	def getMaxPointsPossible(self):
		return 2
		
	def getPercentageOfGamePointsEarned(self, seasonIndex):
		if(self.Won()):
			return 1.000
		elif(self.Tied()):
			return 0.500
		else:
			return 0.000			
