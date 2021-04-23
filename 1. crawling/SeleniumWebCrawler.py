from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


#######
options = webdriver.ChromeOptions()
#options.add_argument('headless')

ua = UserAgent(verify_ssl=False)
userAgent = ua.random

options = Options()
options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\admin1\Documents\chromedriver\chromedriver')
###### ��Ž�� ��ȸ


# �Ϲ������� �� �ڿ� �ε带 ���� 3�ʱ��� ��ٷ� �ش�.
driver.implicitly_wait(3)
time.sleep(3)

url = "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=025&aid=0003087436"

driver.get(url)

Root = driver.find_element_by_class_name("_article_body_contents").text
print(Root)
