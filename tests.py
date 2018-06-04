from api import AZLyricsScraper as scraper

def searchSongTest1(query):
	o = scraper()
	l = o.searchSong(query)
	for i in l:
		print(i)
def getLyricsTest1(url):
	o = scraper()
	print(o.getLyrics(url))


searchSongTest1("time in a bottle")
# getLyricsTest1("https://www.azlyrics.com/lyrics/queen/killerqueen.html")