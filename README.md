# feeds2txt.py

## What is it?

Read some RSS feeds, output item titles, dates and URLs to text.  
Use it in crontab or pipe output to more or less.

## TODO

* ...

## Required Python modules

* configparser
* datetime
* dateutil
* feedparser
* sys

## History

* 2021-03-24: Initial release
* 2021-03-26: Upload to github
* 2021-04-01: Read feeds and parameters from .ini file
* 2021-04-01: Read .ini file name as argument
* 2021-04-04: Add lastseen option to avoid redisplaying already seen RSS items
* 2021-06-08: Add line dividers between feeds, like "NN = --", where NN is any text



 vim:ft=markdown
