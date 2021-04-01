#!/usr/bin/python3
import feedparser
from datetime import datetime
from dateutil import parser
from configparser import ConfigParser


# Read config.ini file
config_object = ConfigParser()
config_object.read("feeds2txt.ini")
newsurls = config_object["FEEDS"]
parameters = config_object["PARAMETERS"]
try:
	days2show = int(parameters["days2show"])
except:
	days2show = 1

allheadlines = []
today = datetime.today().date()


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
