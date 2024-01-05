A Python wrapper for extracting historical data (given also a daily time range) from IG's Trading API. This is a quota-efficient method of extracting data (as can extract data between the hours of for example 13:00-16:00 on specified days of the week).

### Output Format

Data outputted is in the form of a *pandas.DataFrame* with the following columns:
* openPxMid
* highPxMid
* lowPxMid
* closePxMid

* lastTradedVolume

* openPxBid
* highPxBid
* lowPxBid
* closePxBid

* openPxAsk
* highPxAsk
* lowPxAsk
* closePxAsk

* openPxSpread
* highPxSpread
* lowPxSpread
* closePxSpread

### Differences with other packages

The difference between this package and others found so far is the following:
* Given that each user has a **limited weekly quota for downloading historical data**, this package allows you to select a **time range** of interest during **whichever days of the week are of interest** (example below)
* Only data in this specified range is fetched, hence **saving your quota**

> Example:
> * We are interested only in gathering data for Wednesdays and Fridays
> * We are also interested only in data between the hours of 13:00-16:00
> * We want HOURLY data during this time period and days from date X to date Y

> * Using this package we can get exactly what we want (conserving significant amounts of quota)
> * Using other packages, you would get data for EVERY day of the week and EVERY hour of the day (where data is available) between dates X and Y

# Quickstart




