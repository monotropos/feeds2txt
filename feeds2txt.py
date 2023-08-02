#!/usr/bin/python3

import feedparser
from time import strftime, localtime
from datetime import datetime
from dateutil import parser
from configparser import ConfigParser
import sys

# Allow insecure connections to sites (especially after letsencrypt fiasco)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# define delimiters
CHAR_ABOVE_TITLE = "."
CHAR_BELOW_TITLE = "^"
CHAR_BELOW_SECTION = "–"
CHAR_BELOW_FEED = "—"
DELIMITER_ITEM = "\n"


# Function to print separator lines
def sep_line(start, character, n):
    print(start, character*n)


# Function grabs the rss feed headlines (titles) and returns them as a list
def getHeadlines(rss_url):
    headlines = []
    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        print(e)
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
parameters = config_object["PARAMETERS"]

try:
    newsurls = config_object["FEEDS"]
except KeyError:
    newsurls = []

try:
    time2show = int(parameters["time2show"])
except (KeyError, NameError):
    time2show = 86400

try:
    lastseen = float(parameters["lastseen"])
    t = strftime('%Y-%m-%d %H:%M:%S', localtime(lastseen))
    print("Last update:" + t + " (" + parameters["lastseen"] + ")")
except (KeyError, NameError):
    lastseen = datetime.now().timestamp() - time2show


allheadlines = []
printheadlines = []

# Iterate over the allheadlines list and print each headline
if len(newsurls):
    for key, url in newsurls.items():
        # When url is "--" just print a line divider
        if url == "--":
            sep_line("#", CHAR_ABOVE_TITLE, 58)
            print("#", "»"*20, key, "«"*(36-len(key)))
            sep_line("#", CHAR_BELOW_TITLE, 58)
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
                title = hl["title"].replace("&#039;", "’").replace("&#x27;", "’").replace("&quot;", '”')
                title = title.replace("&#x2f;", "&").replace("&amp;", "&")        # must be the last replace
                printheadlines.append("### " + title + " — " + pdate + "\n### " + hl["link"])

        if len(printheadlines) > 0:
            print(f"## {key}")
            sep_line("##", CHAR_BELOW_FEED, 57)
            for hl in printheadlines:
                print(hl + DELIMITER_ITEM)
            sep_line("", CHAR_BELOW_SECTION, 59)

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
