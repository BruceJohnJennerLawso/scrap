## webScrewdriver.py ###########################################################
## trying to yank js delivered content from a webpage, need an external ########
## lib to do it ################################################################
################################################################################
#!/usr/bin/env python
from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
from bs4 import BeautifulSoup

import time
import sys

def getTextInput(prompt):
	output = ""
	while(output == ""):
		print prompt,
		output = raw_input()
	return output

if(__name__ == "__main__"):
	
	from sys import argv
	## add this line
	
	if(len(argv) >= 3):
		username = argv[1]
		password = argv[2]
	else:
		username = getTextInput("Please Input Username: ")
		password = getTextInput("Please Input Password: ")		
	
	url = "https://www.imleagues.com/spa/team/662222b25eb54b88b4eebb4090cb455a/home"
	with closing(Firefox()) as browser:

		##driver = webdriver.Firefox()

		driver = browser
	

		driver.get("https://nike.uwaterloo.ca/Login.aspx?soi=IM&ref=Intramurals")
		element = driver.find_element_by_id("ctl00_contentMain_ASPxRoundPanel2_loginMain_UserName_I")
		element.send_keys(username)
		element = driver.find_element_by_id("ctl00_contentMain_ASPxRoundPanel2_loginMain_Password_I")
		element.send_keys(password)	
		
		buttonId = 'ctl00_contentMain_ASPxRoundPanel2_loginMain_LoginButton'
		##buttonId = 'ctl00_contentMain_ASPxRoundPanel2_loginMain_LoginButton_I'		
		
		WebDriverWait(browser, timeout=10).until(
				lambda x: x.find_element_by_id(buttonId))
		button = browser.find_element_by_id(buttonId)
		##print button.tag_name, button.text
		##print browser.page_source
		button.click()
		##button.click()	
		##WebDriverWait(browser, timeout=90).until(
		##		lambda x: x.find_element_by_class_name('head-title iml-main-header-name'))
		##myNameElement = browser.find_element_by_xpath("/html/body[@class='iml-nonresponsiveness iml-body-gray im-showads']/div[@id='mainView']/div[1]/div[@id='imlHead']/div[@id='imlStickerTab-sticky-wrapper']/div[@id='imlStickerTab']/div[@class='container iml-override-container']/div[@class='row'][1]/div[@class='col-xs-12']/div[@class='media iml-header-avatar iml-head-low-height']/div[@class='media-body']/div[@id='imlDefaultMenu']/h3[@class='media-heading schoolMainNavigBack']/a[@class='head-title iml-main-header-name']")
		##print myNameElement, myNameElement.text
		while(browser.current_url != "https://www.imleagues.com/spa/member/player"):
			pass
		print "Finished signing into IMLeagues"
		browser.get(url)
		##driver.manage().timeouts().pageLoadTimeout(20, TimeUnit.SECONDS);
		time.sleep(15)
		print driver.find_element_by_tag_name('html'), driver.find_element_by_tag_name('html').text, driver.find_element_by_tag_name('html').get_attribute('innerHTML')
		
		
		loadedHtmlContent = driver.find_element_by_tag_name('html').get_attribute('innerHTML').encode('utf8')
		print type(loadedHtmlContent)
		
		Html_file= open("./visiblePage.html","w")
		Html_file.write(loadedHtmlContent)
		Html_file.close()		
		##soup = BeautifulSoup("%s" % loadedHtmlContent, "lxml")
		soup = BeautifulSoup("%s" % loadedHtmlContent, 'html.parser')
		print soup, type(soup)
		try:
			content = soup.findAll(lambda tag: tag.name=='div', {"class": "col-xs-12"}) 
			for row in content:
				print row, row,getText()
		except:
			pass


if(__name__ == "__brain__"):
	##url = "https://www.imleagues.com/spa/team/662222b25eb54b88b4eebb4090cb455a/home"
	##url = "http://google.ca"
	##url = "http://www.quackit.com/html/html_editors/scratchpad/preview.cfm"
	url = "http://127.0.0.1/js.html"
	## use firefox to get page with javascript generated content
	with closing(Firefox()) as browser:
		##browser.get(url)
		
		
		#WebElement inputElement = driver.findElement(By.id("input_field_1"));
		#inputElement.clear();
		#inputElement.sendKeys("12");
		#//here you have to wait for javascript to finish. E.g wait for a css Class or id to appear
		#Assert.assertEquals("12", inputElement.getAttribute("value"));
		
		try:
			browser.get(url)
			button = browser.find_element_by_tag_name('button')
			button.click()
			## wait for the page to load
			##browser.refresh();
			WebDriverWait(browser, timeout=10).until(
				lambda x: x.find_element_by_id('demo'))
				##lambda x: x.find_element_by_id('mainView'))			
			## store it to string variable
		except:
			pass
		page_source = browser.page_source
	print(page_source)
