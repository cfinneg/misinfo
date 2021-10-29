import matplotlib.pyplot as plt
import matplotlib
import requests
from lxml import html
from bs4 import BeautifulSoup
from textblob import TextBlob
import json
from datetime import datetime
import numpy as np
import re
import time
from matplotlib.dates import (YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange)
def monthToNum(shortMonth):
    return {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9, 
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
    }[shortMonth]
tweets = []
for line in open('tuckertweets.json', 'r'):
    tweets.append(json.loads(line))
count = 0
urls = []
dates = []
for tweet in tweets:
    if len(tweet['entities']['urls']) != 0: # if tweet has a link store it and the date
        if not ('twitter' in tweet['entities']['urls'][0]['expanded_url']): # filter out twitter links
            if not ('youtube' in tweet['entities']['urls'][0]['expanded_url']): # filter out youtube links
                if not ('youtu.be' in tweet['entities']['urls'][0]['expanded_url']): # filter out youtube links
                    if not ('tiktok' in tweet['entities']['urls'][0]['expanded_url']): # filter out tiktok links
                        if not ('vimeo' in tweet['entities']['urls'][0]['expanded_url']): # filter out vimeo links
                            urls.append(tweet['entities']['urls'][0]['expanded_url'])
                            dates.append(tweet['created_at'])
# for url in urls:
#     print(url)
# formatteddates = []
# for date in dates:
#     splitdate = date.split(' ')
#     formatteddates.append(splitdate[5])

# thin some urls out
thinnames = []
thindates = []
for i in range(len(urls)):
     if i % 5 == 0:
        thinnames.append(urls[i])
        thindates.append(dates[i])
# # random ys
# s = np.random.rand(len(thin))
# plt.plot(list(reversed(thin)),s,'bo')
# p = 0
# for x, y in zip(list(reversed(thin)),s):
#     label = thinnames[p]
#     plt.annotate(label, (x,y), textcoords='offset points', xytext=(0,10),ha ='center')
#     p += 1
# plt.show()
# TODO:
# next grab html from the links and get sentiment analysis on article titles
# for i in range(len(urls)):
#     # make sure our links are accessible
#     try:
#         page = requests.get(urls[i])
#         print(page.status_code)
#     except:
#         print('bad link')
#     # tree = html.fromstring(page.content)
#     # articletitle = tree.xpath('/html/body/div[2]/div/div/section/article/header/h1/text()')
#     # print(articletitle)
textarr = []
badurls = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
for url in thinnames:
    time.sleep(1)
    try:
        print(url)
        page = requests.get(url, headers=headers)
        print(page.status_code)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            plist = soup.find_all('p')
            pattern = '<.*?>'
            toadd = ''
            for p in plist:
                strung = str(p)
                substring = re.sub(pattern,' ',strung)
                toadd += substring
            textarr.append(toadd)
        else: 
            badurls.append(url)
            textarr.append('error')
            # textarr.append('error: ' + str(page.status_code))
    except:
        badurls.append(url)
        textarr.append('error')
countnormal = 0
counterror = 0
for text in textarr:
    if 'error' in text or text == '':
        counterror += 1
    countnormal += 1
percent = (counterror/countnormal)*100
formatperc = '{:.2f}'.format(percent)
print('ephemerality: ' + str(formatperc) + '%')
dateformat = '%a %b %d %X %z %Y'
fdates = []
for dt in thindates:
    fdates.append(datetime.strptime(dt,dateformat))
datesfinal = matplotlib.dates.date2num(fdates)
values = []
for text in textarr:
    if text == 'error':
        values.append(-1)
    else:
        val = 1
        if 'vaccine' in text:
            val+= 1
        values.append(val)
for text in textarr:
    print(text)
plt.plot_date(datesfinal,values)
plt.gcf().autofmt_xdate()
plt.show(block=True)