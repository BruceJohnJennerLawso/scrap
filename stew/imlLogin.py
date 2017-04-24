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

		browser.get("https://warrior.uwaterloo.ca/Account/Login?returnUrl=%2F")
		element = browser.find_element_by_name("UserName")
		element.send_keys(username)
		element = browser.find_element_by_name("Password")
		element.send_keys(password)	
		
		buttonId = 'Log In'		
		WebDriverWait(browser, timeout=10).until(
				lambda x: x.find_element_by_value(buttonId))
		button = browser.find_element_by_id(buttonId)
		button.click()
		while(browser.current_url != "https://warrior.uwaterloo.ca/"):
			pass
		print "Finished signing into IMLeagues"


if(__name__ == "__main__"):
	if(len(argv) >= 2):
		username = argv[1]
		password = argv[2]
		##semester = argv[3]
	else:
		username = getTextInput("Please Input Username: ")
		password = getTextInput("Please Input Password: ")
		##semester = getTextInput("Please Semester to build teamIds for: ")			
	getAuthenticatedBrowser(username, password)
