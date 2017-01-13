## player.py ###################################################################
## object representing an individual player in the waterloo ####################
## intramurals system ##########################################################
################################################################################
import team


class Player(object):
	def __init__(self, name):
		self.Name = name
		## whats in a name, eh?
		
		## overall, the general structure of a player in our context here is a
		## list of team objects that it has played for, which we can use to
		## pull career data about the teams that we played for
		
		## for teams that had individual player data, we can obviously use it
		## to directly return the numbers, but we might be able to do 
		## interesting things with interpolating career curves out of small
		## samples of a players individual numbers
		
		## FFUUUTUURE
		
	def getName(self):
		return self.Name

	def getNumberOfSeasonsPlayed(self):
		return len(self.playedFor)

	def getPlayerCareerTotalStatValue(self, statCall, currentSeasonIndex=-1):
		## step through every season up to the current one (if specified)
		## add up the MaAWQIs of the team the player played for each season
		## and average them over the total seasons played
		
		## yes I know its hilariously vague, but its something
		output = 0.000
		if(self.getNumberOfSeasonsPlayed() > 0):
			## not sure how its here otherwise, but whatever
			for team in self.playedFor:
				if(currentSeasonIndex != -1):
					## if a season cutoff was specified, we only
					if(team.getSeasonIndex() < currentSeasonIndex):
						output += statCall(team)
				else:
					output += statCall(team)
		return output

	def getPlayerCareerMeanStatValue(self, statCall, currentSeasonIndex=-1):
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
						output += statCall(team)
						seasonCount += 1
				else:
					output += statCall(team)
					seasonCount += 1
			if(seasonCount > 0):
				output /= float(seasonCount)
		return output
	

	def plotSeasonBySeasonStats(self, output_path, output_directory, output_filename):
		## quick & dirty function to save the big picture view of a players
		## career team numbers to file
		import matplotlib.pyplot as plt
		
		seasonIndexes = []
		seasonCPQIs = []
		seasonOQI = []
		seasonDQI = []
		
		for team in self.playedFor:
			seasonIndexes.append(team.getSeasonIndex())
			seasonCPQIs.append(team.getCPQI())
			seasonOQI.append(team.getOffenceQualityIndex())
			seasonDQI.append(team.getDefenceQualityIndex())
		plt.plot(seasonIndexes, seasonMawquees, 'go', label='CPQI')
		plt.plot(seasonIndexes, seasonOQI, 'ro', label='OQI')
		plt.plot(seasonIndexes, seasonDQI, 'bo', label='DQI')		
		
		
		plt.xlabel('Season Number')
		plt.ylabel("Team Value")
		plt.legend()
		output_ = "%s/%s/%s" % (output_path, output_directory, output_filename)
		plt.savefig(output_)
		plt.close()


	def getStatsLine(self, currentSeasonIndex=-1):
		## get a general desc of the player, kinda like the player card ;)
		
		## note the currentSeasonIndex here, which is meant to cap the players
		## stats at a specific season, instead of the entire career
		## (if we wanted to do forecasts on a specific season)
		return "Player: %s, %i seasons played\nTeam Averages:\nAGCI %.3f, MaAWQI %.3f, MaAPQI %.3f\nADQI %.3f, AOQI %.3f, CPQI %.3f\nOffense %.3f, Defence %.3f, +/- %.3f" % (self.getName(), self.getNumberOfSeasonsPlayed(), self.getPlayerCareerMeanStatValue(team.Team.getAGCI), self.getPlayerCareerMeanStatValue(team.Team.getMaAWQI), self.getPlayerCareerMeanStatValue(team.Team.getMaAPQI), self.getPlayerCareerMeanStatValue(team.Team.getADQI), self.getPlayerCareerMeanStatValue(team.Team.getAOQI), self.getPlayerCareerMeanStatValue(team.Team.getCPQI), self.getPlayerCareerMeanStatValue(team.Team.getSeasonGoalsForAverage), self.getPlayerCareerMeanStatValue(team.Team.getSeasonGoalsAgainstAverage), self.getPlayerCareerMeanStatValue(team.Team.getSeasonPlusMinus))
		
		for teamPlayedFor in self.playedFor:
			print teamPlayedFor.getDescriptionString(), '\n'
			

