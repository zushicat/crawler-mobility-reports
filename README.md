# crawler-mobility-reports
Get mobility data from different sources.

Get mobility data of various granularity from following sources:
- Apple
- Google
- teralytics / RKI

All crawled files are csv files.    

Please keep in mind: All sources lag behind to various degrees (from a few up to several days).    

## Data
### Apple Mobilitytrends
Source: https://www.apple.com/covid19/mobility    

International (partially) incl. granularity down to city level    

Analysis of the requests to their map service and distinction between:
- driving
- Walking
- transit


### Google Mobility Report
Source: https://www.google.com/covid19/mobility/    
Documentation: https://www.google.com/covid19/mobility/data_documentation.html?hl=en

International and state level       

Analysis of Google Location History (see documentation) and distinction between:
- retail and recreation
- grocery and pharmacy
- parks
- transit stations
- workplaces
- residential


### teralytics / RKI
Source: https://rki.mobility-covid19.teralytics.net/    

This data (analyzed and aggregated by the company Teralytics) is use by COVID-19 MOBILTY PROJECT:    
https://www.covid-19-mobility.org/mobility-monitor/ (res.: http://rocs.hu-berlin.de/covid-19-mobility/de/mobility-monitor)    

Documentation: https://www.covid-19-mobility.org/data-info/ (see also: https://www.teralytics.net/mobility-and-covid-19/)

German cities down to neighbourhood/district level

Analysis of mobility flow data of mobile phones with no distinction.


#### Due to copyright reasons there is no crawled data available in this repo.


## Usage
### Install
Change into cloned/downloaded repo and install environment:
```
$ pipenv install
```

Then change into environment:
```
$ pipenv shell
````
(You can leave the shell with "exit".)



### Crawl sources
Call main request script to crawl all sources:
```
$ python request_data.py
```

Or call script with additional flag:
```
  Request sources by options

Options:
  --all     Request all sources
  --apple   Request Apple
  --google  Request Google
  --rki     Request RIK
  --help    Show this message and exit.
```

A new directory in /data will be created, named by current date, where the crawled csv files will be saved.
