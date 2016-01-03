# Twitter Analysis
A short script for parsing and analyzing tweets by location with the twitter API. No effort has been made to correct for the sampling biases that are introduced when you work with Twitter data; this is just for my own entertainment. It's very much a work in progress and you're probably better off starting with the tutorials mentioned below - though maybe the ideas about leveraging census databases are helpful. 

To scrape tweets tweets, check out [this great tutorial](http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/) and [this great tutorial](http://adilmoujahid.com/posts/2014/07/twitter-analytics/).

## Usage
1. In build_dataset.py, set the path to a directory for tables and put the following in it:  

   NST-EST2014-01.csv: Population by state (US)  
      https://www.census.gov/popest/data/state/totals/2014/tables/NST-EST2014-01.csv  
   POP_PLACES_20151201.txt: Database of populated places  
      http://geonames.usgs.gov/domestic/download_data.htm  

2. Set up output directory. In the output directory, make subdirectories tweets and analysis. Store your raw tweets in tweets. Output will be written to analyis. You're not allowed to publish tweets so be sure to keep your data and your src separate. 
