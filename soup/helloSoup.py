## helloSoup.py ################################################################
## just mucking around with beautiful soup to get ##############################
## a feel for it ###############################################################
################################################################################
from bs4 import BeautifulSoup
from lxml import html
import requests


if(__name__ == "__main__"):

	url = "https://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=11256"

	page = requests.get(url)
	
	soup = BeautifulSoup(page.content)
	##table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="Table1") 
	##rows = table.findAll(lambda tag: tag.name=='tr')
	for link in soup.find_all('a'):
		print(link.get('href'))
