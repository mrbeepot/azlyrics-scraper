from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException, SessionNotCreatedException
from bs4 import BeautifulSoup as bs

import time

class AZLyricsScraper:

	def __init__(self):
		self.options = Options()
		self.options.add_argument("-headless")

	def openDriver(self):
		self.driver = Firefox(firefox_options=self.options)

	def closeDriver(self):
		try:	
			self.driver.close()
		except SessionNotCreatedException as e:
			print("You are trying to close a session which was not created.")

	def searchSong(self,query):
		self.openDriver()
		try:
			self.driver.get("https://search.azlyrics.com/")
		except WebDriverException as e:
			print("Unable to open the url, please chack your network connection")
			self.closeDriver()
			return ""
		else:	
			try:
				searchBox = self.driver.find_element_by_name("q")
			except NoSuchElementException as e:
				print("The element cannot be found.")
				self.closeDriver()
				return ""
			else:	
				searchBox.click()
				searchBox.clear()
				searchBox.send_keys(query)
				searchBox.send_keys(Keys.RETURN)
				time.sleep(1)
				queryResultHTML = bs(self.driver.page_source,"lxml")
				songData = []
				queryResultPanels = queryResultHTML.find_all("div",{"class":"panel"})
				if queryResultPanels is not None:
					for panel in queryResultPanels:
						heading = panel.find("b")
						if "Song" in heading.string:
							songResultTableData = panel.find_all("td")
							if songResultTableData is not None:
								for song in songResultTableData:
									temp = []
									boldTags = song.find_all("b")
									if boldTags is not None:	
										for b in boldTags:
											temp.append(b.get_text())
										temp.append(song.a.get("href"))
										songData.append(temp)
									else:
										print("Error fetching the song data.")
										self.closeDriver()
										return ""
							else:
								print("No songs related to your query were found.")
								self.closeDriver()
								return ""
					self.closeDriver()
					if len(songData[0]) == 2:
						return songData[1:-1]
					return songData[:-1]
				else:
					print("No songs related to your query were found.")
					self.closeDriver()
					return ""
					
	def getLyrics(self,url):
		self.openDriver()
		try:
			self.driver.get(url)
		except WebDriverException as e:
			print("Unable to open the url, please chack your network connection")
			self.closeDriver()
			return ""
		else:
			time.sleep(1)
			pageSource = self.driver.page_source
			index = pageSource.find("<!-- content -->")
			if index > -1:	
				pageSource = pageSource[index:]
				soup = bs(pageSource,"lxml")
				outerDiv = soup.find("div",{"class":["col-xs-12","col-lg-8"]})
				if outerDiv is not None:	
					requiredDivList = outerDiv.find_all("div")
					if requiredDivList is not None:
						try:	
							lyrics = requiredDivList[8].get_text()
							self.closeDriver()
							return lyrics
						except IndexError as e:
							print("The index of div containing lyrics was not found.")
							self.closeDriver()
							return ""
				else:
					self.closeDriver()
					return ""
			else:
				self.closeDriver()
				return ""