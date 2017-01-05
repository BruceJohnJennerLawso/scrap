## nhljsonScraper.py ###########################################################
## scrape nhl game jsons from statsapi.web.nhl.com #############################
## save them into file under the season folder in data/nhl/season/games ########
################################################################################
import json



if(__name__ == "__main__"):
	gameId = "2010030416"
	seasonId = "2011"
	with open('./data/nhl/%s/games/%s.json' % (seasonId, gameId), 'w') as outfile:
		json.dump(data, outfile)
