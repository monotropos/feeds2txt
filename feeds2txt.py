#!/usr/bin/python3
import feedparser
from datetime import datetime
from dateutil import parser


# List of RSS feeds that we will fetch and combine
newsurls = {
	"vimeo.dionysia":		"https://vimeo.com/user12810887/videos/rss",
	"vimeo.katzourakis":	"https://vimeo.com/user6077796/videos/rss",
	"vimeo.movieteller":	"https://vimeo.com/movieteller/videos/rss",
	"youtube.BrodieRobertson":	"https://www.youtube.com/feeds/videos.xml?channel_id=UCld68syR8Wi-GY_n4CaoJGA",
	"reddit.greece":	"https://www.reddit.com/r/greece.rss",
	"hackernews": "https://news.ycombinator.com/rss",
}
allheadlines = []
today = datetime.today().date()
days2show = 1


# Function grabs the rss feed headlines (titles) and returns them as a list
def getHeadlines(rss_url):
	headlines = []
	feed = feedparser.parse(rss_url)
	for newsitem in feed['items']:
		headlines.append(newsitem)
	return headlines


# print(str(today))
# Iterate over the allheadlines list and print each headline
for key, url in newsurls.items():
	print("# "+key+" "+"-"*20)
	allheadlines.extend(getHeadlines(url))
	for hl in allheadlines:
		try:
			pdate = hl["updated"]
		except KeyError:
			pdate = hl["published"]
		d = parser.parse(pdate).date()
		days = (today - d).days
		if days <= days2show:
			print(key+" » "+hl["title"]+" @"+pdate+" | "+hl["link"])
	allheadlines = []

# end of code
