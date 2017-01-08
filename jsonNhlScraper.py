## nhljsonScraper.py ###########################################################
## scrape nhl game jsons from statsapi.web.nhl.com #############################
## save them into file under the season folder in data/nhl/season/games ########
################################################################################
import json
from pprint import pprint
import urllib
import os

def saveGameToJson(gameId, seasonId):
	##gameId = "2010030416"
	##seasonId = "2011"
	
	
	url = 'http://statsapi.web.nhl.com/api/v1/game/%s/feed/live' % gameId
	
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	##pprint(data)
	try:
		with open('./data/nhl/%s/games/%s.json' % ("%.4i" % (seasonId+1), gameId), 'w') as outfile:
			json.dump(data, outfile)
	except IOError:
		os.mkdir("./data/nhl/%s/games/" % "%.4i" % (seasonId+1))
		with open('./data/nhl/%s/games/%s.json' % ("%.4i" % (seasonId+1), gameId), 'w') as outfile:
			json.dump(data, outfile)
			
if(__name__ == "__main__"):

	years = [2010, 2011, 2012, 2013, 2014, 2015, 2016]
	for year in years:
		for gameNo in range(1, 1230):
			gameId = "%s02%.4i" % (year, gameNo)
			
			print year, gameId
			
			saveGameToJson(gameId, year)
