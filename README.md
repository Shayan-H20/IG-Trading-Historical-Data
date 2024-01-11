A Python wrapper for extracting historical data in a quota-efficient way from IG's Trading API (can specify a daily time range for data gathering).

### Slightly more detailed description
This is a quota-efficient method of extracting data as can extract data between the hours of for example 13:00-16:00 on specified days of the week. This is instead of the default action of gathering all 24H of data for every single day of the week (given availability) which consumes increased quota allowance.

*- Quickstart Guide Further Below -*

### Output Format

Data outputted is in the form of a *pandas.DataFrame* with the following columns:
* lastTradedVolume

* openPxMid
* highPxMid
* lowPxMid
* closePxMid

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
* Only data in this specified range is fetched, hence **saving your quota**:

> Example:
> * We are interested only in gathering data for Wednesdays and Fridays
> * We are also interested only in data between the hours of 13:00-16:00
> * We want HOURLY data during this time period and days from date X to date Y
> ---
> * Using this package we can get exactly what we want (conserving significant amounts of quota)
> * Using other packages (found so far), you would get data for EVERY day of the week and EVERY hour of the day (where data is available) between dates X and Y

# Quickstart

Install using pip:

```
pip install ig_trading_historical_data
```

Prepare a 'user_info.py' file (storage of sensitive information) in your projects directory with the following code:

```python
# DEMO ACCOUNT DETAILS
username = 'example username'
pw = 'example pw'
api_key = 'example api key'
```

Create your main file (i.e. 'quickstart.py') and use the following code:

```python
<!-- include: quickstart.py -->
```