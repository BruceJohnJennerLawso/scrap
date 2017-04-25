## imlLogin.py #################################################################
## standard route to get an instance of selenium thats through authentication #
## for imleagues ###############################################################
################################################################################
from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
from bs4 import BeautifulSoup

import selenium

import time
import sys
from sys import argv
import string
import csv
import os
import watMuSportInfo

from selenium.webdriver.common.keys import Keys

def getTextInput(prompt):
	output = ""
	while(output == ""):
		print prompt,
		output = raw_input()
	return output


	
def getAuthenticatedBrowser(username, password):
	## add this line
	
	firefox_options = webdriver.FirefoxProfile()
	prefs = {"dom.webnotifications.enabled" : False}
	firefox_options.set_preference('dom.webnotifications.enabled', False)
	firefox_options.set_preference('dom.webnotifications.serviceworker.enabled', False)	
	## might actually be "false"
	##driver = webdriver.Firefox(profile)
	


	with closing(Firefox(firefox_options)) as browser:	



		browser.get("https://warrior.uwaterloo.ca/Account/Login?returnUrl=%2F")
		element = browser.find_element_by_name("UserName")
		element.send_keys(username)
		element = browser.find_element_by_name("Password")
		element.send_keys(password)	
		
		buttonId = "//input[@value='Log In']"	
		WebDriverWait(browser, timeout=10).until(
				lambda x: x.find_element_by_xpath(buttonId))
		button = browser.find_element_by_xpath(buttonId)
		button.click()
		while(browser.current_url != "https://warrior.uwaterloo.ca/"):
			pass
		print "Finished signing into uwaterloo intramurals site"
		intramuralsButtonId = "//img[@class='img-responsive' and @alt='Intramurals']"	
		WebDriverWait(browser, timeout=10).until(
			lambda x: x.find_element_by_xpath(intramuralsButtonId))
		button = browser.find_element_by_xpath(intramuralsButtonId)
		browser.get("https://warrior.uwaterloo.ca/IMLeague")
		intramuralsButtonId = "//img[@class='img-responsive' and @alt='IMLeagues Login']"	
		WebDriverWait(browser, timeout=10).until(
			lambda x: x.find_element_by_xpath(intramuralsButtonId))
		button = browser.find_element_by_xpath(intramuralsButtonId)	
		button.click()
		while(browser.current_url != "https://www.imleagues.com/spa/member/player"):
			##WebDriverWait(browser, timeout=10).until(
			##	lambda x: x.find_element_by_xpath("/html"))
			##browser.find_element_by_xpath("/html").send_keys(Keys.ESCAPE);
			pass
		time.sleep(5)
		print "Finished signing into IMLeagues"
		return browser
		
if(__name__ == "__main__"):
	if(len(argv) >= 2):
		username = argv[1]
		password = argv[2]
		##semester = argv[3]
	else:
		username = getTextInput("Please Input Username: ")
		password = getTextInput("Please Input Password: ")
		##semester = getTextInput("Please Semester to build teamIds for: ")			
	browser = getAuthenticatedBrowser(username, password)
	url = "https://www.imleagues.com/spa/team/662222b25eb54b88b4eebb4090cb455a/home"
	browser.get(url)
