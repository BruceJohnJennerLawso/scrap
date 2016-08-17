## playerWatMu.py ##############################################################
## player object, specific to the waterloo intramurals system ##################
## generally just in the format used from 2008-2016 ############################
## (ie very limited information) ###############################################
################################################################################
from player import *


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
		self.playedFor.sort(key=lambda x: x.getSeasonIndex, reverse=True)
		## sort the list in place by season index to get a proper chronological
		## order
		
	def getStatsLine(self, currentSeasonIndex=-1):
		## get a general desc of the player, kinda like the player card ;)
		
		## note the currentSeasonIndex here, which is meant to cap the players
		## stats at a specific season, instead of the entire career
		## (if we wanted to do forecasts on a specific season)
		print "\n\nPlayer: %s, %i seasons played, average MaAWQI of %.3f\n" % (self.getName(), self.getNumberOfSeasonsPlayed(), self.getPlayerMaAWQI(currentSeasonIndex))
		
		##for team in self.playedFor:
		##	print team.getDescriptionString(), '\n'
			
			
	def getNumberOfSeasonsPlayed(self):
		return len(self.playedFor)

	def getPlayerMaAWQI(self, currentSeasonIndex=-1):
		## step through every season up to the current one (if specified)
		## add up the MaAWQIs of the team the player played for each season
		## and average them over the total seasons played
		
		## yes I know its hilariously vague, but its something
		output = 0.000
		if(self.getNumberOfSeasonsPlayed() > 0):
			## not sure how its here otherwise, but whatever
			seasonCount = 0
			for team in self.playedFor:
				if(currentSeasonIndex != -1):
					## if a season cutoff was specified, we only
					if(team.getSeasonIndex() < currentSeasonIndex):
						output += team.getMaAWQI()
						seasonCount += 1
				else:
					output += team.getMaAWQI()
					seasonCount += 1
			if(seasonCount > 0):
				output /= float(seasonCount)
			return output

	
	def getPlayerMaAPQI(self, currentSeasonIndex=-1):
		## same idea, now for MaPQWI
		output = 0.000
		if(self.getNumberOfSeasonsPlayed() > 0):
			seasonCount = 0
			for team in self.playedFor:
				if(currentSeasonIndex != -1):
					if(team.getSeasonIndex() < currentSeasonIndex):
						output += team.getMaAPQI()
						seasonCount += 1
				else:
					output += team.getMaAPQI()
					seasonCount += 1
			if(seasonCount > 0):
				output /= float(seasonCount)
			return output
						
		
	def plotSeasonBySeasonStats(self, output_path, output_directory, output_filename):
		## quick & dirty function to save the big picture view of a players
		## career team numbers to file
		import matplotlib.pyplot as plt
		
		seasonIndexes = []
		seasonMawquees = []
		seasonOQI = []
		seasonDQI = []
		
		for team in self.playedFor:
			seasonIndexes.append(team.getSeasonIndex())
			seasonMawquees.append(team.getMaAWQI())
			seasonOQI.append(team.getOffenceQualityIndex())
			seasonDQI.append(team.getDefenceQualityIndex())
		plt.plot(seasonIndexes, seasonMawquees, 'go', label='MaAWQI')
		plt.plot(seasonIndexes, seasonOQI, 'ro', label='OQI')
		plt.plot(seasonIndexes, seasonDQI, 'bo', label='DQI')		
		
		
		plt.xlabel('Season Number')
		plt.ylabel("Team Value")
		plt.legend()
		output_ = "%s/%s/%s" % (output_path, output_directory, output_filename)
		plt.savefig(output_)
		plt.close()
