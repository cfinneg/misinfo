import matplotlib.pyplot as plt
import requests
from lxml import html
from bs4 import BeautifulSoup
from textblob import TextBlob
import json
import datetime
import numpy as np
import re
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
for line in open('bernietweets.json', 'r'):
    tweets.append(json.loads(line))
count = 0
urls = []
dates = []
for tweet in tweets:
    if len(tweet['entities']['urls']) != 0: # if tweet has a link store it and the date
        if not ('twitter' in tweet['entities']['urls'][0]['expanded_url']): # filter out twitter links
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
for i in range(len(urls)):
     if i % 20 == 0:
        thinnames.append(urls[i])
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
for url in thinnames:
    try:
        page = requests.get(url)
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
            textarr.append('error')
    except:
        textarr.append('error')
countnormal = 0
counterror = 0
for text in textarr:
    if text == 'error' or text == '':
        counterror += 1
    countnormal += 1
percent = (counterror/countnormal)*100
formatperc = '{:.2f}'.format(percent)
print('ephemerality: ' + str(formatperc) + '%')