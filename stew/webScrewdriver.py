## webScrewdriver.py ###########################################################
## trying to yank js delivered content from a webpage, need an external ########
## lib to do it ################################################################
################################################################################
#!/usr/bin/env python
from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait




if(__name__ == "__main__"):
	url = "https://www.imleagues.com/spa/team/662222b25eb54b88b4eebb4090cb455a/home"
	
	## use firefox to get page with javascript generated content
	with closing(Firefox()) as browser:
		browser.get(url)
		##button = browser.find_element_by_name('button')
		##button.click()
		## wait for the page to load
		WebDriverWait(browser, timeout=10).until(
			lambda x: x.find_element_by_id('mainView'))
		## store it to string variable
		page_source = browser.page_source
	print(page_source)
