# scrap
Hockey stats analysis done by scraping the data to a csv file, then processing/analyzing them with more python.

scrap.py is the web scraper, currently only works to scrape the strobe.uwaterloo site for intramurals teams,
and there are guaranteed to be many bugs due to some team pages being fixed in odd ways. The data is saved 
in a predictable format to ./data/[season name]/[team id #].csv

readata.py is the analysis part, loads the data from the csv files and constructs it in an object hierarchy,
(((game)team)league) which can then output more complex stats for the data at each level. Stats are loaded
in layers (I, II, III, ...) in order to allow for stats that rely on one another 
(AWQI (Tier II) relying on points and goals (Tier I), and MaAWQI (Tier III) relying on AWQI (Tier II))
The functions for this part of the analysis are about 40% ish done right now
