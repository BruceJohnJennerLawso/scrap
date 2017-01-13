## playerWatMu.py ##############################################################
## player object, specific to the waterloo intramurals system ##################
## generally just in the format used from 2008-2016 ############################
## (ie very limited information) ###############################################
################################################################################
from player import *
import team

class watMuPlayer(Player):
	def __init__(self, name, seasons):
		super(watMuPlayer, self).__init__(name)
		## call the parent constructor, assigning a name to our player
		self.playedFor = []
		## list of team objects that have this players name on the roster
		for season in reversed(seasons):
			## I think the reversed part is so that we get the seasons in
			## chronological order, but we do it properly down below anyways
			for team in season.Teams:
				if(self.getName() in team.getRoster()):
					self.playedFor.append(team)
		self.playedFor.sort(key=lambda x: x.getSeasonIndex(), reverse=True)
		## sort the list in place by season index to get a proper chronological
		## order
		





