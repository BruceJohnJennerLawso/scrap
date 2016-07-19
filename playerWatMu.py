## playerWatMu.py ##############################################################
## player object, specific to the waterloo intramurals system ##################
## generally just in the format used from 2008-2016 ############################
## (ie very limited information) ###############################################
################################################################################
from player import *


class watMuPlayer(Player):
	def __init__(self, name, seasons):
		super(watMuPlayer, self).__init__(name)
		self.playedFor = []
		for season in reversed(seasons):
			for team in season.Teams:
				if(self.getName() in team.getRoster()):
					self.playedFor.append(team)
		
	def getStatsLine(self):
		print "Player: %s, %i seasons played\n\n" % (self.getName(), len(self.playedFor))
		
		for team in self.playedFor:
			print team.getDescriptionString(), '\n'
	
