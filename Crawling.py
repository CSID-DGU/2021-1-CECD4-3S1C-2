import os
import sys
import re
import urllib.request
import requests
import json
import lxml
from requests_html import HTMLSession
from bs4 import BeautifulSoup

#from konlpy.tag import Twitter
from konlpy.tag import Okt
from collections import Counter

from urllib.request import urlopen, Request
from fake_useragent import UserAgent

common = []

List = []

texts_article = ''
texts_comment = ''
texts_title = ''

# https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1124024323657751380678_1616590122616&lang=ko&country=KR&objectId=news008%2C0004562103&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=1&initialize=true&userType=&useAltSort=true&replyPageSize=20&sort=new&includeAllStatus=true&_=1616590122617


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
    title = soup.find('h3', attrs={'id': 'articleTitle'})
    # comment = soup.find('span', attrs={'class': 'u_cbox_contents'})
    if article:
        # twit = Twitter()
        # print(keyword_extractor(twit, article.text))

        # okt = Okt()
        # noun = okt.nouns(article.text)
        # count = Counter(noun)

        # noun_list = count.most_common(100)
        # common.append(noun_list)
        # for v in noun_list:
        #     print(v)
        # for i in len(comment):
        #     print(comment[i].text)
        global texts_article
        global texts_title
        texts_article = texts_article + article.text
        texts_title = texts_title + title.text + '\n'

        # print(article.text)
    else:
        print("No such tag")

    return article


def crawlings(url):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')
    comment = soup.find_all('span', attrs={'class': 'u_cbox_contents'})
    if comment:
        for i in len(comment):
            print(comment[i].text)
    else:
        print("No such tag")
    return comment


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
display = 5

s_url = []

encText = urllib.parse.quote("삼성")
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
    # print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

urls = []

text_data = response_body.decode('utf-8')
json_data = json.loads(text_data)

for x in json_data['items']:
    link = x['link']
    if 'news.naver.com' in link:
        urls.append(link)

print("*********url 정보***********")
print(urls)

oid = []
aid = []
page = 1
headers = []
comments = []
com_url = []
# rank_json = []

for y in range(len(urls)):
    oid.append(urls[y].split("oid=")[1].split("&")[0])
    aid.append(urls[y].split("aid=")[1])

useragent = UserAgent()

for v in range(len(urls)):
    headers.append({
        'referer': urls[v],
        'User-Agent': useragent.chrome
    })
for x in range(len(urls)):
    com_url.append("https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news" + oid[x] + "%2C" + aid[x] + "&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=" + str(
        page) + "&refresh=false&sort=FAVORITE")

for y in range(len(urls)):
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
        texts_comment = texts_comment + \
            rank_json['result']['commentList'][w]['contents']
        # print(rank_json['result']['commentList'][w]['contents'])

for y in range(len(urls)):
    crawling(urls[y])

# print(common[0])

print("**********title************")
print(texts_title)
print("**********article**********")
print(texts_article)
print("**********comments**********")
print(texts_comment)
print("\n\n")

okt1 = Okt()
okt2 = Okt()
noun_article = okt1.nouns(texts_article)
count_article = Counter(noun_article)

print("*******article word frequency***********")

article_list = count_article.most_common(150)
for v in article_list:
    print(v)

print("*******comment word frequency***********")

noun_comment = okt2.nouns(texts_comment)
count_comment = Counter(noun_comment)

comment_list = count_comment.most_common(150)
for v in comment_list:
    print(v)
