## webScrewdriver.py ###########################################################
## trying to yank js delivered content from a webpage, need an external ########
## lib to do it ################################################################
################################################################################
#!/usr/bin/env python
from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait




if(__name__ == "__main__"):
	##url = "https://www.imleagues.com/spa/team/662222b25eb54b88b4eebb4090cb455a/home"
	##url = "http://google.ca"
	##url = "http://www.quackit.com/html/html_editors/scratchpad/preview.cfm"
	url = "http://127.0.0.1/js.html"
	## use firefox to get page with javascript generated content
	with closing(Firefox()) as browser:
		##browser.get(url)
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
