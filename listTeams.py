## listTeams.py ################################################################
## need just all of the teams and their info ###################################
################################################################################

from sys import argv
from outputs import *

from collections import Counter


if(__name__ == "__main__"):
		
	leagueId = argv[1]
	## ie 'watMu'
	levelId = argv[2]
	## ie 'beginner'
	
	## ids needed to open the proper folders and csv files contained within
	seasons = getAllSeasons(leagueId, levelId)
	## retrieve list of seasons from the manifest for this level
	franchises = getFranchiseList(leagueId, levelId)
	
	seasonIndexList = getSeasonIndexList(leagueId)
	
	print "################################################################################"
	print "Season Teams ###################################################################"
	print "################################################################################\n"	
	
	for season in seasons:
		print season.seasonId, '\n'
		for team in season.Teams:
			print "		", team.getTeamName(), "Franchise: %s" % (team.getFranchise(franchises))
			print team.getDescriptionString()
			print team.Roster
	print "################################################################################\n\n\n"

	playerNames = []
	## list of all names on teams
	for season in seasons:
		for team in season.Teams:
			for player in team.Roster:
				playerNames.append(player)
	playerCounts = Counter(playerNames)
	
	topForty = playerCounts.most_common(40)
	for p in topForty:
		print p[0], ' ', p[1]
		## p[0] is the name, p[1] is the count
		playah = watMuPlayer(p[0], seasons)
		playah.getStatsLine()
	
	seasonHits = []
	
	for name in playerCounts:
		seasonHits.append(playerCounts[name])
		
	occurenceCounts = Counter(seasonHits)
				
	seasonCounts = []
	
	for o in occurenceCounts:
		seasonCounts.append(occurenceCounts[o])
		print occurenceCounts[o], ' ', o
	
	plotHistogram('Seasons Played', 'Count', 'Histogram of Total Seasons Played by Players', seasonHits, './results/%s/%s' % (leagueId, levelId), 'playerData', 'playerSeasonCountHistogram.png', 'foo', 'bar', 39, max(seasonCounts)+20)
	print "Seasons played distribution:\n\n"
	
	
	
	##jimbo = watMuPlayer('Jim Brooks', seasons)
	##jimbo.getStatsLine()
	
	##brucie = watMuPlayer('John Lawson', seasons)
	##brucie.getStatsLine()
	
	##tallionStallion = watMuPlayer('Giacomo Torlai', seasons)
	##tallionStallion.getStatsLine()

##	for season in seasons:
##		print season.seasonId, '\n'
##		for team in season.Teams:
##			if(team.getFranchise(franchises)=="None"):
##				print "		", team.getTeamName(), "Franchise: %s" % (team.getFranchise(franchises))
	
