#!/usr/bin/python3
import feedparser
from datetime import datetime
from dateutil import parser
from configparser import ConfigParser
import sys


# Function grabs the rss feed headlines (titles) and returns them as a list
def getHeadlines(rss_url):
    headlines = []
    try:
        feed = feedparser.parse(rss_url)
    except:
        return headlines
    for newsitem in feed['items']:
        headlines.append(newsitem)
    return headlines


if len(sys.argv) > 1:
    inifile = sys.argv[1]
else:
    inifile = "feeds2txt.ini"

# Read .ini file
config_object = ConfigParser()
config_object.read(inifile)
try:
    newsurls = config_object["FEEDS"]
except KeyError:
    newsurls = []

try:
    parameters = config_object["PARAMETERS"]
    time2show = int(parameters["time2show"])
except (KeyError, NameError):
    time2show = 86400

try:
    lastseen = float(parameters["lastseen"])
    print("Last update: " + parameters["lastseen"])
except (KeyError, NameError):
    lastseen = datetime.now().timestamp() - time2show

allheadlines = []
printheadlines = []

# Iterate over the allheadlines list and print each headline
if len(newsurls):
    for key, url in newsurls.items():
        # When url is "--" just print a line divider
        if url == "--":
            print(">", "»"*30, key, "«"*30)
            continue
        allheadlines.extend(getHeadlines(url))
        for hl in allheadlines:
            try:
                pdate = hl["updated"]
            except KeyError:
                pdate = hl["published"]
            d = parser.parse(pdate).timestamp()
            difftime = d - lastseen
            if difftime > 0:
                printheadlines.append(" » " + hl["title"]
                                      + " @" + pdate + " — " + hl["link"])

        if len(printheadlines) > 0:
            print(f">> {key} "+"-"*20)
            for hl in printheadlines:
                print(hl)

        printheadlines = []
        allheadlines = []

# Write .ini file
config_object["PARAMETERS"] = {
    "time2show": time2show,
    "lastseen": datetime.now().timestamp()
}

with open(inifile, 'w') as conf:
    config_object.write(conf)

# end of code
