import os
import sys
import re
import urllib.request
import requests
import json
import lxml
from requests_html import HTMLSession
from bs4 import BeautifulSoup

# from konlpy.tag import Twitter
from konlpy.tag import Okt
from collections import Counter

from urllib.request import urlopen, Request
from fake_useragent import UserAgent

import pandas as pd

from wordcloud import WordCloud
import matplotlib.pyplot as plt

common = []

List = []

texts_article = []
texts_comment = []
texts_title = []
texts_url = []

commentss = ''


def crawling_url(url):
    global texts_url
    session = HTMLSession()
    res = session.get(url)
# https://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=001&aid=0012295158&isYeonhapFlash=Y&rc=N
# https://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=001&aid=0012295158&isYeonhapFlash=Y&rc=N
# https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=586&aid=0000022599
    soup = BeautifulSoup(res.content, 'html.parser')
    url = soup.find_all('a')
    for x in range(len(url)):
        if url[x].text:
            check = url[x]['href']
            if 'mid=sec' in check:
                if 'oid=' in check:
                    if 'news.naver.com' in check:
                        if 'aid=' in check:
                            texts_url.append(check)
                    # else:
                    #     if '/main/clusterArticles' in check:
                    #         temp_url = 'https://news.naver.com' + check
                    #         crawling_url_cluster(temp_url)
                    #     else:
                    #         temp_url = 'https://news.naver.com' + check
                    #         texts_url.append(temp_url)
    # url = soup.find_all('ul')
    # for x in range(len(url)):
    #     r_url = url[x].find_all('li')
    #     for y in range(len(r_url)):
    #         real_url = r_url[y].find_all('a')
    #         for z in range(len(real_url)):
    #             check = real_url[z]['href']
    #             if 'sid1=100' in check:
    #                 if 'oid=' in check:
    #                     if 'news.naver.com' in check:
    #                         texts_url.append(check)
    #                     else:
    #                         if '/main/clusterArticles' in check:
    #                             print("cluster_haha")
    #                             temp_url = 'https://news.naver.com'+check
    #                             crawling_url_cluster(temp_url)
    #                         else:
    #                             temp_url = 'https://news.naver.com'+check
    #                             texts_url.append(temp_url)

    return url


def crawling_url_cluster(url):
    global texts_url
    session = HTMLSession()
    res = session.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    url = soup.find_all('a', attrs={'class': 'nclicks(cls_pol.clsart1)'})
    if url:
        for x in range(len(url)):
            if url[x].text:
                texts_url.append(url[x]['href'])
    else:
        print("No such tag")

    return url


def crawling_article(url):
    session = HTMLSession()
    res = session.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    article = soup.find('div', attrs={'id': 'articleBodyContents'})
    title = soup.find('h3', attrs={'id': 'articleTitle'})
    if article:
        global texts_article
        global texts_title

        texts_title.append(title.text)
        texts_article.append(article.text)
    else:
        print("No such tag")

    return article


# crawling_url('https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001')
# crawling_url('https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=100')
crawling_url(
    'https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&sid1=001&sid2=140&oid=001&isYeonhapFlash=Y')
# for x in range(2, 5):
#     crawling_url('https://news.naver.com/main/list.nhn?mode=LPOD&sid2=140&sid1=001&mid=sec&oid=001&isYeonhapFlash=Y&date=20210330&page={}'.format(x))

# for x in range(2, 5):
#     crawling_url(
#         'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page={}'.format(x))


texts_url = set(texts_url)
texts_url = list(texts_url)

# print("*********url 정보***********")
print(texts_url)
print(len(texts_url))


oid = []
aid = []
page = 1
headers = []
comments = []
com_url = []

for y in range(len(texts_url)):
    a = texts_url[y]
    oid.append(texts_url[y].split("oid=")[1].split("&")[0])
    aid.append(texts_url[y].split("aid=")[1].split("&is")[0])

useragent = UserAgent()

for x in range(len(texts_url)):
    comps_url = []
    for y in range(1, 3):
        comps_url.append("https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_politics_m1&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news" +
                         oid[x] + "%2C" + aid[x] + "&categoryId=&pageSize=100&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=" + str(y) + "&refresh=false&sort=FAVORITE")
    com_url.append(comps_url)
print(com_url[0][1])

for v in range(len(texts_url)):
    headers.append({
        'referer': texts_url[v],
        'User-Agent': useragent.chrome
    })
    # headerL = []
    # for z in range(len(com_url)):
    #     headerL.append({
    #         'referer': texts_url[v],
    #         'User-Agent': useragent.chrome
    #     })
    # headers.append(headerL)
e = 0
for v in range(len(texts_url)):
    for y in range(len(com_url[v])):
        # print("v:")
        # print(v)
        # print("Y:")
        # print(y)
        resp = urlopen(
            Request(com_url[v][y], headers=headers[v])).read().decode('utf-8')
        if resp:
            x = 0
            while(resp[x] != '{'):
                x += 1
            # print(response[x:])

            z = len(resp)-1
            while(resp[z] != '}'):
                z -= 1
            # print(response[x:y]+'}')

            rank_json = json.loads(resp[x:z]+'}')
            if rank_json['result']['commentList']:
                for w in range(len(rank_json['result']['commentList'])):
                    texts_comment.append(
                        rank_json['result']['commentList'][w]['contents'])
                    # commentss = commentss + \
                    #     rank_json['result']['commentList'][w]['contents']

# for y in range(len(texts_url)):
#     crawling_article(texts_url[y])


# print("**********title************")
# print(texts_title)
# print("**********article**********")
# print(texts_article)
print("**********comments**********")
texts_comment = set(texts_comment)
# print(texts_comment)
print(texts_comment)
print(len(texts_comment))

data = pd.DataFrame(texts_comment)

data.to_csv('news_articles_10.csv',
            index=False, encoding='utf-8-sig')
# data_read = pd.read_csv('news_articles_10.csv', header=None)
# print(data_read)

# haha test

wordcloud = WordCloud(font_path='C:\WINDOWS\FONTS\GULIM.TTC',
                      background_color='white').generate(str(texts_comment))
plt.figure(figsize=(25, 25))
plt.imshow(wordcloud, interpolation='lanczos')
plt.axis('off')
plt.show()
