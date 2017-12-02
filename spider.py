from googleapiclient.discovery import build
import pprint
from bs4 import BeautifulSoup
import urllib2
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)
import sys
import bs4
import os

my_api_key = "AIzaSyBDwrrdkFcL8QEbQT-wqlm8DrEaG1IO1nk"
my_cse_id = "015303713816810430314:e1skftpzsik"
pytrends = TrendReq(hl='en-US', tz=360)

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

"""
get Artical from search_result
"""
"""
:param search_results: results returned by google_search func 
:return: list of artical urls
"""

def getArticalUrl(search_results):
    urls=[]
    for i in range(len(search_results)):
        urls.append(search_results[i]['pagemap']['metatags'][0]['og:url'])
    return urls

"""
get popularTrend searched by google
"""
"""
return: list of hot topics
return type: list
"""

def getPopularTrend():
    hot_names = pytrends.trending_searches()['title'].tolist()
    return hot_names

def getRelatedTopic(hot_names):
    all_related_list=[]
    while(len(all_related_list)<3000):
        for name in hot_names:
            key=[]
            key.append(name)
            pytrends.build_payload(key,cat=0, timeframe='today 5-y', geo='', gprop='news')
            related = pytrends.related_topics()[name]['title'].tolist()
            for relate_relate in related:
                relate_topic=[]
                relate_topic.append(relate_relate)
                pytrends.build_payload(relate_topic, cat=0, timeframe='today 5-y', geo='', gprop='news')
                if(pytrends.related_topics() is not None):
                    try:
                        if(pytrends.related_topics()[relate_relate] is not None):
                            relate_relate_list = pytrends.related_topics()[relate_relate]['title'].tolist()
                    except KeyError, TypeError:
                        relate_relate_list = []
                    for topic in relate_relate_list:
                        all_related_list.append(topic)
                        print("add topic"+" "+u''.join((topic)).encode('utf-8').strip())
                        print(len(all_related_list))
    return all_related_list
"""
write text to txt file
"""
"""
para topic, index: name the new txt file
para content: str needs to written to txt
return: list of hot topics
return type: list
"""

def write_to_txt(index,content):
    filename = 'txtfile' + str(index)
    text_file = open(filename, "w")
    text_file.write(content)
    text_file.close()
    return filename

def ifEnough20M(content):
    isEnough = False
    if(sys.getsizeof(content)>20000000):
        isEnough = True

def getString(name,num):
    newlist = []
    results = google_search(name, my_api_key, my_cse_id, num=num)
    urls = getArticalUrl(results)
    for url in urls:
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.find_all('p')
        for tag in tags:
            for content in tag.contents:
                if(isinstance(content,bs4.element.NavigableString)):
                    newlist.append(u''.join((content)).encode('utf-8').strip())
    string1 = ''.join(newlist)
    return string1
    print(sys.getsizeof(string1))



# results = google_search('movie star', my_api_key, my_cse_id, num=10)
# titles = getPopularTrend()
# print(titles)
# filename = write_to_txt('movie',1,'I love jack chen')
# current_size = os.path.getsize(filename)
# print(current_size < 20000000)


def main():
    trends = getPopularTrend()
    all_relate_topic = getRelatedTopic(trends)
    i=0
    while(i<101):
        for topic in all_relate_topic:
            print("Getting %s" %(topic))
            content = getString(topic,10)
            filename = write_to_txt(index=i,content=content)
            current_size = os.path.getsize(filename)
            print("Writing to %s \t CurrentSzie is %s" % (filename, str(current_size)))
            if(current_size > 20000000):
                i = i+1

if __name__ == '__main__':
        main()

