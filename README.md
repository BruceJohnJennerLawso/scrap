# scrap
Hockey stats analysis done by scraping the data to a csv file, then processing/analyzing them with more python.

scrap.py is the web scraper, currently only works to scrape the strobe.uwaterloo site for intramurals teams,
and there are guaranteed to be many bugs due to some team pages being fixed in odd ways. The data is saved 
in a predictable format to ./data/[season name]/[team id #].csv

readata.py is the analysis part, loads the data from the csv files and constructs it in an object hierarchy,
(((game)team)league) which can then output more complex stats for the data at each level. Stats are loaded
in layers (I, II, III, ...) in order to allow for stats that rely on one another 
(AWQI (Tier II) relying on points and goals (Tier I), and MaAWQI (Tier III) relying on AWQI (Tier II))



Care and Feeding Instructions:

To get started, you'll need python installed along with pip. Take a look at
dependencies.txt for a list of packages you'll need to install to run the
project.

Once you have the dependencies needed installed, the project can be run in
two steps. The first part, the scraper (scrap.py) requests data from either

https://strobe.uwaterloo.ca/athletics/intramurals/

for the waterloo intramurals data, and

http://hockey-reference.com

for the nhl data

to scrape all beginner data out of the waterloo intramurals system, run the
following command:

python scrap.py 'watMu' 'beginner'

which will then save every team listed under the ./data/watMu/beginner/YEARNAME
manifest files as a csv file will all of the available data for that team

nhl data can be scraped by running

python scrap.py 'nhl'



Once the team data has been saved to hard disk, we can easily reload it and
start manipulating it with more python code. Running

python readata.py 'watMu' 'beginner'

or

python readata.py 'nhl' 'default'

will load that data and graph it using matplotlib. To see these
results, take a look at the images saved under ./results/watMu/beginner
which contains a variety of histograms and scatterplots of the results of
this data.


python teamSummary.py 'watMu' 'beginner'

will print out a text readout of stats for each team in the league
to the console

