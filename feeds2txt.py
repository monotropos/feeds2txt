#!/usr/bin/python3

import feedparser
from datetime import datetime
from dateutil import parser
from configparser import ConfigParser
from ast import literal_eval
import sys

# Allow insecure connections to sites (especially after letsencrypt fiasco)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


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
    print("Last update: " + parameters["lastseen"])
except (KeyError, NameError):
    lastseen = datetime.now().timestamp() - time2show

try:
    delimiter_item = literal_eval(parameters["delimiter_item"])
except (KeyError, NameError):
    delimiter_item = ""

try:
    delimiter_section = literal_eval(parameters["delimiter_section"])
except (KeyError, NameError):
    delimiter_section = ""


allheadlines = []
printheadlines = []

# Iterate over the allheadlines list and print each headline
if len(newsurls):
    for key, url in newsurls.items():
        # When url is "--" just print a line divider
        if url == "--":
            print("#", "»"*20, key, "«"*(40-len(key)))
            # print("#", key)
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
                # printheadlines.append("» " + hl["title"].replace("&#039;", "’")
                #                       + " — " + pdate + "\n\t" + hl["link"])
                printheadlines.append(hl["title"].replace("&#039;", "’")
                                      + " — " + pdate + "\n→ " + hl["link"])

        if len(printheadlines) > 0:
            # print(f">> ––– {key} "+"-"*20)
            print(f"## {key}")
            for hl in printheadlines:
                print(hl + delimiter_item)
            print(delimiter_section)

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
