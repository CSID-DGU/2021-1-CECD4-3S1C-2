from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time


#######
options = webdriver.ChromeOptions()
# options.add_argument('headless')

ua = UserAgent(verify_ssl=False)
userAgent = ua.random

options = Options()
options.add_argument('headless')
options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(
    options=options, executable_path=r'크롬 드라이버 절대경로')
# 봇탐지 우회
# 헤드리스 기능 추가


# 암묵적으로 웹 자원 로드를 위해 1초까지 기다려 준다.
driver.implicitly_wait(1)
time.sleep(1)

url = []

# url.append(
#     "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=025&aid=0003087436")
url.append(
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=104&oid=081&aid=0003178388")

# url.append("https://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=001&aid=0012325226&isYeonhapFlash=Y&rc=N")

# Crawling the Statistical figure
for x in range(len(url)):
    driver.get(url[x])
    Root = driver.find_elements_by_class_name("u_cbox_chart_per")
    # print(len(Root))
    if Root:
        for y in range(len(Root)):
            texts = Root[y].text
            print(texts.split("%")[0])
            print(y)
            # print("**********")
            # print(texts.split("%")[0])
            # print(texts.split("%")[1])
            # print("**********")
            # print(texts.split("%")[0])
    else:
        print("Haha")
