## gameWatMu.py ################################################################
## game object specifically representing a waterloo intramurals ################
## game, since the nhl game will need to work a bit differently ################
################################################################################

from game import *

class watMuGame(Game):
	def __init__(self, dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName):
		super(watMuGame, self).__init__(dateString, Location, gameResult, goalsFor, goalsAgainst, SOC, opponentName)
			
