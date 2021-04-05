import os
import sys
import re
import urllib.request
import requests
import json
import lxml
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from collections import OrderedDict

from urllib.request import urlopen, Request
from fake_useragent import UserAgent

import pandas as pd

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from dateutil.parser import parse
import csv

from datetime import datetime

texts_article = []
time_zone = []
for i in range(0, 144):
    time_zone.append(str(i))
texts_comment = dict.fromkeys(time_zone, [])

texts_title = []
texts_url = []

page_url = [1]

commentss = ''


def crawling_url(url):
    global texts_url
    global page_url
    session = HTMLSession()
    res = session.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    urls = soup.find_all('a')
    for x in range(len(url)):
        if urls[x].text:
            check = urls[x]['href']
            if 'mid=sec' in check:
                if 'oid=' in check:
                    if 'news.naver.com' in check:
                        if 'aid=' in check:
                            if 'isYeonhapFlash=Y' in check:
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

    # return url


def crawling_url_cluster(url):
    global texts_url
    session = HTMLSession()
    res = session.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    urls = soup.find_all('a', attrs={'class': 'nclicks(cls_pol.clsart1)'})
    if urls:
        for x in range(len(urls)):
            if urls[x].text:
                texts_url.append(ursl[x]['href'])
    else:
        print("No such tag")

    # return url


def find_Maxpage(url):
    global page_url
    session = HTMLSession()
    res = session.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    urls = soup.find_all('a', attrs={'class': 'nclicks(fls.page)'})
    if urls:
        for x in range(len(urls)):
            check = urls[x].text
            if check != '다음':
                if check != '이전':
                    page_url.append(check)
            else:
                next_page = 'https://news.naver.com/main/list.nhn' + \
                    urls[x]['href']
                find_Maxpage(next_page)
    else:
        print("No such tag")

    # return url


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

    # return article


today = datetime.now().strftime('%Y%m%d')
find_Maxpage('https://news.naver.com/main/list.nhn?mode=LPOD&sid2=140&sid1=001&mid=sec&oid=001&isYeonhapFlash=Y&date={}&page=1'.format(today))
print(page_url)

for x in range(len(page_url)):
    crawling_url(
        'https://news.naver.com/main/list.nhn?mode=LPOD&sid2=140&sid1=001&mid=sec&oid=001&isYeonhapFlash=Y&date={}&page={}'.format(today, page_url[x]))

# today = datetime.now().strftime('%Y%m%d')
# find_Maxpage('https://news.naver.com/main/list.nhn?mode=LPOD&sid2=140&sid1=001&mid=sec&oid=001&isYeonhapFlash=Y&date=20210402&page=1')
# print(page_url)

# for x in range(len(page_url)):
#     crawling_url(
#         'https://news.naver.com/main/list.nhn?mode=LPOD&sid2=140&sid1=001&mid=sec&oid=001&isYeonhapFlash=Y&date=20210402&page={}'.format(page_url[x]))


texts_url = set(texts_url)
texts_url = list(texts_url)

# print("*********url 정보***********")
print(texts_url)
print(len(texts_url))


oid = []
aid = []
headers = []
com_url = []

for y in range(len(texts_url)):
    a = texts_url[y]
    oid.append(texts_url[y].split("oid=")[1].split("&")[0])
    aid.append(texts_url[y].split("aid=")[1].split("&is")[0])

useragent = UserAgent()

for x in range(len(texts_url)):
    comps_url = []
    for y in range(1, 19):
        comps_url.append("https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_politics_m1&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news" +
                         oid[x] + "%2C" + aid[x] + "&categoryId=&pageSize=100&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=" + str(y) + "&refresh=false&sort=FAVORITE")
    com_url.append(comps_url)
# print(com_url[0][1])

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
for v in range(len(texts_url)):
    for y in range(len(com_url[v])):
        # print("v:")
        # print(v)
        # print("Y:")
        # print(y)
        resp = urlopen(
            Request(com_url[v][y], headers=headers[v])).read().decode('utf-8')
        # print(resp)
        if not '"commentList":[]' in resp:
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
                    date_str = rank_json['result']['commentList'][w]['modTime']
                    dt = parse(date_str)
                    time_str = str(dt.time())

                    time = int(time_str.split(":")[0])
                    minute = int(time_str.split(":")[1])
                    key_timezone = int((60*time + minute)/10)
                    # print(key_timezone)

                    texts_comment[str(key_timezone)] = texts_comment[str(
                        key_timezone)] + [rank_json['result']['commentList'][w]['contents']]
                    # commentss = commentss + \
                    #     rank_json['result']['commentList'][w]['contents']
        else:
            break

num_values = []

for x in range(0, 144):
    num_values.append(len(texts_comment[str(x)]))
plt.bar(range(0, 144), num_values)
plt.show()


# for y in range(len(texts_url)):
#     crawling_article(texts_url[y])


# print("**********title************")
# print(texts_title)
# print("**********article**********")
# print(texts_article)

print("**********comments**********")

data1 = pd.DataFrame({str(0): texts_comment[str(0)]})
data2 = pd.DataFrame({str(1): texts_comment[str(1)]})

result = pd.concat([data1, data2], axis=1)

for x in range(0, 144):
    data = pd.DataFrame({str(x): texts_comment[str(x)]})
    result = pd.concat([result, data], axis=1)

current_csv = datetime.now().strftime('%Y%m%d%H%M')
result.to_csv('news_articles_{}_{}.csv'.format(
    current_csv, today), index=False, encoding='utf-8-sig')


wordcloud = WordCloud(font_path='C:\WINDOWS\FONTS\GULIM.TTC',
                      background_color='white').generate(str(texts_comment.values()))
plt.figure(figsize=(25, 25))
plt.imshow(wordcloud, interpolation='lanczos')
plt.axis('off')
plt.show()

# 댓글을 달 수 없는 기사는 크롤링 안됨(url 정보는 크롤링 되나 html코드가 일반 뉴스 코드와는 달라서 기사 본문이나 제목 크롤링 불가)
# 제목은 필요가 없으면 250~255 line 주석처리
