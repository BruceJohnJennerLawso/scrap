## imlLogin.py #################################################################
## standard route to get an instance of selenium thats through authentication #
## for imleagues ###############################################################
################################################################################
from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
from bs4 import BeautifulSoup

import time
import sys
from sys import argv
import string
import csv
import os
import watMuSportInfo



def getTextInput(prompt):
	output = ""
	while(output == ""):
		print prompt,
		output = raw_input()
	return output


	
def getAuthenticatedBrowser(username, password):
	## add this line
	

	
	url = "https://www.imleagues.com/spa/team/662222b25eb54b88b4eebb4090cb455a/home"
	with closing(Firefox()) as browser:	

		browser.get("https://nike.uwaterloo.ca/Login.aspx?soi=IM&ref=Intramurals")
		element = browser.find_element_by_id("ctl00_contentMain_ASPxRoundPanel2_loginMain_UserName_I")
		element.send_keys(username)
		element = browser.find_element_by_id("ctl00_contentMain_ASPxRoundPanel2_loginMain_Password_I")
		element.send_keys(password)	
		
		buttonId = 'ctl00_contentMain_ASPxRoundPanel2_loginMain_LoginButton'		
		WebDriverWait(browser, timeout=10).until(
				lambda x: x.find_element_by_id(buttonId))
		button = browser.find_element_by_id(buttonId)
		button.click()
		while(browser.current_url != "https://www.imleagues.com/spa/member/player"):
			pass
		print "Finished signing into IMLeagues"
		semesters = [semester]
		for semester in semesters:
			
			with open('%shooks.csv' % semester, 'rb') as f:
				reader = csv.reader(f)
				i = 0
				for row in reader:
					i+=1
					print row
					teamId = row[0]
					sportId = int(row[1])
					levelId = row[2]
					saveIdsInLinkedLeague(browser, "https://www.imleagues.com/spa/team/%s/home" % teamId, sportId, levelId, semester)


if(__name__ == "__main__"):
	if(len(argv) >= 4):
		username = argv[1]
		password = argv[2]
		##semester = argv[3]
	else:
		username = getTextInput("Please Input Username: ")
		password = getTextInput("Please Input Password: ")
		##semester = getTextInput("Please Semester to build teamIds for: ")			
