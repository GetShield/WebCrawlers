# Product Summary

WebCrawlers
https://github.com/GetShield/WebCrawlers

## Major Features
- 1. twitter crawler
crawl phishing domains form twitter

- 2. google crawler
craw ad domain from google by keywords

## Running the Product
1. cd WebCrawler
2. source ./venv/bin/activate
3. pip3 install -r requirements.txt
4. add your API KEY in .env
5. nohup python3 -u twitter.py  > twitter.log 2>&1 &
5. nohup python3 -u gsearch.py  > gsearch.log 2>&1 &

## Feature 1
- 1. mintSimulation
### Description
Simulate expected outcome of any blockchain contract
### Components
- twitter crawler
https://github.com/GetShield/WebCrawlers/tree/feat/tweepy
- google crawler
https://github.com/GetShield/WebCrawlers/tree/feat/googleAd
 
### Notes
- Any additional notes or considerations that developers should be aware of when working on this feature.

### References
- Any relevant references or external resources that were used in the development of the feature.
