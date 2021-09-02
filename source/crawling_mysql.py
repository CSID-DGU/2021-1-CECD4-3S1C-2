import json
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from urllib.request import urlopen, Request
from fake_useragent import UserAgent

from dateutil.parser import parse
from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pymysql

from dateutil.parser import parse


# * 셀레니움 옵션 
options = webdriver.ChromeOptions()
# options.add_argument('headless')

ua = UserAgent(verify_ssl=False)
userAgents = ua.random

options = Options()
# options.add_argument('headless')
options.add_argument(f'user-agent={userAgents}')
driver = webdriver.Chrome(
    options=options, executable_path=r'크롬드라이버 경로')
# 봇탐지 우회


# 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
driver.implicitly_wait(3)
time.sleep(3)


#* 뉴스 본문 기사 추출 Array, 하지만 본문기사를 디비에 넣지 않음
texts_article = []

#* 기존 댓글작성 시계열 자료 배열, 현 모듈에서는 사용 안함 
time_zone = []
for i in range(0, 144):
    time_zone.append(str(i))
texts_comment = dict.fromkeys(time_zone, [])

texts_url = []

page_url = [1]


#* 크롤링할 뉴스 기사의 url 수집 
def crawling_url(url):
    global texts_url
    global page_url
    session = HTMLSession()
    res = session.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    urls = soup.find_all('a')
    for x in range(len(urls)):
        if urls[x].text:
            check = urls[x]['href']
            if 'mid=sec' in check:
                if 'oid=' in check:
                    if 'news.naver.com' in check:
                        if 'aid=' in check:
                            if 'isYeonhapFlash=Y' in check:
                                texts_url.append(check)  

#* 연합뉴스 페이지가 몇 페이지 까지 있는지 확인
def find_Maxpage(url, a):
    global page_url
    session = HTMLSession()
    res = session.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    urls = soup.find_all('a', attrs={'class': 'nclicks(fls.page)'})
    if a > 0:
        page_url.append(a*10+1)
    if urls:
        for x in range(len(urls)):
            check = urls[x].text
            if check != '다음':
                if check != '이전':
                    page_url.append(check)
            else:
                a = a+1
                next_page = 'https://news.naver.com/main/list.nhn' + \
                    urls[x]['href']
                find_Maxpage(next_page, a)
    else:
        print("No such tag")


#* 뉴스기사 본문을 크롤링. Database에는 저장 안함.(사용 안함)
def crawling_article(url):
    session = HTMLSession()
    res = session.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    article = soup.find('div', attrs={'id': 'articleBodyContents'})    
    if article:
        global texts_article
        texts_article.append(article.text)
    else:
        print("No such tag, article")

#* 뉴스기사의 제목을 크롤링
def crawling_title(url):
    session = HTMLSession()
    res = session.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    article = soup.find('div', attrs={'id': 'articleBodyContents'})
    title = soup.find('h3', attrs={'id': 'articleTitle'})
    if article:
        return title.text
    else:
        return "No such tag, title"

#* 뉴스 댓글 api의 resoponse를 json 형식으로 바꿈.
def getJson_NewsInfo(resp):
    x = 0
    while(resp[x] != '{'):
        x += 1
     # print(response[x:])

    z = len(resp)-1
    while(resp[z] != '}'):
        z -= 1
    # print(response[x:y]+'}')

    rank_json = json.loads(resp[x:z]+'}')

    return rank_json


today = datetime.now().strftime('%Y%m%d')
find_Maxpage('https://news.naver.com/main/list.nhn?mode=LPOD&sid2=140&sid1=001&mid=sec&oid=001&isYeonhapFlash=Y&date={}&page=1'.format(today), 0)
print(page_url)

for x in range(len(page_url)):
    crawling_url(
        'https://news.naver.com/main/list.nhn?mode=LPOD&sid2=140&sid1=001&mid=sec&oid=001&isYeonhapFlash=Y&date={}&page={}'.format(today, page_url[x]))


texts_url = set(texts_url)
texts_url = list(texts_url)

# print("*********url 정보***********")
print(texts_url)
print(len(texts_url))


oid = []
aid = []
headers = []
com_url = []

#* 뉴스의 url에서 oid와 aid를 수집
def getOid_Aid(uri):
    global oid
    global aid
    oid.append(uri.split("oid=")[1].split("&")[0])
    aid.append(uri.split("aid=")[1].split("&is")[0])


for y in range(len(texts_url)):
    a = texts_url[y]
    getOid_Aid(a)

useragent = UserAgent()

for x in range(len(texts_url)):
    comps_url = []
    for y in range(1, 30):
        comps_url.append("https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_politics_m1&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news" +
                         oid[x] + "%2C" + aid[x] + "&categoryId=&pageSize=100&indexSize=100&groupId=&listType=OBJECT&pageType=more&page=" + str(y) + "&refresh=false&sort=FAVORITE")
    com_url.append(comps_url)
# print(com_url[0][1])

for v in range(len(texts_url)):
    headers.append({
        'referer': texts_url[v],
        'User-Agent': useragent.chrome
    })


male = 0
female = 0
tens = 0
twenties = 0
thirties = 0
fourties = 0
fifties = 0
sixties = 0
comments_array = []
writer_array = []
recommended_array = []
unrecommended_array = []
date_comment_array = []

#* 이 부분을 기준으로
# * 윗부분 코드 : 크롤링 하기 위한 기사 url 및 댓글 api 수집
# * 아랫부분 코드 : 데이터를 네이버로부터 가져오는 단계 및 크롤링한 데이터를 데이터베이스에 저장

