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
rreal_url = []
choreal_url = []

commentss = ''


def crawling_url(url):
    global rreal_url
    global choreal_url
    session = HTMLSession()
    res = session.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    url = soup.find_all('ul')
    for x in range(len(url)):
        r_url = url[x].find_all('li')
        for y in range(len(r_url)):
            real_url = r_url[y].find_all('a')
            for z in range(len(real_url)):
                check = real_url[z]['href']
                if 'https://news.naver.com' in check:
                    if 'sid1=100' in check:
                        rreal_url.append(check)
    rreal_url = set(rreal_url)

    print("******")
    print(rreal_url)
    print("*******")
    # if url:
    #     global texts_url

    #     for x in range(len(url)):
    #         texts_url.append(url[x]['a']['href'])

    # else:
    #     print("No such tag")

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
crawling_url('https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=100')


print("*********url 정보***********")
print(texts_url)

oid = []
aid = []
page = 1
headers = []
comments = []
com_url = []

for y in range(len(texts_url)):
    oid.append(texts_url[y].split("oid=")[1].split("&")[0])
    aid.append(texts_url[y].split("aid=")[1])

useragent = UserAgent()

for v in range(len(texts_url)):
    headers.append({
        'referer': texts_url[v],
        'User-Agent': useragent.chrome
    })
for x in range(len(texts_url)):
    com_url.append("https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news" + oid[x] + "%2C" + aid[x] + "&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=" + str(
        page) + "&refresh=false&sort=FAVORITE")

for y in range(len(texts_url)):
    resp = urlopen(
        Request(com_url[y], headers=headers[y])).read().decode('utf-8')
    x = 0
    while(resp[x] != '{'):
        x += 1
    # print(response[x:])

    z = len(resp)-1
    while(resp[z] != '}'):
        z -= 1
    # print(response[x:y]+'}')

    rank_json = json.loads(resp[x:z]+'}')
    for w in range(len(rank_json['result']['commentList'])):
        texts_comment.append(rank_json['result']['commentList'][w]['contents'])
        commentss = commentss + \
            rank_json['result']['commentList'][w]['contents']

for y in range(len(texts_url)):
    crawling_article(texts_url[y])


print("**********title************")
print(texts_title)
print("**********article**********")
print(texts_article)
print("**********comments**********")
print(texts_comment)
