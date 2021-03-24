# from pprint import pprint
# from datetime import datetime
# import time
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import pickle

# url = "https://openapi.naver.com/v1/search/news.json?query={}"

# keyword = input('검색 키워드:')

# headers = {
#     'X-Naver-Client-Id': "6s9vEfhgOSkIWBuO28e_",
#     'X-Naver-Client-Secret': "6B_vwqD7eP"
# }

# res = requests.get(url.format(keyword), headers=headers)
# if res.status_code == 200:
#     datas = res.json()
#     print('총 검색 건수 : ', datas['total'])
#     print(type(datas), type(datas['items']))

#     df = pd.DataFrame(datas['items'])
#     df.to_csv('naver_{}_검색결과.csv'.format(keyword),
#               encoding='utf-8', index=False)


# def get_naver_news_search(keyword, start=1, display=30):
#     base_url = "https://openapi.naver.com/v1/search/news.json?query={}&start={}&display={}"
#     news_links = []

#     while start <= 1000:
#         url = base_url.format(keyword, start, display)
#         res = requests.get(url, headers=headers)
#         if res.status_code == 200:
#             result = res.json()
#             items = result['items']

#             for item in items:
#                 link = item['link']
#                 if 'news.naver.com' in link:
#                     news_link.append(link)
#             start = start + display
#             time.sleep(0.15)
#     else:
#         raise Exception('검색 실패 : {}'.format(res.status_code))

#     curr = datetime.now().strftime('%Y-%m-%d')
#     filename = '네이버뉴스검색.pkl'.format(keyword, curr)
#     with open(filename, 'wb') as f:
#         pickle.dump(news_links, f)


# print('error_cnt: {}'.format(error_cnt))
# df = pd.DataFrame(result, columns=['기사제목', '입력일', '기사내용'])
# df.to_csv('news_articles.csv', index=False, encoding='utf-8')


# crawling(urllib.request.)


# def get_naver_news(url):
#     res = requests.get(url)

#     if(rescode == 200):
#         #response_body = response.read()
#         # print(response_body.decode('utf-8'))
#         soup = BeautifulSoup(res.text)
#         title = soup.select_one('h3#articleTitle').text.strip()
#         input_date = soup.select_one('span.t11').text.strip()
#         article = soup.select_one('div#articleBodyContents').text.strip()
#         article = article.replace

#         return title, input_date, article
#     else:
#         raise Exception("요청 실패 : {}".format(res.status_code))


# with open('네이버뉴스검색_오세훈_2021-03-24.pkl', 'rb') as f:
#     l = pickle.load(f)
# result = []
# error_cnt = 0
# for url in l:
#     try:
#         info = get_naver_news(url)
#         result.append(info)
#     except:
#         error_cnt += 1

# print('error_cnt: {}'.format(error_cnt))
# df = pd.DataFrame(result, columns=['기사제목', '입력일', '기사내용'])
# df.to_csv('news_articles.csv', index=False, encoding='utf-8')

import os
import sys
import urllib.request
import requests
import json
import lxml
from requests_html import HTMLSession
from bs4 import BeautifulSoup

#from konlpy.tag import Twitter
from konlpy.tag import Okt
from collections import Counter

common = []


def keyword_extractor(tagger, text):
    tokens = tagger.phrases(text)
    tokens = [token for token in tokens if len(token) > 1]  # 한 글자인 단어는 제외
    count_dict = [(token, text.count(token)) for token in tokens]
    ranked_words = sorted(count_dict, key=lambda x: x[1], reverse=True)[:10]
    return [keyword for keyword, freq in ranked_words]


def crawling(url):
    # res = requests.get(url)
    session = HTMLSession()
    res = session.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    article = soup.find('div', attrs={'id': 'articleBodyContents'})
    if article:
        # twit = Twitter()
        # print(keyword_extractor(twit, article.text))

        okt = Okt()
        noun = okt.nouns(article.text)
        count = Counter(noun)

        noun_list = count.most_common(100)
        common.append(noun_list)
        for v in noun_list:
            print(v)

        print(article.text)
    else:
        print("No such tag")

    return article


def crawlings(url):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')
    article = soup.find('div', attrs={'id': 'articleBodyContents'})
    print(article.text)
    return article


def get_naver_news(url):
    res = requests.get(url)

    if(rescode == 200):
        # response_body = response.read()
        # print(response_body.decode('utf-8'))
        soup = BeautifulSoup(res.text)
        title = soup.select_one('h3#articleTitle').text.strip()
        input_date = soup.select_one('span.t11').text.strip()
        article = soup.select_one('div#articleBodyContents').text.strip()
        article = article.replace

        return title, input_date, article
    else:
        raise Exception("요청 실패 : {}".format(res.status_code))


client_id = "6s9vEfhgOSkIWBuO28e_"
client_secret = "6B_vwqD7eP"

start = 1
display = 3

s_url = []

encText = urllib.parse.quote("오세훈")
# base_url = "https://openapi.naver.com/v1/search/news.json?query={}&start={}&display={}"
# url = base_url.format(keyword, start, display)
base_url = "https://openapi.naver.com/v1/search/news?query={}&start={}&display={}"  # json 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
url = base_url.format(encText, start, display)
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode == 200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

print("**")

urls = []

text_data = response_body.decode('utf-8')
json_data = json.loads(text_data)

for x in json_data['items']:
    urls.append(x['link'])
print(urls)


for y in range(len(urls)):
    crawling(urls[y])

print(common[0])

# for z in range(len(common)):
#     print(common[z])

# for y in urls:
#     crawling(y)


# for x in json_data['items']:
#     result = re.sub('<.+?>', '', x['title'], 0, re.I | re.S)
#     print(result)


# response_body = response.read().decode('utf-8')
# with open("crawledq.json", 'w') as json_file:
#     a = json.dump(response_body, json_file)

# with open('crawledq.json', 'rb') as f:
#     l = json.load(f)
# result = []
# error_cnt = 0
# for url in l:
#     try:
#         info = get_naver_news(url)
#         result.append(info)
#     except:
#         error_cnt += 1
# print('error_cnt: {}'.format(error_cnt))
# df = pd.DataFrame(result, columns=['기사제목', '입력일', '기사내용'])
# df.to_csv('news_articles.csv', index=False, encoding='utf-8')