# * mysql 객체 맵핑
mysql = pymysql.connect(host='localhost',
                      user='유저',
                      password='비밀번호',
                      database='데이터베이스 이름',
                      charset='utf8')
cursor = mysql.cursor(pymysql.cursors.DictCursor)

# * mysql Test part
# sql = 'select * from `News`;'
# cursor.execute(sql)
# result = cursor.fetchall()
# print("result : ", result)

news_id = 0
gender_id = 0
age_id = 0
comments_id = 0

for v in range(len(texts_url)):
    graph_exists = False
    for y in range(len(com_url[v])):
        
        resp = urlopen(
            Request(com_url[v][y], headers=headers[v])).read().decode('utf-8')
        
        if not '"commentList":[]' in resp:
            rank_json = getJson_NewsInfo(resp)

            if y == 0:                
                driver.get(texts_url[v])
                
                try:
                    date_news = driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr/td[1]/div/div[1]/div[3]/div/span").text
                except:
                    date_news = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/span").text
                
                date_news = date_news.replace(".","-",2)
                date_news = date_news.replace(".","")

                if date_news.split(" ")[1] == '오후':
                    date_news = date_news.replace("오후 ","")
                    date_news = date_news + "PM"    

                if date_news.split(" ")[1] == '오전':
                    date_news = date_news.replace("오전 ","")
                    date_news = date_news + "AM"

                date_news = parse(date_news)


                print(date_news)
                figures = driver.find_elements_by_class_name(
                    "u_cbox_chart_per")
                if figures:
                    graph_exists = True

                    #* mysql insert data 추출 코드
                    for t in range(len(figures)):
                        statics = figures[t].text
                        if t == 0:
                            male = int(statics.split("%")[0])
                        if t == 1:
                            female = int(statics.split("%")[0])
                        if t == 2:
                            tens = int(statics.split("%")[0])
                        if t == 3:
                            twenties = int(statics.split("%")[0])
                        if t == 4:
                            thirties = int(statics.split("%")[0])
                        if t == 5:
                            fourties = int(statics.split("%")[0])
                        if t == 6:
                            fifties = int(statics.split("%")[0])
                        if t == 7:
                            sixties = int(statics.split("%")[0])

            if rank_json['result']['commentList']:
                for w in range(len(rank_json['result']['commentList'])):
                    # * mysql Insert 데이터 추출
                    contents = str(rank_json['result']['commentList'][w]['contents'])
                    # contents = contents.replace("'","")
                    # contents = contents.replace("\"","")
                    # contents = contents.replace("/","")
                    # contents = contents.replace("\\","")
                    comments_array.append(contents)
                    writer = str(rank_json['result']['commentList'][w]['maskedUserId'])
                    writer_array.append(writer)
                    recommended = str(rank_json['result']['commentList'][w]['sympathyCount'])
                    recommended_array.append(recommended)
                    unrecommended = str(rank_json['result']['commentList'][w]['antipathyCount'])
                    unrecommended_array.append(unrecommended)
                    
                    date_raw = str(rank_json['result']['commentList'][w]['modTime'])                    
                    dc = str(parse(date_raw))                    
                    date_comment_changed = dc.split("+")[0]
                    date_comment_array.append(date_comment_changed)                    
        else:
            break
    url = texts_url[v]
    
    title = crawling_title(texts_url[v])
    title = title.replace("'","")
    title = title.replace("\"","")
    title = title.replace("/","")
    title = title.replace("\\","")
    title = title.encode('utf-8', 'ignore').decode('utf-8')    

    date_news_figure = date_news
    male_figure = male
    female_figure = female
    tens_figure = tens
    twenties_figure = twenties
    thirties_figure = thirties
    fourties_figure = fourties
    fifties_figure = fifties
    sixties_figure = sixties    
    
    if graph_exists:    
        print("sql")    
        sql_news = """insert into News values('{}','{}','{}','{}');""".format(news_id, title, url, date_news_figure)
        cursor.execute(sql_news)
        mysql.commit()
        sql_gender = """insert into GenderAnalysis values('{}','{}','{}','{}');""".format(gender_id, news_id, male_figure, female_figure)
        cursor.execute(sql_gender)
        mysql.commit()
        sql_age = """insert into AgeAnalysis values('{}','{}','{}','{}','{}','{}','{}','{}');""".format(age_id, news_id, tens_figure, twenties_figure, thirties_figure, fourties_figure, fifties_figure, sixties_figure)
        cursor.execute(sql_age)
        mysql.commit()

        for index in range(len(comments_array)):
            # print(comments_array[index])
            try:
                comments_array[index] = comments_array[index].encode('utf-8', 'ignore').decode('utf-8')
                sql_comments = """insert into Comments values('{}','{}','{}','{}','{}','{}','{}');""".format(comments_id, news_id, comments_array[index], writer_array[index], recommended_array[index], unrecommended_array[index], date_comment_array[index])
                cursor.execute(sql_comments)
                mysql.commit()
                comments_id += 1 
            except:
                print("sql comments insert error")
              
        

        news_id = news_id + 1
        gender_id = gender_id + 1
        age_id = age_id + 1
        # comments_id = comments_id + 1

    comments_array.clear()
    writer_array.clear()
    recommended_array.clear()
    unrecommended_array.clear()
    date_comment_array.clear()



