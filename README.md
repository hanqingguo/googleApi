# googleApi

This project Analyze Google trend hot topics and show most frequency words of related News.

The spider.py collect all hottest topics and related topics, then put those topics to google search api,

get all articals urls related those topics, use beautiful soup to parse words and save into 100 .txt file, each of them larger than 20MB.

  [Google Trend Api](#google-trend-api)
  
  [Google Search Api](#google-search-api)
  
  [Hadoop](#hadoop)
  
  [wordCloud](#WordCloud)
  

## Google Trend Api

## Introduction

Unofficial API for Google Trends, Use Google Trend Api get hottest topics.

[Installation](#installation)

[API](#api)


## Installation

    pip install pytrends


## API

### Connect to Google

    from pytrends.request import TrendReq

    pytrends = TrendReq(hl='en-US', tz=360)


### Get Hottest topics

	hot_names = pytrends.trending_searches()

### Get Related topics
	
	for name in hot_names:
		kw_list = name
		pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
		related = pytrends.related_topics()[name]['title'].tolist()
		print(related)


## Google Search Api

## Introduction

Use this api get result of googled words.

[Installation](#installation)

[API](#api)

## Installation

	pip install --upgrade google-api-python-client

## API

Build a Customer Google search Engine, then get api key and cse id.

search_term is what we want to search. Here my search engine only search articals.

	from googleapiclient.discovery import build
	
	my_api_key = "AIzaSyBDwrrdkFcL8QEbQT-wqlm8DrEaG1IO1nk"
	my_cse_id = "015303713816810430314:e1skftpzsik"
	"""
	Build custom google search api
	"""
	"""
	:param search_term: name of what you want to search 
	:type search_term: str
	"""

	def google_search(search_term, api_key, cse_id, **kwargs):
	    service = build("customsearch", "v1", developerKey=api_key)
	    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
	    return res['items']
	    
	google_search("中国",my_api_key,my_cse_id)
	
	
### Use function below to get all urls of articals
	
	def getArticalUrl(search_results):
    	    urls=[]
	    for i in range(len(search_results)):
		if('metatags' in search_results[i]['pagemap'].keys()):
		    if('og:url' in search_results[i]['pagemap']['metatags'][0].keys()):
			urls.append(search_results[i]['pagemap']['metatags'][0]['og:url'])
	    return urls

