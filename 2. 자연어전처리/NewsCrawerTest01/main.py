from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

import time
import random

#######
options = webdriver.ChromeOptions()
#options.add_argument('headless')

ua = UserAgent(verify_ssl=False)
userAgent = ua.random

options = Options()
options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\admin1\Documents\chromedriver\chromedriver')
###### 봇탐지 우회


# 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
driver.implicitly_wait(3)
time.sleep(3)

url = "https://news.naver.com/main/ranking/read.nhn?mode=LSD&mid=shm&sid1=001&oid=015&aid=0004521863&rankingType=RANKING"

driver.get(url)

list = driver.find_elements_by_class_name("u_cbox_area")

"u_cbox_btn_more".click();

#Root.
#print(Root)

for item in list:
    print(item.text)