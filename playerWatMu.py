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
		self.playerMaAWQI = 0.000
		if(self.getNumberOfSeasonsPlayed() > 0):
			for team in self.playedFor:
				self.playerMaAWQI += team.getMaAWQI()
			self.playerMaAWQI /= float(self.getNumberOfSeasonsPlayed())
		
	def getStatsLine(self):
		print "\n\nPlayer: %s, %i seasons played, average MaAWQI of %.3f\n" % (self.getName(), self.getNumberOfSeasonsPlayed(), self.getPlayerMaAWQI())
		
		for team in self.playedFor:
			print team.getDescriptionString(), '\n'
			
	def getNumberOfSeasonsPlayed(self):
		return len(self.playedFor)
	
	def getPlayerMaAWQI(self):
		return self.playerMaAWQI
